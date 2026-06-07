#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Audio Processor for Gaming Video Editor
Handles multiple audio tracks with compression and balancing
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import numpy as np
from dataclasses import dataclass

try:
    from pydub import AudioSegment
    from pydub.utils import make_mono
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    import librosa
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False

try:
    from scipy import signal
    from scipy.ndimage import uniform_filter1d
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


@dataclass
class AudioTrack:
    """Single audio track information"""
    index: int
    language: str
    codec: str
    sample_rate: int
    channels: int
    bitrate: str
    duration: float


class AudioProcessor:
    """Advanced audio processor for gaming content"""

    def __init__(self):
        self.temp_dir = Path("temp_audio")
        self.temp_dir.mkdir(exist_ok=True)

    def list_audio_tracks(self, video_path: str) -> List[AudioTrack]:
        """Detect all audio tracks in a video file"""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-select_streams", "a",
                "-show_entries", "stream=index,codec_type,codec_name,sample_rate,channels,bit_rate,tags=language",
                "-of", "json",
                video_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)

            tracks = []
            for stream in data.get("streams", []):
                track = AudioTrack(
                    index=stream.get("index"),
                    language=stream.get("tags", {}).get("language", "unknown"),
                    codec=stream.get("codec_name", "unknown"),
                    sample_rate=int(stream.get("sample_rate", 48000)),
                    channels=stream.get("channels", 2),
                    bitrate=stream.get("bit_rate", "128k"),
                    duration=0.0
                )
                tracks.append(track)

            return tracks
        except Exception as e:
            print(f"✗ Failed to detect audio tracks: {e}")
            return []

    def extract_audio_track(self, video_path: str, track_index: int, output_path: str) -> bool:
        """Extract specific audio track from video"""
        try:
            print(f"Extracting audio track {track_index}...")
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-map", f"0:a:{track_index}",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Extracted track {track_index} to {output_path}")
                return True
            else:
                print(f"✗ Extraction failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Extract failed: {e}")
            return False

    def extract_all_audio_tracks(self, video_path: str, output_dir: str) -> Dict[int, str]:
        """Extract all audio tracks from video"""
        tracks = self.list_audio_tracks(video_path)
        extracted = {}

        Path(output_dir).mkdir(exist_ok=True)

        for track in tracks:
            output_file = Path(output_dir) / f"track_{track.index}_{track.language}.aac"
            if self.extract_audio_track(video_path, track.index, str(output_file)):
                extracted[track.index] = str(output_file)

        return extracted

    def normalize_audio(self, audio_path: str, output_path: str, target_db: float = -20.0) -> bool:
        """Normalize audio to target loudness (LUFS)"""
        if not PYDUB_AVAILABLE:
            print("✗ pydub required for normalization")
            return False

        try:
            print(f"Normalizing audio to {target_db}dB...")
            audio = AudioSegment.from_file(audio_path)

            # Calculate current loudness
            current_db = audio.dBFS
            gain = target_db - current_db

            # Apply gain
            normalized = audio.apply_gain(gain)
            normalized.export(output_path, format="aac", bitrate="192k")

            print(f"✓ Normalized: {current_db:.1f}dB → {target_db:.1f}dB")
            return True
        except Exception as e:
            print(f"✗ Normalization failed: {e}")
            return False

    def compress_audio(self, audio_path: str, output_path: str,
                      threshold: float = -20.0, ratio: float = 4.0) -> bool:
        """Apply dynamic range compression to audio"""
        if not (LIBROSA_AVAILABLE and SCIPY_AVAILABLE):
            print("✗ librosa and scipy required for compression")
            return False

        try:
            print(f"Compressing audio (threshold={threshold}dB, ratio={ratio}:1)...")

            # Load audio
            y, sr = librosa.load(audio_path, sr=None)

            # Convert to dB
            S = librosa.stft(y)
            S_db = librosa.power_to_db(np.abs(S) ** 2)

            # Apply compression
            compressed = S_db.copy()
            above_threshold = compressed > threshold

            # For samples above threshold, reduce by ratio
            compressed[above_threshold] = threshold + (compressed[above_threshold] - threshold) / ratio

            # Convert back
            compressed_linear = librosa.db_to_power(compressed) ** 0.5
            compressed_audio = librosa.istft(compressed_linear)

            # Normalize to prevent clipping
            max_val = np.max(np.abs(compressed_audio))
            if max_val > 0:
                compressed_audio = compressed_audio / max_val

            # Save
            sf.write(output_path, compressed_audio, sr)
            print(f"✓ Compressed and saved to {output_path}")
            return True
        except Exception as e:
            print(f"✗ Compression failed: {e}")
            return False

    def balance_multiple_tracks(self, track_paths: List[str], output_path: str,
                               levels: Optional[List[float]] = None) -> bool:
        """Balance and mix multiple audio tracks"""
        if not PYDUB_AVAILABLE:
            print("✗ pydub required for mixing")
            return False

        try:
            print(f"Balancing {len(track_paths)} audio tracks...")

            # Load all tracks
            tracks = []
            for i, path in enumerate(track_paths):
                print(f"  Loading track {i+1}...")
                audio = AudioSegment.from_file(path)
                tracks.append(audio)

            # Ensure all same duration
            max_duration = max(len(t) for t in tracks)
            normalized_tracks = []
            for i, audio in enumerate(tracks):
                if len(audio) < max_duration:
                    # Pad with silence
                    silence = AudioSegment.silent(duration=max_duration - len(audio))
                    audio = audio + silence
                normalized_tracks.append(audio)

            # Apply levels if provided
            if levels:
                print("  Applying custom levels...")
                for i, (audio, level) in enumerate(zip(normalized_tracks, levels)):
                    # level is 0.0 to 1.0
                    db = 20 * np.log10(level + 0.001)  # Convert to dB
                    normalized_tracks[i] = audio.apply_gain(db)
            else:
                # Auto-balance: normalize all to same loudness
                print("  Auto-balancing levels...")
                target_db = -20.0
                balanced = []
                for audio in normalized_tracks:
                    current_db = audio.dBFS
                    gain = target_db - current_db
                    balanced.append(audio.apply_gain(gain))
                normalized_tracks = balanced

            # Mix tracks
            print("  Mixing tracks...")
            mixed = normalized_tracks[0]
            for audio in normalized_tracks[1:]:
                mixed = mixed.overlay(audio)

            # Final normalization
            mixed = mixed.normalize()

            # Export
            mixed.export(output_path, format="aac", bitrate="256k")
            print(f"✓ Balanced audio saved to {output_path}")
            return True
        except Exception as e:
            print(f"✗ Balancing failed: {e}")
            return False

    def apply_compression_and_normalize(self, audio_path: str, output_path: str) -> bool:
        """Apply compression then normalization (best for gaming audio)"""
        if not PYDUB_AVAILABLE:
            print("✗ pydub required")
            return False

        try:
            print("Applying compression + normalization...")

            # Step 1: Normalize first
            temp_normalized = self.temp_dir / "temp_normalized.aac"
            self.normalize_audio(audio_path, str(temp_normalized), target_db=-20.0)

            # Step 2: Apply gentle compression
            temp_compressed = self.temp_dir / "temp_compressed.aac"
            self.compress_audio(str(temp_normalized), str(temp_compressed),
                              threshold=-15.0, ratio=2.0)

            # Step 3: Final normalization
            audio = AudioSegment.from_file(str(temp_compressed))
            audio = audio.normalize()
            audio.export(output_path, format="aac", bitrate="256k")

            print(f"✓ Final processed audio saved to {output_path}")
            return True
        except Exception as e:
            print(f"✗ Processing failed: {e}")
            return False

    def create_balanced_soundtrack(self, video_path: str, output_audio_path: str,
                                  track_weights: Optional[Dict[int, float]] = None) -> bool:
        """Complete workflow: extract, balance, and create final audio"""
        try:
            print(f"\n{'='*60}")
            print("CREATING BALANCED SOUNDTRACK")
            print(f"{'='*60}\n")

            # Step 1: List tracks
            print("[1/4] Detecting audio tracks...")
            tracks = self.list_audio_tracks(video_path)
            if not tracks:
                print("✗ No audio tracks found")
                return False

            print(f"Found {len(tracks)} audio track(s):")
            for track in tracks:
                print(f"  • Track {track.index}: {track.language} ({track.channels}ch, {track.sample_rate}Hz)")

            # Step 2: Extract all tracks
            print("\n[2/4] Extracting audio tracks...")
            extracted = self.extract_all_audio_tracks(video_path, str(self.temp_dir))
            if not extracted:
                print("✗ Failed to extract tracks")
                return False

            # Step 3: Process and balance
            print("\n[3/4] Balancing audio levels...")
            track_paths = [extracted[i] for i in sorted(extracted.keys())]

            # Apply custom weights or auto-balance
            if track_weights:
                levels = [track_weights.get(i, 0.5) for i in sorted(extracted.keys())]
                print(f"Applying custom levels: {levels}")
            else:
                levels = None
                print("Using auto-balance (equal levels)")

            temp_mixed = self.temp_dir / "mixed.aac"
            self.balance_multiple_tracks(track_paths, str(temp_mixed), levels)

            # Step 4: Final compression + normalization
            print("\n[4/4] Finalizing audio...")
            self.apply_compression_and_normalize(str(temp_mixed), output_audio_path)

            print(f"\n{'='*60}")
            print(f"✓ Balanced soundtrack: {output_audio_path}")
            print(f"{'='*60}\n")

            return True
        except Exception as e:
            print(f"✗ Soundtrack creation failed: {e}")
            return False

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("Cleaned up temporary files")


# Example usage
if __name__ == "__main__":
    processor = AudioProcessor()

    print("Audio Processor - Advanced Multi-Track Audio Handling")
    print("=" * 60)
    print("\nFeatures:")
    print("  ✓ Detect all audio tracks in video")
    print("  ✓ Extract individual tracks")
    print("  ✓ Normalize audio levels")
    print("  ✓ Apply dynamic range compression")
    print("  ✓ Balance multiple tracks")
    print("  ✓ Create professional mixed audio")
    print("\nExample:")
    print("  processor.create_balanced_soundtrack('video.mp4', 'audio_balanced.aac')")
