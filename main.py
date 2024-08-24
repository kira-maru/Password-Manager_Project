from tkinter import *
from password_dictionary import *
import random
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    password = []
    for x in range(10):
        random_symbols = [n for n in random.choice(symbols)]
        password += random_symbols
    password = ''.join(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_in_file():
    website_text = website_entry.get()
    email_text = email_entry.get()
    password_text = password_entry.get()
    new_websites_passwords = {
        website_text: {
            "email": email_text,
            "password": password_text,

        }
    }

    if (len(website_text) and len(email_text) and len(password_text)) > 1:
        messagebox.askokcancel("Data confirmation", f"Do you want to save data as below?\n"
                                                    f"Website: {website_text}\nEmail: {email_text}\n"
                                                    f"Password: {password_text}")
        try:
            with open("websites_passwords.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data.update(new_websites_passwords)

        with open("websites_passwords.json", mode="w") as new_file:
            json.dump(data, new_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
    else:
        messagebox.showwarning("Not enough data", "Make sure you haven't left any fields empty.")

# ---------------------------- SEARCH MECHANISM ------------------------------- #


def search_website():
    website_text = website_entry.get()

    try:
        with open("websites_passwords.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Data error", "No such data saved.")
    else:
        for (key) in data:
            if data[key] != website_text:
                messagebox.showerror("Data error", "No such data saved.")
                break
            else:
                messagebox.showinfo("Website information", f"Website name: {website_text}\n"
                                                           f"Website email: {data[key]["email"]}\n"
                                                           f"Website password: {data[key]["password"]}")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "emailname@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

# Buttons
generate_button = Button(text="Generate Password", command=password_generator)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save_in_file)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(row=1, column=2)

window.mainloop()
