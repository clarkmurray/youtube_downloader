from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import subprocess

# TODO: Make downloads compatible with Quicktime Player
# TODO: Look into changing fps (currently set at 60)

def download_video():
    try:
        output_directory = "/Users/clarkmurray/Movies/YouTube Downloads"

        video_url = input("Input YouTube video URL: ")
        custom_file_name = get_custom_file_name_input()

        youtube_video = YouTube(video_url, on_progress_callback=on_progress)
        youtube_video_stream = youtube_video.streams.get_highest_resolution(False)
        
        file_name_with_extension = get_file_name_with_extension(custom_file_name, youtube_video.title)

        print("Downloading \"" + youtube_video.title + "\" from YouTube in " + youtube_video_stream.resolution + " resolution")

        if youtube_video_stream.is_adaptive:
            audio_stream = get_adaptive_audio_stream(youtube_video)
            video_path = download_adaptive_video(youtube_video_stream)
            audio_path = download_adaptive_audio(audio_stream)
            output_path = output_directory + "/" + file_name_with_extension
            combine_video_and_audio(video_path, audio_path, output_path)
            cleanup(video_path, audio_path)
        else:
            youtube_video_stream.download(output_path=output_directory, filename=file_name_with_extension)
        print("\nDownload completed!")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_custom_file_name_input():
    custom_file_name = ""
    use_custom_file_name = input("Would you like to give the file a custom name? (Y/N): ").lower().strip() == 'y'
    if (use_custom_file_name):
        custom_file_name = input("Enter a custom file name: ")
    return custom_file_name

def get_file_name_with_extension(custom_file_name, youtube_video_title):
    file_name = custom_file_name if len(custom_file_name) > 0 else youtube_video_title
    extension = ".mp4"
    file_name_with_extension = file_name + extension
    return file_name_with_extension

def get_adaptive_audio_stream(youtube_video):
    audio_stream = youtube_video.streams.filter(only_audio=True).order_by('abr').desc().first()
    print(f"Selected audio stream: {audio_stream.abr}")
    if not audio_stream:
        raise Exception('No suitable audio stream found.')
    return audio_stream

def download_adaptive_video(youtube_video_stream):
    video_path = youtube_video_stream.download(output_path="./target", filename="target/video.mp4")
    print(f"Video stream downloaded: {video_path}")
    return video_path

def download_adaptive_audio(audio_stream):
    audio_path = audio_stream.download(output_path="./target",filename="target/audio.mp4")
    print(f"Audio stream downloaded: {audio_path}")
    return audio_path

def combine_video_and_audio(video_path, audio_path, output_path):
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

def cleanup(video_path, audio_path):
    os.remove(video_path)
    os.remove(audio_path)



if __name__ == "__main__":
    download_video()
