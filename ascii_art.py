from typing import Optional

import pyfiglet
import time


def stop():
    time.sleep(2)

class AsciiArt:
    def __init__(self, speed: Optional[bool] = None):
        self.speed = speed

    def _print(self, messasge):
        for char in messasge:
            print(char, end="", flush=True)
            time.sleep(0.001) 

    def _sleep_short(self):
        if self.speed:
            time.sleep(0.05) 
        else:
            time.sleep(0.1)

    def _sleep(self):
        if self.speed:
            time.sleep(0.15) 
        else:
            time.sleep(0.3)

    def _sleep_long(self):
        if self.speed:
            time.sleep(0.05) 
        else:
            time.sleep(0.1)
    
    def message(self, message: str):
        ascii_art = pyfiglet.figlet_format(message)
        self._print(ascii_art)
        self._sleep()
        print("\033[F\033[K" * 5, end="")
    
    def message_long(self, message: str):
        ascii_art = pyfiglet.figlet_format(message)
        self._sleep()
        self._print(ascii_art)
        print("\033[F\033[K" * 5, end="")


    def welcome_ascii(self):
        self.message("HELLO")
        self.message("WELCOME")
        self.message("SPOTIFY")
        self.message("EXTENSION")
        self.message("BY")
        self.message("JANUS")


    def welcome_random(self):
        self.message("FUCK")
        self.message("YEAH")
        self.message("TRULY")
        self.message("RANDOM")
        self.message("SONGS")
    
    def by(self):
        self.message_long("BY")
        stop()

    def exit(self):
        self.message_long("EXIT")

    def by_track(self):
        self.message_long("BY")
        self.message_long("TRACK")

    def home(self):
        self.message("HOME`")

    def random(self):
        self.message_long("RANDOM")

    def success_auth_ascii(self):
        self.message_long("SUCCESS")
        self.message_long("AUTH")

    def by_ascii(self):
        pass
