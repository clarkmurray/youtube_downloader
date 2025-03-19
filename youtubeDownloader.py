# from pytube import YouTube
# from sys import argv

# link = argv[1] # First command line argument; argv[0] is always the program name

# yt = YouTube(link)

# stream = yt.streams.get_highest_resolution()

# print("Downloading \"" + yt.title + "\" from " + yt.author + " in " + stream.resolution)
# stream.download("/Users/clarkmurray/Movies/YouTube Downloads")
# print("Download is complete")



from pytubefix import YouTube
from pytubefix.cli import on_progress
from sys import argv


# url = "url"

url = argv[1] # First command line argument; argv[0] is always the program name

yt = YouTube(url, on_progress_callback=on_progress)

print(yt.title)
# print("Downloading \"" + yt.title + "\" from " + yt.author + " in " + stream.resolution)
ys = yt.streams.get_highest_resolution()
ys.download()
print("Download is complete")