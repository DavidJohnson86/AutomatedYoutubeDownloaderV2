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
from queue import Queue, Empty

class Application():
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
        playlist = open(playlist_file, 'r')
        self.songs = playlist.readlines()
        playlist.close()
        self.song_num = 1
        self.downloadbylink = True
        self.searching()
    
    def searching(self):
        """Search on google if needed else not searchind just downloads"""
        for song in self.songs:
            if self.downloadbylink is False:
                resObj = Search.Search(song)
                results = resObj.getlinks
                for result in results:
                    title = result['title']
                    url = result['link']
                    # regular expression looking for youtube url
                    if re.search(r'www.youtube.com', url):
                        Application.CONSOLE_MESSAGE.put("Downloading", title.encode("utf-8"))
                        decoded_url = urllib.parse.unquote(url)
                        Application.CONSOLE_MESSAGE.put("Link: %s" % decoded_url)
            else:
                title = song
                Application.CONSOLE_MESSAGE.put("Downloading %s" % title)
                decoded_url = song
                Application.CONSOLE_MESSAGE.put("Link: %s" % decoded_url)
                
            try:
                os.chdir(Application.youtubedl_path)
            except FileNotFoundError:
                import sys
                os.chdir(os.path.dirname(os.path.realpath((sys.argv[0])))+ '\Data')
            if self.reply == 'Audio':
                self.run_win_cmd(
                    [ 'youtube-dl', '-o', self.output_path+'/%(title)s.(ext)s',
                    "--extract-audio", "--audio-format", "mp3",
                    decoded_url])
                
            elif self.reply == 'Video':
                self.run_win_cmd(
                    ['youtube-dl', '-o', self.output_path+'/%(title)s',
                    decoded_url])
            song_flag = 1
            
            if song_flag == 1:
                Application.CONSOLE_MESSAGE.put("Media %s %s %s " % (self.song_num, song, "DOWNLOADED"))
            else:
                Application.CONSOLE_MESSAGE.put("Media %s %s %s " % (self.song_num, song, "NOT DOWNLOADED"))
                #todo create a log if download not succesfull
            time.sleep(randint(10, 15))
            self.song_num += 1

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