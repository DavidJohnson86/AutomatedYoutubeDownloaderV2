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

class Application():
    
    youtubedl_path = os.path.dirname(__file__) + '\Data'
    cmd_output_container = []
    
       
    
    
    def __init__(self,playlist_file,output_path,param):
        
        self.output_path = output_path
        self.reply = param
        playlist = open(playlist_file, 'r')
        self.songs = playlist.readlines()
        playlist.close()
        self.song_num = 1
        self.searching()
    
    def searching(self):
        for song in self.songs:
            command = ['ls', '-l']
            resObj = Search.Search(song)
            results = resObj.getlinks
            song_flag = 0
            for result in results:
                title = result['title']
                url = result['link']
                # regular expression looking for youtube url
                if re.search(r'www.youtube.com', url):
                    print ("DOWNLOADING", title.encode("utf-8"))
                    decoded_url = urllib.parse.unquote(url)
                    print (decoded_url)
                    try:
                        os.chdir(Application.youtubedl_path)
                    except FileNotFoundError:
                        import sys
                        os.chdir(os.path.dirname(os.path.realpath((sys.argv[0])))+ '\Data')
                    if self.reply == 'Audio':
                        print (os.getcwd())
                        subprocess.call(
                            [ 'youtube-dl', '-o', self.output_path+'/%(title)s.(ext)s',
                            "--extract-audio", "--audio-format", "mp3",
                            decoded_url])
                        song_flag = 1
                    elif self.reply == 'Video':
                        subprocess.call(
                            ['youtube-dl', '-o', self.output_path+'/%(title)s',
                            decoded_url])
                        song_flag = 1
                    break
            if song_flag == 1:
                print ("Line Number"+str(self.song_num), song, "DOWNLOADED")
                print (100 * '-')
                song_flag = 0
            else:
                print ("Line Number"+str(self.song_num), song, "NOT DOWNLOADED")
                print (100 * '-')
                self.output_temp.write(song)
            time.sleep(randint(10, 15))
            self.song_num += 1
    
           
    @staticmethod
    def run_win_cmd(cmd):
        try:
            Application.cmd_output_container.append(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
        except subprocess.CalledProcessError:
            raise Exception
        
    
                 
if __name__ == '__main__':
  a = Application()
  