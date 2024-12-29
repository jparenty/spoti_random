import click
import time
import inquirer

from src.user import User
from ascii_art import AsciiArt



class Navigation:
    def __init__(self, ascii: AsciiArt, user: User):
        self.ascii = ascii
        self.user = user

    def _genre():
        raise NotImplementedError

    def _random_by_track(self):
        while True:
            route = [
                inquirer.List(
                    "choice",
                    message="Random",
                    choices=["Play Random Track", "Exit"],
                ),
            ]
            route = inquirer.prompt(route)
            self.ascii.remove_menu()
            if route["choice"] == "Play Random Track":
                self.ascii.random()
                self.user.play_random_track()
            if route["choice"] == "Exit":
                self.ascii.exit()
                return

    def _random(self):
    
        while True:

            self.ascii.random_menu()

            route = [
                inquirer.List(
                    "choice",
                    message="Random",
                    choices=["By Track", "By Mood", "Exit"],
                ),
            ]
            route = inquirer.prompt(route)
            self.ascii.remove_menu()

            if route["choice"] == "By Track":
                self.ascii.random_by_track()
                self._random_by_track()
                self.ascii.random_menu()
                
                continue

            if route["choice"] == "By Mood":
                print("Not implemented yet")
                self.ascii.random_menu()
                pass

            if route["choice"] == "Exit":
                self.ascii.exit()
                return

    def _set_playback_device(self):

        devices = self.user.connection.get_available_devices()

        if devices == []:
            click.secho("No devices available", fg="red")
            return
        
        device = [
            inquirer.List(
                "choice",
                message="Select a device for playback:",
                choices=devices,
            ),
        ]
        device = inquirer.prompt(device)
        self.ascii.remove_menu()

        self.user.device = device["choice"]

    def _profile_home(self):
        while True:

            route = [
                    inquirer.List(
                        "choice",
                        message="Profile",
                        choices=["Playback Device", "Update Tracks", "Exit"],
                    ),
                ]
            route = inquirer.prompt(route)
            self.ascii.remove_menu()

            if route["choice"] == "Playback Device":
                self._set_playback_device()
                continue

            if route["choice"] == "Update Tracks":
                self.user.update_tracks()
                continue

            if route["choice"] == "Exit":
                self.ascii.exit()
                return

    def home(self):
        
        self._set_playback_device()
        

        while True:
            
            self.ascii.home()

            route = [
                inquirer.List(
                    "choice",
                    message="Menu",
                    choices=["Profile", "Random", "Genre", "Exit"],
                ),
            ]
            route = inquirer.prompt(route)
            self.ascii.remove_menu()

            if route["choice"] == "Profile":
                self._profile_home()
                self.ascii.home()
                continue
            if route["choice"] == "Random":
                self._random()
                self.ascii.home()
                continue
            # case "playlist genre":
            #     self.ascii.navigate_genre()
            if route["choice"] == "Exit":
                self.ascii.bye()
                return
            else:
                click.secho("Unknown route, try again...", fg="red")


@click.command()
@click.argument("user_name")
@click.option("-s", "--speed", is_flag=True, help="Speed animations")
def main(user_name, speed):
    if speed:
        ascii = AsciiArt(speed=speed)
    else:
        ascii = AsciiArt()

    ascii.welcome_ascii()
    user = User(user_name)
    ascii.success_auth_ascii()

    navigation = Navigation(ascii, user)
    navigation.home()

    return

if __name__ == '__main__':
    main()