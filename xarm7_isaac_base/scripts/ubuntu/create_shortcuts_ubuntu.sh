#!/usr/bin/env bash
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DESKTOP="$HOME/Desktop/xarm7_isaac_research.desktop"

cat > "$DESKTOP" << EOF
[Desktop Entry]
Type=Application
Name=xArm7 Isaac Research
Exec=xdg-open "$ROOT"
Icon=folder
Terminal=false
EOF

chmod +x "$DESKTOP"
echo "Created desktop shortcut:"
echo "$DESKTOP"
