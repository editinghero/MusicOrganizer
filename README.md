# 🎵 Music Organizer (Windows GUI)

A simple and smart Windows tool that organizes your music files into artist-based folders.

## ✨ Features

- Supports `.mp3`, `.flac`, `.wav`, `.m4a`
- Automatically detects multiple artists (e.g., `Artist1; Artist2`) and creates separate folders for each
- Clean GUI — no coding required
- Preview categorization before organizing
- Copies songs into artist folders (does not move or delete originals)
- Summary plan generated before organizing

## 🖥️ How to Use

1. Run the tool (`.py` or `.exe`)
2. Select your music folder
3. Click **Preview Plan** to see folder structure
4. Click **Organize Now** to copy songs to artist folders

## 📦 Build from Source (Optional)

```bash
pip install mutagen
pyinstaller --onefile --noconsole music_Organizer.py
