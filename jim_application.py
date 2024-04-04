import tkinter as tk
try: 
    import sqlite3
except ImportError:
    import pysqlite3 as sqlite3

# Global variables
first_name: tk.StringVar
last_name: tk.StringVar
phone_number: tk.StringVar
birthday: tk.StringVar
output_label: tk.StringVar

DB_NAME = "phone_numbers.db"

def create_table() -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    birth TEXT
                );''')
    conn.commit()
    conn.close()

def search_db(fname: str, lname: str, pnum: str, birth: str) -> str:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    first = f"%{fname}%" if fname else ""
    last = f"%{lname}%" if lname else ""
    num = f"%{pnum}%" if pnum else ""
    birth = f"%{birth}%" if birth else ""

    c.execute(f"SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR birth LIKE ?;", (first, last, num, birth))
    results = c.fetchall()
    conn.close()

    if results:
        result_str = ""
        for result in results:
            result_str += f"{result[0]}, {result[1]}: {result[2]}, {result[3]}\n"
        return result_str
    else:
        return "No results found"

def insert_db(fname: str, lname: str, pnumber: str, birth: str) -> None:
    assert len(pnumber) == 10, "Phone Number Incorrect"
    assert len(birth) == 8, "Birthday Is Incorrect"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO contacts VALUES (?, ?, ?, ?);", (fname, lname, pnumber, birth))
    conn.commit()
    conn.close()

def edit_db(fname: str, lname: str, pnumber: str, birth: str) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE contacts SET phone = ?, first_name = ?, last_name = ?, birth = ? WHERE first_name = ? OR last_name = ? OR phone = ?;", (pnumber, fname, lname, birth, fname, lname, pnumber))
    conn.commit()
    conn.close()

def del_row(fname: str, lname: str, pnumber: str, birth: str) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE first_name = ? OR last_name = ? OR phone = ? OR birth = ?;", (fname, lname, pnumber, birth))
    conn.commit()
    conn.close()

def delete() -> None:
    output_label.set("")
    fname = first_name.get()
    lname = last_name.get()
    pnumber = phone_number.get()
    birth = birthday.get()
    if not fname and not lname and not pnumber and not birth:
        output_label.set("Please fill out at least one field")
    else:
        del_row(fname, lname, pnumber, birth)
        output_label.set("Attempted to delete row")
    phone_number.set("") 
    first_name.set("")
    last_name.set("")
    birthday.set("")

def edit() -> None:
    output_label.set("")
    fname = first_name.get()
    lname = last_name.get()
    pnumber = phone_number.get()
    birth = birthday.get()
    if not fname or not lname or not pnumber or not birth:
        output_label.set("Please fill out all fields")
    else:
        edit_db(fname, lname, pnumber, birth)
        output_label.set(f"{fname}, {lname}: {pnumber}, {birth} edited")
    phone_number.set("") 
    first_name.set("")
    last_name.set("")
    birthday.set("")

def insert() -> None:
    output_label.set("")

    fname = first_name.get()
    lname = last_name.get()
    pnumber = phone_number.get()
    birth = birthday.get()

    if not fname or not lname or not pnumber or not birth:
        output_label.set("Please fill out all fields")
    elif len(birth) != 8:
        output_label.set("Birthday must be 8 digits") 
    elif len(pnumber) != 10:
        output_label.set("Phone number must be 10 digits")
    elif fname and lname and len(pnumber) == 10:
        insert_db(fname, lname, pnumber, birth)
        output_label.set(f"{fname}, {lname}: {pnumber}, {birth} inserted")
    else:
        output_label.set("Please fill out all fields")
    
    phone_number.set("") 
    first_name.set("")
    last_name.set("")
    birthday.set("")

def search():
    output_label.set("")
    fname = first_name.get()
    lname = last_name.get()
    pnumber = phone_number.get()
    birth = birthday.get()
    if not fname and not lname and not pnumber and not birth:
        output_label.set("Please fill out at least one field")
    else:
        result = search_db(fname, lname, pnumber, birth)
        if result:
            output_label.set(result)
        else:
            output_label.set("No results found")
    phone_number.set("") 
    first_name.set("")
    last_name.set("")
    birthday.set("")

def only_int(char: str) -> bool:
    return char.isdigit()

def no_tic(char: str) -> bool:
    return char != "'"

def create_widgets(root: tk.Tk, validated_int_func: str, validated_no_tic: str) -> None: 
    fname_label = tk.Label(root, text='First Name', font=('calibre', 10, 'bold'))
    fname_entry = tk.Entry(root, textvariable=first_name, validate="key", validatecommand=(validated_no_tic, "%S"), font=('calibre', 10, 'normal'))
  
    lname_label = tk.Label(root, text='Last Name', font=('calibre', 10, 'bold'))
    lname_entry = tk.Entry(root, textvariable=last_name, validate="key", validatecommand=(validated_no_tic, "%S"), font=('calibre', 10, 'normal'))
  
    phone_label = tk.Label(root, text='Phone Number', font=('calibre', 10, 'bold'))
    phone_entry = tk.Entry(root, textvariable=phone_number, validate="key", validatecommand=(validated_int_func, "%S"), font=('calibre', 10, 'normal'))

    birth_label = tk.Label(root, text='Birthday', font=('calibre', 10, 'bold'))
    birth_entry = tk.Entry(root, textvariable=birthday, validate="key", validatecommand=(validated_int_func, "%S"), font=('calibre', 10, 'normal'))

    search_btn = tk.Button(root, text='Search', command=search)
    insert_btn = tk.Button(root, text='Insert', command=insert)
    edit_btn = tk.Button(root, text='Edit', command=edit)
    delete_btn = tk.Button(root, text='Delete', command=delete)

    output_lbl = tk.Label(root, textvariable=output_label, font=('calibre', 10, 'bold'))
    output_lbl.grid(row=4, column=0)
  
    fname_label.grid(row=0, column=0)
    fname_entry.grid(row=0, column=1)
    lname_label.grid(row=1, column=0)
    lname_entry.grid(row=1, column=1)
    phone_label.grid(row=2, column=0)
    phone_entry.grid(row=2, column=1)
    birth_label.grid(row=3, column=0)
    birth_entry.grid(row=3, column=1)
    search_btn.grid(row=4, column=0)
    insert_btn.grid(row=4, column=1)
    edit_btn.grid(row=4, column=2)
    delete_btn.grid(row=4, column=3)
  

def main():
    create_table()
    root = tk.Tk() 
    global first_name, last_name, phone_number, birthday, output_label
    first_name = tk.StringVar()
    last_name = tk.StringVar()
    phone_number = tk.StringVar()
    birthday = tk.StringVar()
    output_label = tk.StringVar()

    root.geometry("700x700")
    root.title("Jim's Phonebook")

    validated_int_func = root.register(only_int)
    validated_no_tic = root.register(no_tic)

    create_widgets(root, validated_int_func, validated_no_tic)
    root.mainloop()

if __name__ == "__main__":
    main()
