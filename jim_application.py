import tkinter as tk
try: 
    import sqlite3
except ImportError:
    import pysqlite3 as sqlite3


# sorry for globals...
first_name: tk.StringVar
last_name: tk.StringVar
phone_number: tk.StringVar
output_label: tk.StringVar 

DB_NAME="phone_numbers.db"

def search_db(fname: str, lname: str, pnum: str) -> str:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    first = f"%{fname}%" if fname else ""
    last = f"%{lname}%" if lname else ""
    num = f"%{pnum}%" if pnum else ""

    c.execute(f"SELECT * FROM contacts WHERE first_name like '{first}' OR last_name like '{last}' OR phone like '{num}';")
    result = ""
    for fname, lname, pnum in c.fetchall():
        result += f"{fname}, {lname}: {pnum}\n"
    conn.close()
    return result

def insert_db(fname: str, lname: str, pnumber: str) -> None:
    assert len(pnumber) == 10, "Phone Number Incorrect"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"INSERT INTO contacts VALUES ('{fname}', '{lname}', '{pnumber}');")
    conn.commit()
    conn.close()

def edit_db(fname: str, lname: str, pnumber: str) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"UPDATE contacts SET phone = '{pnumber}', first_name = '{fname}', last_name = '{lname}' where first_name = '{fname}' OR last_name = '{last_name}' OR phone = '{pnumber}' ;")
    conn.commit()
    conn.close()

def del_row(fname: str, lname: str, pnumber: str) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f"DELETE FROM contacts WHERE first_name = '{fname}' OR last_name = '{last_name}' OR phone = '{pnumber}';")
    conn.commit()
    conn.close()

def delete() -> None:
    output_label.set("")
    fname=first_name.get()
    lname=last_name.get()
    pnumber=phone_number.get()
    if not fname and not lname and not pnumber:
        output_label.set("Please fill out at least one field")
    else:
        del_row(fname, lname, pnumber)
        output_label.set("Attempted to delete row")
    phone_number.set("") 
    first_name.set("")
    last_name.set("")

def edit() -> None:
    output_label.set("")
    fname=first_name.get()
    lname=last_name.get()
    pnumber=phone_number.get()
    if not fname or not lname or not pnumber:
        output_label.set("Please fill out all fields")
    else:
        edit_db(fname, lname, pnumber)
        output_label.set(f"{fname}, {lname}: {pnumber} edited")
    phone_number.set("") 
    first_name.set("")
    last_name.set("")

def insert() -> None:
    output_label.set("")

    fname=first_name.get()
    lname=last_name.get()
    pnumber=phone_number.get()


    if not fname or not lname or not pnumber:
        output_label.set("Please fill out all fields")
    elif len(pnumber) != 10:
        output_label.set("Phone number must be 10 digits")
    elif fname and lname and len(pnumber) == 10:
        insert_db(fname, lname, pnumber)
        output_label.set(f"{fname}, {lname}: {pnumber} inserted")
    else:
        output_label.set("Please fill out all fields")
    
    phone_number.set("") 
    first_name.set("")
    last_name.set("")

def search():
    output_label.set("")
    fname=first_name.get()
    lname=last_name.get()
    pnumber=phone_number.get()
    if not fname and not lname and not pnumber:
        output_label.set("Please fill out at least one field")
    else:
        result = search_db(fname, lname, pnumber)
        if result:
            output_label.set(result)
        else:
            output_label.set("No results found")
    phone_number.set("") 
    first_name.set("")
    last_name.set("")

def only_int(char: str) -> bool:
    return char.isdigit()

def no_tic(char: str) -> bool:
    if char == "'":
        return False
    return True

def create_widgets(root: tk.Tk, validated_int_func: str, validated_no_tic: str) -> None: 
    fname_label = tk.Label(root, text = 'First Name', font=('calibre',10, 'bold'))
    fname_entry = tk.Entry(root,textvariable = first_name, validate="key", validatecommand=(validated_no_tic, "%S"), font=('calibre',10,'normal'))
  
    lname_label = tk.Label(root, text = 'Last Name', font = ('calibre',10,'bold'))
    lname_entry=tk.Entry(root, textvariable = last_name, validate="key", validatecommand=(validated_no_tic, "%S"), font = ('calibre',10,'normal'))
  
    phone_label = tk.Label(root, text = 'Phone Number', font = ('calibre',10,'bold'))
    phone_entry=tk.Entry(root, textvariable = phone_number, validate="key", validatecommand=(validated_int_func, "%S"), font = ('calibre',10,'normal'))


    search_btn=tk.Button(root,text = 'Search', command = search)
    insert_btn=tk.Button(root,text = 'Insert', command = insert)
    edit_btn=tk.Button(root,text = 'Edit', command = edit)
    delete_btn=tk.Button(root,text = 'Delete', command = delete)



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
    edit_btn.grid(row=3,column=2)
    delete_btn.grid(row=3,column=3)
  

def main():
    root=tk.Tk() 
    # create variables
    global first_name, last_name, phone_number, output_label
    first_name=tk.StringVar()
    last_name=tk.StringVar()
    phone_number=tk.StringVar()
    output_label=tk.StringVar()
    # set the title of the window
    root.geometry("700x700")
    root.title("Jim's Phonebook")

    validated_int_func = root.register(only_int)
    validated_no_tic = root.register(no_tic)

    # create the widgets
    create_widgets(root, validated_int_func, validated_no_tic)
    # run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()