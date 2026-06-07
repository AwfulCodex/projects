#!/usr/bin/env python3
"""
Audio Processing Examples for Gaming Video Editor
Demonstrates multiple audio track handling and balancing
"""

from video_editor import GamingVideoEditor
from audio_processor import AudioProcessor

# ============================================
# EXAMPLE 1: Detect Audio Tracks in Video
# ============================================
def example_list_audio_tracks():
    """Detect all audio tracks in a video"""
    editor = GamingVideoEditor(project_dir="projects")

    print("Detecting audio tracks...")
    tracks = editor.list_audio_tracks("projects/input/gameplay.mp4")

    print(f"\nFound {len(tracks)} audio track(s):")
    for track in tracks:
        print(f"  • Index {track['index']}: {track['language']}")
        print(f"    - Codec: {track['codec']}")
        print(f"    - Sample Rate: {track['sample_rate']}Hz")
        print(f"    - Channels: {track['channels']}ch")


# ============================================
# EXAMPLE 2: Extract Specific Audio Track
# ============================================
def example_extract_single_track():
    """Extract one audio track from video (e.g., English dialogue)"""
    editor = GamingVideoEditor(project_dir="projects")

    # Extract track 0 (usually primary audio)
    editor.extract_audio_track(
        video_path="projects/input/gameplay.mp4",
        track_index=0,
        output_path="projects/output/primary_audio.aac"
    )


# ============================================
# EXAMPLE 3: Extract ALL Audio Tracks
# ============================================
def example_extract_all_tracks():
    """Extract all audio tracks (useful for multi-language videos)"""
    editor = GamingVideoEditor(project_dir="projects")

    print("Extracting all audio tracks...")
    extracted = editor.extract_all_audio_tracks("projects/input/gameplay.mp4")

    print(f"\nExtracted {len(extracted)} track(s):")
    for track_idx, audio_file in extracted.items():
        print(f"  • Track {track_idx}: {audio_file}")


# ============================================
# EXAMPLE 4: Normalize Audio (Balance Levels)
# ============================================
def example_normalize_audio():
    """Normalize audio to standard loudness (-20 LUFS)"""
    editor = GamingVideoEditor(project_dir="projects")

    print("Normalizing audio to -20dB...")
    editor.normalize_audio(
        audio_path="projects/input/gameplay_audio.aac",
        output_path="projects/output/audio_normalized.aac",
        target_db=-20.0  # Professional standard
    )


# ============================================
# EXAMPLE 5: Compress Audio (Dynamic Range)
# ============================================
def example_compress_audio():
    """Apply dynamic range compression for more consistent levels"""
    editor = GamingVideoEditor(project_dir="projects")

    print("Compressing audio...")
    editor.compress_audio(
        audio_path="projects/input/gameplay_audio.aac",
        output_path="projects/output/audio_compressed.aac",
        threshold=-20.0,  # dB threshold above which compression applies
        ratio=4.0         # 4:1 compression ratio
    )


# ============================================
# EXAMPLE 6: Balance Multiple Audio Tracks
# ============================================
def example_balance_multiple_tracks():
    """Mix multiple audio tracks with balanced levels"""
    editor = GamingVideoEditor(project_dir="projects")

    print("Balancing multiple audio tracks...")

    # Method 1: Auto-balance (equal levels)
    editor.balance_audio_tracks(
        video_path="projects/input/multi_audio.mp4",
        output_audio_path="balanced_audio.aac"
    )

    # Method 2: Custom levels (0.0-1.0)
    editor.balance_audio_tracks(
        video_path="projects/input/multi_audio.mp4",
        output_audio_path="balanced_audio_custom.aac",
        track_weights={
            0: 0.7,  # Game audio: 70%
            1: 0.3,  # Commentary: 30%
        }
    )


# ============================================
# EXAMPLE 7: Complete Workflow - From Multi-Track to Balanced Audio
# ============================================
def example_complete_audio_workflow():
    """
    Complete workflow:
    1. Detect all audio tracks
    2. Extract all tracks
    3. Normalize each
    4. Balance and mix
    5. Apply compression
    6. Final result: professional balanced audio
    """
    print("\n" + "="*60)
    print("COMPLETE AUDIO WORKFLOW")
    print("Multi-track Video → Balanced Professional Audio")
    print("="*60 + "\n")

    editor = GamingVideoEditor(project_dir="projects")
    processor = AudioProcessor()

    # Step 1: Detect tracks
    print("[1/5] Detecting audio tracks...")
    tracks = editor.list_audio_tracks("projects/input/gameplay_multi.mp4")
    print(f"Found {len(tracks)} track(s)")

    # Step 2: Extract all
    print("\n[2/5] Extracting all audio tracks...")
    extracted = editor.extract_all_audio_tracks("projects/input/gameplay_multi.mp4")
    print(f"Extracted {len(extracted)} file(s)")

    # Step 3: Balance with custom levels
    print("\n[3/5] Balancing audio tracks...")
    # Assuming: Track 0 = Game audio, Track 1 = Voice comms
    editor.balance_audio_tracks(
        video_path="projects/input/gameplay_multi.mp4",
        output_audio_path="temp_balanced.aac",
        track_weights={
            0: 0.8,  # Game audio louder
            1: 0.5,  # Voice quieter
        }
    )

    # Step 4: Normalize
    print("\n[4/5] Normalizing audio levels...")
    editor.normalize_audio(
        audio_path="projects/output/temp_balanced.aac",
        output_path="projects/output/audio_normalized.aac",
        target_db=-20.0
    )

    # Step 5: Final compression for consistency
    print("\n[5/5] Applying final compression...")
    editor.compress_audio(
        audio_path="projects/output/audio_normalized.aac",
        output_path="projects/output/FINAL_BALANCED_AUDIO.aac",
        threshold=-15.0,
        ratio=2.0
    )

    print("\n" + "="*60)
    print("✓ Complete workflow finished!")
    print("Output: projects/output/FINAL_BALANCED_AUDIO.aac")
    print("="*60 + "\n")


# ============================================
# EXAMPLE 8: Gaming-Specific Audio Preset
# ============================================
def example_gaming_audio_preset():
    """
    Gaming-specific audio balancing:
    - Game audio: 80% (footsteps, gunfire, ambient)
    - Voice chat: 20% (teammates, comms)
    Result: Professional balance suitable for content creation
    """
    editor = GamingVideoEditor(project_dir="projects")

    print("Applying gaming preset...")
    print("  • Game audio: 80%")
    print("  • Voice comms: 20%")

    editor.balance_audio_tracks(
        video_path="projects/input/gameplay_with_voicecomm.mp4",
        output_audio_path="projects/output/gaming_balanced.aac",
        track_weights={
            0: 0.8,  # Primary audio (game sounds)
            1: 0.2,  # Secondary audio (voice chat)
        }
    )

    # Then normalize
    editor.normalize_audio(
        audio_path="projects/output/gaming_balanced.aac",
        output_path="projects/output/gaming_final.aac",
        target_db=-20.0
    )


if __name__ == "__main__":
    print("Audio Processing Examples - Gaming Video Editor")
    print("=" * 60)
    print("\nAvailable examples:")
    print("  1. List audio tracks in video")
    print("  2. Extract single audio track")
    print("  3. Extract all audio tracks")
    print("  4. Normalize audio levels")
    print("  5. Apply audio compression")
    print("  6. Balance multiple tracks")
    print("  7. Complete audio workflow")
    print("  8. Gaming-specific preset")
    print("\nTo run: Uncomment the function call below")
    print("=" * 60 + "\n")

    # Uncomment the example you want to run:

    # example_list_audio_tracks()
    # example_extract_single_track()
    # example_extract_all_tracks()
    # example_normalize_audio()
    # example_compress_audio()
    # example_balance_multiple_tracks()
    # example_complete_audio_workflow()
    # example_gaming_audio_preset()

    print("To get started with audio processing:")
    print("1. Place your multi-audio video in: projects/input/")
    print("2. Uncomment an example function above")
    print("3. Run: python audio_examples.py")
