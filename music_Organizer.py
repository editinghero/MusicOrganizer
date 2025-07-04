import os
import shutil
from mutagen import File
from tkinter import Tk, Label, Button, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

SUPPORTED_FORMATS = ('.mp3', '.flac', '.wav', '.m4a')


import re

def get_artists(filepath):
    try:
        audio = File(filepath, easy=True)
        if audio is None:
            return []

        tags = audio.get('artist') or audio.get('albumartist') or []
        if isinstance(tags, str):
            tags = [tags]

        artists = []
        for tag in tags:
            # Normalize and split on multiple delimiters
            tag = re.sub(r'(?i)\b(feat\.?|ft\.?)\b', ',', tag)
            parts = re.split(r'[;,:&]+|:', tag)
            for part in parts:
                clean = part.strip()
                if clean:
                    artists.append(clean)

        return artists or ["Unknown Artist"]
    except Exception:
        return ["Unknown Artist"]



class MusicOrganizerApp:
    def __init__(self, master):
        self.master = master
        master.title("🎧 Music Organizer Pro")
        master.geometry("700x580")

        Label(master, text="🎵 Step 1: Choose your music folder", font=("Arial", 12)).pack(pady=(15, 5))

        Button(master, text="📂 Browse Folder", width=20, command=self.choose_folder).pack()

        Label(master, text="📝 Step 2: Preview and organize by artist", font=("Arial", 12)).pack(pady=(20, 5))

        self.preview_button = Button(master, text="🔍 Preview Plan", width=20, state="disabled", command=self.preview)
        self.preview_button.pack()

        self.run_button = Button(master, text="🚀 Organize Now", width=20, state="disabled", command=self.organize)
        self.run_button.pack(pady=(10, 20))

        self.status = ScrolledText(master, height=20, width=85, font=("Courier", 9))
        self.status.pack(padx=10, pady=5)

        self.music_folder = None
        self.organization = {}

    def log(self, msg):
        self.status.insert('end', msg + '\n')
        self.status.see('end')
        self.status.update()

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Select Your Music Folder")
        if folder:
            self.music_folder = folder
            self.log(f"📁 Selected folder: {folder}")
            self.preview_button.config(state="normal")
            self.run_button.config(state="disabled")
            self.organization = {}

    def preview(self):
        self.status.delete(1.0, 'end')
        self.organization = {}

        for root, _, files in os.walk(self.music_folder):
            for file in files:
                if file.lower().endswith(SUPPORTED_FORMATS):
                    full_path = os.path.join(root, file)
                    artists = get_artists(full_path)
                    if not artists:
                        artists = ["Unknown Artist"]
                    for artist in artists:
                        self.organization.setdefault(artist, []).append(full_path)

        if not self.organization:
            self.log("⚠️ No supported music files found.")
            return

        self.log("📊 Preview of artist-wise categorization:\n")
        for artist, files in self.organization.items():
            self.log(f"{artist}:")
            for file in files:
                self.log(f"  {os.path.basename(file)}")
            self.log("")

        # Save summary
        plan_path = os.path.join(self.music_folder, "music_organization_plan.txt")
        with open(plan_path, 'w', encoding='utf-8') as f:
            for artist, files in self.organization.items():
                f.write(f"{artist}:\n")
                for file in files:
                    f.write(f"  {file}\n")
                f.write("\n")
        self.log(f"✅ Plan saved to: {plan_path}")
        self.run_button.config(state="normal")

    def organize(self):
        dest_root = os.path.join(self.music_folder, "Organized")
        os.makedirs(dest_root, exist_ok=True)

        for artist, files in self.organization.items():
            artist_folder = os.path.join(dest_root, artist)
            os.makedirs(artist_folder, exist_ok=True)
            for file_path in files:
                dest_path = os.path.join(artist_folder, os.path.basename(file_path))
                try:
                    shutil.copy2(file_path, dest_path)
                except Exception as e:
                    self.log(f"⚠️ Error copying {file_path} to {artist_folder}: {e}")

        self.log("\n✅ All songs copied into their respective artist folders.")
        messagebox.showinfo("Done", "🎉 Music successfully organized by artist!")

if __name__ == "__main__":
    root = Tk()
    app = MusicOrganizerApp(root)
    root.mainloop()
