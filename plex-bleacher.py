import os
import json
from pathlib import Path
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.video import Show, Episode, Season
from plexapi.base import MediaContainer
from datetime import datetime, date

with open('episodes.json', encoding='utf-8') as f:
    series_data = json.load(f)

with open('config.json') as f:
    plex_data = json.load(f)

with open('tybw.json', encoding='utf-8') as f:
    tybw_data = json.load(f)

# your plex username or email
PLEX_LOGIN = plex_data['plex_username']

# your plex password
PLEX_PASSWORD = plex_data['plex_password']

# the name of your plex media server
PLEX_SERVER_NAME = plex_data['plex_server_name']

plex_account: MyPlexAccount = None
plex_server: PlexServer = None
cb_series: Show = None


def get_bleach_episode_metadata(season: int, episode: int):
    for key, value in series_data.get('episodes').items():
        if value['season'] == season and value['episode'] == episode:
            return key, value

    return None, None


def main():
    organize_files()
    apply_plex_metadata()
    apply_tybw_metadata()
    apply_cb_thumbnails()


def organize_files():
    # prompt user to scan for bleach episodes
    confirm = input('Scan for and organize edited Bleach episodes?\nY/N\n')
    if confirm.lower() != 'y':
        return

    files_moved = 0
    # organize files first
    for path, dirs, files in os.walk('.'):
        for file in files:
            if series_data['episodes'].get(file) is not None:
                # get episode metadata ready
                episode = series_data['episodes'].get(file)
                season_number = episode['season']
                episode_number = episode['episode']
                episode_title = episode['title']
                absolute_episode = episode['absolute_episode']

                # prepare the new file name
                extension = Path(file).suffix
                if file.find('Hollowed Bleach') != -1:
                    newname = f'Hollowed Bleach S{season_number:02d}E{episode_number:02d} - {episode_title} (HB {absolute_episode}){extension}'
                elif file.find('Chipped Bleach') != -1:
                    newname = f'Chipped Bleach S{season_number:02d}E{episode_number:02d} - {episode_title} (Chipped Bleach {absolute_episode}){extension}'
                else:
                    newname = f'Concentrated Bleach S{season_number:02d}E{episode_number:02d} - {episode_title} (CB {absolute_episode}){extension}'

                # prepare directories
                cb_root = 'Concentrated Bleach'
                if os.path.exists(cb_root) is False:
                    print('creating root series directory for Concentrated Bleach')
                    os.makedirs(cb_root)

                if season_number == 0:
                    season_path = 'Specials'
                else:
                    season_path = f'Season {season_number:02d}'

                if os.path.exists(f'{cb_root}/{season_path}') is False:
                    print(f'creating season folder for season {season_number}')
                    os.makedirs(f'{cb_root}/{season_path}')

                final_file = Path(f'{cb_root}/{season_path}/{newname}')
                if os.path.exists(final_file):
                    # skip over already existing episodes
                    continue

                # copy (hard link) episode to its destination
                print(f'copying {file} to {season_path} as {newname}')
                os.link(f'{path}/{file}', final_file)
                files_moved += 1

    print(f'{files_moved} episode(s) have been moved to their appropriate folders.\n')


def apply_plex_metadata():
    confirm = input('Would you like to apply episode metadata to Plex? Please only proceed when you\'ve moved the edited episodes and verified they\'re present in your media server.\nY/N\n')
    if confirm.lower() != 'y':
        return

    if plex_auth() is False:
        return

    print('Successfully found Concentrated Bleach series. Searching for episodes to apply metadata to.')
    episodes_changed = 0
    episodes: MediaContainer[Episode] = cb_series.episodes()
    for episode in episodes:
        _, metadata = get_bleach_episode_metadata(episode.seasonNumber, episode.episodeNumber)
        if metadata is None:
            continue

        changed = False
        if episode.title != metadata['title']:
            episode.editTitle(metadata['title'])
            episode.editSortTitle(metadata['title'])
            print(f"Applied episode title to {episode.seasonEpisode.upper()} ({metadata['title']})")
            changed = True

        newsummary = f'{metadata['summary']}\nManga Chapters: {metadata['chapters']}\nEdited Episodes: {metadata['episodes']}'
        if episode.summary != newsummary:
            episode.editSummary(newsummary)
            print(f"Applied episode summary to {episode.seasonEpisode.upper()}")
            changed = True

        date_comp = datetime.combine(date.fromisoformat(metadata['release_date']), datetime.min.time())
        if episode.originallyAvailableAt != date_comp:
            episode.editOriginallyAvailable(metadata['release_date'])
            print(f'Applied fake release date to {episode.seasonEpisode.upper()}')
            changed = True

        if changed is True:
            episodes_changed += 1

    print(f'Applied metadata to {episodes_changed} edited Bleach episode(s).')


def apply_tybw_metadata():
    confirm = input('OPTIONAL: Would you like to apply metadata to the TYBW arc? Only select this if those episodes are present under a Season 5 folder.\nY/N\n')
    if confirm.lower() != 'y':
        return

    if plex_auth() is False:
        return

    season: Season = cb_series.seasons()[-1]  # assume the last element in the list is TYBW
    episodes: MediaContainer[Episode] = season.episodes()
    episodes_changed = 0

    for episode in episodes:
        metadata = tybw_data[episode.episodeNumber - 1]

        changed = False
        if episode.title != metadata['title']:
            episode.editTitle(metadata['title'])
            episode.editSortTitle(metadata['title'])
            print(f"Applied episode title to {episode.seasonEpisode.upper()} ({metadata['title']})")
            changed = True

        newsummary = f'{metadata['summary']}\nManga Chapters: {metadata['chapters']}'
        if episode.summary != newsummary:
            episode.editSummary(newsummary)
            print(f"Applied episode summary to {episode.seasonEpisode.upper()}")
            changed = True

        if changed is True:
            episodes_changed += 1

    print(f'Applied metadata to {episodes_changed} edited Bleach episode(s).')


def apply_cb_thumbnails():
    confirm = input('Would you like to apply custom thumbnails authored by the creator of Concentrated Bleach? If you select no, Plex will simply use ones that it automatically generates. Sometimes they\'re kind of bad.\nY/N\n')
    if confirm.lower() != 'y':
        return

    if plex_auth() is False:
        return

    episodes: Episode = cb_series.episodes()
    for episode in episodes:
        originalname, metadata = get_bleach_episode_metadata(episode.seasonNumber, episode.episodeNumber)

        if originalname is None:
            # skip episodes that don't resolve any metadata
            continue

        if originalname.find('Hollowed Bleach') != -1 or originalname.find('Chipped Bleach') != -1:
            # skip episodes that aren't Concentrated Bleach edits
            continue

        absolute_episode = metadata['absolute_episode']
        if isinstance(metadata['absolute_episode'], str):
            absolute_episode = absolute_episode.rsplit(' ')[0]  # remove the (0) from episode 35.5 (jank)
        elif isinstance(absolute_episode, int):
            absolute_episode = f'{absolute_episode:02d}'  # apply leading zeroes when the CB episode is a regular int

        print(f'Applied custom thumbnail to {episode.seasonEpisode.upper()}')
        path = f'thumbnails/{absolute_episode}.png'
        episode.uploadPoster(filepath=path)


def plex_auth():
    global plex_account
    if plex_account is None:
        print('Attempting to authenticate with Plex using the credentials provided.')
        plex_account = MyPlexAccount(PLEX_LOGIN, PLEX_PASSWORD)
        if plex_account is None:
            print('Failed to authenticate with Plex.')
            return False

    global plex_server
    if plex_server is None:
        print(f'Successfully authenticated with Plex. Now attempting to connect to media server ({PLEX_SERVER_NAME})')
        plex_server = plex_account.resource(PLEX_SERVER_NAME).connect()
        if plex_server is None:
            print(f'Failed to connected to the media server ({PLEX_SERVER_NAME})')
            return False

    global cb_series
    if cb_series is None:
        print('Searching for Concentrated Bleach TV series')
        cb_series = plex_server.search('Concentrated Bleach', 'show')[0]
        if cb_series is None:
            print('Unable to find Concentrated Bleach TV series. Pleae add it to your plex library and populate it with Bleach episodes.')
            return False

    return True


main()
