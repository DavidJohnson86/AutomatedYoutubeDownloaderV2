import tkinter as tk
from PIL import Image, ImageTk
import sys
import threading
import YotubeDownloader_Mock
from easygui import fileopenbox, diropenbox
from tkinter import messagebox
class MainApplication(tk.Frame):


    def __init__(self, parent, *args, **kwargs):
        '''INIT Objects'''
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = tk.Frame(parent)
        self.parent.pack()
        root.title('Yotube Downloader')
        self.resetInputs()
        self.initUI()

    def resetInputs(self):
        self.file_one = u''
        self.save_list = u''

    def initUI(self):
        #=======================================================================
        # Create Container For MainFrame
        #=======================================================================
        self.hintone = tk.LabelFrame(self.parent, text=" 1. Enter File Details: ")
        self.hintone.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        #=======================================================================
        # Create Container for Picture
        #=======================================================================
        self.hintpic = tk.LabelFrame(self.hintone)
        self.hintpic.grid(row=5, columnspan=14, sticky='N', padx=10, pady=10, ipadx=5, ipady=5)
        #=======================================================================
        # Create Buttons
        #=======================================================================
        self.ok_button = tk.Button(self.parent, text="OK", command=self.OKButton)
        self.ok_button.grid(row=4, column=0, sticky='W' + 'E', padx=5, pady=5, ipadx=1, ipady=1)
        self.exit_button = tk.Button(self.parent, text="Exit", command=self.cancelbutton)
        self.exit_button.grid(row=4, column=1, sticky='W', padx=5, pady=5, ipadx=30, ipady=1)
        browseBtnone = tk.Button(self.hintone, text="Browse ...", command=self.browseFirst)
        browseBtnone.grid(row=0, column=8, sticky='W', padx=5, pady=2)
        browseBtntwo = tk.Button(self.hintone, text="Browse ...", command=self.browseSecond)
        browseBtntwo.grid(row=1, column=8, sticky='W', padx=5, pady=2)
        #=======================================================================
        # Draw the Labels
        #=======================================================================
        labelone = tk.Label(self.hintone, text="Select Music File: ")
        labelone.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        labeltwo = tk.Label(self.hintone, text="Select the Output Directory: ")
        labeltwo.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        labelthree = tk.Label(self.hintone, text="Select output format: ")
        labelthree.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        #=======================================================================
        # Draw Check Buttons
        #=======================================================================
        self.cb_audio_var = tk.IntVar()
        self.cb_video_var = tk.IntVar()
        cb_audio = tk.Checkbutton(self.hintone, text="Audio", variable=self.cb_audio_var,
                                  command=self.cb_audio)
        cb_audio.grid(row=2, column=1, sticky='E', padx=5, pady=2)
        cb_video = tk.Checkbutton( self.hintone, text="Video",  variable=self.cb_video_var,
                                   command=self.cb_video)
        cb_video.grid(row=2, column=2, sticky='E', padx=5, pady=2)
        
        #=======================================================================
        # File Selection Entry
        #=======================================================================
        self.labelent_one = tk.Entry(self.hintone)
        self.labelent_one.grid(row=0, column=1, columnspan=7, sticky="W", pady=3)
        self.labelent_two = tk.Entry(self.hintone)
        self.labelent_two.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)
        self.image('yt.jpeg')
        self.get_centercoordinate(root)
        root.attributes('-alpha', 1.0)
        
    def cb_audio(self):
        self.cb_audio_var.get()
        
    def cb_video(self):
        self.cb_video_var.get()

    def browseFirst(self):
        '''Select the files to Edit'''
        current_entry = self.labelent_one
        self.file_one = fileopenbox()
        if self.file_one.encode('utf-8') == '.':
            pass
        elif self.file_one:
            current_entry.insert(0, str(self.file_one))

    def browseSecond(self):
        '''Select the files to Edit'''
        current_entry = self.labelent_two
        self.file_two = diropenbox()
        if self.file_two.encode('utf-8') == '.':
            pass
        elif self.file_two:
            current_entry.insert(0, str(self.file_two))

    def savebutton(self):
        '''Select the files save path'''
        current_entry = self.labelent_three
        self.save_list = diropenbox(default=r'd:\\')
        if self.save_list:
            current_entry.insert(0, self.save_list.encode('utf-8'))

    def OKButton(self):
        '''Input Verification and start the process'''
        self.get_inputs()
        if self.file_one and self.file_two :
            self.t1 = threading.Thread(target=self.parse, name='controller')
            self.t1.start()
            self.disablebuttons()
        elif not (self.file_one and self.file_two):
            self.errormessage()
        elif not self.t1.is_alive():
            self.enablebuttons()

    def queue_event(self, message):
        '''This is a thread handler what checks that worker thread is alive'''
        if self.t1.is_alive():
            self.master.after(100, self.queue_event, message)
        elif message=='Success':
            self.enablebuttons()
            tk.messagebox.showinfo( 'Finished','Process has been finished.')
        elif message=='Error':
            self.enablebuttons()
            #===================================================================
            # sp.Popen(["notepad.exe", openlog])
            #===================================================================
            
    def cancelbutton(self):
        sys.exit()

    def errormessage(self):
        '''Show an Error window'''
        tk.messagebox.showinfo("Error", "Missing Data")


    def parse(self):
        if self.cb_audio_var.get():
            self.param = 'Audio'
            self.call_downloader()
        elif self.cb_video_var.get():
            self.param = 'Video'
            self.call_downloader()
        else:
            messagebox.showinfo('Error','Please choose Audio/Video' )
            self.queue_event('Error')
   
    def call_downloader(self):
        YotubeDownloader_Mock.Application(self.file_one,self.file_two,self.param)
        self.queue_event('Success')
        
    

    def disablebuttons(self):
        self.ok_button.config(state='disabled')

    def enablebuttons(self):
        self.ok_button.config(state='normal')

    def image(self, nameofpic):
        image = Image.open(nameofpic)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.hintpic, image=photo)
        label.image = photo
        label.grid()

    def get_inputs(self):
        self.file_one = self.labelent_one.get()
        self.file_two = self.labelent_two.get()

    def get_centercoordinate(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        '''win.deiconify()'''


if __name__ == "__main__":

    root = tk.Tk()
    root.attributes('-alpha', 0.0)  # Transparent GUI until Initialization
    run = MainApplication(root)
    root.mainloop()
