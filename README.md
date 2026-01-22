# Plex Bleacher
Plex Bleacher is a simple and somewhat jank script that can be used to organize various edits of the Bleach anime on your Plex library. It offers the ability to organize your files into season folders appropriately, apply respective metadata through the Plex API and also assign custom episode thumbnails.

It is primarily meant to be used with the Concentrated Bleach edit, but also supports Hollowed Bleach and Chipped Bleach.

Optional support for the Thousand-Year Blood War arc to create a seamless watching experience for all of Bleach.

[Click here to download](https://github.com/TommyB123/plex-bleacher/archive/refs/heads/main.zip)

# Prerequisites
Requires episodes from the following edited versions of the Bleach anime to be present with **their file names untouched**
 * Concentrated Bleach (Substitute Soul Reaper, Soul Society and Arrancar (WIP) arcs)
 * Hollowed Bleach (Arrancar arc)
 * Chipped Bleach (Fullbring arc)

Requires a custom series named Concentrated Bleach to be present on your media server.


# How to use
* Ensure the Python programming language is available on your system. If you don't have it, you can easily grab it through the [Microsoft Store](https://apps.microsoft.com/detail/9pnrbtzxmb4z)
* Install the Plex API library for Python. Enter `pip install plexapi` into your command prompt/terminal.
* Download the latest release [here](https://github.com/TommyB123/plex-bleacher/archive/refs/heads/main.zip).
* Extract the zip file to the folder containing your edited Bleach episodes.
* Edit `config.json` with any text editor and fill out your Plex username and password alongside the name of the media server you will be creating your Concentrated Bleach series entry on.
* Answer Y/N (yes/no) to each prompt as they appear. 

# Benefits of this script
* Very easy to update with new releases.
* Hardlinks files when organizing into season folders, avoiding needless file duplication while also keeping original downloads intact.
* Uses the Plex API to directly apply metadata to edited Bleach episode entries inside of Plex.

# Data sources
[Concentrated Bleach Episode Names](https://docs.google.com/spreadsheets/d/1bz-Ye4yAXmX31K_abAV7kNUq3lwOBg6aiOxAHaFDRl8)

[Concentrated Bleach Episode Descriptions](https://gablog520.wordpress.com/)

[Concentrated Bleach Episode Thumbnails](https://drive.google.com/file/d/1GBQ3VMIPcpzyfH9bFfAZyFPlhv2XVrpX/view)

[Hollowed Bleach Episode Names](https://docs.google.com/spreadsheets/d/1-ipC6DpZw4GlmMnUw4fOsIWXCbK0s0St2vbsMPr6WfI/edit?gid=0#gid=0)

[Chipped Bleach Episode Names](https://docs.google.com/spreadsheets/d/1_mWoBFl2kmhKYDwkO4zM6O4YQscehVpGdzJ79Ro5YgU/edit?gid=463466426#gid=463466426)
