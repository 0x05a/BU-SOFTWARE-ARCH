from jim_application import check_valid_birthday
import os

def rm_db():
    try:
        os.remove("test.db")
    except FileNotFoundError:
        pass
# test birthdays
def test_birthday():
    rm_db()
    assert check_valid_birthday("January 1, 2000".split(" "))
    assert not check_valid_birthday("asfddfa 1, 2000".split(" "))
    assert not check_valid_birthday("January 1, 2000a".split(" "))
    assert not check_valid_birthday("January 1, 2000 1".split(" "))
    assert not check_valid_birthday("February 29, 2001".split(" "))
    assert check_valid_birthday("February 29, 2000".split(" "))
    assert check_valid_birthday("February 28, 2001".split(" "))

# test that we can create a database and enter info
def test_database():
    rm_db()
    from jim_application import create_table, insert_db, show_all
    create_table("test.db")
    insert_db("Jim", "Faulker", "1112223333", "January 1, 2000", db_name="test.db")
    assert show_all("test.db") == [('Jim', 'Faulker', "1112223333", 'January 1, 2000')]
    insert_db("Joe", "Faulker", "2223334444", "December 1, 2000", db_name="test.db")
    assert show_all("test.db") == [('Jim', 'Faulker', "1112223333", 'January 1, 2000'), ('Joe', 'Faulker',"2223334444", 'December 1, 2000')]

# test that we can delete a row from the database
def test_delete():
    rm_db()
    from jim_application import create_table, insert_db, show_all, del_row
    create_table("test.db")
    insert_db("Jim", "Faulker", "1234554321", "January 1, 2000", db_name="test.db")
    insert_db("Joe", "Faulker", "1234554322", "December 1, 2000", db_name="test.db")
    del_row("Joe", "Faulkner",  "1234554322", "December 1, 2000", db_name="test.db")
    assert show_all("test.db") == [('Jim', 'Faulker',  '1234554321', 'January 1, 2000')]





