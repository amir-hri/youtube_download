"""
This program helps you download videos from youtube
If you have only one video to download, you can specity the resolution;
However if you have multiple videos, the program will download the highest resolution for each.

Tip: If YouTube is banned in your country, you'll have to use a VPN or a proxy in order to bypass this restriction!
"""
# Main module for downloading videos from youtube
from pytube import YouTube
# We use tkinter to provide dialog box
import tkinter as tk 
from tkinter import filedialog
# This is used simply to sort the resolutions in ascending order
from natsort import natsorted

# The following function handles downloading only a single video
def download_single(vid_link):

    try:
        vid = YouTube(vid_link)
    except:
        return ("Network error!")
    print(vid.title)

    # We only want the video formats
    streams = vid.streams.filter(file_extension='mp4')
    resolutions = set()
    for stream in streams:
        resolutions.add(stream.resolution)
    if None in resolutions:
        resolutions.remove(None)
    resolutions = natsorted(resolutions)
    res = ''
    while res not in resolutions:
        res = input(f'Please choose a valid resolution from the list below:\n{resolutions}\n')

    # The following prompts a dialog box for the user to choose a directory
    root = tk.Tk()
    root.withdraw()
    print("Where do you want to save the video?")
    folder_path = filedialog.askdirectory()

    dl_vid = vid.streams.get_by_resolution(res)
    try:
        dl_vid.download(folder_path)
    except:
        return ("Download error!")
    print(f'{vid.title} has been successfully downloaded.')

def download_multiple(links_list, vids_number, quality):
    
    root = tk.Tk()
    root.withdraw()
    print("Where do you want to save the videos?")
    folder_path = filedialog.askdirectory()

    for i in range(vids_number):
        current = links_list[i]
        try:
            vid = YouTube(current)
        except:
            return ("Network error!")
        print(vid.title)

        if quality == 'highest':
            dl_vid = vid.streams.get_highest_resolution()
        elif quality == 'lowest':
            dl_vid = vid.streams.get_lowest_resolution()

        try:
            dl_vid.download(folder_path)
        except:
            return ("Download error!")
        print(f'{vid.title} has been successfully downloaded.')


if __name__ == '__main__':
    
    vids_number = int(input("How many videos would you like to download? "))

    # If the number of videos is one, we call the first function
    if vids_number == 1:
        vid_link = input("Enter the video link: ")
        download_single(vid_link)
    
    # If the number of videos is more than one, we call the second function
    elif vids_number > 1:
        quality = ''
        while quality not in ['highest', 'lowest']:
            quality = input("Enter highest or lowest for the resolution of your videos: ")
        links_list = []
        for i in range(vids_number):
            current = input(f"Enter the link for video number {i+1}: ")
            links_list.append(current)
        download_multiple(links_list, vids_number, quality)

    else:
        print("Please enter a number greater than zero")
