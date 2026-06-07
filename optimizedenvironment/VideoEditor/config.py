# Video Editor Configuration

# Output Settings
OUTPUT = {
    "format": "mp4",
    "codec": "libx264",
    "fps": 60,  # Gaming standard (60fps)
    "quality": "medium",  # low, medium, high
    "bitrate": "10M",  # Adjust for file size
}

# Audio Settings
AUDIO = {
    "codec": "aac",
    "bitrate": "192k",
    "sample_rate": 48000,
}

# Default Presets
PRESETS = {
    "highlight_reel": {
        "speed": 1.0,
        "add_intro": True,
        "add_outro": True,
        "music": "cinematic",
    },
    "speed_run": {
        "speed": 1.5,
        "add_intro": False,
        "add_outro": False,
    },
    "tutorial": {
        "speed": 1.0,
        "add_intro": True,
        "add_outro": False,
    },
    "clip_compilation": {
        "speed": 1.0,
        "add_intro": False,
        "add_outro": False,
    },
}

# Text Overlay Settings
TEXT = {
    "font": "Arial",
    "fontsize": 50,
    "color": "white",
    "position": "center",
}

# Gaming Content Templates
GAMING_TEMPLATES = {
    "kill_streak": {
        "description": "Highlight a series of eliminations",
        "speed_ramp": [1.0, 1.5, 1.0],  # Ramp up for intensity
    },
    "boss_fight": {
        "description": "Epic boss battle showcase",
        "add_music": True,
        "text_style": "bold",
    },
    "speedrun": {
        "description": "Speed run showcase",
        "speed": 1.5,
        "remove_dead_time": True,
    },
    "fails_compilation": {
        "description": "Funny moments/fails",
        "speed": 1.2,
        "add_effects": True,
    },
}

# Free AI Enhancement Options
AI_FEATURES = {
    "auto_cut_silence": False,  # Remove silence segments
    "auto_scene_detect": False,  # Detect scene changes
    "auto_highlight": False,  # Auto-detect highlights (requires ML model)
    "upscale_video": False,  # AI upscaling (slow)
}

# Project Structure
DIRECTORIES = {
    "input": "input/",
    "output": "output/",
    "clips": "clips/",
    "assets": "assets/",
    "projects": "projects/",
}
