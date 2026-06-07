#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlined Gaming Video Editor
Free AI-powered video editing for gaming content
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import timedelta

try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, ColorClip
    from moviepy.video.fx.speedx import speedx
    from moviepy.video.fx.vfx import rotate
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠ moviepy not installed. Run: pip install moviepy")

from PIL import Image, ImageDraw
import config

try:
    from audio_processor import AudioProcessor
    AUDIO_PROCESSOR_AVAILABLE = True
except ImportError:
    AUDIO_PROCESSOR_AVAILABLE = False

@dataclass
class EditConfig:
    """Configuration for a single edit job"""
    input_file: str
    output_file: str
    clips: List[Tuple[float, float]] = None  # [(start, end), ...]
    speed: float = 1.0
    add_intro: bool = False
    add_outro: bool = False
    background_music: Optional[str] = None
    highlights_only: bool = False


class GamingVideoEditor:
    """Streamlined video editor optimized for gaming content"""

    def __init__(self, project_dir: str = "projects"):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(exist_ok=True)
        self.clips_dir = self.project_dir / "clips"
        self.output_dir = self.project_dir / "output"
        self.assets_dir = self.project_dir / "assets"

        for d in [self.clips_dir, self.output_dir, self.assets_dir]:
            d.mkdir(exist_ok=True)

        self.audio_processor = AudioProcessor() if AUDIO_PROCESSOR_AVAILABLE else None

    # ========== Audio Processing Methods ==========

    def list_audio_tracks(self, video_path: str) -> List[dict]:
        """List all audio tracks in video"""
        if not self.audio_processor:
            print("✗ Audio processor not available")
            return []

        tracks = self.audio_processor.list_audio_tracks(video_path)
        return [
            {
                "index": t.index,
                "language": t.language,
                "codec": t.codec,
                "sample_rate": t.sample_rate,
                "channels": t.channels,
            }
            for t in tracks
        ]

    def extract_audio_track(self, video_path: str, track_index: int, output_path: str) -> bool:
        """Extract specific audio track from video"""
        if not self.audio_processor:
            print("✗ Audio processor not available")
            return False

        return self.audio_processor.extract_audio_track(video_path, track_index, output_path)

    def extract_all_audio_tracks(self, video_path: str) -> dict:
        """Extract all audio tracks from video"""
        if not self.audio_processor:
            print("✗ Audio processor not available")
            return {}

        output_dir = self.assets_dir / "audio_tracks"
        return self.audio_processor.extract_all_audio_tracks(video_path, str(output_dir))

    def balance_audio_tracks(self, video_path: str, output_audio_path: str,
                            track_weights: Optional[dict] = None) -> bool:
        """Balance and mix multiple audio tracks with compression"""
        if not self.audio_processor:
            print("✗ Audio processor not available")
            return False

        output_audio = self.output_dir / output_audio_path if not Path(output_audio_path).is_absolute() else Path(output_audio_path)
        output_audio.parent.mkdir(exist_ok=True, parents=True)

        return self.audio_processor.create_balanced_soundtrack(
            video_path,
            str(output_audio),
            track_weights
        )

    def normalize_audio(self, audio_path: str, output_path: str, target_db: float = -20.0) -> bool:
        """Normalize audio to target loudness"""
        if not self.audio_processor:
            print("✗ Audio processor not available")
            return False

        return self.audio_processor.normalize_audio(audio_path, output_path, target_db)

    def compress_audio(self, audio_path: str, output_path: str,
                      threshold: float = -20.0, ratio: float = 4.0) -> bool:
        """Apply dynamic range compression"""
        if not self.audio_processor:
            print("✗ Audio processor not available")
            return False

        return self.audio_processor.compress_audio(audio_path, output_path, threshold, ratio)

    # ========== Video Processing Methods ==========

    def trim_clip(self, input_path: str, start: float, end: float, output_path: str) -> bool:
        """Trim video clip to specific time range (seconds)"""
        if not MOVIEPY_AVAILABLE:
            return False

        try:
            print(f"Trimming {Path(input_path).name}... ({start}s - {end}s)")
            video = VideoFileClip(input_path)
            trimmed = video.subclipped(start, end)
            trimmed.write_videofile(output_path, verbose=False, logger=None)
            video.close()
            trimmed.close()
            print(f"✓ Saved: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Trim failed: {e}")
            return False

    def speed_up(self, input_path: str, speed_factor: float, output_path: str) -> bool:
        """Speed up video (2.0 = 2x speed)"""
        if not MOVIEPY_AVAILABLE:
            return False

        try:
            print(f"Speed: {speed_factor}x on {Path(input_path).name}")
            video = VideoFileClip(input_path)
            sped_up = video.speedx(speed_factor)
            sped_up.write_videofile(output_path, verbose=False, logger=None)
            video.close()
            sped_up.close()
            print(f"✓ Saved: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Speed change failed: {e}")
            return False

    def concatenate_clips(self, input_files: List[str], output_path: str) -> bool:
        """Join multiple video clips together"""
        if not MOVIEPY_AVAILABLE:
            return False

        try:
            print(f"Concatenating {len(input_files)} clips...")
            videos = [VideoFileClip(f) for f in input_files]
            final = concatenate_videoclips(videos)
            final.write_videofile(output_path, verbose=False, logger=None)
            for v in videos:
                v.close()
            final.close()
            print(f"✓ Saved: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Concatenation failed: {e}")
            return False

    def add_text_overlay(self, input_path: str, text: str, duration: float, output_path: str) -> bool:
        """Add text overlay to video"""
        if not MOVIEPY_AVAILABLE:
            return False

        try:
            print(f"Adding text overlay: '{text}'")
            video = VideoFileClip(input_path)

            txt_clip = TextClip(text, fontsize=50, color='white', font='Arial')
            txt_clip = txt_clip.set_duration(duration).set_position('center')

            final = CompositeVideoClip([video, txt_clip])
            final.write_videofile(output_path, verbose=False, logger=None)

            video.close()
            txt_clip.close()
            final.close()
            print(f"✓ Saved: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Text overlay failed: {e}")
            return False

    def extract_audio(self, input_path: str, output_path: str) -> bool:
        """Extract audio track from video"""
        if not MOVIEPY_AVAILABLE:
            return False

        try:
            print(f"Extracting audio from {Path(input_path).name}")
            video = VideoFileClip(input_path)
            if video.audio is None:
                print("✗ No audio track found")
                return False

            video.audio.write_audiofile(output_path, verbose=False, logger=None)
            video.close()
            print(f"✓ Saved: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Audio extraction failed: {e}")
            return False

    def get_video_info(self, input_path: str) -> dict:
        """Get video information"""
        if not MOVIEPY_AVAILABLE:
            return {}

        try:
            video = VideoFileClip(input_path)
            info = {
                "duration": float(video.duration),
                "fps": float(video.fps),
                "resolution": video.size,
                "has_audio": video.audio is not None,
            }
            video.close()
            return info
        except Exception as e:
            print(f"✗ Failed to get info: {e}")
            return {}

    def create_highlight_reel(self, clips_data: List[dict], output_path: str) -> bool:
        """Create highlight reel from clip timestamps"""
        if not MOVIEPY_AVAILABLE:
            return False

        try:
            print(f"Creating highlight reel ({len(clips_data)} segments)...")
            clips = []

            for clip_info in clips_data:
                input_file = clip_info["file"]
                start = clip_info["start"]
                end = clip_info["end"]

                video = VideoFileClip(input_file)
                segment = video.subclipped(start, end)
                clips.append(segment)

            final = concatenate_videoclips(clips)
            final.write_videofile(output_path, verbose=False, logger=None)

            for clip in clips:
                clip.close()
            final.close()
            print(f"✓ Highlight reel saved: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Highlight reel failed: {e}")
            return False


def main():
    """Example usage"""
    editor = GamingVideoEditor(project_dir="c:\\Users\\lawso\\Documents\\projects\\optimizedenvironment\\VideoEditor\\projects")

    print("╔══════════════════════════════════════════════════════════╗")
    print("║        Streamlined Gaming Video Editor v1.0             ║")
    print("║         Free AI-Powered Video Editing Tool              ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\nAvailable functions:")
    print("  • Trim clips to specific time ranges")
    print("  • Speed up/slow down video")
    print("  • Concatenate multiple clips")
    print("  • Add text overlays")
    print("  • Extract audio")
    print("  • Create highlight reels")
    print("  • Get video information")
    print("\nTo use: Import GamingVideoEditor class in your script")
    print("Example: editor.trim_clip('input.mp4', 10, 30, 'output.mp4')")


if __name__ == "__main__":
    main()
