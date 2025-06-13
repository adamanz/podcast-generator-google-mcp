# Google Cloud TTS Podcast Generator MCP

A podcast generator that leverages Google Cloud Text-to-Speech's multi-speaker feature to create natural conversations with distinct voices.

## 🎙️ Key Features

- **Multi-Speaker Support**: Up to 4 distinct speakers (R, S, T, U) with unique voices
- **Natural Dialogue**: Optimized for conversational flow using Google's MultiSpeakerMarkup
- **Multiple Formats**: Interview, debate, roundtable, storytelling, educational
- **Simple Script Format**: Easy `R|Text` format for dialogue
- **High Quality**: Google's Studio-quality multi-speaker voice

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud Account**
   - Create account at https://cloud.google.com
   - Enable Text-to-Speech API
   - Create service account and download key

2. **Python Setup**
```bash
pip install mcp google-cloud-texttospeech
```

3. **Authentication**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

### Installation

```bash
git clone https://github.com/adamanz/podcast-generator-google-mcp.git
cd podcast-generator-google-mcp
pip install -r requirements.txt
```

### Configuration

Add to your Claude MCP settings:

```json
{
  "mcpServers": {
    "podcast-generator-google": {
      "command": "python",
      "args": ["path/to/google_podcast_server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "path/to/service-account-key.json"
      }
    }
  }
}
```

## 📚 Usage

### Generate a Script

```python
generate_google_script(
    topic="Artificial Intelligence",
    format_type="interview",
    duration_minutes=5,
    additional_context={
        "key_points": ["machine learning", "ethics", "future applications"],
        "tone": "informative yet accessible"
    }
)
```

### Create Audio

```python
create_google_audio(
    script="""
    R|Welcome to our podcast about AI!
    S|Thanks for having me. It's exciting to discuss this topic.
    R|Let's start with the basics. What is AI?
    S|AI is technology that enables machines to simulate human intelligence.
    """,
    output_filename="ai_podcast.mp3"
)
```

### Convert Existing Scripts

```python
convert_to_google_format(
    script="""
    Host: Welcome to the show!
    Expert: Thanks for having me.
    """,
    speaker_mapping={"Host": "R", "Expert": "S"}
)
```

## 🎭 Available Speakers

Google's multi-speaker voice provides 4 distinct speakers:

- **R**: Warm, engaging voice - perfect for hosts
- **S**: Clear, analytical voice - ideal for experts
- **T**: Dynamic, energetic voice - great for commentary
- **U**: Thoughtful, contemplative voice - good for deeper insights

## 📋 Podcast Formats

### 1. Dialogue
Simple two-person conversation
- Speakers: R, S
- Use: General discussions

### 2. Interview
Host interviewing an expert
- Speakers: R (Host), S (Expert)
- Use: Q&A sessions

### 3. Roundtable
Multi-person discussion
- Speakers: R, S, T, U
- Use: Panel discussions

### 4. Storytelling
Narrative with character voices
- Speakers: R (Narrator), S (Character 1), T (Character 2)
- Use: Story podcasts

### 5. Educational
Teaching format
- Speakers: R (Teacher), S (Student)
- Use: Tutorial content

### 6. Debate
Point-counterpoint discussion
- Speakers: R (Moderator), S (Advocate), T (Opponent)
- Use: Exploring different viewpoints

## 🔧 Script Format

Use the pipe format for clarity:

```
R|Welcome to today's episode about space exploration.
S|It's fascinating how far we've come in understanding the cosmos.
R|What excites you most about recent discoveries?
S|The James Webb telescope has revealed incredible details about distant galaxies.
T|And don't forget about the Mars missions!
```

## 💡 Tips

1. **Keep turns concise**: 1-3 sentences per turn works best
2. **Use all speakers**: Distribute dialogue among available speakers
3. **Natural flow**: Include reactions and follow-up questions
4. **Emotional text**: Write emotions into the dialogue itself

## 🌟 Example

### Input Script
```
R|Welcome to Tech Talk! Today we're discussing the future of renewable energy.
S|Thanks for having me. This is such a crucial topic for our planet.
R|Let's start with solar power. What are the latest breakthroughs?
S|We're seeing incredible efficiency improvements, with some panels now exceeding 26% efficiency.
T|That's amazing! I remember when 15% was considered cutting-edge.
R|How does this impact adoption rates?
S|The improved efficiency, combined with lower costs, is accelerating deployment worldwide.
```

### Output
A natural-sounding podcast with three distinct voices having a genuine conversation.

## 🛠️ Advanced Features

### Custom Context
Provide additional context for more focused scripts:

```python
additional_context={
    "key_points": ["solar efficiency", "cost reduction", "global adoption"],
    "tone": "optimistic but realistic",
    "target_audience": "general public",
    "include_data": True
}
```

### Language Support
While optimized for English, supports multiple languages:
```python
create_google_audio(
    script="...",
    language_code="es-ES"  # Spanish
)
```

## 📊 Comparison with ElevenLabs Version

| Feature | Google TTS | ElevenLabs |
|---------|------------|------------|
| Speakers | 4 fixed (R,S,T,U) | Unlimited custom |
| Voice Quality | High | Very High |
| Customization | Limited | Extensive |
| Cost | Pay-per-use | Subscription |
| Setup | More complex | Simpler |
| Multi-speaker | Native support | Manual assignment |

## 🚨 Troubleshooting

### Authentication Error
```
Error: Google Cloud credentials not configured
```
**Solution**: Set GOOGLE_APPLICATION_CREDENTIALS environment variable

### API Not Enabled
```
Error: Text-to-Speech API has not been used in project
```
**Solution**: Enable the API in Google Cloud Console

### Invalid Script Format
```
Error: No valid dialogue turns found
```
**Solution**: Use the `R|Text` format for each line

## 📄 License

MIT License - see LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🔗 Resources

- [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)
- [Multi-speaker Feature Guide](https://cloud.google.com/text-to-speech/docs/multi-speaker)
- [Authentication Setup](https://cloud.google.com/docs/authentication/getting-started)