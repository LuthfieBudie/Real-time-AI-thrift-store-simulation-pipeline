import pygame
import os
from config import music_file

try:
    pygame.mixer.init()
    music_available = True
except:
    music_available = False




sfx_day = None

def load_sfx():
    global sfx_day
    if not music_available:
        return
    try:
        sfx_day = pygame.mixer.Sound("./song/sfx/day.mp3")
    except Exception as e:
        pass

def play_sfx_day(music_playing):
    if sfx_day and music_playing:
        try:
            sfx_day.play()
        except:
            pass

load_sfx()





def autostart_music(music_playing):
    if not music_available:
        return
    try:
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
            return True
    except Exception as e:
        from logger import tulis_log
        tulis_log(f"Music autostart failed: {str(e)}")
    return False

def toggle_music_state(current_state):
    if not music_available:
        return current_state
    new_state = not current_state
    if new_state:
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)
        except Exception as e:
            from logger import tulis_log
            tulis_log(f"Error playing music: {str(e)}")
    else:
        pygame.mixer.music.stop()
    return new_state

def stop_music():
    if not music_available:
        return
    try:
        pygame.mixer.music.stop()
    except:
        pass

def is_music_available():
    return music_available
