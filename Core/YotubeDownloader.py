# -*- coding: utf-8 -*-
"""
==============================================================================
                          Youtube Downloader Manager
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: Youtube Downloader Support
$Source: Youtube_Downloader.py
$Dependencies : youtube-dl.exe
                ffmpeg.exe
                ffprobe.exe
$Revision: 1.0
$Author: David Szurovecz $
$Date: 2016/02/19 16:41:32CEST $
$Name:  $
$History : 2016/02/18 """

import urllib
import re
import time
from random import randint
from easygui import *
import Search
import os
import subprocess
from queue import Queue


class Application:
    """
    Implementation logic around youtube-dl
    Download all input arguments to a specific location
    """
    
    youtubedl_path = os.path.dirname(__file__) + '\Data'
    CONSOLE_MESSAGE = Queue()

    def __init__(self, playlist_file, output_path, param):
        """Init class variables"""
        self.output_path = output_path
        self.reply = param
        self.song_num = 1
        self.downloadbylink = True # Future feature will be implemented
        self.playlist_file = playlist_file
        self.searching()
    
    def searching(self):
        """Search on google if needed else not searchind just downloads"""

        self.songs = self.playlist_file
        title = self.songs
        Application.CONSOLE_MESSAGE.put("Downloading %s" % title)
        self.decoded_url = self.songs
        Application.CONSOLE_MESSAGE.put("Link: %s" % self.decoded_url)
                
        try:
            os.chdir(Application.youtubedl_path)
        except FileNotFoundError:
            import sys
            os.chdir(os.path.dirname(os.path.realpath((sys.argv[0])))+ '\Data')
        if self.reply == 'Audio':
            self.audio_song_command()

        elif self.reply == 'Video':
            self.video_song_command()
        song_flag = 1
            
        if song_flag == 1:
            Application.CONSOLE_MESSAGE.put("%s. %s %s" % (self.song_num, self.songs.strip(), "Downloaded\n"))
        else:
            Application.CONSOLE_MESSAGE.put("%s. %s %s" % (self.song_num, self.songs.strip(), "Downloaded\n"))
            #todo create a log if download not succesfull
            time.sleep(randint(10, 15))
            self.song_num += 1
        Application.CONSOLE_MESSAGE.put("Downloaded files: %s" % self.song_num)

    def audio_song_command(self):
       self.run_win_cmd(
            f"youtube-dl --extract-audio --audio-format mp3 --output {self.output_path}/%(title)s.%(ext)s"
            f" {self.decoded_url}")

    def video_song_command(self):
        self.run_win_cmd(
           f"youtube-dl -o  {self.output_path}/%(title)s, {self.decoded_url}")

    @staticmethod
    def run_win_cmd(cmd):
        process = subprocess.Popen(cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            Application.CONSOLE_MESSAGE.put(line)
        errcode = process.returncode
        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', cmd)


if __name__ == '__main__':
    a = Application()