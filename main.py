from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import requests
from tkinter import messagebox

API_KEY = os.environ['api_key']

window = Tk()
window.title("Remove background")

window_width = 350
window_height = 280
window.geometry(f"{window_width}x{window_height}")


def remove_background():
    try:
        value = file_path_entry.get()
        split_value = value.split("/")
        split_value.pop()
        new_value = ""
        for n in range(len(split_value)):
            new_value += split_value[n] + "/"

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(value, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )
        if response.status_code == requests.codes.ok:
            with open(f'{new_value}/no-bg.png', 'wb') as out:
                out.write(response.content)
                messagebox.showinfo(title="Success", message="The file is in the same location as the selected file")
        else:
            print("Error:", response.status_code, response.text)
    except FileNotFoundError:
        messagebox.showerror(title="File does not exist", message="File does not exist, choose another file")


def browse(entry):
    filename = askopenfilename(title='Select a file')
    entry.delete(0, END)
    entry.insert(0, filename)


label = Label()
label.config(text="Type or browse a file path", font=("Arial", 20, "normal"))
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

file_path_entry = Entry(width=40)
file_path_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

browse_button = Button(text="Browse", command=lambda: browse(file_path_entry), font=("Arial", 20, "normal"))
browse_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

confirm_button = Button(text="Confirm", font=("Arial", 20, "normal"), command=remove_background)
confirm_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


window.mainloop()
