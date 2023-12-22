import json
from tkinter import *
from tkinter import messagebox
import pandas as pd
from pass_generator import letters, numbers, symbols
import random
from datetime import datetime
import pyperclip

LIGHT_RED = "#E4BE9E"
DARK_PURPLE = "#27213C"
ENT_BG = "#dedaed"
FONT_TEXT = "Open Sans"
FONT_SIZE = 10
my_passwords = pd.read_csv("my-passwords/my_passwords.csv", sep=',')

# ---------------------------- SEARCHER PASSWORD -------------------------------- #


def search_pass():
    site = web_ent.get().title()
    try:
        with open("my-passwords/my_sites.json", "r") as datafile:
            # Reading the JSON file
            data = json.load(datafile)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message="There are no sites register yet!")
    else:
        if site in data:
            the_pass = data[site]["password"]
            the_email = data[site]["email"]
            messagebox.showinfo(title=f'{site}', message=f"Email: {the_email}\nPassword: {the_pass}")
            email_ent.delete(0, 'end')
            pass_ent.delete(0, 'end')
            email_ent.insert(0, the_email)
            pass_ent.insert(0, the_pass)
        else:
            messagebox.showinfo(title='Error', message="No details for this website exists.")

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
    website = web_ent.get().title()
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
            # Save as .json
            my_sites = {
                website:
                    {'email': email,
                     'password': passw,
                     'date': date_now}}
            try:
                with open("my-passwords/my_sites.json", "r") as datafile:
                    # Reading the JSON file
                    data = json.load(datafile)
            except FileNotFoundError:
                # Write a new JSON file
                with open("my-passwords/my_sites.json", "w") as datafile:
                    json.dump(my_sites, datafile, indent=4)
            else:
                # Save the alterations into the JSON file

                # Update the JSON file
                data.update(my_sites)

                with open("my-passwords/my_sites.json", "w") as datafile:
                    json.dump(data, datafile, indent=4)
            finally:
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
web_lb = Label(text="Website:", font=(FONT_TEXT, FONT_SIZE, "bold"), bg=DARK_PURPLE, fg=ENT_BG, )
web_lb.grid(column=0, row=1)
email_lb = Label(text="Email/Username:", font=(FONT_TEXT, FONT_SIZE, "bold"), bg=DARK_PURPLE, fg=ENT_BG, )
email_lb.grid(column=0, row=2)
pass_lb = Label(text="Password:", font=(FONT_TEXT, FONT_SIZE, "bold"), bg=DARK_PURPLE, fg=ENT_BG, )
pass_lb.grid(column=0, row=3)

# Buttons
gen = PhotoImage(file="buttons/gen_bt3.png")
add = PhotoImage(file="buttons/add.png")
sear = PhotoImage(file="buttons/search.png")
gen_pass_bt = Button(image=gen,
                     font=(FONT_TEXT, FONT_SIZE),
                     bg=DARK_PURPLE,
                     command=pass_gen,
                     border=0,
                     borderwidth=0)
gen_pass_bt.config(activebackground=DARK_PURPLE)
gen_pass_bt.grid(column=2, row=3, sticky='w')
add_bt = Button(image=add, font=(FONT_TEXT, FONT_SIZE),
                width=36,
                bg=DARK_PURPLE,
                command=save_pass,
                borderwidth=0,
                border=0)
add_bt.config(activebackground=DARK_PURPLE)
add_bt.grid(column=1, row=4, columnspan=2, sticky='we')
search_bt = Button(image=sear,
                   bg=DARK_PURPLE,
                   border=0,
                   borderwidth=0,
                   command=search_pass)
search_bt.config(activebackground=DARK_PURPLE)
search_bt.grid(column=2, row=1, sticky='we')

# Entries
web_ent = Entry(width=35, bg=ENT_BG)
web_ent.grid(column=1, row=1, columnspan=1, sticky='we')
web_ent.focus()
email_ent = Entry(width=54, bg=ENT_BG)
email_ent.grid(column=1, row=2, columnspan=2, sticky='w')
email_ent.insert(0, "youraddress@mail.com")
pass_ent = Entry(width=21, bg=ENT_BG)
pass_ent.grid(column=1, row=3, sticky='we')

window.mainloop()
