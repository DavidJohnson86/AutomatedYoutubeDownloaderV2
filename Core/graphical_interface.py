"""
Graphical user interface designed for downloading videos or audio from Youtube
"""

from tkinter import messagebox
from PIL import Image, ImageTk
from easygui import fileopenbox, diropenbox
from queue import Empty


import tkinter as tk
import sys
import threading
import YotubeDownloader


class StatusBar(tk.Frame):
    """This is an info text with detailed description about the process status during the background
    Reads a queue message from the background"""

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = tk.Frame(parent)
        self.hint = tk.LabelFrame(self.parent, text=" 2. Process Details: ")
        self.hint.grid(row=0)
        self.y_scrollbar = tk.Scrollbar(self.hint)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_scrollbar = tk.Scrollbar(self.hint, orient="horizontal")
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.display_text = tk.Text(self.hint, background='white', foreground='black', height=10, width=70,
                                    font=('Comic Sans MS', 9), yscrollcommand=self.y_scrollbar.set,
                                    xscrollcommand=self.x_scrollbar.set, wrap='none')
        self.display_text.configure(state="disabled")
        self.display_text.tag_config('finished', background="yellow", foreground="green")
        self.display_text.pack()
        self.parent.grid(row=5, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        self.write_status_bar()

    def write_status_bar(self):
        """This function is refreshing the Console every 1 sec if any new message available"""

        try:
            data = YotubeDownloader.Application.CONSOLE_MESSAGE.get(False)
            # -- If `False`, the program is not blocked. `Queue.Empty` is thrown if
            # -- the queue is empty
        except Empty:
            data = None
        if data:
            self.display_text.configure(state="normal")
            if  "Destination" in str(data):
                self.display_text.insert('end', data, 'finished')
            else:
                self.display_text.insert('end', data)
            self.display_text.configure(state="disabled")
            self.display_text.see(tk.END)
        self.parent.after(100, self.write_status_bar)


class MainApplication(tk.Frame):
    """
    User can select a txt input file then google search will find the most relevant hit
    and downloads it with youtube-dl.exe..."""

    TITLE = "Yotube Downloader"

    def __init__(self, parent, *args, **kwargs):
        """INIT Objects"""
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = tk.Frame(parent)
        self.parent.pack()
        ROOT.title(MainApplication.TITLE)
        self.cb_audio_var = None
        self.cb_video_var = None
        self.file_one = None
        self.save_list = None
        self.hint_one = None
        self.hintpic = None
        self.file_two = None
        self.thread1 = None
        self.param = None
        self.ok_button = None
        self.labelent_one = None
        self.labelent_two = None
        self.resetinputs()
        self.init_ui()

    def init_ui(self):
        """Init User interface"""
        self.create_container_mainframe()
        self.create_container_status_bar()
        self.create_buttons()
        self.create_labels()
        self.create_check_buttons()
        self.create_selection_entry()
        self.image('yt.jpeg')
        self.get_centercoordinate(ROOT)
        ROOT.attributes('-alpha', 1.0)

    def resetinputs(self):
        """Reset input entries"""
        self.file_one = u''
        self.save_list = u''

    def create_container_mainframe(self):
        """Create container for mainframe"""
        self.hint_one = tk.LabelFrame(self.parent, text=" 1. Enter File Details: ")
        self.hint_one.grid(row=0, columnspan=1, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)

    def create_container_status_bar(self):
        """Create Container for Picture"""
        self.hintpic = StatusBar(self.parent)


    def create_buttons(self):
        """Create Buttons"""

        self.buttons_frame = tk.LabelFrame(self.parent, relief='flat')
        self.buttons_frame.grid(row=6, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        self.ok_button = tk.Button(self.buttons_frame, text="OK", command=self.push_ok_button)
        self.ok_button.grid(row=6, column=0, sticky='W', padx=5, pady=5,ipadx=30, ipady=1)
        exit_button = tk.Button(self.buttons_frame, text="Exit", command=self.cancel_button)
        exit_button.grid(row=6, column=1, padx=5, pady=5, ipadx=30, ipady=1)

        browse_btn_one = tk.Button(self.hint_one, text="Browse ...", command=self.browse_first)
        browse_btn_one.grid(row=0, column=8, sticky='W', padx=5, pady=2)
        browse_btn_two = tk.Button(self.hint_one, text="Browse ...", command=self.browse_second)
        browse_btn_two.grid(row=1, column=8, sticky='W', padx=5, pady=2)

    def create_labels(self):
        """Create Labels"""
        label_one = tk.Label(self.hint_one, text="Youtube Link \Playlist: ")
        label_one.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        label_two = tk.Label(self.hint_one, text="Select the Output Directory: ")
        label_two.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        label_three = tk.Label(self.hint_one, text="Select output format: ")
        label_three.grid(row=2, column=0, sticky='E', padx=5, pady=2)

    def create_check_buttons(self):
        """Create Check Buttons"""
        self.cb_audio_var = tk.IntVar()
        self.cb_video_var = tk.IntVar()
        cb_audio = tk.Checkbutton(self.hint_one, text="Audio", variable=self.cb_audio_var,
                                  command=self.cb_audio)
        cb_audio.grid(row=2, column=1, sticky='E', padx=5, pady=2)
        cb_video = tk.Checkbutton(self.hint_one, text="Video", variable=self.cb_video_var,
                                  command=self.cb_video)
        cb_video.grid(row=2, column=2, sticky='E', padx=5, pady=2)

    def create_selection_entry(self):
        """File Selection Entry"""
        self.labelent_one = tk.Entry(self.hint_one)
        self.labelent_one.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3)
        self.labelent_two = tk.Entry(self.hint_one)
        self.labelent_two.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)

    def cb_audio(self):
        """Get checkbox variable"""
        self.cb_audio_var.get()

    def cb_video(self):
        """Get checkbox variable"""
        self.cb_video_var.get()

    def browse_first(self):
        """Select the files to Edit"""
        current_entry = self.labelent_one
        self.file_one = fileopenbox()
        if self.file_one is not None:
            if self.file_one.encode('utf-8') == '.':
                pass
            elif self.file_one:
                current_entry.insert(0, str(self.file_one))

    def browse_second(self):
        """Select the files to Edit"""
        current_entry = self.labelent_two
        self.file_two = diropenbox()
        if self.file_two is not None:
            if self.file_two.encode('utf-8') == '.':
                pass
            elif self.file_two:
                current_entry.insert(0, str(self.file_two))

    def save_button(self):
        """Select the files save path"""
        current_entry = None
        self.save_list = diropenbox(default=r'd:\\')
        if self.save_list:
            current_entry.insert(0, self.save_list.encode('utf-8'))

    def push_ok_button(self):
        """Input Verification and start the process"""
        self.get_inputs()
        if self.file_one and self.file_two:
            self.thread1 = threading.Thread(target=self.parse, name='controller', daemon=True)
            self.thread1.start()
            self.disable_buttons()
        elif not (self.file_one and self.file_two):
            self.error_message("Error", "Missing Data")
        elif not self.thread1.is_alive():
            self.enable_buttons()

    def queue_event(self, message):
        """This is a thread handler what checks that worker thread is alive"""
        if self.thread1.is_alive():
            self.master.after(100, self.queue_event, message)
        elif message == 'Success':
            self.enable_buttons()
            tk.messagebox.showinfo("Finished", "Process has been finished.")
        elif message == 'Error':
            self.enable_buttons()

    def parse(self):
        """Decide user selection"""
        if self.cb_audio_var.get():
            self.param = "Audio"
            self.call_downloader()
        elif self.cb_video_var.get():
            self.param = "Video"
            self.call_downloader()
        else:
            messagebox.showinfo("Error", "Please choose Audio/Video")
            self.queue_event('Error')

    def call_downloader(self):
        """Call the Application"""
        try:
            YotubeDownloader.Application(self.file_one, self.file_two, self.param)
        except FileNotFoundError as error:
            self.error_message("Error", error)
        self.queue_event("Success")

    def disable_buttons(self):
        """Disable buttons if process ongoin"""
        self.ok_button.config(state='disabled')

    def enable_buttons(self):
        """Enable button actions"""
        self.ok_button.config(state='normal')

    def image(self, nameofpic):
        """Show image on GUI"""
        image = Image.open(nameofpic)
        photo = ImageTk.PhotoImage(image)
        hintpic = tk.LabelFrame(self.parent, relief="flat")
        label = tk.Label(hintpic, image=photo)
        label.image = photo
        hintpic.grid(row=0, column=2, sticky='W', padx=5, pady=5, ipadx=1, ipady=1)
        label.grid()

    def get_inputs(self):
        """Get inputs"""
        self.file_one = self.labelent_one.get()
        self.file_two = self.labelent_two.get()

    @staticmethod
    def cancel_button():
        """Exit application"""
        sys.exit()

    @staticmethod
    def error_message(*args):
        """Show an Error window"""
        tk.messagebox.showinfo(args[0], args[1])

    @staticmethod
    def get_centercoordinate(win):
        """Get center coordinates of your monitor"""
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x_coords = win.winfo_screenwidth() // 2 - win_width // 2
        y_coords = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x_coords, y_coords))
        win.deiconify()


if __name__ == "__main__":
    ROOT = tk.Tk()
    ROOT.attributes('-alpha', 0.0)  # Transparent GUI until Initialization
    RUN = MainApplication(ROOT)
    ROOT.mainloop()
