"""
Copyright © 2021  Bartłomiej Duda
License: GPL-3.0 License
"""
import math
import os
import sys
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from reversebox.common.logger import get_logger

# default app settings
WINDOW_HEIGHT = 490
WINDOW_WIDTH = 690

logger = get_logger(__name__)

# fmt: off


class ImageFinderGUI:
    def __init__(self, master: tk.Tk, in_version_num: str, in_main_directory: str):
        logger.info("GUI init...")
        self.master = master
        self.VERSION_NUM = in_version_num
        self.MAIN_DIRECTORY = in_main_directory
        master.title(f"ReverseBox - image finder {in_version_num}")
        master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_dir = self.MAIN_DIRECTORY + "\\data\\icon.ico"
        self.gui_font = ('Arial', 8)

        try:
            self.master.iconbitmap(self.icon_dir)
        except tk.TclError:
            logger.info("Can't load the icon file from %s", self.icon_dir)


        # main frame
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)


        ########################
        # PARAMETERS BOX #     #
        ########################
        self.parameters_labelframe = tk.LabelFrame(self.main_frame, text="Parameters", font=self.gui_font)
        self.parameters_labelframe.place(x=5, y=5, width=160, relheight=1, height=-20)


        #############################
        # PARAMETERS - IMAGE WIDTH  #
        ############################
        self.width_label = tk.Label(self.parameters_labelframe, text="Img Width", anchor="w", font=self.gui_font)
        self.width_label.place(x=5, y=5, width=60, height=20)

        self.width_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.width_spinbox.place(x=5, y=25, width=60, height=20)


        ################################
        # PARAMETERS - IMAGE HEIGHT    #
        ################################
        self.height_label = tk.Label(self.parameters_labelframe, text="Img Height", anchor="w", font=self.gui_font)
        self.height_label.place(x=80, y=5, width=60, height=20)

        self.height_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.height_spinbox.place(x=80, y=25, width=60, height=20)


        #####################################
        # PARAMETERS - IMAGE START OFFSET   #
        #####################################
        self.img_start_offset_label = tk.Label(self.parameters_labelframe, text="Start Offset", anchor="w", font=self.gui_font)
        self.img_start_offset_label.place(x=5, y=50, width=60, height=20)

        self.img_start_offset_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.img_start_offset_spinbox.place(x=5, y=70, width=60, height=20)

        ####################################
        # PARAMETERS - IMAGE END OFFSET    #
        ####################################
        self.img_end_offset_label = tk.Label(self.parameters_labelframe, text="End Offset", anchor="w", font=self.gui_font)
        self.img_end_offset_label.place(x=80, y=50, width=60, height=20)

        self.img_end_offset_spinbox = tk.Spinbox(self.parameters_labelframe, from_=0, to=sys.maxsize)
        self.img_end_offset_spinbox.place(x=80, y=70, width=60, height=20)

        ########################
        # IMAGE BOX            #
        ########################
        self.image_labelframe = tk.LabelFrame(self.main_frame, text="Image preview", font=self.gui_font)
        self.image_labelframe.place(x=170, y=5, relwidth=1, relheight=1, height=-20, width=-175)

        ##############################
        # IMAGE BOX - IMAGE CANVAS   #
        ##############################

        self.PREVIEW_HEIGHT = 200
        self.PREVIEW_WIDTH = 300

        im = Image.new('RGB', (self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT))
        # draw = ImageDraw.Draw(im)
        # for x in range(100):
        #     draw.point((x, 15), fill="red")
        # draw.ellipse((25, 25, 75, 75), fill=(255, 6, 6))
        for x in range(self.PREVIEW_WIDTH):
            for y in range(math.floor(self.PREVIEW_HEIGHT / 2)):
                im.putpixel((x, y), (44, 44, 44))

        self.canvas = tk.Canvas(self.image_labelframe)
        self.image = ImageTk.PhotoImage(im)
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        self.canvas.place(x=5, y=5, height=self.PREVIEW_HEIGHT, width=self.PREVIEW_WIDTH)






        ###############################################################################################################
        ############ menu
        ###############################################################################################################
        self.menubar = tk.Menu(master)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(
            label="Open File",
            command=lambda: self.open_file(),
            accelerator="Ctrl+O",
        )
        master.bind_all("<Control-o>", lambda x: self.open_file())
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label="Quit", command=lambda: self.quit_program(), accelerator="Ctrl+Q"
        )
        master.bind_all("<Control-q>", lambda x: self.quit_program())
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="Options", command=lambda: None)
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(
            label="About...", command=lambda: self.show_about_window()
        )
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        master.config(menu=self.menubar)

    ######################################################################################################
    #                                             methods                                                #
    ######################################################################################################

    def quit_program(self):
        logger.info("Quit GUI...")
        self.master.destroy()

    def open_file(self):
        try:
            in_file = filedialog.askopenfile(
                mode="rb"
            )
            if not in_file:
                return
            in_file_path = in_file.name
            in_file_name = in_file_path.split("/")[-1]
        except Exception as error:
            logger.error("Failed to open file! Error: %s", error)
            messagebox.showwarning("Warning", "Failed to open file!")
            return

        logger.info("Loading file %s...", in_file_name)

    def show_about_window(self):
        pass

    @staticmethod
    def set_text_in_box(in_box, in_text):
        in_box.config(state="normal")
        in_box.delete("1.0", tk.END)
        in_box.insert(tk.END, in_text)
        in_box.config(state="disabled")

    @staticmethod
    def close_toplevel_window(wind):
        wind.destroy()

    @staticmethod
    def web_callback(url):
        webbrowser.open_new(url)

# fmt: on
