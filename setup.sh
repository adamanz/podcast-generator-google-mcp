#!/bin/bash
# Setup script for Google TTS Podcast Generator

echo "🎙️ Setting up Google TTS Podcast Generator..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install mcp google-cloud-texttospeech

# Check for Google credentials
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo ""
    echo "⚠️  Warning: GOOGLE_APPLICATION_CREDENTIALS not set"
    echo ""
    echo "To use this tool, you need to:"
    echo "1. Create a Google Cloud account"
    echo "2. Enable the Text-to-Speech API"
    echo "3. Create a service account key"
    echo "4. Set the environment variable:"
    echo "   export GOOGLE_APPLICATION_CREDENTIALS='path/to/your-key.json'"
    echo ""
fi

# Create output directory
echo "📁 Creating output directory..."
mkdir -p ~/Desktop/google_podcasts

# Create sample config
cat > mcp_config_sample.json << 'EOF'
{
  "mcpServers": {
    "podcast-generator-google": {
      "command": "python",
      "args": ["google_podcast_server.py"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your-service-account-key.json"
      }
    }
  }
}
EOF

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Set up Google Cloud credentials (see README.md)"
echo "2. Update mcp_config_sample.json with your key path"
echo "3. Add to your Claude MCP configuration"
echo "4. Run: python google_podcast_server.py"
echo ""
echo "🎯 Quick test:"
echo "   python test_google_tts.py"