from typing import Optional

import pyfiglet
import time

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
    

    def welcome_ascii(self):

        message1 = "HELLO WORLD"
        message2 = "WELCOME"
        message3 = "TO"
        message4 = "THE"
        message5 = "TRULY"
        message6 = "RANDOM"
        message7 = "EXPERIENCE"

        ascii_art1 = pyfiglet.figlet_format(message1)
        self._print(ascii_art1)
        self._sleep_long()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message2)
        self._print(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message3)
        self._print(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message4)
        self._print(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message5)
        self._print(ascii_art2)
        self._sleep()

        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message6)
        self._print(ascii_art2)
        self._sleep()
        
        print("\033[F\033[K" * 5, end="")
        ascii_art2 = pyfiglet.figlet_format(message7)
        self._print(ascii_art2)
        self._sleep()
        
        print("\033[F\033[K" * 5, end="")

    def welcome_random(self):
        message1 = "FUCK"
        message2 = "YEAH"
        message3 = "TRULY"
        message4 = "RANDOM"
        message5 = "SONGS"

        ascii_art1 = pyfiglet.figlet_format(message1)
        self._sleep_short()
        self._print(ascii_art1)
        print("\033[F\033[K" * 5, end="")

        ascii_art2 = pyfiglet.figlet_format(message2)
        self._sleep_short()
        self._print(ascii_art2)
        print("\033[F\033[K" * 5, end="")

        ascii_art3 = pyfiglet.figlet_format(message3)
        self._sleep_short()
        self._print(ascii_art3)
        print("\033[F\033[K" * 5, end="")

        ascii_art4 = pyfiglet.figlet_format(message4)
        self._sleep_short()
        self._print(ascii_art4)
        print("\033[F\033[K" * 5, end="")

        ascii_art5 = pyfiglet.figlet_format(message5)
        self._sleep_short()
        self._print(ascii_art5)
        print("\033[F\033[K" * 5, end="")
    
    def by_track(self):
        message1 = "BY"
        message2 = "TRACK"

        ascii_art1 = pyfiglet.figlet_format(message1)
        self._sleep()
        self._print(ascii_art1)
        print("\033[F\033[K" * 5, end="")

        ascii_art2 = pyfiglet.figlet_format(message2)
        self._sleep()
        self._print(ascii_art2)
        print("\033[F\033[K" * 5, end="")

    def success_auth_ascii(self):
        message1 = "SUCCESS"
        message2 = "AUTH"


        ascii_art1 = pyfiglet.figlet_format(message1)
        ascii_art2 = pyfiglet.figlet_format(message2)
        self._print(ascii_art1)
        self._print(ascii_art2)
        self._sleep_long()
        print("\033[F\033[K" * 11, end="")
        print(ascii_art2)
        print("\033[F\033[K" * 6, end="")
        #delay(ascii_art2)
        self._sleep()

    # def random(self):
    #     message1 = "Random ."
    #     message2 = "Random .."
    #     message3 = "Random ..."
        
    #     ascii_art1 = pyfiglet.figlet_format(message1)
    #     ascii_art2 = pyfiglet.figlet_format(message2)
    #     ascii_art3 = pyfiglet.figlet_format(message3)

    #     self._print(ascii_art1)
    #     self.print(ascii_art2)
    #     self.print(ascii_art3)



    def by_ascii(self):
        pass

