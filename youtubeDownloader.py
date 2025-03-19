# from pytubefix import YouTube
# from pytubefix.cli import on_progress
# # from sys import argv

# output_directory = "/Users/clarkmurray/Movies/YouTube Downloads"
# file_name = ""

# # video_url = argv[1] # First command line argument; argv[0] is always the program name

# video_url = input("Input YouTube video URL: ")

# youtube_video = YouTube(video_url, on_progress_callback=on_progress)
# youtube_video_title = youtube_video.title

# use_custom_file_name = input("Would you like to give the file a custom ? (Y/N): ").lower().strip() == 'y'

# if (use_custom_file_name):
#     file_name = input("Enter a custom file name: ")
# else:
#     file_name = youtube_video_title

# youtube_video_stream = youtube_video.streams.get_highest_resolution(False)
# print("Downloading \"" + youtube_video_title + "\" from YouTube in " + youtube_video_stream.resolution + " resolution")
# youtube_video_stream.download(output_path=output_directory, filename=file_name + ".mp4")
# print("\nDownload is complete")


# # Prompt for URL in the command line
# # Custom file name

# # Download in 1080p resolution
# # Make download compatible with Quicktime Player
# # Combine mp4 & mp3 files if necessary

from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess

def download_video():
    # Ask the user to provide the YouTube video URL
    url = input("Please enter the YouTube video URL: ")

    try:
        # Create a YouTube object
        yt = YouTube(url, on_progress_callback=on_progress)

        # Display the video title
        print(f"Downloading video: {yt.title}")

        # Get the stream with the highest resolution (may be adaptive)
        video_stream = yt.streams.get_highest_resolution(False)
        print(f"Selected video stream: {video_stream.resolution} ({video_stream.fps}fps)")

        # Check if the stream is adaptive
        if not video_stream.is_progressive:
            # Get the audio stream with the best quality
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            print(f"Selected audio stream: {audio_stream.abr}")

            if not audio_stream:
                raise Exception('No suitable audio stream found.')

            # Download the video and audio streams
            video_path = video_stream.download(filename="video.mp4")
            print(f"Video stream downloaded: {video_path}")
            audio_path = audio_stream.download(filename="audio.mp4")
            print(f"Audio stream downloaded: {audio_path}")

            # Combine the video and audio streams with ffmpeg
            output_path = "final_video.mp4"
            subprocess.run([
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_path
            ])
            print(f"Combined video saved: {output_path}")

            # Clean up temporary files
            os.remove(video_path)
            os.remove(audio_path)

            print("Download and combination completed!")
        else:
            # Download the progressive stream
            video_stream.download(filename="final_video.mp4")
            print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_video()