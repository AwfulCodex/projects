#!/usr/bin/env python3
"""
Example usage of the Gaming Video Editor
Copy and modify this script for your own projects
"""

from video_editor import GamingVideoEditor
import config

def example_trim_clip():
    """Example: Trim a specific section from your gameplay"""
    editor = GamingVideoEditor(project_dir="projects")

    # Trim from 10 seconds to 30 seconds
    editor.trim_clip(
        input_path="projects/input/gameplay.mp4",
        start=10,
        end=30,
        output_path="projects/output/clip_trimmed.mp4"
    )


def example_speed_ramp():
    """Example: Speed up boring sections, keep action normal"""
    editor = GamingVideoEditor(project_dir="projects")

    # Speed up 1.5x (useful for walking, loading screens, etc.)
    editor.speed_up(
        input_path="projects/output/clip_trimmed.mp4",
        speed_factor=1.5,
        output_path="projects/output/clip_fast.mp4"
    )


def example_highlight_reel():
    """Example: Create a highlight reel from multiple clips"""
    editor = GamingVideoEditor(project_dir="projects")

    # Define highlights: file path, start time, end time
    highlights = [
        {
            "file": "projects/input/session1.mp4",
            "start": 45,      # Start at 45 seconds
            "end": 60,        # End at 60 seconds
        },
        {
            "file": "projects/input/session2.mp4",
            "start": 120,
            "end": 145,
        },
        {
            "file": "projects/input/session3.mp4",
            "start": 200,
            "end": 220,
        },
    ]

    editor.create_highlight_reel(
        clips_data=highlights,
        output_path="projects/output/highlight_reel.mp4"
    )


def example_add_title():
    """Example: Add text overlay (title, commentary)"""
    editor = GamingVideoEditor(project_dir="projects")

    editor.add_text_overlay(
        input_path="projects/output/clip_trimmed.mp4",
        text="INSANE CLUTCH!",
        duration=3,  # Show text for 3 seconds
        output_path="projects/output/clip_with_title.mp4"
    )


def example_get_info():
    """Example: Check video information"""
    editor = GamingVideoEditor(project_dir="projects")

    info = editor.get_video_info("projects/input/gameplay.mp4")

    print("\nVideo Information:")
    print(f"  Duration: {info.get('duration', 'N/A')}s")
    print(f"  FPS: {info.get('fps', 'N/A')}")
    print(f"  Resolution: {info.get('resolution', 'N/A')}")
    print(f"  Has Audio: {info.get('has_audio', 'N/A')}")


def example_extract_audio():
    """Example: Extract audio track for voiceover"""
    editor = GamingVideoEditor(project_dir="projects")

    editor.extract_audio(
        input_path="projects/input/gameplay.mp4",
        output_path="projects/output/gameplay_audio.mp3"
    )


def example_concatenate():
    """Example: Combine multiple clips into final video"""
    editor = GamingVideoEditor(project_dir="projects")

    editor.concatenate_clips(
        input_files=[
            "projects/output/intro.mp4",
            "projects/output/gameplay.mp4",
            "projects/output/outro.mp4",
        ],
        output_path="projects/output/final_video.mp4"
    )


def example_complete_workflow():
    """Example: Complete workflow - from raw gameplay to highlight reel"""
    print("\n" + "="*60)
    print("COMPLETE WORKFLOW: Raw Gameplay → Highlight Reel")
    print("="*60 + "\n")

    editor = GamingVideoEditor(project_dir="projects")

    # Step 1: Extract interesting moments
    print("[1/4] Extracting interesting moments...")
    editor.trim_clip("projects/input/raw_gameplay.mp4", 0, 120, "projects/output/segment1.mp4")
    editor.trim_clip("projects/input/raw_gameplay.mp4", 200, 300, "projects/output/segment2.mp4")

    # Step 2: Speed up slower sections
    print("[2/4] Optimizing pacing...")
    editor.speed_up("projects/output/segment1.mp4", 1.2, "projects/output/segment1_fast.mp4")

    # Step 3: Add titles
    print("[3/4] Adding titles...")
    editor.add_text_overlay(
        "projects/output/segment1_fast.mp4",
        "OPENING PLAY",
        2,
        "projects/output/segment1_titled.mp4"
    )

    # Step 4: Combine
    print("[4/4] Creating final reel...")
    editor.concatenate_clips(
        input_files=[
            "projects/output/segment1_titled.mp4",
            "projects/output/segment2.mp4",
        ],
        output_path="projects/output/FINAL_HIGHLIGHT_REEL.mp4"
    )

    print("\n✓ Workflow complete! Check projects/output/")


if __name__ == "__main__":
    print("Gaming Video Editor - Examples")
    print("=" * 50)
    print("\nAvailable examples:")
    print("  1. Trim a clip")
    print("  2. Speed up footage")
    print("  3. Create highlight reel")
    print("  4. Add title text")
    print("  5. Get video info")
    print("  6. Extract audio")
    print("  7. Concatenate clips")
    print("  8. Complete workflow")
    print("\nTo run: Uncomment the function call below")
    print("=" * 50 + "\n")

    # Uncomment the example you want to run:

    # example_get_info()
    # example_trim_clip()
    # example_speed_ramp()
    # example_add_title()
    # example_highlight_reel()
    # example_extract_audio()
    # example_concatenate()
    # example_complete_workflow()

    print("\nTo get started:")
    print("1. Place your video in: projects/input/")
    print("2. Uncomment an example function above")
    print("3. Run this script: python example_usage.py")
