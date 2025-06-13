#!/usr/bin/env python3
"""
Google Cloud TTS Podcast Generator MCP Server
Uses Google's multi-speaker dialogue feature for natural conversations
"""

import json
import logging
import os
import random
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple
from datetime import datetime

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("podcast-generator-google")


# Google TTS speaker configurations
GOOGLE_SPEAKERS = {
    "R": {
        "name": "Speaker R",
        "personality": "warm_engaging",
        "description": "Friendly, conversational voice suitable for hosts"
    },
    "S": {
        "name": "Speaker S", 
        "personality": "analytical",
        "description": "Clear, informative voice suitable for experts"
    },
    "T": {
        "name": "Speaker T",
        "personality": "energetic", 
        "description": "Dynamic voice suitable for enthusiastic commentary"
    },
    "U": {
        "name": "Speaker U",
        "personality": "contemplative",
        "description": "Thoughtful voice suitable for deeper discussions"
    }
}


# Podcast formats optimized for Google's multi-speaker
PODCAST_FORMATS = {
    "dialogue": {
        "description": "Two-person conversational format",
        "speakers": ["R", "S"],
        "style": "Natural back-and-forth discussion"
    },
    "interview": {
        "description": "Host interviewing an expert",
        "speakers": ["R", "S"],
        "roles": {"R": "Host", "S": "Expert"}
    },
    "roundtable": {
        "description": "Multi-person discussion (up to 4 speakers)",
        "speakers": ["R", "S", "T", "U"],
        "style": "Collaborative discussion with multiple viewpoints"
    },
    "storytelling": {
        "description": "Narrative with character voices",
        "speakers": ["R", "S", "T"],
        "roles": {"R": "Narrator", "S": "Character 1", "T": "Character 2"}
    },
    "educational": {
        "description": "Teaching format with Q&A",
        "speakers": ["R", "S"],
        "roles": {"R": "Teacher", "S": "Student"}
    },
    "debate": {
        "description": "Point-counterpoint discussion",
        "speakers": ["R", "S", "T"],
        "roles": {"R": "Moderator", "S": "Advocate", "T": "Opponent"}
    }
}


def generate_dialogue_turns(
    topic: str,
    format_type: str,
    duration_minutes: int,
    additional_context: Optional[Dict] = None
) -> List[Dict[str, str]]:
    """
    Generate dialogue turns optimized for Google's MultiSpeakerMarkup
    Returns list of {speaker: "R/S/T/U", text: "dialogue"}
    """
    format_info = PODCAST_FORMATS.get(format_type, PODCAST_FORMATS["dialogue"])
    speakers = format_info["speakers"]
    roles = format_info.get("roles", {})
    
    # Calculate approximate number of turns based on duration
    # Assuming ~30 seconds per turn on average
    num_turns = duration_minutes * 2
    
    turns = []
    
    # Opening
    if format_type == "interview":
        turns.append({
            "speaker": "R",
            "text": f"Welcome to today's discussion about {topic}. I'm here with an expert who's going to share fascinating insights with us."
        })
        turns.append({
            "speaker": "S", 
            "text": "Thank you for having me! I'm excited to dive into this topic with your listeners."
        })
    elif format_type == "debate":
        turns.append({
            "speaker": "R",
            "text": f"Welcome to our debate on {topic}. We have two distinguished speakers with opposing viewpoints."
        })
        turns.append({
            "speaker": "S",
            "text": "I'm here to argue for the positive aspects and potential benefits."
        })
        turns.append({
            "speaker": "T",
            "text": "And I'll be presenting the concerns and challenges we need to consider."
        })
    else:
        turns.append({
            "speaker": speakers[0],
            "text": f"Let's explore {topic} together."
        })
        if len(speakers) > 1:
            turns.append({
                "speaker": speakers[1],
                "text": "Absolutely! This is such a relevant topic right now."
            })
    
    # Main content turns
    content_prompts = [
        "What's the most important thing people should understand?",
        "Can you give us a specific example?",
        "How does this impact our daily lives?",
        "What are the common misconceptions?",
        "What does the future hold?",
        "What challenges do we face?",
        "Are there any surprising aspects?",
        "How can people get involved?",
        "What's your personal experience with this?",
        "What advice would you give?"
    ]
    
    responses = [
        "That's a great question. Let me explain...",
        "Actually, it's quite fascinating when you look at it closely...",
        "People often don't realize that...",
        "From my perspective, the key is...",
        "What's really interesting is...",
        "The data shows us that...",
        "In my experience...",
        "Here's what I've learned...",
        "The breakthrough came when...",
        "This reminds me of..."
    ]
    
    # Generate main dialogue
    for i in range(min(num_turns - 4, len(content_prompts))):
        # Question from host/moderator
        question_speaker = speakers[0]
        turns.append({
            "speaker": question_speaker,
            "text": content_prompts[i % len(content_prompts)]
        })
        
        # Response from expert/other speaker
        response_speaker = speakers[1 % len(speakers)]
        response_intro = responses[i % len(responses)]
        
        # Add topic-specific content
        if additional_context and "key_points" in additional_context:
            point = additional_context["key_points"][i % len(additional_context["key_points"])]
            response_text = f"{response_intro} When it comes to {point} in {topic}, we're seeing significant developments."
        else:
            response_text = f"{response_intro} {topic} has many dimensions we need to consider."
        
        turns.append({
            "speaker": response_speaker,
            "text": response_text
        })
        
        # Add reactions or follow-ups for multi-speaker formats
        if len(speakers) > 2 and i % 3 == 0:
            reaction_speaker = speakers[2 % len(speakers)]
            reactions = [
                "I'd like to add to that point...",
                "That's interesting, but have you considered...",
                "Building on what was just said...",
                "From another angle..."
            ]
            turns.append({
                "speaker": reaction_speaker,
                "text": reactions[i % len(reactions)]
            })
    
    # Closing
    turns.append({
        "speaker": speakers[0],
        "text": f"This has been an enlightening discussion about {topic}. Any final thoughts?"
    })
    
    if len(speakers) > 1:
        turns.append({
            "speaker": speakers[1],
            "text": "The key takeaway is to stay informed and engaged with these developments."
        })
    
    turns.append({
        "speaker": speakers[0],
        "text": "Thank you for joining us today. Until next time!"
    })
    
    return turns


def generate_google_tts_prompt(
    topic: str,
    format_type: str,
    duration_minutes: int,
    additional_context: Optional[Dict] = None
) -> str:
    """
    Generate a prompt optimized for creating Google TTS multi-speaker scripts
    """
    format_info = PODCAST_FORMATS.get(format_type, PODCAST_FORMATS["dialogue"])
    
    prompt = f"""Create a natural {format_type} podcast script about "{topic}" using Google's multi-speaker format.

FORMAT: {format_info['description']}
SPEAKERS: {', '.join(format_info['speakers'])} (Google TTS speaker IDs)
DURATION: Approximately {duration_minutes} minutes

SPEAKER ASSIGNMENTS:
"""
    
    for speaker_id in format_info['speakers']:
        speaker_info = GOOGLE_SPEAKERS[speaker_id]
        role = format_info.get('roles', {}).get(speaker_id, speaker_info['name'])
        prompt += f"- {speaker_id}: {role} ({speaker_info['description']})\n"
    
    prompt += f"""

CONTENT REQUIREMENTS:
1. Create {duration_minutes * 2} dialogue turns (approximately)
2. Each turn should be 1-3 sentences
3. Make dialogue natural and conversational
4. Include personality in the speaking style
5. Add natural reactions and follow-ups

FORMAT EACH TURN AS:
Speaker ID|Dialogue text

Example:
R|Welcome to our podcast about artificial intelligence!
S|Thanks for having me. AI is transforming how we live and work.
R|Can you give us a specific example?
S|Sure! Take healthcare - AI is now helping doctors diagnose diseases earlier than ever before.

IMPORTANT:
- Use only the speaker IDs: {', '.join(format_info['speakers'])}
- Keep each turn concise but natural
- Include appropriate emotions and reactions in the text
- Make it sound like a real conversation, not a script

Topic focus areas:"""
    
    if additional_context:
        for key, value in additional_context.items():
            prompt += f"\n- {key}: {value}"
    
    return prompt


def parse_google_script(script: str) -> List[Dict[str, str]]:
    """
    Parse script formatted for Google TTS multi-speaker
    Expected format: R|Text or S|Text etc.
    """
    turns = []
    lines = script.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('//'):
            continue
            
        # Try pipe format first (R|Text)
        if '|' in line:
            parts = line.split('|', 1)
            if len(parts) == 2:
                speaker = parts[0].strip().upper()
                text = parts[1].strip()
                
                # Validate speaker ID
                if speaker in GOOGLE_SPEAKERS and text:
                    turns.append({
                        "speaker": speaker,
                        "text": text
                    })
        
        # Try colon format as fallback (R: Text)
        elif ':' in line:
            match = re.match(r'^([RSTU]):\s*(.+)$', line)
            if match:
                speaker = match.group(1)
                text = match.group(2).strip()
                if text:
                    turns.append({
                        "speaker": speaker,
                        "text": text
                    })
    
    # If no valid turns found, try to auto-assign
    if not turns and script.strip():
        paragraphs = [p.strip() for p in script.split('\n\n') if p.strip()]
        speakers = ["R", "S"]
        
        for i, para in enumerate(paragraphs):
            turns.append({
                "speaker": speakers[i % len(speakers)],
                "text": para
            })
    
    return turns


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri="podcast://google-voices",
            name="Google TTS Multi-Speaker Voices",
            description="Available Google Cloud TTS multi-speaker voices",
            mimeType="application/json"
        ),
        types.Resource(
            uri="podcast://formats",
            name="Podcast Formats",
            description="Available podcast formats for Google TTS",
            mimeType="application/json"
        ),
        types.Resource(
            uri="podcast://guide",
            name="Google TTS Podcast Guide",
            description="Guide for using Google Cloud TTS for podcasts",
            mimeType="text/markdown"
        )
    ]


@server.read_resource()
async def read_resource(uri: types.AnyUrl) -> str:
    """Read a specific resource."""
    if str(uri) == "podcast://google-voices":
        return json.dumps({
            "speakers": GOOGLE_SPEAKERS,
            "voice": "en-US-Studio-MultiSpeaker",
            "languages": ["en-US"],
            "note": "Google's multi-speaker voice supports up to 4 distinct speakers (R, S, T, U)"
        }, indent=2)
    
    elif str(uri) == "podcast://formats":
        return json.dumps(PODCAST_FORMATS, indent=2)
    
    elif str(uri) == "podcast://guide":
        guide = """# Google Cloud TTS Podcast Generator Guide

## Overview
This podcast generator uses Google Cloud Text-to-Speech's multi-speaker feature to create natural dialogues with distinct voices.

## Key Features
- **Multi-Speaker Support**: Up to 4 distinct speakers (R, S, T, U)
- **Natural Conversations**: Optimized for dialogue flow
- **Simple Format**: Easy-to-use script format
- **High Quality**: Google's Studio-quality voices

## Available Speakers
- **R**: Warm, engaging voice (great for hosts)
- **S**: Clear, analytical voice (perfect for experts)
- **T**: Dynamic, energetic voice (ideal for commentary)
- **U**: Thoughtful, contemplative voice (good for deeper insights)

## Podcast Formats
1. **dialogue**: Two-person conversation
2. **interview**: Host and expert Q&A
3. **roundtable**: Multi-person discussion (up to 4)
4. **storytelling**: Narrative with character voices
5. **educational**: Teacher-student format
6. **debate**: Point-counterpoint with moderator

## Script Format
Use the pipe format for best results:
```
R|Welcome to our show!
S|Thanks for having me.
R|Let's dive into today's topic.
```

## Usage Example
```python
# Generate script
generate_google_script(
    topic="Future of Technology",
    format_type="interview",
    duration_minutes=5
)

# Create audio
create_google_audio(
    script="[Generated script]",
    output_filename="tech_podcast.mp3"
)
```

## Requirements
- Google Cloud account
- Text-to-Speech API enabled
- Authentication configured
"""
        return guide.strip()
    
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="generate_google_script",
            description="Generate a podcast script optimized for Google's multi-speaker TTS",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The main topic for the podcast"
                    },
                    "format_type": {
                        "type": "string",
                        "description": "Podcast format",
                        "enum": list(PODCAST_FORMATS.keys()),
                        "default": "dialogue"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Target duration in minutes (1-30)",
                        "minimum": 1,
                        "maximum": 30,
                        "default": 5
                    },
                    "additional_context": {
                        "type": "object",
                        "description": "Additional context (key_points, tone, etc.)"
                    }
                },
                "required": ["topic"]
            }
        ),
        types.Tool(
            name="create_google_audio",
            description="Convert a multi-speaker script to audio using Google Cloud TTS",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Script with format: R|Text or S|Text etc."
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Output filename",
                        "default": "google_podcast.mp3"
                    },
                    "language_code": {
                        "type": "string",
                        "description": "Language code",
                        "default": "en-US"
                    }
                },
                "required": ["script"]
            }
        ),
        types.Tool(
            name="convert_to_google_format",
            description="Convert a standard dialogue script to Google's multi-speaker format",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Script in any dialogue format"
                    },
                    "speaker_mapping": {
                        "type": "object",
                        "description": "Map speaker names to R/S/T/U IDs"
                    }
                },
                "required": ["script"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
    """Handle tool calls."""
    if not arguments:
        arguments = {}

    if name == "generate_google_script":
        topic = arguments.get("topic")
        if not topic:
            return [types.TextContent(
                type="text",
                text="Error: topic parameter is required"
            )]
        
        format_type = arguments.get("format_type", "dialogue")
        duration_minutes = arguments.get("duration_minutes", 5)
        additional_context = arguments.get("additional_context", {})
        
        # Generate optimized prompt for Google TTS
        prompt = generate_google_tts_prompt(
            topic=topic,
            format_type=format_type,
            duration_minutes=duration_minutes,
            additional_context=additional_context
        )
        
        # Also generate a sample script
        sample_turns = generate_dialogue_turns(
            topic=topic,
            format_type=format_type,
            duration_minutes=duration_minutes,
            additional_context=additional_context
        )
        
        # Format sample as Google script
        sample_script = "\n".join([f"{turn['speaker']}|{turn['text']}" for turn in sample_turns])
        
        return [types.TextContent(
            type="text",
            text=f"""Generated Google TTS podcast script prompt:

{prompt}

---
SAMPLE SCRIPT (Generated):

{sample_script}

---
Note: This script is formatted for Google Cloud Text-to-Speech multi-speaker feature.
Each line uses the format: SPEAKER_ID|Dialogue text
Valid speakers: R, S, T, U"""
        )]

    elif name == "create_google_audio":
        script = arguments.get("script")
        if not script:
            return [types.TextContent(
                type="text",
                text="Error: script parameter is required"
            )]
        
        output_filename = arguments.get("output_filename", "google_podcast.mp3")
        language_code = arguments.get("language_code", "en-US")
        
        try:
            # Check for Google Cloud credentials
            if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                return [types.TextContent(
                    type="text",
                    text="""Error: Google Cloud credentials not configured.

Please set up Google Cloud TTS:
1. Create a Google Cloud account
2. Enable Text-to-Speech API
3. Create a service account key
4. Set environment variable:
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
"""
                )]
            
            try:
                from google.cloud import texttospeech
                
                # Initialize client
                client = texttospeech.TextToSpeechClient()
                
                # Parse script into turns
                turns = parse_google_script(script)
                
                if not turns:
                    return [types.TextContent(
                        type="text",
                        text="Error: No valid dialogue turns found. Use format: R|Text"
                    )]
                
                # Create MultiSpeakerMarkup
                multi_speaker_markup = texttospeech.MultiSpeakerMarkup(
                    turns=[
                        texttospeech.MultiSpeakerMarkup.Turn(
                            text=turn["text"],
                            speaker=turn["speaker"]
                        )
                        for turn in turns
                    ]
                )
                
                # Create synthesis input
                synthesis_input = texttospeech.SynthesisInput(
                    multi_speaker_markup=multi_speaker_markup
                )
                
                # Configure voice
                voice = texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    name=f"{language_code}-Studio-MultiSpeaker"
                )
                
                # Configure audio
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=1.0,
                    pitch=0.0
                )
                
                # Generate speech
                logger.info(f"Generating audio with {len(turns)} dialogue turns...")
                response = client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )
                
                # Save audio file
                output_dir = os.path.expanduser("~/Desktop/google_podcasts")
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, "wb") as out:
                    out.write(response.audio_content)
                
                # Generate summary
                speaker_counts = {}
                for turn in turns:
                    speaker = turn["speaker"]
                    speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
                
                result_message = f"""
✅ Google TTS podcast created successfully!

📁 Output: {output_path}
🎙️ Voice: {language_code}-Studio-MultiSpeaker
📊 Statistics:
- Total turns: {len(turns)}
- Speakers used: {', '.join(sorted(speaker_counts.keys()))}
- Turn distribution: {', '.join([f'{k}:{v}' for k, v in sorted(speaker_counts.items())])}
- File size: {len(response.audio_content) / 1024:.1f} KB

🎭 Speaker Guide:
{chr(10).join([f"  • {k}: {GOOGLE_SPEAKERS[k]['description']}" for k in sorted(speaker_counts.keys())])}

🎧 Your multi-speaker podcast is ready!
"""
                
                return [types.TextContent(
                    type="text",
                    text=result_message.strip()
                )]
                
            except ImportError:
                return [types.TextContent(
                    type="text",
                    text="""Error: Google Cloud TTS library not installed.

Please install:
pip install google-cloud-texttospeech

Then set up authentication:
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
"""
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error creating audio: {str(e)}"
            )]

    elif name == "convert_to_google_format":
        script = arguments.get("script")
        if not script:
            return [types.TextContent(
                type="text",
                text="Error: script parameter is required"
            )]
        
        speaker_mapping = arguments.get("speaker_mapping", {})
        
        # Auto-create mapping if not provided
        if not speaker_mapping:
            # Find all speakers in the script
            speakers = []
            lines = script.split('\n')
            
            for line in lines:
                # Try different formats
                if ':' in line:
                    match = re.match(r'^([A-Za-z\s\-\'\.]+?)(?:\s*\[.*?\])?\s*:\s*', line)
                    if match:
                        speaker = match.group(1).strip()
                        if speaker and speaker not in speakers:
                            speakers.append(speaker)
            
            # Map to Google speakers
            google_ids = ["R", "S", "T", "U"]
            for i, speaker in enumerate(speakers[:4]):  # Max 4 speakers
                speaker_mapping[speaker] = google_ids[i]
        
        # Convert script
        converted_lines = []
        lines = script.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to parse speaker and text
            if ':' in line:
                match = re.match(r'^([A-Za-z\s\-\'\.]+?)(?:\s*\[.*?\])?\s*:\s*(.+)$', line)
                if match:
                    speaker = match.group(1).strip()
                    text = match.group(2).strip()
                    
                    # Map to Google speaker ID
                    google_id = speaker_mapping.get(speaker)
                    if google_id and text:
                        converted_lines.append(f"{google_id}|{text}")
        
        if not converted_lines:
            return [types.TextContent(
                type="text",
                text="Error: Could not convert script. No valid dialogue found."
            )]
        
        converted_script = "\n".join(converted_lines)
        
        return [types.TextContent(
            type="text",
            text=f"""✅ Script converted to Google format:

SPEAKER MAPPING:
{chr(10).join([f"  • {k} → {v} ({GOOGLE_SPEAKERS[v]['description']})" for k, v in speaker_mapping.items()])}

CONVERTED SCRIPT:
{converted_script}

---
Ready to use with create_google_audio tool!"""
        )]

    else:
        return [types.TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]


async def run():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="podcast-generator-google",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())