try: 
    import sqlite3
except ImportError:
    import pysqlite3 as sqlite3

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from PyQt6.QtCore import (
    pyqtSignal,
)

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

def search_db(fname: str, lname: str, pnum: str, birth: str) -> list[list[str]]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    first = f"%{fname}%" if fname else ""
    last = f"%{lname}%" if lname else ""
    num = f"%{pnum}%" if pnum else ""
    birth = f"%{birth}%" if birth else ""

    c.execute("SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR birth LIKE ? LIMIT 5;", (first, last, num, birth))
    results = c.fetchall()
    conn.close()

    if results:
        result_list = []
        for result in results:
            result_list.append([result[0], result[1], result[2], result[3]])
        return result_list
    else:
        return []

def insert_db(fname: str, lname: str, pnumber: str, birth: str) -> None:
    assert len(pnumber) == 10, "Phone Number Incorrect"
    # assert len(birth) == 8, "Birthday Is Incorrect"
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

def show_all() -> list[list[str]]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM contacts;")
    results = c.fetchall()
    conn.close()
    return results

def only_int(char: str) -> bool:
    return char.isdigit()

def no_tic(char: str) -> bool:
    return char != "'"

class DayComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()
    def showPopup(self) -> None:
        self.popupAboutToBeShown.emit()
        return super(DayComboBox, self).showPopup()


class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Jim's Application")

        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(QLabel("First Name:"))
        self.fname = QLineEdit()
        self.hbox1.addWidget(self.fname)
        self.hbox1.addWidget(QLabel("Last Name:"))
        self.lname = QLineEdit()
        self.hbox1.addWidget(self.lname)
        self.vbox.addLayout(self.hbox1)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(QLabel("Phone Number:"))
        
        self.pnumber = QLineEdit()
        self.pnumber.setInputMask("999-999-9999")
        self.hbox2.addWidget(self.pnumber)
        
        self.hbox2.addWidget(QLabel("Birthday:"))
        self.combo_month = QComboBox()
        self.combo_month.addItem("January")
        self.combo_month.addItem("February")
        self.combo_month.addItem("March")
        self.combo_month.addItem("April")
        self.combo_month.addItem("May")
        self.combo_month.addItem("June")
        self.combo_month.addItem("July")
        self.combo_month.addItem("August")
        self.combo_month.addItem("September")
        self.combo_month.addItem("October")
        self.combo_month.addItem("November")
        self.combo_month.addItem("December")
        self.hbox2.addWidget(self.combo_month)
        self.combo_day = DayComboBox()
        self.combo_day.popupAboutToBeShown.connect(self.get_days)
        self.combo_day.addItem("1")
        self.hbox2.addWidget(self.combo_day)
        self.combo_year = QComboBox()
        for i in range(2024, 1900, -1):
            self.combo_year.addItem(str(i))
        self.hbox2.addWidget(self.combo_year)

        self.vbox.addLayout(self.hbox2)
        self.button_box = QHBoxLayout()
        self.show_all_button = QPushButton("Show All")
        self.show_all_button.clicked.connect(self.show_all)
        self.button_box.addWidget(self.show_all_button)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        self.button_box.addWidget(self.search_button)
        self.insert_button = QPushButton("Insert")
        self.insert_button.clicked.connect(self.insert)
        self.button_box.addWidget(self.insert_button)
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit)
        self.button_box.addWidget(self.edit_button)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)
        self.button_box.addWidget(self.delete_button)
        self.vbox.addLayout(self.button_box)
        self.result_label = QLabel()
        
        self.table_view = QTableWidget()
        self.table_view.setRowCount(5)
        self.table_view.setColumnCount(4)
        self.table_view.setHorizontalHeaderLabels(["First Name", "Last Name", "Phone Number", "Birthday"])
        vh = self.table_view.verticalHeader()
        if vh:
            vh.setHidden(True)
        hh = self.table_view.horizontalHeader()
        if hh:
            hh.setStretchLastSection(True)
            hh.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table_view.cellChanged.connect(self.handle_cell_changed)
        
        self.vbox.addWidget(self.result_label)
        self.vbox.addWidget(self.table_view)
        self.updating_cell = False
        self.show_all() 
        self.setLayout(self.vbox)
    
    def get_days(self):
        print("Displaying days!")
        months_with_30_days = ["April", "June", "September", "November"]
        month_name = self.combo_month.currentText()
        year = int(self.combo_year.currentText(), base=10)
        # remove all items
        self.combo_day.clear()

        if month_name in months_with_30_days:
            for i in range(1, 31):
                self.combo_day.addItem(str(i))
        elif month_name == "February":
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                for i in range(1, 30):
                    self.combo_day.addItem(str(i))
            else:
                for i in range(1, 29):
                    self.combo_day.addItem(str(i))
        else:
            for i in range(1, 32):
                self.combo_day.addItem(str(i))
    
    def handle_cell_changed(self, row, column) -> None:
        if not self.updating_cell:
            print(f"{row=}, {column=}")
            # get firstname or lastname in row
            first_name = self.table_view.item(row, 0)
            if not first_name:
                return
            last_name = self.table_view.item(row, 1)
            if not last_name:
                return
            pnumber = self.table_view.item(row, 2)
            if not pnumber:
                return
            birth = self.table_view.item(row, 3)
            if not birth:
                return
            if len(pnumber.text().replace("-", "")) != 10:
                self.reset_widgets()
                self.result_label.setText("Phone Number Incorrect")
                return
            if not first_name.text() or not last_name.text():
                self.reset_widgets()
                self.result_label.setText("First Name or Last Name is Empty")
                return
            if  len(birth.text().split(" ")) != 3:
                self.reset_widgets()
                self.result_label.setText("Birthday is Empty or Incorrect")
                return
            edit_db(first_name.text(), last_name.text(), pnumber.text(), birth.text())
            self.result_label.setText("Edited")

    def get_birthday(self) -> str:
        month = self.combo_month.currentText()
        day = self.combo_day.currentText()
        year = self.combo_year.currentText()
        return f"{month} {day}, {year}"
    
    def populate_table(self, data: list[list[str]]) -> None:
        self.table_view.clearContents()
        self.table_view.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                self.table_view.setItem(i, j, QTableWidgetItem(cell))

    def reset_widgets(self) -> None:
        self.fname.setText("")
        self.lname.setText("")
        self.pnumber.setText("")
        self.result_label.setText("")
        self.show_all()

    def search(self) -> None:
        results = search_db(self.fname.text(), self.lname.text(), self.pnumber.text(), self.get_birthday())
        self.updating_cell = True
        self.populate_table(results)
        self.updating_cell = False
        self.result_label.setText("Searched")
    
    def insert(self) -> None:
        if len(self.pnumber.text().replace("-", "")) != 10:
            self.result_label.setText("Phone Number Incorrect")
            return
        if self.fname.text() == "" or self.lname.text() == "":
            self.result_label.setText("First Name or Last Name is Empty")
            return
        
        insert_db(self.fname.text(), self.lname.text(), self.pnumber.text().replace("-", ""), self.get_birthday())
        self.reset_widgets()
        self.result_label.setText("Inserted")
    
    def edit(self) -> None:
        if not self.fname.text() or not self.lname.text() or not self.pnumber.text().replace("-", ""):
            self.result_label.setText("First Name, Last Name, or Phone Number is Empty")
            return

        edit_db(self.fname.text(), self.lname.text(), self.pnumber.text().replace("-", ""), self.get_birthday())
        self.reset_widgets()
        self.result_label.setText("Edited")
        
    
    def delete(self) -> None:
        del_row(self.fname.text(), self.lname.text(), self.pnumber.text().replace("-", ""), self.get_birthday())
        self.reset_widgets()
        self.result_label.setText("Deleted")

    def show_all(self) -> None:
        self.updating_cell = True
        results = show_all()
        self.populate_table(results)
        self.updating_cell = False


def ui() -> None:
    app = QApplication([])
    window = QWidget()
    main_widget = MainWidget()
    window.setLayout(main_widget.layout())
    window.show()
    app.exec()


def main():
    create_table()
    ui()

if __name__ == "__main__":
    main()
