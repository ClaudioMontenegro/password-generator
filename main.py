from tkinter import *
from tkinter import messagebox
import pandas as pd
from pass_generator import letters, numbers, symbols
import random
from datetime import datetime
import pyperclip

LIGHT_RED = "#E4BE9E"
DARK_PURPLE = "#27213C"
LIGHT = "#dedaed"
ENT_BG = "#dedaed"
FONT_TEXT = "Open Sans"
FONT_SIZE = 10
my_passwords = pd.read_csv("my-passwords/my_passwords.csv", sep=',')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pass_gen():
    pass_ent.delete(0, 'end')
    password = []
    range_pass = random.randint(12, 16)
    let = random.choices(letters, k=int(range_pass / 2))
    password += let
    numb = random.choices(numbers, k=int(range_pass / 3))
    password += numb
    sym = random.choices(symbols, k=int(range_pass / 3))
    password += sym
    random.shuffle(password)
    password = "".join(str(element) for element in password)
    pyperclip.copy(password)
    pass_ent.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    # Information required
    global my_passwords
    website = web_ent.get()
    email = email_ent.get()
    passw = pass_ent.get()
    date = datetime.now()
    date_now = date.strftime("%d/%m/%Y %H:%M:%S")

    # Validation
    if len(website) == 0 or len(email) == 0 or len(passw) == 0:
        messagebox.showinfo(title='Warning!', message="Please fill out all the fields")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details provided: \nEmail: {email}"
                                                              f"\nPassword: {passw}. \nWant to save it?")
        if is_ok:
            # Concat the information into a base dataframe
            new_record = pd.DataFrame([{'sites': website,
                                        'emails': email,
                                       'passwords': passw,
                                        'date': date_now}])
            my_passwords = pd.concat([my_passwords, new_record], ignore_index=True)

            # Save as .csv file
            my_passwords.to_csv("my-passwords/my_passwords.csv", sep=',', index=False)

    # Delete the information on the entries
    web_ent.delete(0, 'end')
    pass_ent.delete(0, 'end')

# ---------------------------- UI SETUP ------------------------------- #


# Window
window = Tk()
window.config(padx=50, pady=50, bg=DARK_PURPLE)
window.title("My Password Manager")

# Canvas
logo = PhotoImage(file="logo/logo.png")
canvas = Canvas(width=200, height=200, bg=DARK_PURPLE, highlightthickness=0)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
web_lb = Label(text="Website:", font=(FONT_TEXT, FONT_SIZE, "bold"), bg=DARK_PURPLE, fg=LIGHT,)
web_lb.grid(column=0, row=1)
email_lb = Label(text="Email/Username:", font=(FONT_TEXT, FONT_SIZE, "bold"), bg=DARK_PURPLE, fg=LIGHT,)
email_lb.grid(column=0, row=2)
pass_lb = Label(text="Password:", font=(FONT_TEXT, FONT_SIZE, "bold"), bg=DARK_PURPLE, fg=LIGHT,)
pass_lb.grid(column=0, row=3)

# Buttons
gen = PhotoImage(file="buttos/gen_bt3.png")
add = PhotoImage(file="buttos/add2.png")
gen_pass_lb = Button(image=gen,
                     font=(FONT_TEXT, FONT_SIZE),
                     bg=DARK_PURPLE,
                     command=pass_gen,
                     border=0,
                     borderwidth=0)
gen_pass_lb.config(activebackground=DARK_PURPLE)
gen_pass_lb.grid(column=2, row=3, sticky='w')
add_lb = Button(image=add, font=(FONT_TEXT, FONT_SIZE),
                width=36,
                bg=DARK_PURPLE,
                command=save_pass,
                borderwidth=0,
                border=0)
add_lb.config(activebackground=DARK_PURPLE)
add_lb.grid(column=1, row=4, columnspan=2, sticky='ew')

# Entries
web_ent = Entry(width=35, bg=ENT_BG)
web_ent.grid(column=1, row=1, columnspan=2, sticky='we')
web_ent.focus()
email_ent = Entry(width=35, bg=ENT_BG)
email_ent.grid(column=1, row=2, columnspan=2, sticky='we')
email_ent.insert(0, "youraddress@mail.com")
pass_ent = Entry(width=21, bg=ENT_BG)
pass_ent.grid(column=1, row=3, sticky='we')

window.mainloop()
