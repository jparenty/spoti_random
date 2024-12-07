import click
import time

from utils.user import User
from ascii_art import AsciiArt



class Navigation:
    def __init__(self, ascii: AsciiArt, user: User):
        self.ascii = ascii
        self.user = user

    def bye():
        raise NotImplementedError

    def genre():
        raise NotImplementedError

    def _random_by_track(self):

        while True:
            route = click.prompt(click.style("Enter a route (by track, by playlist)"), type=str)
            
            if route == "":
                #self.ascii.random()
                self.user.generate_random_track()

            #if route == "":

    def _random(self):
    
        self.ascii.welcome_random()
        
        while True:
            route = click.prompt(click.style("Enter a route (by track, by playlist)"), type=str)
            route = route.lower()

            if route in ["by track", "tracks", "t"]:
                self.ascii.by_track()
                self._random_by_track()
            # match route:
            #     case "by track":
            #         user.get_user_tracks()
            #     case "by playlist":
            #         self.ascii.navigate_random()
            #     case _ if route == "exit" or route == "e":
            #         return

    def home(self):
        while True:
        
            route = click.prompt(click.style("Enter a route (update tacks, random, playlists)"), type=str)

            match route:
                case "update tracks":
                    self.user.update_tracks()
                case "random":
                    self._random()
                # case "playlist genre":
                #     self.ascii.navigate_genre()
                # case "exit":
                #     self.ascii.bye()
                case _:
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

    #db = DbUtil(user_name=user_name)
    
    user = User(user_name)
    ascii.success_auth_ascii()

    navigation = Navigation(ascii, user)
    navigation.home()
       
    
    breakpoint()
    #songs_number = int(songs_number)
    #print current user information

    #navigate(user, songs_number)

    return

if __name__ == '__main__':
    main()