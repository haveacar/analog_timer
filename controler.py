import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import math

# Colors Constants and fonts
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# dir path
TIMER_PATH = os.path.join(os.path.dirname(__file__), 'images.png')

class Analog_timer(Tk):
    """ Class analog timer"""

    def __init__(self):
        super().__init__()

        self.title("Timer")
        self.geometry("500x600+10+100")
        self.config(padx=100, pady=50, bg=YELLOW)
        self.resizable(False, False)

        # Labels & Buttons
        Label(text="Timer", font=("Algerian", 50), fg=GREEN, bg=YELLOW).pack(side=TOP)

        self.canvas = Canvas(width=350, height=350, background=YELLOW, highlightthickness=0)
        self.canvas.pack()

        self.timer_text = self.canvas.create_text(140, 140, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))

        # Frame
        self.bottom_frame = Frame(background=YELLOW)
        self.bottom_frame.pack()

        self.oval_coords = (5, 5, 290, 290)

        # validation numer
        self.vcmd = (self.register(self.validate), '%P')

        # timer constants
        self.flag = False
        self.timer = None
        self.work_min = 1

        self.arc_object = self.canvas.create_arc(
            self.oval_coords,
            start=90,
            extent=359.9,
            outline='',
            fill="#ff0000",
        )

        # move canvas object behind
        self.canvas.tag_lower(self.arc_object)

        # load voice image
        with Image.open(TIMER_PATH) as img:
            bg_image = ImageTk.PhotoImage(img.resize(size=(262, 149)))
        obj_img=self.canvas.create_image(150, 150, image=bg_image)
        self.canvas.tag_lower(obj_img)


        self.start()

        self.mainloop()

    def validate(self, new_value) -> str | int:
        """
        validation function int
        :param new_value: string Entry()
        :return: "" or int
        """
        return new_value == "" or new_value.isnumeric()

    def start(self) -> None:
        """Func start widgets"""

        # Labels & Buttons
        self.my_label_checkmark = Label(master=self.bottom_frame, fg=GREEN, bg=YELLOW, font=("Arial", 20))
        self.my_label_checkmark.grid(column=1, row=3)

        self.button_start = Button(master=self.bottom_frame, text="Start", highlightthickness=0,
                                   highlightbackground=YELLOW, command=self.start_timer)
        self.button_start.grid(column=0, row=0)

        button_reset = Button(master=self.bottom_frame, text="Reset", highlightthickness=0,
                              highlightbackground=YELLOW, command=self.reset_timer)
        button_reset.grid(column=2, row=0)

        self.entry_setup = Entry(master=self.bottom_frame, highlightthickness=0, width=5, validate='key',
                                 validatecommand=self.vcmd)
        self.entry_setup.grid(column=1, row=0)

        button_setup = Button(master=self.bottom_frame, text="set up", highlightthickness=0,
                              highlightbackground=YELLOW, command=self.set_up)
        button_setup.grid(column=1, row=2)

        # create oval
        self.canvas.create_oval(self.oval_coords, outline='black', width=11)


    def arc_move(self, count: int) -> None:
        """
        func draw arc move
        :param count: int
        """
        self.canvas.itemconfig(self.arc_object, extent=count)
        # function once after given time
        if count > 0:
            self.timer = self.after(self.work_min * 164, self.arc_move, count - 1)

    def set_up(self) -> None:
        """
        Func set up timer
        """
        entry_get = self.entry_setup.get()
        if len(entry_get) != 0: self.work_min = int(entry_get)

    def reset_timer(self) -> None:
        """ Reset timer func"""
        if self.flag:
            self.button_start.config(state="normal")
            self.after_cancel(self.timer)
            self.canvas.itemconfig(self.timer_text, text="00:00")
            self.canvas.itemconfig(self.arc_object, extent=359.9)
            self.my_label_checkmark.config(text="")

    def start_timer(self) -> None:
        """Start timer func"""
        self.flag = True
        self.button_start.config(state="disabled")
        work_sec = self.work_min * 60
        self.count_down(work_sec)
        self.arc_move(360)

    def count_down(self, count: int) -> None:
        """
        Count func sec
        :param count: int sec
        """
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            self.timer = self.after(1000, self.count_down, count - 1)
        else:
             messagebox.showinfo("Time!")
