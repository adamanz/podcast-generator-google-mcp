# 🚀 Google TTS Podcast Generator - Quick Start

## New Repository Created!

✅ Repository: https://github.com/adamanz/podcast-generator-google-mcp

## What's Been Created

A complete MCP server for podcast generation using Google Cloud Text-to-Speech's multi-speaker feature.

### Key Features
- **4 Distinct Speakers**: R (Host), S (Expert), T (Commentator), U (Analyst)
- **6 Podcast Formats**: Interview, Debate, Roundtable, Storytelling, Educational, Dialogue
- **Native Multi-speaker**: Uses Google's MultiSpeakerMarkup for natural conversations
- **Simple Format**: `R|Text` script format

### Files Created
- `google_podcast_server.py` - Main MCP server
- `README.md` - Comprehensive documentation
- `examples.md` - Script examples for all formats
- `test_google_tts.py` - Test suite
- `setup.sh` - Setup script
- `COMPARISON.md` - Google vs ElevenLabs comparison

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/adamanz/podcast-generator-google-mcp.git
cd podcast-generator-google-mcp
```

### 2. Google Cloud Setup
1. Create a Google Cloud account
2. Enable Text-to-Speech API
3. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Create new service account
   - Download JSON key file

### 3. Install Dependencies
```bash
./setup.sh
# Or manually:
pip install mcp google-cloud-texttospeech
```

### 4. Configure Authentication
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-key.json"
```

### 5. Add to Claude MCP Config

Update `/Users/adamanzuoni/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "podcast-generator-google": {
      "command": "python",
      "args": [
        "/Users/adamanzuoni/podcast-generator-google-mcp/google_podcast_server.py"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your-key.json"
      }
    }
  }
}
```

## Test the Tools

### 1. Run Test Suite
```bash
python test_google_tts.py
```

### 2. Generate a Script
After restarting Claude:
```
Use the Google podcast generator to create a 5-minute interview about "The Future of Renewable Energy" with clear speaker distinctions.
```

### 3. Create Audio
```
Create audio from this script:
R|Welcome to Green Future podcast!
S|Thanks for having me to discuss renewable energy.
R|What excites you most about solar technology?
S|The efficiency improvements are remarkable - we're seeing 30% efficiency now.
```

## Example Output

The Google TTS multi-speaker voice creates natural conversations with 4 distinct voices that are designed to work well together.

## Comparison with ElevenLabs

| Aspect | Google TTS | ElevenLabs |
|--------|------------|------------|
| Setup | More complex | Simpler |
| Voices | 4 fixed | Unlimited |
| Quality | High | Very high |
| Cost | Pay-per-use | Subscription |
| Best for | Quick podcasts | Premium content |

## Troubleshooting

### Authentication Error
```
export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/key.json"
```

### API Not Enabled
Enable Text-to-Speech API in Google Cloud Console

### Script Format Issues
Use the exact format: `R|Your text here`

## Next Steps

1. ✅ Set up Google Cloud credentials
2. ✅ Test with the provided examples
3. ✅ Create your own podcasts!

Enjoy creating natural multi-speaker podcasts with Google Cloud TTS! 🎙️