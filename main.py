import click

from utils.db import DbUtil

def navigate(user: DbUtil, songs_number: int):
    while True:
      
      route = click.prompt(click.style("Enter a route (get tracks, about, contact, help, exit)"), type=str)

      match route:
        case "get tracks":
            user.get_user_tracks(songs_number)
        # case "generate playlists":
        #     user.generate_playlists(genres_liked_songs)
        # case "get playlists stats":
        #     user.get_playlists_stats(playlists)
        # case "write playlists to spotify":
        #     user.user_write_spotify_playlists(playlists)
        case _:
            click.secho("Unknown route, try again...", fg="red")


@click.command()
@click.option("-u",'--user_name')
@click.option("-s",'--songs_number')
def main(user_name, songs_number):
    
    songs_number = int(songs_number)
    #print current user information
    user = DbUtil(user_name=user_name)

    navigate(user, songs_number)

    return

if __name__ == '__main__':
    main()