from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess

# Prompt for URL in the command line
# Custom file name
# Download in 1080p resolution
# Combine mp4 & mp3 files
# Clean up ffmpeg from pip


# Clean up code
# Push to GitHub
# Script to run without navigating to directory
# Make download compatible with Quicktime Player

def download_video():
    try:
        output_directory = "/Users/clarkmurray/Movies/YouTube Downloads"
        custom_file_name = ""

        video_url = input("Input YouTube video URL: ")
        use_custom_file_name = input("Would you like to give the file a custom ? (Y/N): ").lower().strip() == 'y'

        if (use_custom_file_name):
            custom_file_name = input("Enter a custom file name: ")

        youtube_video = YouTube(video_url, on_progress_callback=on_progress)
        youtube_video_stream = youtube_video.streams.get_highest_resolution(False)
        
        file_name_with_extension = (custom_file_name if len(custom_file_name) > 0 else youtube_video.title) + ".mp4"

        print("Downloading \"" + youtube_video.title + "\" from YouTube in " + youtube_video_stream.resolution + " resolution")

        if not youtube_video_stream.is_progressive: # stream is adaptive
            output_path = output_directory + "/" + file_name_with_extension
            combine_video(youtube_video, youtube_video_stream, output_path)
            print("\nDownload and combination completed!")
        else: # stream is progressive
            youtube_video_stream.download(output_path=output_directory, filename=file_name_with_extension)
            print("\nDownload completed!")

    except Exception as e:
        print(f"An error occurred: {e}")


def combine_video(youtube_video, youtube_video_stream, output_path):

    audio_stream = youtube_video.streams.filter(only_audio=True).order_by('abr').desc().first()
    print(f"Selected audio stream: {audio_stream.abr}")

    if not audio_stream:
        raise Exception('No suitable audio stream found.')

    video_path = youtube_video_stream.download(filename="target/video.mp4")
    print(f"Video stream downloaded: {video_path}")
    audio_path = audio_stream.download(filename="target/audio.mp4")
    print(f"Audio stream downloaded: {audio_path}")

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

    os.remove(video_path)
    os.remove(audio_path)

if __name__ == "__main__":
    download_video()
