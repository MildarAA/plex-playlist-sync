import os
import logging
import subprocess
import re

from .helperClasses import Playlist, UserInputs, Track

def downloadPlaylist(playlist : Playlist,userInputs : UserInputs ):
	if userInputs.download_folder and playlist.url:
		#dowload to playlist folder
		playlist_folder = os.path.join(userInputs.download_folder.replace('"', ''),playlist.name)

		if not os.path.isdir(playlist_folder):
			os.makedirs(playlist_folder)
		output = os.path.join(playlist_folder,r"{title}")
		subprocess.run(["spotdl","sync", playlist.url, "--save-file","sync.spotdl", "--output", output],cwd=playlist_folder)

def sort_playlist_into_albums(playlist: Playlist, tracks: list[Track], userInputs : UserInputs):
	#sort downloaded into albums
	if userInputs.download_folder and playlist.url and (len(tracks)>0):
		playlist_folder = os.path.join(userInputs.download_folder.replace('"', ''),playlist.name)
		i=0
		for track in tracks:
			i=i+1
			filename = track.title + ".mp3"
			filename = filename.replace('"','\'').replace("/","")
			org_path = os.path.join(playlist_folder,filename) 
			if os.path.isfile(org_path):
				new_path = os.path.join(userInputs.plex_folder.replace('"', ''), re.sub(r'[\\/*?:"<>|]',"_",track.artist), re.sub(r'[\\/*?:"<>|]',"_",track.album),filename)
				if not os.path.isfile(new_path):
					new_folder = os.path.dirname(new_path)
					if not os.path.isdir(new_folder):
						os.makedirs(new_folder)
					os.link(org_path,new_path)
					if not os.path.isfile(new_path):
						logging.error ("File not sucessfully sorted to plex folder: " + new_path)
				else:
					logging.info("File already sorted into plex folder: "+ filename)
			else:
				logging.info("Downloaded file not found: "+org_path)