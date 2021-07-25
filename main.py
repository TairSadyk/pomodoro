from tkinter import *
from tkmacosx import Button
from math import floor
from tkinter import messagebox
from tkinter.simpledialog import Dialog

# Constants
PINK = "#e2979c"
ORANGE = "#E45826"
BLACK_CYAN = "#213741"
CYAN = "#A3D2CA"
FONT_NAME = "Courier"
# Initial values
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# Create Dialog Class for input window that changes constant WORK values
class MyDialog(Dialog):

    def body(self, master):
        Label(master, text="Work (min):").grid(row=0)
        Label(master, text="Short brake (min):").grid(row=1)
        Label(master, text="Long brake (min):").grid(row=2)
        try:
            self.e1 = Entry(master)
            self.e2 = Entry(master)
            self.e3 = Entry(master)
        except ValueError:
            pass
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        # return self.e1 # initial focus

    def apply(self):

        global WORK_MIN
        global SHORT_BREAK_MIN
        global LONG_BREAK_MIN
        try:
            WORK_MIN = int(self.e1.get())
            SHORT_BREAK_MIN = int(self.e2.get())
            LONG_BREAK_MIN = int(self.e3.get())
        except ValueError:
            pass
        canvas.itemconfig(timer_text, text=f"{WORK_MIN}:00")


# Create functions d
def focus_window(option):
    if option == "on":
        window.deiconify()
        window.focus_force()
        window.attributes('-topmost', 1)
    elif option == "off":
        window.attributes('-topmost', 0)


# Create reset timer function
def reset_timer():
    focus_window("off")
    global reps
    canvas.itemconfig(timer_text, text=f"{WORK_MIN}:00")
    checkmark.config(text="")
    title.config(text="Timer", fg=BLACK_CYAN)
    window.after_cancel(timer)

    reps = 0
    reset_btn.config(state="disabled", disabledbackground="#c3f7ef")
    start_btn.config(state="normal")


#
def start_timer():
    global reps
    reps += 1
    start_btn.config(state="disabled", disabledbackground="#c3f7ef")
    reset_btn.config(state="normal")
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    # if it's the 1st/3rd/5th/7th rep:
    if reps % 2 == 0:
        focus_window("on")
        messagebox.showinfo(title="Break", message="It's time for a short break!")
        countdown(short_break_sec)
        title.config(text="Break", fg=BLACK_CYAN)
    # if its 8th rep:
    elif reps % 8 == 0:
        focus_window("on")
        messagebox.showinfo(title="Break", message="It's time for a long break")
        countdown(long_break_sec)
        title.config(text="Break", fg=BLACK_CYAN)
    # if its 2nd/4th/6th
    else:
        focus_window("off")
        messagebox.showinfo(title="Work", message="Time to work!!!")
        countdown(work_sec)
        title.config(text="Work", fg=ORANGE)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(count):
    global reps
    global timer
    count_min = floor(count/60)
    count_sec = count % 60
    if count > 0:
        timer = window.after(1000, countdown, count-1)
    else:
        start_timer()
        mark = ""
        for _ in range(floor(reps/2)):
            mark += "✓️"
            checkmark.config(text=mark)
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
# # ---------------------------- UI SETUP ------------------------------- #


def modify_timer():
    try:
        reset_timer()
    except ValueError:
        pass

    MyDialog(window)

window = Tk()
window.title("Timer")

# create canvas
canvas = Canvas(width=300, height=300, highlightthickness=0, bg=CYAN)
# create Timer title
title = Label(text="Pomodoro", font=(FONT_NAME, 35, "bold"),
              fg=BLACK_CYAN, bg=CYAN, pady=20)
title.grid(column=1, row=0)
# create tomato image with countdown text
tomato_img = PhotoImage(file="sand_clock.png")
canvas.create_image(150, 150, image=tomato_img)
timer_text = canvas.create_text(150, 150, text=f"{WORK_MIN}:00", fill="#424642",
                                font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)
# create start and reset buttons
# start_img = PhotoImage(file="start.png")
start_btn = Button(text="►", bg=CYAN, highlightthickness=0,
                   borderless=1, width=50, height=50, font=(FONT_NAME, 30),
                   fg=BLACK_CYAN, command=start_timer)
start_btn.grid(column=2, row=2)
# reset_img = PhotoImage(file="reset.png")
reset_btn = Button(text="↩︎", highlightthickness=0, borderless=1,
                   width=50, height=50, fg=ORANGE, bg=CYAN,
                   font=(FONT_NAME, 30), command=reset_timer)
reset_btn.grid(column=0, row=2)
checkmark = Label(font=(FONT_NAME, 30), fg=BLACK_CYAN, bg=CYAN)
checkmark.grid(column=1, row=3)

# create question mark button with link to wikipedia page

question_mark_btn = Button(text="⚙️", highlightthickness=0,
                           borderless=1, command=modify_timer, width=50, height=50,
                           fg=PINK, bg=CYAN, font=(FONT_NAME, 20), anchor="center")
question_mark_btn.grid(column=2, row=0)
window.config(padx=20, pady=20, bg=CYAN)
window.mainloop()


