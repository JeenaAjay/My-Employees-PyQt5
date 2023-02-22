import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import sqlite3
from PIL import Image

####################################Creating a database###################################
con = sqlite3.connect("employees.db")
cur = con.cursor()
# Table is created in db using DB Browser app for SQLite

defaultImg = "person.png"            # Default img when user doesn't upload one
id = None                            # Global variable so that this can be used in multiple classes

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(550, 150, 850, 750)
        self.setWindowTitle("My Employees")
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getEmployees()
        self.displayFirstRecord()

    def mainDesign(self):
        self.setStyleSheet('font-size: 12pt; font-family: Arial Bold')
        self.employeeList = QListWidget()
        self.employeeList.itemClicked.connect(self.singleClick)
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpd = QPushButton("Update")
        self.btnUpd.clicked.connect(self.updateEmployee)
        self.btnDel = QPushButton("Delete")
        self.btnDel.clicked.connect(self.deleteEmployee)

    def addEmployee(self):
        self.newEmployee = AddEmployee()    # Creates instance of new class 'AddEmployee'. ie, new window appears
        self.close()                        # Closes current window

    def deleteEmployee(self):
        if self.employeeList.selectedItems():                    # If a person is selected:
            employee = self.employeeList.currentItem().text()
            # print(employee)
            id = employee.split("-")[0]
            mbox = QMessageBox.question(self, "Warning!", "Are you sure to delete?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM employees WHERE id=?"
                    cur.execute(query, (id,))
                    con.commit()
                    QMessageBox.information(self, "Success", "Person has been deleted")
                    self.close()               # close current window
                    self.main = Main()          #Reopen so that list is now updated

                except:
                    QMessageBox.information(self, "Warning!", "Person has not been deleted")

        else:                               # If a person is not selected:
            QMessageBox.information(self, "Warning!", "Please select a person to delete")


    def getEmployees(self):
        query = "SELECT id, name, surname FROM employees"
        employees = cur.execute(query).fetchall()
        for employee in employees:
            self.employeeList.addItem(str(employee[0])+"-"+employee[1]+" "+employee[2])

    def displayFirstRecord(self):
        query = "SELECT * FROM employees ORDER BY ROWID ASC LIMIT 1"       # Display only 1st record
        employee = cur.execute(query).fetchone()               # Returns a tuple (id,name,surname,phone,email,img,addr)
        img = QLabel()
        img.setPixmap(QPixmap("images/"+employee[5]))
        name = QLabel(employee[1])
        surname = QLabel(employee[2])
        phone = QLabel(employee[3])
        email = QLabel(employee[4])
        address = QLabel(employee[6])
        self.leftLayout.setVerticalSpacing(20)                   # Sets vertical space of 20px between rows
        self.leftLayout.addRow("", img)
        self.leftLayout.addRow("Name : ", name)
        self.leftLayout.addRow("Surname : ", surname)
        self.leftLayout.addRow("Phone : ", phone)
        self.leftLayout.addRow("Email : ", email)
        self.leftLayout.addRow("Address : ", address)

    def singleClick(self):
        # To remove the details of current selected emp, we use takeAt()
        for i in reversed(range(self.leftLayout.count())):    # Reversed because otherwise, it messes with widget order
            widget = self.leftLayout.takeAt(i).widget()  # Removed widget at that point
            if widget is not None:                           # If not removed:
                widget.deleteLater()                       # Schedule to delete later
        employee = self.employeeList.currentItem().text()
        id = employee.split('-')[0]
        query = "SELECT * FROM employees WHERE id=?"
        employee = cur.execute(query, (id,)).fetchone()  # Returns a tuple (id,name,surname,phone,email,img,addr)
        img = QLabel()
        img.setPixmap(QPixmap("images/" + employee[5]))
        name = QLabel(employee[1])
        surname = QLabel(employee[2])
        phone = QLabel(employee[3])
        email = QLabel(employee[4])
        address = QLabel(employee[6])
        self.leftLayout.setVerticalSpacing(20)  # Sets vertical space of 20px between rows
        self.leftLayout.addRow("", img)
        self.leftLayout.addRow("Name : ", name)
        self.leftLayout.addRow("Surname : ", surname)
        self.leftLayout.addRow("Phone : ", phone)
        self.leftLayout.addRow("Email : ", email)
        self.leftLayout.addRow("Address : ", address)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QFormLayout()
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightBottomLayout = QHBoxLayout()
        ############################Adding child layouts to main layout###################
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout, 40)                          # aspect ratio is 40% of window
        self.mainLayout.addLayout(self.rightMainLayout, 60)                     # aspect ratio is 60% of window
        ###########################Adding widgets to layout###############################
        self.rightTopLayout.addWidget(self.employeeList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpd)
        self.rightBottomLayout.addWidget(self.btnDel)

        self.setLayout(self.mainLayout)

    def updateEmployee(self):
        global id
        if self.employeeList.selectedItems():                    # If a person is selected:
            employee = self.employeeList.currentItem().text()
            id = employee.split("-")[0]
            self.close()
            self.updateWindow = updateEmployee()

        else:
            QMessageBox.information(self, "Warning!", "Please select a person to update")


class updateEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(650, 150, 550, 750)
        self.setWindowTitle("Update Employee")
        self.UI()
        self.show()

    def UI(self):
        self.getEmployee()
        self.mainDesign()
        self.layouts()

    def getEmployee(self):
        global id
        query = "SELECT * FROM employees WHERE id=?"
        employee = cur.execute(query, (id,)).fetchone()
        self.name = employee[1]
        self.surname = employee[2]
        self.phone = employee[3]
        self.email = employee[4]
        self.image = employee[5]
        self.address = employee[6]

    def mainDesign(self):
        self.setStyleSheet('background-color: white; font-size: 12pt; font-family: Arial')  # Set style for whole window
        ##########################Top Layout########################################
        self.title = QLabel("Update Person")
        self.title.setStyleSheet('font-size: 24pt; font-family: Arial Bold')
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("images/{}".format(self.image)))
        ##########################Bottom Layout#####################################
        self.nameLbl = QLabel("Name : ")
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.name)
        self.surnameLbl = QLabel("Surname : ")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setText(self.surname)
        self.phoneLbl = QLabel("Phone : ")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phone)
        self.emailLbl = QLabel("Email : ")
        self.emailEntry = QLineEdit()
        self.emailEntry.setText(self.email)
        self.imgLbl = QLabel("Image : ")
        self.imgBtn = QPushButton("Browse")
        self.imgBtn.clicked.connect(self.uploadImage)
        self.imgBtn.setStyleSheet('background-color: orange; font-size: 10pt')  # Set style for button
        self.addressLbl = QLabel("Address : ")
        self.addressEntry = QTextEdit()
        self.addressEntry.setText(self.address)
        self.addBtn = QPushButton("Update")
        self.addBtn.setStyleSheet('background-color: orange; font-size: 10pt')  # Set style for button
        self.addBtn.clicked.connect(self.updateEmp)

    def uploadImage(self):
        global defaultImg
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", 'Image Files (*.jpg *.png)')

        if ok:
            defaultImg = os.path.basename(self.fileName) # Returns 'tree.png' if filename is "C:/Downloads/images/tree.png"
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImg))   # Image saved to 'images' folder

    def updateEmp(self):
        global defaultImg
        global id
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImg
        address = self.addressEntry.toPlainText()
        if (name and surname and phone != ""):
            try:
                query = "UPDATE employees SET name=?, surname=?, phone=?, email=?, img=?, address=? WHERE id=?"
                cur.execute(query, (name, surname, phone, email, img, address, id))
                con.commit()
                QMessageBox.information(self, "Success!", "Person has been updated!")
                self.close()                             # Close current window
                self.main = Main()                       # Open main window

            except:
                QMessageBox.information(self, "Warning!", "Person has not been updated!")

        else:
            QMessageBox.information(self, "Warning!", "Fields cannot be empty!")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        ##############################Adding child layouts###########################
        self.mainLayout.addLayout(self.topLayout, 30)
        self.mainLayout.addLayout(self.bottomLayout, 70)
        #############################Adding widgets##################################
            ########################Top Layout widgets##########################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(180, 20, 10, 30)
            #####################Bottom layout widgets##########################
        self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
        self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
        self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
        self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
        self.bottomLayout.addRow(self.imgLbl, self.imgBtn)
        self.bottomLayout.addRow(self.addressLbl, self.addressEntry)
        self.bottomLayout.addRow("", self.addBtn)            # To keep button at RHS
        #############################Setting main layout#############################
        self.setLayout(self.mainLayout)

class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(650, 150, 550, 750)
        self.setWindowTitle("Add Employee")
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()



    def mainDesign(self):
        self.setStyleSheet('background-color: white; font-size: 12pt; font-family: Arial')  # Set style for whole window
        ##########################Top Layout########################################
        self.title = QLabel("Add Person")
        self.title.setStyleSheet('font-size: 24pt; font-family: Arial Bold')
        self.imgAdd = QLabel()
        self.imgAdd.setPixmap(QPixmap("icons/person.png"))
        ##########################Bottom Layout#####################################
        self.nameLbl = QLabel("Name : ")
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name")
        self.surnameLbl = QLabel("Surname : ")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter surname")
        self.phoneLbl = QLabel("Phone : ")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter phone")
        self.emailLbl = QLabel("Email : ")
        self.emailEntry = QLineEdit()
        self.emailEntry.setPlaceholderText("Enter email")
        self.imgLbl = QLabel("Image : ")
        self.imgBtn = QPushButton("Browse")
        self.imgBtn.clicked.connect(self.uploadImage)
        self.imgBtn.setStyleSheet('background-color: orange; font-size: 10pt')   # Set style for button
        self.addressLbl = QLabel("Address : ")
        self.addressEntry = QTextEdit()
        self.addBtn = QPushButton("Add")
        self.addBtn.setStyleSheet('background-color: orange; font-size: 10pt')   # Set style for button
        self.addBtn.clicked.connect(self.addEmp)

    def uploadImage(self):
        global defaultImg
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", 'Image Files (*.jpg *.png)')

        if ok:
            defaultImg = os.path.basename(self.fileName) # Returns 'tree.png' if filename is "C:/Downloads/images/tree.png"
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImg))   # Image saved to 'images' folder

    def addEmp(self):
        global defaultImg
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImg
        address = self.addressEntry.toPlainText()
        if (name and surname and phone != ""):
            try:
                query = "INSERT INTO employees (name, surname, phone, email, img, address) VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(query, (name, surname, phone, email, img, address))
                con.commit()
                QMessageBox.information(self, "Success!", "Person has been added!")
                self.close()                             # Close current window
                self.main = Main()                       # Open main window

            except:
                QMessageBox.information(self, "Warning!", "Person has not been added!")

        else:
            QMessageBox.information(self, "Warning!", "Fields cannot be empty!")


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        ##############################Adding child layouts###########################
        self.mainLayout.addLayout(self.topLayout, 30)
        self.mainLayout.addLayout(self.bottomLayout, 70)
        #############################Adding widgets##################################
            ########################Top Layout widgets##########################
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title)
        self.topLayout.addWidget(self.imgAdd)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(180, 20, 10, 30)
            #####################Bottom layout widgets##########################
        self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
        self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
        self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
        self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
        self.bottomLayout.addRow(self.imgLbl, self.imgBtn)
        self.bottomLayout.addRow(self.addressLbl, self.addressEntry)
        self.bottomLayout.addRow("", self.addBtn)            # To keep button at RHS
        #############################Setting main layout#############################
        self.setLayout(self.mainLayout)


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
