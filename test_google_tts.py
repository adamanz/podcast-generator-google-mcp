#!/usr/bin/env python3
"""
Test script for Google TTS Podcast Generator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_podcast_server import (
    generate_dialogue_turns,
    parse_google_script,
    GOOGLE_SPEAKERS,
    PODCAST_FORMATS
)


def test_dialogue_generation():
    """Test dialogue generation"""
    print("🎭 Testing Dialogue Generation\n")
    
    turns = generate_dialogue_turns(
        topic="The Future of Space Exploration",
        format_type="interview",
        duration_minutes=3,
        additional_context={
            "key_points": ["Mars missions", "private companies", "new technologies"],
            "tone": "exciting and informative"
        }
    )
    
    print(f"Generated {len(turns)} dialogue turns:\n")
    for i, turn in enumerate(turns[:8]):  # Show first 8
        speaker_info = GOOGLE_SPEAKERS[turn['speaker']]
        print(f"{turn['speaker']} ({speaker_info['name']}): {turn['text']}")
    
    if len(turns) > 8:
        print(f"\n... and {len(turns) - 8} more turns")


def test_script_parsing():
    """Test script parsing"""
    print("\n\n📝 Testing Script Parsing\n")
    
    test_scripts = [
        # Pipe format
        """R|Welcome to our show!
S|Thanks for having me.
R|Let's dive into AI.
S|It's a fascinating topic.""",
        
        # Colon format
        """R: Welcome everyone!
S: Great to be here!
T: Let's get started.""",
        
        # Mixed format
        """R|This is the pipe format
S: This uses colons
R|Back to pipes
S: And colons again"""
    ]
    
    for i, script in enumerate(test_scripts):
        print(f"\nTest {i+1}:")
        print("Input format:", "pipe" if "|" in script.split('\n')[0] else "colon")
        
        turns = parse_google_script(script)
        print(f"Parsed {len(turns)} turns:")
        
        for turn in turns:
            print(f"  {turn['speaker']}: {turn['text'][:50]}...")


def test_formats():
    """Test available formats"""
    print("\n\n📚 Available Podcast Formats\n")
    
    for format_name, format_info in PODCAST_FORMATS.items():
        print(f"\n{format_name.upper()}:")
        print(f"  Description: {format_info['description']}")
        print(f"  Speakers: {', '.join(format_info['speakers'])}")
        
        if 'roles' in format_info:
            print(f"  Roles: {format_info['roles']}")


def test_speaker_info():
    """Test speaker information"""
    print("\n\n🎤 Google Multi-Speaker Voices\n")
    
    for speaker_id, info in GOOGLE_SPEAKERS.items():
        print(f"\nSpeaker {speaker_id}:")
        print(f"  Name: {info['name']}")
        print(f"  Personality: {info['personality']}")
        print(f"  Description: {info['description']}")


def create_sample_script():
    """Create a sample script"""
    print("\n\n✨ Sample Script for Testing\n")
    
    sample = """R|Welcome to Tech Insights! Today we're exploring artificial intelligence.
S|Thanks for having me. AI is truly revolutionizing every industry.
R|Let's start with healthcare. What are the most exciting developments?
S|We're seeing AI assist in early disease detection with incredible accuracy.
T|I'd like to add that AI is also personalizing treatment plans.
R|That's fascinating! How does it work exactly?
S|AI analyzes vast amounts of patient data to identify patterns humans might miss.
T|And it's getting better every day as it learns from more cases.
R|What about concerns regarding privacy and ethics?
S|Those are valid concerns that the industry is actively addressing.
T|Transparency and patient consent are becoming top priorities.
R|Thank you both for these insights. Any final thoughts?
S|The future of AI in healthcare is bright, but we must proceed thoughtfully.
T|Agreed. It's about augmenting human expertise, not replacing it.
R|Wonderful discussion! Thanks for joining us today."""
    
    print(sample)
    print("\n✅ Copy this script to test with create_google_audio!")


def main():
    print("=" * 60)
    print("🚀 Google TTS Podcast Generator Test Suite")
    print("=" * 60)
    
    test_dialogue_generation()
    test_script_parsing()
    test_formats()
    test_speaker_info()
    create_sample_script()
    
    print("\n" + "=" * 60)
    print("✅ All tests complete!")
    print("\nNote: To test audio generation, you need:")
    print("1. Google Cloud credentials configured")
    print("2. Text-to-Speech API enabled")
    print("3. Run the MCP server")
    print("=" * 60)


if __name__ == "__main__":
    main()