import os
from openpyxl import load_workbook
IN_FILE = os.getcwd() + '\Playlist.xlsx'
wb = load_workbook(filename = IN_FILE)
current_sheet = wb['YouTube-Playlist']
max_row = (len(current_sheet['A']))
title_name = 'D'
for i in range (3,max_row+1):
    with open('input.txt','a') as files:
        files.write(current_sheet[title_name + str(i)].value + '\n')
