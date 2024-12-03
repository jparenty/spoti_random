from typing import Optional

import pyfiglet
import time

class AsciiArt:
    def __init__(self, speed: Optional[bool] = None):
        self.speed = speed

    def _delay(self, messasge):
        if self.speed:
            for char in messasge:
                print(char, end="", flush=True)
                time.sleep(0.00001) 
        else:
            for char in messasge:
                print(char, end="", flush=True)
                time.sleep(0.001) 

    def _sleep(self):
        if self.speed:
            time.sleep(0.1) 
        else:
            time.sleep(0.5)
    
    def _sleep_long(self):
        if self.speed:
            time.sleep(0.3)
        else:
            time.sleep(1.5) 


    def welcome_ascii(self):

        message1 = "HELLO WORLD"
        message2 = "WELCOME"
        message3 = "TO"
        message4 = "THE"
        message5 = "TRULY"
        message6 = "RANDOM"
        message7 = "EXPERIENCE"

        ascii_art1 = pyfiglet.figlet_format(message1)
        self._delay(ascii_art1)
        self._sleep_long()
        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message2)
        self._delay(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message3)
        self._delay(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message4)
        self._delay(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message5)
        self._delay(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message6)
        self._delay(ascii_art2)
        self._sleep()
        
        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message7)
        self._delay(ascii_art2)
        self._sleep()
        
        print("\033[F\033[K" * 5, end="")

    def success_auth_ascii(self):
        message1 = "SUCCESS"
        message2 = "AUTH"


        ascii_art1 = pyfiglet.figlet_format(message1)
        ascii_art2 = pyfiglet.figlet_format(message2)
        self._delay(ascii_art1)
        self._delay(ascii_art2)
        self._sleep_long()
        print("\033[F\033[K" * 11, end="")
        print(ascii_art2)
        print("\033[F\033[K" * 6, end="")
        #delay(ascii_art2)
        self._sleep()

    def by_ascii(self):
        pass