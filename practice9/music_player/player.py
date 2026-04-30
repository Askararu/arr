import pygame
import os
import glob


class MusicPlayer:

    # Colors
    BG_COLOR = (20, 20, 40)
    PRIMARY = (100, 180, 255)
    SECONDARY = (180, 180, 180)
    HIGHLIGHT = (255, 220, 50)
    WHITE = (255, 255, 255)
    GREEN = (80, 200, 120)
    RED = (220, 80, 80)
    DARK_GRAY = (50, 50, 70)
    PROGRESS_BG = (60, 60, 80)
    PROGRESS_FG = (100, 180, 255)

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.playback_pos = 0.0
        self.track_length = 0.0

        # Fonts
        self.font_title = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_body = pygame.font.SysFont("Arial", 22)
        self.font_small = pygame.font.SysFont("Arial", 16)
        self.font_key = pygame.font.SysFont("Consolas", 18, bold=True)

        # Load music
        self._load_playlist()

        self._elapsed_ms = 0

    def _load_playlist(self):
        """Load tracks from music/sample_tracks folder"""
        music_dir = os.path.join(os.path.dirname(__file__), "music", "sample_tracks")

        if not os.path.exists(music_dir):
            print("❌ Folder not found:", music_dir)
            self.playlist = []
            return

        self.playlist = []
        self.playlist += glob.glob(os.path.join(music_dir, "*.wav"))
        self.playlist += glob.glob(os.path.join(music_dir, "*.mp3"))

        self.playlist.sort()

        print("✅ Loaded tracks:", self.playlist)

    def _current_track_name(self):
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_index])

    def play(self):
        if not self.playlist:
            return

        track = self.playlist[self.current_index]

        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
            self.is_playing = True
            self._elapsed_ms = 0

            try:
                sound = pygame.mixer.Sound(track)
                self.track_length = sound.get_length()
            except:
                self.track_length = 0

        except Exception as e:
            print("Error:", e)

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.playback_pos = 0

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def update(self):
        if self.is_playing:
            if not pygame.mixer.music.get_busy():
                self.next_track()
            else:
                self._elapsed_ms += 1000 // 30
                self.playback_pos = self._elapsed_ms / 1000.0

    def draw(self):
        self.screen.fill(self.BG_COLOR)

        # Title
        title = self.font_title.render("Music Player", True, self.PRIMARY)
        self.screen.blit(title, (20, 15))

        # Track info
        track_name = self._current_track_name()
        status = "PLAYING" if self.is_playing else "STOPPED"
        status_color = self.GREEN if self.is_playing else self.RED

        self.screen.blit(self.font_body.render(status, True, status_color), (20, 70))
        self.screen.blit(self.font_body.render(track_name, True, self.WHITE), (20, 110))

        if self.playlist:
            info = f"{self.current_index + 1} / {len(self.playlist)}"
        else:
            info = "No tracks"
        self.screen.blit(self.font_small.render(info, True, self.SECONDARY), (20, 140))

        # Progress bar
        bar_x, bar_y = 20, 180
        bar_w, bar_h = self.width - 40, 10

        pygame.draw.rect(self.screen, self.PROGRESS_BG, (bar_x, bar_y, bar_w, bar_h))
        if self.track_length > 0:
            progress = self.playback_pos / self.track_length
            fill_w = int(bar_w * min(progress, 1))
            pygame.draw.rect(self.screen, self.PROGRESS_FG, (bar_x, bar_y, fill_w, bar_h))

        # Playlist
        y = 210
        for i, track in enumerate(self.playlist[:5]):
            name = os.path.basename(track)
            color = self.HIGHLIGHT if i == self.current_index else self.SECONDARY
            self.screen.blit(self.font_small.render(name, True, color), (20, y + i * 20))

        # Controls
        controls = "[P] Play  [S] Stop  [N] Next  [B] Back  [Q] Quit"
        self.screen.blit(self.font_small.render(controls, True, self.SECONDARY),
                         (20, self.height - 40))

    @staticmethod
    def _fmt_time(seconds):
        s = int(seconds)
        return f"{s // 60:02d}:{s % 60:02d}"

