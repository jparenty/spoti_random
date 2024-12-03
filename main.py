import click
import time

from utils.db import DbUtil
from ascii_art import AsciiArt



def navigate(ascii, user: DbUtil):
    while True:
      
      route = click.prompt(click.style("Enter a route (get tracks, about, contact, help, exit)"), type=str)

      match route:
        case "get tracks":
            user.get_user_tracks()
        # case "generate playlists":
        #     user.generate_playlists(genres_liked_songs)
        # case "get playlists stats":
        #     user.get_playlists_stats(playlists)
        # case "write playlists to spotify":
        #     user.user_write_spotify_playlists(playlists)
        case "exit":
            ascii.by_ascii()
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

    user = DbUtil(user_name=user_name)
    ascii.success_auth_ascii()

    navigate(ascii, user)
       
    
    breakpoint()
    #songs_number = int(songs_number)
    #print current user information

    #navigate(user, songs_number)

    return

if __name__ == '__main__':
    main()