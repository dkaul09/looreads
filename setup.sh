#!/bin/bash
set -e

PROJ="/Users/dhruvkaul/Desktop/looreads"
PLIST="$HOME/Library/LaunchAgents/com.looreads.plist"

echo "=== LooReads Setup ==="
cd "$PROJ"

# Create virtual environment using Python 3.13
echo "Creating virtual environment..."
/usr/local/bin/python3.13 -m venv .venv

# Install dependencies
echo "Installing dependencies..."
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q

# Ensure .env exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  Created .env from template. Fill in your credentials:"
    echo "   $PROJ/.env"
    echo ""
fi

# Make scripts executable
chmod +x run.sh

# Create logs directory
mkdir -p logs

# Install LaunchAgent
echo "Installing LaunchAgent (daily 7:30 AM)..."
cp com.looreads.plist "$PLIST"

# Unload first if already loaded
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API credentials:"
echo "     nano $PROJ/.env"
echo ""
echo "  2. Test the digest now (dry run):"
echo "     cd $PROJ && source .venv/bin/activate && python main.py"
echo ""
echo "  3. LooReads will run automatically at 7:30 AM daily."
echo "     Logs: $PROJ/logs/looreads.log"
echo ""
echo "Twilio WhatsApp sandbox: text 'join <sandbox-keyword>' to +1 415 523 8886"
