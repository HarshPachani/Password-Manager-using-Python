import random
from tkinter import *
from tkinter import messagebox
import pyperclip
import sqlite3

conn = sqlite3.connect('passwords.db')
myCursor = conn.cursor()
myCursor.execute("""CREATE TABLE IF NOT EXISTS pass(
                        website TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL 
                        );""")

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', "$", '%', '&', '(', ')', '*', '+']

def save_password():
    # getting user entry data
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    # Dialog to user to make sure password is correct
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you have not left any fields empty")
    else:
        is_ok = messagebox.askokcancel(title="Confirm entries", message=f"These are the details you entered\n"
                                                                        f"Email: {email}"
                                                                        f"\nPassword: {password}\nIs it okay to save ?")
        if is_ok:
            #Copying password to our clipboard
            pyperclip.copy(password)

            # new user data to be entered into current password into the sqlite database
            myCursor.execute("INSERT INTO pass(website, email, password) VALUES(?, ?, ?)", (website, email, password))
            conn.commit()

def search_password():
    # Getting user website entry
    website = website_entry.get()
    # Get password data
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a website to search")
    else:
        query = f"SELECT * FROM pass WHERE website = '{website}'"
        myCursor.execute(query)
        data = myCursor.fetchall()
        if not data:
            messagebox.showinfo("No passwords saved", f"There are no passwords save for the website '{website}'")
        else:
            # website = data[0][0]
            email = data[0][1]
            password = data[0][2]
            is_clipboard = messagebox.askokcancel(title=website, message=f"Email: {email}\nPassword: {password}"
                                                                             f"\n\nSave to clipboard ?")
            if is_clipboard:
                # saving password to clipboard
                pyperclip.copy(password)
                messagebox.showinfo(title="Saved to clipboard", message="Password has been saved to clipboard")

def get_password():
    # Generate new password from password generator
    password = pass_generator()
    # Copying password to our clipboard
    pyperclip.copy(password)
    # print(password)

    # clear password entry widget
    password_entry.delete(0, END)
    # entering new password to password entry widget
    password_entry.insert(END, password)


def pass_generator():
    # no of random latters, symbols and numbers
    nr_letters = random.randint(8, 10) #Returns a number between 8 and 10 both included.
    # print(nr_latters)
    nr_symbols = random.randint(2, 4)
    # print(nr_symbols)
    nr_numbers = random.randint(2, 4)
    # print(nr_numbers)

    # initialising password variable to populate with for loop
    password = [random.choice(letters) for i in range(nr_letters)]
    # print(password)
    password += [random.choice(symbols) for i in range(nr_symbols)]
    # print(password)
    password += [random.choice(numbers) for i in range(nr_numbers)]
    # print(password)

    #shuffling password characters
    random.shuffle(password)
    # print("Shuffled Pass: ", password)
    password = "".join(password) #For converting a list into the string.
    return password

# print(type([print(pass_generator()) for i in range(5)]))
# generated = pass_generator()
# print(generated)

# ---------------------------- UI COLORS AND FONT ------------------------------- #
WINDOW_BG = "#111d5e" #For background of the window.
FONT = ("Courier", 15, "normal")
LABEL_COLOR = "white"
FIELD_COLORS = "#dddddd"
FIELD_FONT_COLOR = "#c70039"

root = Tk()
root.title("Password Manager")
root.config(padx = 20, pady = 20, bg = WINDOW_BG)

PASS_IMG = PhotoImage(file = "logo.png")
canvas = Canvas(width = 200, height = 200, bg = WINDOW_BG, highlightthickness=0) #for removing the highlighted border.
canvas.config()
canvas.create_image(100, 100, image = PASS_IMG)
canvas.grid(row = 0, column = 1)

# Label
# Label for Website
website_label = Label(text="Website", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
website_label.grid(column=0, row=1, sticky=W)

# Label for Email/Username
email_label = Label(text="Email/Username", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
email_label.grid(column=0, row=2, sticky=W)

# Label for Password
password_label = Label(text="Password", bg=WINDOW_BG, padx=20, font=FONT, fg=LABEL_COLOR)
password_label.grid(column=0, row=3,sticky=W)
root.grid_columnconfigure(1, weight=1)

# Entry
website_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
website_entry.insert(END, string="")
website_entry.grid(column=1, row=1)

# starting cursor focus
website_entry.focus()

email_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
email_entry.insert(END, string="")
email_entry.grid(column=1, row=2)
# set default email
email_entry.insert(0, "example@email.com")

password_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
password_entry.insert(END, string="")
password_entry.grid(column=1, row=3)

# buttons
search_button = Button(text="Search", padx=95, font=FONT, command=search_password)
search_button.grid(column=3, row=1)

generate_button = Button(text="Generate Password", command=get_password, font=FONT)
generate_button.grid(column=3, row=3)

add_button = Button(text="Add", width=36, command=save_password, font=FONT)
add_button.grid(column=1, row=5, columnspan=2, sticky=W)


root.mainloop()
