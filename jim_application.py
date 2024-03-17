import tkinter as tk
import sqlite3

# sorry for globals...
first_name: tk.StringVar
last_name: tk.StringVar
phone_number: tk.StringVar
output_label: tk.StringVar 
  
# defining a function that will
# get the name and password and 
# print them on the screen
def insert() -> None:
    output_label.set("")

    fname=first_name.get()
    lname=last_name.get()
    pnumber=phone_number.get()

    phone_number.set("") 
    first_name.set("")
    last_name.set("")
    output_label.set(f"{fname}, {lname}: {pnumber}")

def search():
    pass

def only_int(char: str) -> bool:
    return char.isdigit()

def create_widgets(root: tk.Tk, validated_int_func: str) -> None: 
    # creating a label for 
    fname_label = tk.Label(root, text = 'First Name', font=('calibre',10, 'bold'))
    fname_entry = tk.Entry(root,textvariable = first_name, font=('calibre',10,'normal'))
  
    lname_label = tk.Label(root, text = 'Last Name', font = ('calibre',10,'bold'))
    lname_entry=tk.Entry(root, textvariable = last_name, font = ('calibre',10,'normal'))
  
    phone_label = tk.Label(root, text = 'Phone Number', font = ('calibre',10,'bold'))
    phone_entry=tk.Entry(root, textvariable = phone_number, validate="key", validatecommand=(validated_int_func, "%S"), font = ('calibre',10,'normal'))


    search_btn=tk.Button(root,text = 'Search', command = search)
    insert_btn=tk.Button(root,text = 'Insert', command = insert)

    output_lbl = tk.Label(root, textvariable = output_label, font = ('calibre',10,'bold'))
    output_lbl.grid(row=4,column=0)
  
    fname_label.grid(row=0,column=0)
    fname_entry.grid(row=0,column=1)
    lname_label.grid(row=1,column=0)
    lname_entry.grid(row=1,column=1)
    phone_label.grid(row=2,column=0)
    phone_entry.grid(row=2,column=1)
    search_btn.grid(row=3,column=0)
    insert_btn.grid(row=3,column=1)
  

def main():
    root=tk.Tk() 
    # create variables
    global first_name, last_name, phone_number, output_label
    first_name=tk.StringVar()
    last_name=tk.StringVar()
    phone_number=tk.StringVar()
    output_label=tk.StringVar()
    # set the title of the window
    root.geometry("400x400")
    root.title("Jim's Phonebook")

    validated_int_func = root.register(only_int)

    # create the widgets
    create_widgets(root, validated_int_func)
    # run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()