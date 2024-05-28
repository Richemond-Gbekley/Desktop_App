import sys
import uuid
import hashlib
import re
import logging
import random
import datetime
import schedule
import time
import decimal
from scheduler import start_scheduler
import csv
import mysql.connector
from scheduler import start_scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from PyQt5.QtCore import pyqtSlot
from decimal import Decimal, InvalidOperation
from PyQt5 import QtCore 
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QPixmap,QPalette,QBrush,QPen,QPainter, QColor
from PyQt5.QtCore import QRectF, QPoint, QObject,pyqtSignal, Qt, QPropertyAnimation, QRect, QTimer, QSize,QDate ,QCalendar ,QDateTime# Qt core manages the alignment, and the Qpropertyanimation, with the Qreact handles the animation
from PyQt5.QtWidgets import QApplication, QMainWindow,QFormLayout, QAbstractItemView,QTableWidget,QTableWidgetItem,QLabel,QListWidgetItem,QListWidget, QVBoxLayout,QFileDialog, QPushButton, QWidget, QLineEdit, QComboBox,QTextEdit, QStyle, QAction, QToolBar,QToolButton, QCheckBox, QMenu, QDateEdit, QMessageBox,QCalendarWidget,QStackedWidget,QFrame,QHBoxLayout
logging.basicConfig(level=logging.DEBUG)


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = self.create_db_connection()  # Initialize db attribute during object creation
        self.current_user_email = None  # Store logged-in user info

        self.setWindowTitle("Login Window")
        self.setGeometry(100, 100, 1500, 900)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)


        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 1500, 900)

        # Loading a list of images
        self.image_paths = ["desk.jpg"]


        # Load intial image
        self.load_image()

        # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Log into your</><p> account</>", self)
        label_height = 200  # Adjust the width of the label as needed
        label_width =900
        self.welcome_label.setGeometry(300, 10, label_width, label_height)
        self.welcome_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 20px; font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignCenter)


        # Button for "Login"
        self.login1_button = QPushButton("Login", self)
        button_width = 400  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.login1_button.setGeometry(button_x, 500, button_width, 70)
        self.login1_button.setStyleSheet("""
                 QPushButton {
                 background-color: blue;
                  font-size: 12pt; 
                  border-radius: 35px;
                  }
                   QPushButton:hover{
                    background-color:brown

                  }
              """)
        self.login1_button.clicked.connect(self.open_Main1_window)


        # Button for "Create Account"
        self.create_account_button = QPushButton("Create Account", self)
        button_width = 400  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.create_account_button.setGeometry(button_x, 550, button_width, 70)
        self.create_account_button.setStyleSheet("""
                      QPushButton {
                      background-color: transparent;
                      border:none;
                       font-size: 14pt; 
                       border-radius: 35px;
                       color: black;
                       }
                        QPushButton:hover{
                           font-size: 20pt;
                       }
                   """)
        self.create_account_button.clicked.connect(self.open_register_window)

        # Button for "Forgot Password"
        self.forgot_password_button = QPushButton("forgot Password ?", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = 700 # Center the button horizontally
        self.forgot_password_button.setGeometry(button_x, 410, button_width, 30)
        self.forgot_password_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 16px; 
                              border-radius: 35px;
                              color: black;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        self.forgot_password_button.clicked.connect(self.open_forgot_password_window)

        # Create a line edit for the email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(575, 290, 350, 50)  # Adjust the position and size of the input field

        # Set placeholder text for the email input field
        self.email_input.setPlaceholderText("Enter Email")


        # Apply styling to the email input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

        # Enable the clear button to clear the input
        self.email_input.setClearButtonEnabled(True)

        # Set an icon for the input field
        icon = QIcon("user.png")  # Replace "icon.png" with the path to your icon file
        self.email_input.addAction(icon, QLineEdit.LeadingPosition)

        # Connect textChanged signal to validate_email slot
        self.email_input.textChanged.connect(self.validate_input)
        self.email_input.editingFinished.connect(self.reset_email_input_style)


        #Create a line edit for password input field

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(575, 350, 350, 50)

        #Set placeholder text for the password input field
        self.password_input.setPlaceholderText("Enter Password")

        #Appply styling to the password input field
        self.password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")

        #Enable the clear button to the clear input
        self.password_input.setClearButtonEnabled(True)

        #Set an icon for the input field
        icon = QIcon("padlock.png")
        self.password_input.addAction(icon, QLineEdit.LeadingPosition)

        self.password_input.setEchoMode(QLineEdit.Password)


        # Create checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setGeometry(570, 410, 200, 30)
        self.show_password_checkbox.setStyleSheet("font-size:16px; color:black")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

    
   






    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            # Show password
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.password_input.setEchoMode(QLineEdit.Password)

    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel

    def validate_input(self, text):
        # Regular expression pattern for validating email addresses
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^[0-9]{10}$'  # Assuming a 10-digit phone number
        account_pattern = r'^[0-9]{6,12}$'  # Example pattern for account number (6 to 12 digits)

        # Compile the pattern into a regular expression object
        email_regex = re.compile(email_pattern)
        phone_regex = re.compile(phone_pattern)
        account_regex = re.compile(account_pattern)

        # Use match method to check if the input text matches the pattern
        if email_regex.match(text):
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        elif phone_regex.match(text):
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        elif account_regex.match(text):
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid red;")




            # Set font size back to normal
            font = self.email_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.email_input.setFont(font)

    @pyqtSlot()
    def reset_email_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

   
    

    
              
        self.db = self.create_db_connection()
        self.current_user_email = None # Store logged-in user info

    def create_db_connection(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="S3cR3tUs3R",
                database="desktopdb"
            )
            return db
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to the database. Error: {e}")
            return None


    def open_Main1_window(self):
        email = self.email_input.text()
        password = self.password_input.text()
        


        try:
            if self.db is None:
                return
            
            #Create Cursor:
            cursor = self.db.cursor()
            hash_password = hashlib.sha256(password.encode()).hexdigest()
        
            
            # Execute SELECT query to check login credentials
            query = "SELECT * FROM registerdb WHERE Email = %s AND PasswordHash = %s"
                 
            cursor.execute(query, (email, hash_password))
            result = cursor.fetchone()
            print(hash_password)
            print(password)
            

            if result:
          

                # Assuming the login is successful and you have retrieved user details
                Firstname, Lastname, Phonenumber = self.get_user_details(email)
                self.log_login(Firstname, Lastname, email, Phonenumber)
                self.my_accountdb(Firstname, Lastname,  Phonenumber, email)
                self.current_user_email = email #Sets the session variable
                self.current_password = hash_password
                cursor.close()
                print(hash_password)
                self.Main1_window = Main1Window(db=self.db, Firstname=Firstname, Lastname = Lastname,  Phonenumber=Phonenumber,current_password= self.current_password, current_user_email=self.current_user_email)
                self.Main1_window.show()
                


            # Close the current window (RegisterWindow)
                self.close()
                QMessageBox.information(self, "Login Successful", "You have successfully logged in.")
      
                
               
            else:
                
                
                

                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
       
        except mysql.connector.Error as e :
            QMessageBox.critical(self,"Error",f"Failed to register user. Error:{e}")

    def get_user_details(self, email):
        # Fetch user details from the database based on the email
        # Modify this according to your database structure and query method
        cursor = self.db.cursor()
        # Execute the SELECT query to fetch user details based on email
        sql = "SELECT FirstName, LastName, Phonenumber FROM registerdb WHERE Email = %s"
        cursor.execute(sql, (email,))
       
        result = cursor.fetchone()  # Assuming there's only one user with the email
        cursor.close()
        return result if result else (None, None)

    def log_login(self, Firstname, Lastname, email, Phonenumber):
        try:
           cursor = self.db.cursor()
           login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           sql = "INSERT INTO login_logs (Firstname, Lastname, Email, login_time, PhoneNumber) VALUES (%s,%s, %s, %s,%s)"
           values = (Firstname, Lastname, email, login_time, Phonenumber,)
           cursor.execute(sql, values)
           self.db.commit()
           cursor.close() 
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error logging login: {e}")

    def my_accountdb(self, Firstname, Lastname, Phonenumber,email):
        try:
            cursor = self.db.cursor()
              # Execute SELECT query to check login credentials
            query1 = "SELECT * FROM my_accountdb WHERE Email = %s "
                 
            cursor.execute(query1, (email,))
            result = cursor.fetchone()

            Balance = 0.00
            

            if result:
                return
            
            else:
                sql1 = "INSERT INTO my_accountdb (Email, Firstname, Lastname, Balance, Phonenumber) VALUES (%s,%s, %s, %s,%s)"
                values = (email, Firstname, Lastname,Balance,Phonenumber,)
                cursor.execute(sql1, values)
                self.db.commit()
                cursor.close() 
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error logging login: {e}")


                    




    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    def open_forgot_password_window(self):
        self.forgot_password_window = Forgot_PasswordWindow()
        self.forgot_password_window.show()
        self.close()


class Main1Window(QMainWindow):
    
    
  
    def __init__(self, db, current_user_email,Firstname,Lastname, Phonenumber, current_password):
        super().__init__()
        self.setWindowTitle(" Main  Window")
        self.setGeometry(100, 100, 1500, 900)
          # Create a signal manager instance
        
    
   

        self.current_user_email = current_user_email 
        self.db = db
        self.first_name = Firstname
        self.last_name = Lastname
        self.phone_number = Phonenumber
        self.current_password = current_password
              # Create central widget and layout
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 1500, 900)

        # Loading a list of images
        self.image_paths = ["image10.jpg"]

        # Load intial image
        self.load_image()


          # Connect the update_home_page signal to a slot in the home page
        #self.update_home_page.connect(self.update_home_page_slot)

                 # Create a stacked widget to hold multiple pages


        self.stacked_widget = QStackedWidget(self.centralWidget())
       # self.central_layout = QVBoxLayout(self.centralWidget())
       # self.central_layout.addWidget(self.stacked_widget)
      #  self.stacked_widget.setStyleSheet("background-color: transparent")
        self.stacked_widget.setGeometry(200, 0, 1300, 900)  # Adjust size and position as needed
        #.stacked_widget.setStyleSheet("QStackedWidget{background-image: url(desk.jpg); background-repeat; no-repeat; background-position: center; background-size: cover; }")
        self.current_user_email = current_user_email 
        self.db = db
        self.first_name = Firstname
        self.last_name = Lastname
        self.phone_number = Phonenumber
        self.current_password = current_password
        

        # Create a QLabel to display the image
        image_label = QLabel(self.stacked_widget)
        image_label.setGeometry(200, 0 , 1300, 900)
        self.image_path = ["desk.jpg"]

        self.load1_image()
       # pixmap = QPixmap("desk.jpg")
       # background_label = QLabel(self.stacked_widget)
        #background_label.setPixmap(pixmap.scaled(self.stacked_widget.size()))
        
        #background_label.setScaledContents(self)
        #image_label = QLabel()
        #image_path = "stack.jpg"  # Replace with the actual path to your image file
        #pixmap = QPixmap(image_path)
        #image_label.setPixmap(pixmap)

# Add the QLabel to the stacked widget
   #     self.stacked_widget.addWidget(image_label)

        # Add pages to the stacked widget
        self.home_page(db, current_user_email,Firstname) #0
        self.account_page() #1
        self.susu_page() #2
        self.savings_page() #3
        self.transfer_page() #4
        self.loan_page() #5
        self.profile_page() #6
        self.edit_profile_page() #7
        self.change_password_page(db, current_password, current_user_email) #8
        self.check_balance_page() #9
        self.mini_statement_page() # 10
        self.susu_details_page() #11
        self.create_account_page() #12
        self.own_account_page() #13
        self.another_account_page()# 14
        self.wallet_page() # 15
        self.loan_balance_page() #16
        self.loan_request_page() #17
        self.savings_account_page(db, current_user_email) #18
        self.notification_page() #19
        self.email_page(db, current_user_email) # 20
        self.mobile_number_page(db, Phonenumber) #21
        self.myaccount_page(db, current_user_email) #22
        self.create_pin_page(db, current_user_email) #23
        self.change_pin_page(db, current_user_email, Phonenumber) #24
        self.saving_balance_page(db, current_user_email) #25
        self.my_saving_account() #26
        self.transfer_to_my_account() #27
        self.saving_to_my_account_transfer()#28
        self.susu_to_my_wallet_transfer() #29
        self.mobile_wallet_to_account_transfer() #30
        self.transfer_to_my_saving_account() #31
        self.transfer_to_susu_account() #32
        self.join_susu_group() #33
        self.personal_susu_account() #34
        self.forgot_pin() #35
        self.transfer_to_susu_group() #36
        
        self.stacked_widget.currentChanged.connect(self.handle_page_change)

      

        # Create a frame
        self.frame = QFrame(self.centralWidget())
       # self.frame.setFrameShape(QFrame.StyledPanel)  # Set the frame shape
        self.frame.setStyleSheet("background-color: #333333;")  # Set background color
             
       # frame.setGeometry(280,300,50,50)
        self.frame.setGeometry(0,0,200,900)   

        
        # Create a layout for the frame
       # frame_layout = QVBoxLayout(self.frame)    

        Home_button = QPushButton("Dashboard", self.frame)
       
        Home_button.setGeometry(-20, 150, 200, 30)
        self.set_button_icon0(Home_button, "home.png")  # Set button icon
        Home_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        Home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))  # Switch to home page

        account_button = QPushButton("Account", self.frame)
        account_button.setGeometry(-7,230,150,30)
        self.set_button_icon1(account_button, "user.png")
        account_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))  # Switch to home page
        

        susu_button = QPushButton("Susu", self.frame)
        susu_button.setGeometry(-19,310,150,30)
        self.set_button_icon2(susu_button, "group.png")
        susu_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        susu_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))  # Switch to home page


        savings_button = QPushButton("Savings", self.frame)
        savings_button.setGeometry(-7,390,150,30)
        self.set_button_icon3(savings_button, "piggy-bank.png")
        savings_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        savings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))  # Switch to home page


        
        transfer_button = QPushButton("Transfer", self.frame)
        transfer_button.setGeometry(-7,470,150,30)
        self.set_button_icon4(transfer_button, "money.png")
        transfer_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        transfer_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))  # Switch to home page



        loan_button = QPushButton("Loan", self.frame)
        loan_button.setGeometry(-25,550,150,30)
        self.set_button_icon5(loan_button, "payment.png")
        loan_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        loan_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))  # Switch to home page



        profile_button = QPushButton("Profile", self.frame)
        profile_button.setGeometry(-15,630,150,30)
        self.set_button_icon6(profile_button, "user.png")
        profile_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 23px; 
                              border-radius: 35px;
                              color: white;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        profile_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))  # Switch to home page




        
    def set_button_icon0(self, Home_button, icon_path):
        icon = QIcon(icon_path)
        Home_button.setIcon(icon)
        Home_button.setIconSize(Home_button.size())  # Set icon size to button size

    def set_button_icon1(self, account_button, icon_path):
        icon = QIcon(icon_path)
        account_button.setIcon(icon)
        account_button.setIconSize(account_button.size())  # Set icon size to button size
    
    def set_button_icon2(self, susu_button, icon_path):
        icon = QIcon(icon_path)
        susu_button.setIcon(icon)
        susu_button.setIconSize(susu_button.size())  # Set icon size to button size
    

    def set_button_icon3(self, savings_button, icon_path):
        icon = QIcon(icon_path)
        savings_button.setIcon(icon)
        savings_button.setIconSize(savings_button.size())  # Set icon size to button size

    
    def set_button_icon4(self, transfer_button, icon_path):
        icon = QIcon(icon_path)
        transfer_button.setIcon(icon)
        transfer_button.setIconSize(transfer_button.size())  # Set icon size to button size

      
    def set_button_icon5(self, loan_button, icon_path):
        icon = QIcon(icon_path)
        loan_button.setIcon(icon)
        loan_button.setIconSize(loan_button.size())  # Set icon size to button size
    
    def set_button_icon6(self, profile_button, icon_path):
        icon = QIcon(icon_path)
        profile_button.setIcon(icon)
        profile_button.setIconSize(profile_button.size())  # Set icon size to button size
    

        schedule.every().day.at("00:00").do(self.calculate_and_update_balance)
      

   
#Page index 0
     # Pages
    def home_page(self, db , current_user_email,Firstname):
        self.current_user_email = current_user_email
        self.db = db
        self.first_name = Firstname
        
        

        self.home_widget = QWidget()
        self.icon_label = QLabel(self.central_widget)
        self.setCircularIcon(self.icon_label, "user1.png", size = 130, position= (50,10))  # Set your icon path
        self.layout.addWidget(self.icon_label)
        self.icon_label.setParent(self.home_widget)

        
        home_label = QLabel(f"Welcome, {Firstname} ",self.home_widget)
        home_label.setGeometry(200,48,500,80)
        home_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home_label.setAlignment(Qt.AlignCenter)

        transaction_alert = self.transactions()

        # Calendar Widget
        calendar = self.calendar()
        
        alert = self.alert()
        
        user_info = self.user_info()
        
        logout_button = QPushButton(self)
        logout_button.setGeometry(950,800,300,70)
        icon = QIcon("log-out.png")
        icon_size = QSize(30, 30)  # Adjust the size as needed
        logout_button.setIconSize(icon_size)
        logout_button.setStyleSheet("""
                           QPushButton {
                                       background-color: blue;
                                       font-size: 20pt;
                                       border-radius: 35px;
                                       color: black;
                                    text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)
        # Set the icon to the left of the button text
        icon = QIcon("log-out.png")
        logout_button.setIcon(icon)

# Set the text for the button
        logout_button.setText(" | log Out")

        logout_button.clicked.connect(self.open_main_window)

        logout_button.setParent(self.home_widget)

        
        
        
        self.stacked_widget.addWidget(self.home_widget)

    def calendar(self) :
        self.calendar_section_widget = QWidget()
        self.calendar_section_widget.setGeometry(900, 150, 350, 300)
        self.calendar_section_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.calendar_section_widget.setParent(self.home_widget)
        #calendar_layout = QVBoxLayout(self.calendar_section_widget)


        self.widget_layout =QVBoxLayout(self.calendar_section_widget)


        # Calendar title label
        calendar_title = QLabel("Calendar")
        calendar_title.setFont(QFont("Arial", 16, QFont.Bold))
        calendar_title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(calendar_title)

         # Calendar widget
        calendar = QCalendarWidget()
        #calendar.setGridVisible(True)
        calendar.setStyleSheet("""
        QCalendarWidget {
            background-color: black;
            color: white;
            border-radius: 10px;
        }
        QCalendarWidget QToolButton {
            color: white;
        }
        QCalendarWidget QToolButton:hover {
            color: yellow;
        }
        QCalendarWidget QMenu {
            background-color: black;
            color: white;
        }
        QCalendarWidget QWidget {
            alternate-background-color: black;
            color: white;
        }
        QCalendarWidget QAbstractItemView:enabled {
            background-color: black;
            selection-background-color: darkgray;
            selection-color: black;
            color: white;
        }
        QCalendarWidget QAbstractItemView:disabled {
            color: gray;
        }
        QCalendarWidget QAbstractItemView:focus {
            color: yellow;
        }
        QCalendarWidget QTableView {
            border: 1px solid #8f8f91;
            border-top: 0;
            gridline-color: gray;
        }
        QCalendarWidget QHeaderView::section {
            background-color: #333333;
            color: white;
            padding: 5px;
            border: 1px solid gray;
        }
    """)
        self.widget_layout.addWidget(calendar)

        
        


    def alert (self):    
        self.alert_widget = QWidget()
        self.alert_widget.setGeometry(50, 600, 800, 280)
        self.alert_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.alert_widget.setParent(self.home_widget)


        self.widget_layout =QVBoxLayout(self.alert_widget)

        alert_title = QLabel("Alerts")
        alert_title.setFont(QFont("Arial", 16, QFont.Bold))
        alert_title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(alert_title)

        # Create QListWidget to display transactions
        self.alert_list = QListWidget()
        self.alert_list.setStyleSheet("background-color: balck; color: white; padding: 10px; border-radius: 10px; font-size: 11pt")
        self.widget_layout.addWidget(self.alert_list)

    # Load previous transactions from the database
        self.load_alert()

    def load_alert(self):
    # Clear the current transaction list
        self.alert_list.clear()

    # Fetch transactions from the database
        cursor = self.db.cursor()
        cursor.execute("SELECT created_at, message FROM alertdb  WHERE Email = %s ORDER BY created_at DESC LIMIT 5" , (self.current_user_email,))
        alerts = cursor.fetchall()
        cursor.close()

    # Add transactions to the transaction list
        if not alerts:
            no_alerts_item = QListWidgetItem("No alerts to display.")
            no_alerts_item.setForeground(QtGui.QColor("white"))
            self.alert_list.addItem(no_alerts_item)
            return
         # Add alerts to the alert list
        for alert in alerts:
            created_at, message = alert
            item_text = f"{created_at} - {message}"
            item = QListWidgetItem(item_text)

        # Check if the alert is new (within the last 24 hours)
            if (datetime.now() - created_at).days < 1:
                item.setForeground(QtGui.QColor("red"))  # New messages in red
            else:
                item.setForeground(QtGui.QColor("white"))  # Old messages in white

            self.alert_list.addItem(item)

    def transactions(self):
        self.transaction_widget = QWidget()
        self.transaction_widget.setGeometry(50, 150, 800, 400)
        self.transaction_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.transaction_widget.setParent(self.home_widget)


        self.widget_layout =QVBoxLayout(self.transaction_widget)

        transaction_title = QLabel("Transactions")
        transaction_title.setFont(QFont("Arial", 16, QFont.Bold))
        transaction_title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(transaction_title)

        # Create QListWidget to display transactions
        self.transaction_list = QListWidget()
        self.transaction_list.setStyleSheet("background-color: balck; color: white; padding: 10px; border-radius: 10px; font-size: 14pt")
        self.widget_layout.addWidget(self.transaction_list)

    # Load previous transactions from the database
        self.load_transactions()

    def load_transactions(self):
    # Clear the current transaction list
        self.transaction_list.clear()

    # Fetch transactions from the database
        cursor = self.db.cursor()
        cursor.execute("SELECT Date, From_Account, To_Account, Debit, Credit, Transaction_ID, Type_  FROM transactionsdb  WHERE Email = %s ORDER BY Date DESC LIMIT 5" , (self.current_user_email,))
        transactions = cursor.fetchall()
        cursor.close()

        if not transactions:
            no_transactions_item = QListWidgetItem("No transactions to display.")
            no_transactions_item.setForeground(QtGui.QColor("white"))
            self.transaction_list.addItem(no_transactions_item)
            return

    # Add transactions to the transaction list
        for transaction in transactions:
                date, from_account, to_account, debit, credit, transaction_id, type_ = transaction
                item_text = f"{date} - {from_account} to {to_account}: {debit if debit else credit} ({type_})"
                item = QListWidgetItem(item_text)

                # Check if the transaction is new (within the last 24 hours)
                if (datetime.now() - date).days < 1:
                    item.setForeground(QtGui.QColor("red"))  # New transactions in red
                else:
                    item.setForeground(QtGui.QColor("white"))  # Old transactions in white

                self.transaction_list.addItem(item)
  


        
    def user_info(self):
        mobile_number = self.phone_number
        Firstname = self.first_name 
        Lastname = self.last_name

    # Create the main widget for user info
        self.user_info_widget = QWidget()
        self.user_info_widget.setGeometry(900, 480, 350, 300)
        self.user_info_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.user_info_widget.setParent(self.home_widget)

    # Layout for user info widget
        self.widget_layout = QVBoxLayout(self.user_info_widget)

    # User info label
        user_info_label = QLabel("User Info")
        user_info_label.setFont(QFont("Arial", 16, QFont.Bold))
        user_info_label.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(user_info_label)

    # Check if the user has a PIN
        cursor = self.db.cursor()
        cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
        result = cursor.fetchone()
        cursor.close()

    # Determine which set of labels to use based on whether the PIN is set
        if result and result[0]:  # PIN is not empty
            info_labels = [
            ("Email:", self.current_user_email),
            ("Wallet:", "Activated"),
            ("First Name:", Firstname),
            ("Last Name:", Lastname),
            ("Mobile Number:", mobile_number)
            ]
        else:
            info_labels = [
            ("Email:", self.current_user_email),
            ("Wallet:", "NOT Activated"),
            ("First Name:", Firstname),
            ("Last Name:", Lastname),
            ("Mobile Number:", mobile_number)
        ]

    # Add the labels to the layout
        for label_text, value in info_labels:
            hbox = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setFont(QFont("Arial", 12, QFont.Bold))
            lbl.setStyleSheet("color: white;")
            hbox.addWidget(lbl)

            val = QLabel(value)
            val.setFont(QFont("Arial", 12))
            val.setStyleSheet("color: white;")
            hbox.addWidget(val)

            self.widget_layout.addLayout(hbox)

        return self.user_info_widget

        
    def setCircularIcon(self, label, icon_path, size=80, position=(10, 10)):
        pixmap = QPixmap(icon_path).scaled(QSize(size, size), Qt.KeepAspectRatio)
        rounded_pixmap = QPixmap(pixmap.size())
        rounded_pixmap.fill(Qt.transparent)

        # Create a circular mask
        mask = QPainter(rounded_pixmap)
        mask.setBrush(QBrush(Qt.black))
        mask.setPen(QPen(Qt.transparent))
        mask.drawEllipse(0, 0, size, size)
        mask.setCompositionMode(QPainter.CompositionMode_SourceIn)
        mask.drawPixmap(0, 0, pixmap)
        mask.end()

        label.setPixmap(rounded_pixmap)
        label.setFixedSize(size, size)
        label.move(position[0], position[1])  # Set the position
        label.setScaledContents(True)

    def closeEvent(self, event):

           
        event.accept()
           

    def open_main_window(self):

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return

            cursor = self.db.cursor()
            logout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Update the login_logs table with logout time
            sql = "UPDATE login_logs SET logout_time = %s WHERE Email = %s AND logout_time IS NULL"
            cursor.execute(sql, (logout_time, self.current_user_email))
            self.db.commit()
            cursor.close()

            QMessageBox.information(self, "Logout", "You have been logged out successfully.")
             # Create and show the MainWindow instance
            self.main_window = MainWindow()
            self.main_window.show()

        # Set the is_logging_out flag to True
            
            # Close the Main1Window after logout
            self.close()
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
            print(e)

        self.main_window = MainWindow()
        self.main_window.show()
        self.close()   

  

    def account_page(self):
        account_widget =QWidget()
        account_label = QLabel("<html><p> My Account <p></html>", account_widget)
        account_label.setGeometry(350, 50, 600 , 80)
        account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        account_label.setAlignment(Qt.AlignCenter)



        check_balance_button = QPushButton(self)
        check_balance_button.setGeometry(50, 200, 500, 50)
        icon = QIcon("money.png")                  
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        check_balance_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        check_balance_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("financial.png")
        check_balance_button.setIcon(icon)

# Set the text for the button
        check_balance_button.setText(" | Check Balance")

        check_balance_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))

        check_balance_button.setParent(account_widget)

        self.stacked_widget.addWidget(account_widget)

        #Mini statement Button

        mini_statement_button = QPushButton(self)
        mini_statement_button.setGeometry(50, 280, 500, 50)
                     
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        mini_statement_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        mini_statement_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("tax.png")
        mini_statement_button.setIcon(icon)

# Set the text for the button
        mini_statement_button.setText(" | Mini Statement-All Transactions")

        mini_statement_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(10))

        mini_statement_button.setParent(account_widget)

        self.stacked_widget.addWidget(account_widget)


    def check_balance_page(self):
        balance_widget = QWidget()
       
        balance_label = QLabel("<html><p>Balance Enquiry<p></>", balance_widget)
        balance_label.setGeometry(350,50,600,80)
        balance_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        balance_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)

        self.source_account_label = QLabel('<U> Select source Account</>',balance_widget)
        self.source_account_label.setGeometry(50, 180, 600, 80)
        self.source_account_label.setStyleSheet("background-color: transparent; color: white; padding: 20px; border-radius: 40px; font-size: 20pt;")
        self.source_account_label.setParent(balance_widget)



        
      
        my_account_button = QPushButton(self)
        my_account_button.setGeometry(50, 250, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        my_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        my_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("financial.png")
        my_account_button.setIcon(icon)

# Set the text for the button
        my_account_button.setText(" | My Wallet")

        my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(22))

        my_account_button.setParent(balance_widget)


        
        susu_account_button = QPushButton(self)
        susu_account_button.setGeometry(50, 330, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        susu_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        susu_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("financial.png")
        susu_account_button.setIcon(icon)

# Set the text for the button
        susu_account_button.setText(" | Susu Account")

        susu_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(34))

        susu_account_button.setParent(balance_widget)


        
        saving_balance_button = QPushButton(self)
        saving_balance_button.setGeometry(50, 410, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        saving_balance_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        saving_balance_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("financial.png")
        saving_balance_button.setIcon(icon)

# Set the text for the button
        saving_balance_button.setText(" | Saving Account")

        saving_balance_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(25))

        saving_balance_button.setParent(balance_widget)

        
        loan_account_button = QPushButton(self)
        loan_account_button.setGeometry(50, 490, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        loan_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        loan_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("financial.png")
        loan_account_button.setIcon(icon)

# Set the text for the button
        loan_account_button.setText(" | Loan Account ")

      #  my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))

        loan_account_button.setParent(balance_widget)




       

        self.stacked_widget.addWidget(balance_widget)  

    def personal_susu_account(self):
        personal_susu_account__widget = QWidget()
       
        personal_susu_account_label = QLabel("<html><p>Susu Balance Enquiry<p></>", personal_susu_account__widget)
        personal_susu_account_label.setGeometry(350,50,600,80)
        personal_susu_account_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        personal_susu_account_label.setAlignment(Qt.AlignCenter)

        
        self.susu_acc_label = QLabel("<html><p>Gh¢ ×.×× <p></>", personal_susu_account__widget)
        self.susu_acc_label.setGeometry(900,180,300,300)
        self.susu_acc_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        self.susu_acc_label.setAlignment(Qt.AlignCenter)
        self.susu_acc_label.hide()
        self.susu_acc_label.setParent(personal_susu_account__widget)


         # Create a line edit for password input field
        self.susu_pin_input = QLineEdit(self)
        susu_input_width = 350
        susu_input_x = (self.width() - susu_input_width) // 9
        self.susu_pin_input.setGeometry(susu_input_x, 200, susu_input_width, 50)
        # Set placeholder text for the password input field
        self.susu_pin_input.setPlaceholderText("Enter Pin")
        # Appply styling to the password input field
        self.susu_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.susu_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.susu_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.susu_pin_input.setEchoMode(QLineEdit.Password)
      #  self.pin_input.textChanged.connect(self.validate_pin)
        self.susu_pin_input.editingFinished.connect(self.reset_susu_pin_input_style)
        self.susu_pin_input.setParent(personal_susu_account__widget)
        


        # Create checkbox to toggle password visibility
        self.show_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        box_width = 150
        box_x = (self.width() - box_width) // 10
        self.show_pin_checkbox.setGeometry(box_x, 247, box_width , 30)
        self.show_pin_checkbox.stateChanged.connect(self.toggle_susu_pin_visibility)

        self.show_pin_checkbox.setParent(personal_susu_account__widget)




        
        self.check_button = QPushButton("Check Balance", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 8  # Center the button horizontally
        self.check_button.setGeometry(button_x, 320, button_width, 70)
        self.check_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.check_button.clicked.connect(self.check_my_susu_balance)
        self.check_button.setParent(personal_susu_account__widget)


        self.stacked_widget.addWidget(personal_susu_account__widget)

    def check_my_susu_balance(self):
        self.check_susu_pin_and_activate()
        



            
    def check_susu_pin_and_activate(self):
         # Check if the user's account is activated by checking if the PIN is set
        cursor = self.db.cursor()
        email = self.current_user_email  # Assuming you have stored the current user's email
        cursor.execute("SELECT Pin FROM susu_account WHERE Email = %s", (email,))
        result = cursor.fetchone()
        

        if result and result[0]:  # PIN exists and is not empty
            # Account is activated, proceed to verify PIN
            self.verify_susu_pin()
        else:
            # Account is not activated (PIN is empty), show appropriate message
            QMessageBox.warning(self, "Account Not Activated", "Please join a susu group to activate your account.")


    def verify_susu_pin(self):

        susu_pin = self.susu_pin_input.text()
        email = self.current_user_email
        

        if susu_pin == "" :
            QMessageBox.information(self, "Pin field is empty", "Please Enter Pin")
            return



        try:
            susu_pin = self.susu_pin_input.text()
            susu_PIN = self.sha512_64_hash(susu_pin) 
            cursor = self.db.cursor()
            
            
            cursor.execute("SELECT Balance FROM susu_account WHERE Email = %s AND Pin = %s", (email, susu_PIN))
            result = cursor.fetchone()

            if result:
                balance = result[0]
                self.susu_acc_label.setText(f"Gh¢{balance}.")
                self.susu_acc_label.show()
                
            else:
                QMessageBox.warning(self, "Incorrect PIN", "Please enter the correct PIN.")

            cursor.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unable to fetch account balance: {e}")

    

    def myaccount_page(self, db, current_user_email):
        self.current_user_email = current_user_email
        self.db = db

        mybalance_widget = QWidget()
       
        mybalance_label = QLabel("<html><p>Balance Enquiry<p></>", mybalance_widget)
        mybalance_label.setGeometry(350,50,600,80)
        mybalance_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        mybalance_label.setAlignment(Qt.AlignCenter)


        
       
        self.acc_label = QLabel("<html><p>Gh¢ ×.×× <p></>", mybalance_widget)
        self.acc_label.setGeometry(900,180,300,300)
        self.acc_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        self.acc_label.setAlignment(Qt.AlignCenter)
        self.acc_label.hide()
        self.acc_label.setParent(mybalance_widget)


         # Create a line edit for password input field
        self.pin_input = QLineEdit(self)
        input_width = 350
        input_x = (self.width() - input_width) // 9
        self.pin_input.setGeometry(input_x, 200, input_width, 50)
        # Set placeholder text for the password input field
        self.pin_input.setPlaceholderText("Enter Pin")
        # Appply styling to the password input field
        self.pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.pin_input.setEchoMode(QLineEdit.Password)
      #  self.pin_input.textChanged.connect(self.validate_pin)
        self.pin_input.editingFinished.connect(self.reset_pin_input_style)
        self.pin_input.setParent(mybalance_widget)
        print(input_x)


        # Create checkbox to toggle password visibility
        self.show_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        box_width = 150
        box_x = (self.width() - box_width) // 10
        self.show_pin_checkbox.setGeometry(box_x, 247, box_width , 30)
        self.show_pin_checkbox.stateChanged.connect(self.toggle_pin_visibility)

        self.show_pin_checkbox.setParent(mybalance_widget)


        self.forgot_pin_button = QPushButton("forgot Pin ?", self)
        button_width2 = 300
        button_z = (self.width() - button_width2) //4
        self.forgot_pin_button.setGeometry (button_z, 247, button_width2 ,30)
        self.forgot_pin_button.setStyleSheet("""
                             QPushButton {
                             background-color: transparent;
                             border:none;
                              font-size: 16px; 
                              border-radius: 35px;
                              color: black;
                              }
                               QPushButton:hover{
                                  font-size: 15pt;
                              }
                          """)
        self.forgot_pin_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(35))
        self.forgot_pin_button.setParent(mybalance_widget)



        
        self.check_button = QPushButton("Check Balance", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 8  # Center the button horizontally
        self.check_button.setGeometry(button_x, 320, button_width, 70)
        self.check_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.check_button.clicked.connect(self.check_my_balance)
        self.check_button.setParent(mybalance_widget)


    # Button for "Create Account"
        self.activate_acc_button = QPushButton("Have You Activated Your Account ?", self)
        button_width1 = 600  # Adjust the width of the button as needed
        button_y = (self.width() - button_width) //1200 # Center the button horizontally
        self.activate_acc_button.setGeometry(button_y, 400, button_width1, 70)
        self.activate_acc_button.setStyleSheet("""
                      QPushButton {
                      background-color: transparent;
                      border:none;
                       font-size: 14pt; 
                       border-radius: 35px;
                       color: black;
                       }
                        QPushButton:hover{
                           font-size: 20pt;
                       }
                   """)
        self.activate_acc_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(23))
        self.activate_acc_button.setParent(mybalance_widget)
        print(self.width())
        print(button_x)


        
        self.stacked_widget.addWidget(mybalance_widget)

    def forgot_pin(self):    

        forgot_pin_widget = QWidget()
       
        forgot_pin_label = QLabel("<html><p>Forgot Pin Page<p></>", forgot_pin_widget)
        forgot_pin_label.setGeometry(350,50,600,80)
        forgot_pin_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        forgot_pin_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)

       
        # Create a line edit for the email input field
        self.email_input_for_forgot_pin = QLineEdit(self)
        self.email_input_for_forgot_pin.setGeometry(50, 200, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.email_input_for_forgot_pin.setPlaceholderText(" Enter Current Email ")
        # Apply styling to the email input field
        self.email_input_for_forgot_pin.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.email_input_for_forgot_pin.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        self.email_input_for_forgot_pin.addAction(icon, QLineEdit.LeadingPosition)

        # Connect textChanged signal to validate_email slot
        self.email_input_for_forgot_pin.textChanged.connect(self.validate_email_input_for_forgot_pin_style)
        self.email_input_for_forgot_pin.editingFinished.connect(self.reset_email_input_for_forgot_pin_style)
        self.email_input_for_forgot_pin.setParent(forgot_pin_widget)

         # Create a line edit for password input field
        self.forgot_pin_input = QLineEdit(self)
        self.forgot_pin_input.setGeometry(50, 280, 350, 50)
        # Set placeholder text for the password input field
        self.forgot_pin_input.setPlaceholderText("Enter New Pin")
        # Appply styling to the password input field
        self.forgot_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.forgot_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.forgot_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.forgot_pin_input.setEchoMode(QLineEdit.Password)
        self.forgot_pin_input.textChanged.connect(self.validate_forgot_pin)
        self.forgot_pin_input.editingFinished.connect(self.reset_forgot_pin_input_style)
        self.forgot_pin_input.setParent(forgot_pin_widget)


        # Create checkbox to toggle password visibility
        self.forgot_pin_checkbox = QCheckBox("Show Pin", self)
        self.forgot_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.forgot_pin_checkbox.setGeometry(50, 327, 150 , 30)
        self.forgot_pin_checkbox.stateChanged.connect(self.toggle_forgot_pin_visibility)

        self.forgot_pin_checkbox.setParent(forgot_pin_widget)


            # Create a line edit for password input field
        self.confirm_forgot_pin_input = QLineEdit(self)
        self.confirm_forgot_pin_input.setGeometry(50, 380, 350, 50)
        # Set placeholder text for the password input field
        self.confirm_forgot_pin_input.setPlaceholderText("Confirm New Pin")
        # Appply styling to the password input field
        self.confirm_forgot_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.confirm_forgot_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.confirm_forgot_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_forgot_pin_input.setEchoMode(QLineEdit.Password)
        self.confirm_forgot_pin_input.textChanged.connect(self.validate_confirm_forgot_pin)
        self.confirm_forgot_pin_input.editingFinished.connect(self.reset_confirm_forgot_pin_input_style)
        self.confirm_forgot_pin_input.setParent(forgot_pin_widget)


        # Create checkbox to toggle password visibility
        self.show_confirm_forgot_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_confirm_forgot_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_confirm_forgot_pin_checkbox.setGeometry(40, 427, 150 , 30)
        self.show_confirm_forgot_pin_checkbox.stateChanged.connect(self.toggle_confirm_forgot_pin_visibility)

        self.show_confirm_forgot_pin_checkbox.setParent(forgot_pin_widget)

          # Create QLabel for notification messages
        self.forgot_pin_notification_label = QLabel("", self)
        self.forgot_pin_notification_label.setGeometry(50, 480, 600, 50)
        self.forgot_pin_notification_label.setStyleSheet("color: red; font-size: 25px;")
        self.forgot_pin_notification_label.setParent(forgot_pin_widget)



        self.forgot_pin_save_and_submit_button = QPushButton("Save and Submit", self)
        forgot_button_width = 300  # Adjust the width of the button as needed
        forgot_button_x = (self.width() - forgot_button_width) // 3  # Center the button horizontally
        self.forgot_pin_save_and_submit_button.setGeometry(forgot_button_x, 600, forgot_button_width, 70)
        self.forgot_pin_save_and_submit_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.forgot_pin_save_and_submit_button.clicked.connect(self.forgot_pin_save_and_submit)
        self.forgot_pin_save_and_submit_button.setParent(forgot_pin_widget)

        self.regenerate_otp_for_forgot_pin_button = QPushButton(self)
        self.regenerate_otp_for_forgot_pin_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.regenerate_otp_for_forgot_pin_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.regenerate_otp_for_forgot_pin_button.setGeometry(410, 340, 40, 40)
        self.regenerate_otp_for_forgot_pin_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.regenerate_otp_for_forgot_pin_button.hide()
        self.regenerate_otp_for_forgot_pin_button.clicked.connect(self.generate_otp6)  # Connect the clicked signal
        self.regenerate_otp_for_forgot_pin_button.setParent(forgot_pin_widget)
        
     

        self.otp_generated6 = False
        self.otp6 = ""

        #Create a QLabel for the information display 
        self.info_label6_widget = QWidget()
        self.info_label6 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label6_widget)
        self.info_label6.setAlignment(Qt.AlignCenter)
        self.info_label6.setGeometry(50,200,400,40)
        self.info_label6.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label6.hide() # Hide the info label initially
        self.info_label6.setParent(forgot_pin_widget)
        

        #create a container widget for the otp input
        self.container6 = QWidget()
        self.container6.setGeometry(50,240,400,100)
        self.container6.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container6.hide()
        self.container6.setParent(forgot_pin_widget)
        

        # Create a QVBoxLayout for the container
        self.container_layout6 = QVBoxLayout(self.container6)
        self.container_layout6.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp6_boxes = []
        for _ in range(6):
            otp6_box = QLineEdit(self.container6)
            otp6_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp6_box.setMaxLength(1)  # Limit input to one character
            otp6_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp6_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp6_box)
            self.otp6_boxes.append(otp6_box)
             # Connect textChanged signal to handle_otp_input slot
            otp6_box.textChanged.connect(self.handle_otp_input6)


        self.container_layout6.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        # Create a QLabel for time remaining display (initially hidden)
        self.timer_label6_widget = QWidget()
        self.timer_label6 = QLabel("<html><p>Time remaining....180 seconds<p></html> ", self.timer_label6_widget)
        self.timer_label6.setAlignment(Qt.AlignCenter)
        self.timer_label6.setGeometry(50,340,360,40)
        self.timer_label6.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label6.hide()
        self.timer_label6.setParent(forgot_pin_widget)

        self.stacked_widget.addWidget(forgot_pin_widget) 

    def handle_otp_input6(self, text):
        current_box = self.sender()  # Get the sender QLineEdit
        index = self.otp6_boxes.index(current_box)
        if len(text) == 1 and index < len(self.otp6_boxes) - 1:
            self.otp6_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp6_boxes) - 1:
            self.check_otp6()

    

    def update_timer6(self):
        self.time_left -= 1
        self.timer_label6.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input6()
            self.otp_generated6
            self.otp_generated6 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
    
    
    def start_timer6(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer6)
        self.timer.start(1000)  # Update timer every second
          
                   

    def forgot_pin_save_and_submit(self):

        email = self.email_input_for_forgot_pin.text()
        new_pin = self.forgot_pin_input.text()
        confirm_pin = self.confirm_forgot_pin_input.text()
        entered_otp = self.otp6



        if email != self.current_user_email :
            self.forgot_pin_notification_label.setText("Please Current Email do not match")
            self.forgot_pin_notification_label.show()
            return
        
        if len(new_pin) != 4:
            QMessageBox.warning(self, "Invalid PIN", "Confirmation PIN must be exactly 4 digits.")
            return
        
        if new_pin== "":
            self.forgot_pin_notification_label.setText("Please Enter Your New Pin")
            self.forgot_pin_notification_label.show()
            return
        
        if confirm_pin == " ":
            self.forgot_pin_notification_label.setText("Please Confirm Your Pin")
            self.forgot_pin_notification_label.show()
            return
        
        if new_pin != confirm_pin :
            self.forgot_pin_notification_label.setText("Please  Pin do not match")
            self.forgot_pin_notification_label.show()
            return
        
        
        if entered_otp =="":
            self.generate_otp6()
            self.email_input_for_forgot_pin.hide()
            
            self.forgot_pin_input.hide()
            self.confirm_forgot_pin_input.hide()
            
            
            self.forgot_pin_checkbox.hide()
            self.show_confirm_forgot_pin_checkbox.hide()
            
            
            
            self.otp_generated6 = True
            
            self.info_label6.show()
            self.container6.show()
            self.timer_label6.show()
            self.regenerate_otp_for_forgot_pin_button.show()
            self.forgot_pin_notification_label.setText("")
            self.start_timer6()
        self.forgot_pin_notification_label.hide()

    def update_database6(self):
        email = self.email_input_for_forgot_pin.text()
        new_pin = self.forgot_pin_input.text()
        hash_password = self.sha512_64_hash(new_pin) 
        message = " Your Pin has been changed"
        try:
            if self.db is None:
                return
            
            #Create Cursor:
            cursor = self.db.cursor()
            
            
            # Execute SELECT query to check login credentials
            sql = "UPDATE my_accountdb SET PIN = %s WHERE Email = %s"
            cursor.execute(sql, ( hash_password, email))

            self.db.commit()
            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message, self.current_user_email,))
            self.db.commit()
            
            self.load_alert()

            sql = "UPDATE susu_account SET Pin = %s WHERE Email = %s"
            cursor.execute(sql, ( hash_password, email))

            cursor.close()


            QMessageBox.information(self, "Pin Changed", "You have successfully changed your Pin.")
            self.email_input_for_forgot_pin.clear()
            self.forgot_pin_input.clear()
            self.confirm_forgot_pin_input.clear()
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
      

    def generate_otp6(self):
        email = self.email_input_for_forgot_pin.text()
        self.otp6 = str(random.randint(100000, 999999))
        QMessageBox.information(self,"OTP", f"Sending OTP to {email}")
        QMessageBox.information(self,"OTP", f"""Your Verification code: {self.otp6}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Pin""")
        

        
        self.start_timer6()

   

    def clear_otp_input6(self):
        for otp_box in self.otp6_boxes:
            otp_box.clear()  

    def check_otp6(self):
        entered_otp = "".join(box.text() for box in self.otp6_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input6()
           self.otp_generated6 = False
           return
           
        if entered_otp == self.otp6:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input6()
            
            self.info_label6.hide()
            self.container6.hide()
            self.timer_label6.hide()
            self.regenerate_otp_for_forgot_pin_button.hide()
            self.email_input_for_forgot_pin.show()
            self.forgot_pin_input.show()
            self.forgot_pin_checkbox.show()
            self.show_confirm_forgot_pin_checkbox.show()
            self.confirm_forgot_pin_input.show()
            
            self.timer.stop() 

            self.update_database6()
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input6()
            self.otp_generated6 = False  
        



    def validate_email_input_for_forgot_pin_style(self, text):
        # Regular expression pattern for validating email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern)

        # Use match method to check if the input text matches the pattern
        if regex.match(text):
            # Valid email format
            self.email_input_for_forgot_pin.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.email_input_for_forgot_pin.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.email_input_for_forgot_pin.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.email_input_for_forgot_pin.setFont(font)




    @pyqtSlot()
    def reset_email_input_for_forgot_pin_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.email_input_for_forgot_pin.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
    


    def validate_forgot_pin(self,text):
        forgot_pin_pattern = r'^[0-9]{4}$'  # Assuming a 10-digit phone number

        forgot_pin_regex = re.compile(forgot_pin_pattern)

        if forgot_pin_regex.match(text):
            # Valid email format
            self.forgot_pin_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.forgot_pin_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.forgot_pin_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.forgot_pin_input.setFont(font)  
            
    def validate_confirm_forgot_pin(self,text):
            confirm_forgot_pin_pattern = r'^[0-9]{4}$'  # Assuming a 10-digit phone number

            confirm_forgot_pin_regex = re.compile(confirm_forgot_pin_pattern)

            if confirm_forgot_pin_regex.match(text):
            # Valid email format
                self.confirm_forgot_pin_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
            else:
            # Invalid email format
                self.confirm_forgot_pin_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
                font = self.confirm_forgot_pin_input.font()
                font.setPointSize(10)  # Adjust the font size as needed
                self.confirm_forgot_pin_input.setFont(font)   



    def toggle_forgot_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.forgot_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.forgot_pin_input.setEchoMode(QLineEdit.Password) 

    def toggle_confirm_forgot_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.confirm_forgot_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.confirm_forgot_pin_input.setEchoMode(QLineEdit.Password)

    
            
            

    @pyqtSlot()
    def reset_forgot_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.forgot_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
       
    @pyqtSlot()
    def reset_confirm_forgot_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.confirm_forgot_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
                  

   

    def check_my_balance(self):
        self.check_pin_and_activate()
        



            
    def check_pin_and_activate(self):
         # Check if the user's account is activated by checking if the PIN is set
        cursor = self.db.cursor()
        email = self.current_user_email  # Assuming you have stored the current user's email
        cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()

        if result and result[0]:  # PIN exists and is not empty
            # Account is activated, proceed to verify PIN
            self.verify_pin()
        else:
            # Account is not activated (PIN is empty), show appropriate message
            QMessageBox.warning(self, "Account Not Activated", "Please set a PIN to activate your account.")


    def verify_pin(self):

        pin = self.pin_input.text()
        email = self.current_user_email
        

        if pin == "" :
            QMessageBox.information(self, "Pin field is empty", "Please Enter Pin")
            return


        

       
        try:
            pin = self.pin_input.text()
            PIN = self.sha512_64_hash(pin) 
            cursor = self.db.cursor()
            
            
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s AND PIN = %s", (email, PIN))
            result = cursor.fetchone()

            if result:
                balance = result[0]
                self.acc_label.setText(f"Gh¢{balance}.")
                self.acc_label.show()
                
            else:
                QMessageBox.warning(self, "Incorrect PIN", "Please enter the correct PIN.")

            cursor.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unable to fetch account balance: {e}")





    def create_pin_page(self, db, current_user_email):
        self.current_user_email = current_user_email
        self.db = db

        create_pin_widget = QWidget()
       
        create_pin_label = QLabel("<html><p>Create New Pin To Activate Account<p></>", create_pin_widget)
        create_pin_label.setGeometry(350,50,600,80)
        create_pin_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        create_pin_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)

         # Create a line edit for password input field
        self.new_pin_input = QLineEdit(self)
        self.new_pin_input.setGeometry(50, 200, 350, 50)
        # Set placeholder text for the password input field
        self.new_pin_input.setPlaceholderText("Enter New Pin")
        # Appply styling to the password input field
        self.new_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.new_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.new_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.new_pin_input.setEchoMode(QLineEdit.Password)
        self.new_pin_input.textChanged.connect(self.validate_new_pin)
        self.new_pin_input.editingFinished.connect(self.reset_new_pin_input_style)
        self.new_pin_input.setParent(create_pin_widget)


        # Create checkbox to toggle password visibility
        self.show_new_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_new_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_new_pin_checkbox.setGeometry(40, 247, 150 , 30)
        self.show_new_pin_checkbox.stateChanged.connect(self.toggle_new_pin_visibility)

        self.show_new_pin_checkbox.setParent(create_pin_widget)


            # Create a line edit for password input field
        self.confirm_new_pin_input = QLineEdit(self)
        self.confirm_new_pin_input.setGeometry(50, 300, 350, 50)
        # Set placeholder text for the password input field
        self.confirm_new_pin_input.setPlaceholderText("Confirm New Pin")
        # Appply styling to the password input field
        self.confirm_new_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.confirm_new_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.confirm_new_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_new_pin_input.setEchoMode(QLineEdit.Password)
        self.confirm_new_pin_input.textChanged.connect(self.validate_confirm_pin)
        self.confirm_new_pin_input.editingFinished.connect(self.reset_confirm_new_pin_input_style)
        self.confirm_new_pin_input.setParent(create_pin_widget)


        # Create checkbox to toggle password visibility
        self.show_confirm_new_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_confirm_new_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_confirm_new_pin_checkbox.setGeometry(40, 347, 150 , 30)
        self.show_confirm_new_pin_checkbox.stateChanged.connect(self.toggle_confirm_new_pin_visibility)

        self.show_confirm_new_pin_checkbox.setParent(create_pin_widget)

          # Create QLabel for notification messages
        self.notification_label4 = QLabel("", self)
        self.notification_label4.setGeometry(50, 440, 600, 50)
        self.notification_label4.setStyleSheet("color: red; font-size: 25px;")
        self.notification_label4.setParent(create_pin_widget)



        self.pin_save_and_submit_button = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 3  # Center the button horizontally
        self.pin_save_and_submit_button.setGeometry(button_x, 700, button_width, 70)
        self.pin_save_and_submit_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.pin_save_and_submit_button.clicked.connect(self.pin_save_and_submit)
        self.pin_save_and_submit_button.setParent(create_pin_widget)
        self.stacked_widget.addWidget(create_pin_widget) 



    def pin_save_and_submit(self):
       
        self.check_pin_empty()




    def check_pin_empty(self):
        email = self.current_user_email  # Assuming you have stored the current user's email
        
        # Fetch the current PIN from the database
        cursor = self.db.cursor()
        cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()

        if result and result[0]:  # PIN is not empty
            QMessageBox.information(self, "PIN Already Set", "Your PIN is already set.")
        else:
            # Prompt the user to set a new PIN
            self.update_pin_data() 

    def update_pin_data(self):    
        email = self.current_user_email

        new_pin = self.new_pin_input.text()
        confirm_pin = self.confirm_new_pin_input.text()

        hash_new_pin = self.sha512_64_hash(new_pin)
        


        if new_pin == "" :
            self.notification_label4.setText("Please Enter New Pin")
            self.notification_label4.show()
            return
        
        if len(new_pin) != 4:
            QMessageBox.warning(self, "Invalid PIN", "PIN must be exactly 4 digits.")
            return
        
        if confirm_pin == "" :
            self.notification_label4.setText("Please Confirm  Pin")
            self.notification_label4.show()
            return
        
        if len(confirm_pin) != 4:
            QMessageBox.warning(self, "Invalid PIN", "Confirmation PIN must be exactly 4 digits.")
            return

        
        if new_pin != confirm_pin :
            self.notification_label4.setText("New Pin and Confirm Pin do not Macth")
            self.notification_label4.show()
            return
        
        self.notification_label4.hide()

        try:
             
             if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
             cursor = self.db.cursor()
             message = "Congratulations, you've successfully activated your wallet"
             new_pin = self.new_pin_input.text()
             hash_new_pin = self.sha512_64_hash(new_pin)
             


           

             sql = "UPDATE my_accountdb SET PIN = %s WHERE Email = %s"
             cursor.execute(sql, (hash_new_pin, email))
             print(hash_new_pin + " Update pin its still the created pin")
                                
             self.db.commit()
             sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
             cursor.execute(sql, (message, self.current_user_email,))
             self.db.commit()
             cursor.close()
             self.load_alert()
            
             QMessageBox.information(self, "Pin Set", "You have successfully Activated Your Account")
             self.main_window = MainWindow()
             self.main_window.show()
             self.close() 
               
             
       
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
    
        
    def validate_new_pin(self,text):
        new_pin_pattern = r'^[0-9]{4}$'  # Assuming a 10-digit phone number

        new_pin_regex = re.compile(new_pin_pattern)

        if new_pin_regex.match(text):
            # Valid email format
            self.new_pin_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.new_pin_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.new_pin_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.new_pin_input.setFont(font)  
            
    def validate_confirm_pin(self,text):
            confirm_pin_pattern = r'^[0-9]{4}$'  # Assuming a 10-digit phone number

            confirm_pin_regex = re.compile(confirm_pin_pattern)

            if confirm_pin_regex.match(text):
            # Valid email format
                self.confirm_new_pin_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
            else:
            # Invalid email format
                self.confirm_new_pin_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
                font = self.confirm_new_pin_input.font()
                font.setPointSize(10)  # Adjust the font size as needed
                self.confirm_new_pin_input.setFont(font)   

    def toggle_susu_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.susu_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.susu_pin_input.setEchoMode(QLineEdit.Password) 
    
    def toggle_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.pin_input.setEchoMode(QLineEdit.Password) 

    def toggle_new_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.new_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.new_pin_input.setEchoMode(QLineEdit.Password)

    def toggle_confirm_new_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.confirm_new_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.confirm_new_pin_input.setEchoMode(QLineEdit.Password)
                    
            
            

    @pyqtSlot()
    def reset_susu_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.susu_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
       
    @pyqtSlot()
    def reset_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
     
    @pyqtSlot()

    def reset_new_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.new_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
    
    @pyqtSlot()

    def reset_confirm_new_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.confirm_new_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
    

    
    
    
    
    def saving_balance_page(self, db, current_user_email):
        self.current_user_email = current_user_email
        self.db = db

        mysbalance_widget = QWidget()
       
        mysbalance_label = QLabel("<html><p>Savings Balance Enquiry<p></>", mysbalance_widget)
        mysbalance_label.setGeometry(350,50,600,80)
        mysbalance_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        mysbalance_label.setAlignment(Qt.AlignCenter)
        mysbalance_label.setParent(mysbalance_widget)


        
       
        self.sacc_label = QLabel("<html><p>Gh¢ ×.×× <p></>", mysbalance_widget)
        self.sacc_label.setGeometry(900,180,300,300)
        self.sacc_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        self.sacc_label.setAlignment(Qt.AlignCenter)
        self.sacc_label.hide()
        self.sacc_label.setParent(mysbalance_widget)


         # Create a line edit for password input field
        self.accountnum_input = QLineEdit(self)
        account_input_width = 350
        account_x = (self.width() - account_input_width) // 9
        self.accountnum_input.setGeometry(account_x, 200, account_input_width, 50)
        # Set placeholder text for the password input field
        self.accountnum_input.setPlaceholderText("Enter Account ID")
        # Appply styling to the password input field
        self.accountnum_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.accountnum_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.accountnum_input.addAction(icon, QLineEdit.LeadingPosition)
        
        self.accountnum_input.setParent(mysbalance_widget)

        self.check_sab_button = QPushButton("Check Balance", self)
        sab_button_width = 300  # Adjust the width of the button as needed
        sab_button_x = (self.width() - sab_button_width) // 8  # Center the button horizontally
        self.check_sab_button.setGeometry(sab_button_x, 320, sab_button_width, 70)
        self.check_sab_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.check_sab_button.clicked.connect(self.check_my_sabalance)
        self.check_sab_button.setParent(mysbalance_widget)

          # Create QLabel for notification messages
        self.saving_balance_notification_label = QLabel("", self)
        self.saving_balance_notification_label.setGeometry(50, 500, 600, 50)
        self.saving_balance_notification_label.setStyleSheet("color: red; font-size: 25px;")
        self.saving_balance_notification_label.setParent(mysbalance_widget)


                
# Inside your initialization method or where you create the widgets
        self.sab_regenerate_otp_button = QPushButton(self)
        self.sab_regenerate_otp_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.sab_regenerate_otp_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.sab_regenerate_otp_button.setGeometry(910, 335, 40, 40)
        self.sab_regenerate_otp_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.sab_regenerate_otp_button.hide()
        self.sab_regenerate_otp_button.clicked.connect(self.generate_otp4)  # Connect the clicked signal
        self.sab_regenerate_otp_button.setParent(mysbalance_widget)
        
     

        self.otp_generated4 = False
        self.otp4= ""

        #Create a QLabel for the information display 
        self.info_label4_widget = QWidget()
        self.info_label4 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label4_widget)
        self.info_label4.setAlignment(Qt.AlignCenter)
        self.info_label4.setGeometry(550,200,400,40)
        self.info_label4.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label4.hide() # Hide the info label initially
        self.info_label4.setParent(mysbalance_widget)

        #create a container widget for the otp input
        self.container4 = QWidget()
        self.container4.setGeometry(550,235,400,100)
        self.container4.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container4.hide()
        self.container4.setParent(mysbalance_widget)

        # Create a QVBoxLayout for the container
        self.container_layout4 = QVBoxLayout(self.container4)
        self.container_layout4.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp4_boxes = []
        for _ in range(6):
            otp4_box = QLineEdit(self.container4)
            otp4_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp4_box.setMaxLength(1)  # Limit input to one character
            otp4_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp4_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp4_box)
            self.otp4_boxes.append(otp4_box)
             # Connect textChanged signal to handle_otp_input slot
            otp4_box.textChanged.connect(self.handle_otp_input4)


        self.container_layout4.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label4_widget = QWidget()
        self.timer_label4 = QLabel("<html><p>Time remaining....60 seconds<p></html> ", self.timer_label4_widget)
        self.timer_label4.setAlignment(Qt.AlignCenter)
        self.timer_label4.setGeometry(550,335,360,40)
        self.timer_label4.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label4.hide()
        self.timer_label4.setParent(mysbalance_widget)




        self.stacked_widget.addWidget(mysbalance_widget)

        
    def handle_otp_input4(self, text):
        current_box4 = self.sender()  # Get the sender QLineEdit
        index = self.otp4_boxes.index(current_box4)
        if len(text) == 1 and index < len(self.otp4_boxes) - 1:
            self.otp4_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp4_boxes) - 1:
            self.check_otp4()
               

    def update_timer4(self):
        self.time_left -= 1
        self.timer_label4.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input4()
            self.otp_generated4
            self.otp_generated4 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
                



    


    def check_my_sabalance(self):

        account_number = self.accountnum_input.text()
    
        entered_otp = self.otp4 # Get the entered OTP
 
      

        if account_number == "":
            QMessageBox.information(self, "Account","Please Enter Account Number.")
            
            
            return
        
          # Reset UI and state for a new OTP process if OTP is already generated
        if self.otp_generated4:
            self.reset_ui_for_new_otp()
        self.calculate_and_update_balance() 


      

     

        if account_number != "" :
            self.generate_otp4()
            self.otp_generated4 = True
            self.info_label4.show()
            self.container4.show()
            self.timer_label4.show()
            self.sab_regenerate_otp_button.show()
            self.saving_balance_notification_label.setText("")
            self.accountnum_input.hide()
      
            self.start_timer4()
           
          

        self.saving_balance_notification_label.hide()
        
     
    def start_timer4(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer4)
        self.timer.start(1000)  # Update timer every 
        
    
    def update_database4(self):

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
            
            cursor = self.db.cursor()
            account_number = self.accountnum_input.text()
            
           
            cursor.execute("SELECT  Amount FROM saving_accountdb WHERE Account_ID = %s", (account_number,))
            result = cursor.fetchone()

            if result:
                Amount = result[0]
                self.sacc_label.setText(f"Gh¢ {Amount}")
                self.sacc_label.show()
            
            else:
                QMessageBox.warning(self, "Error", "Account not found")

                cursor.close() 
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
    
        
        
        
       
    def generate_otp4(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp4 = str(random.randint(100000, 999999))
        QMessageBox.information(self, "OTP", f"Sending OTP to {email}")
        QMessageBox.information(self,"OTP",f"""Your Verification code: {self.otp4}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully check your balance""")
        QMessageBox.information(self, "OTP", f"Sending OTP to {number}")
        QMessageBox.information(self,"OTP",f"""Your Verification code: {self.otp4}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully check your balance""") # Print the generated OTP
        self.start_timer4()

    def send_otp4(self,number):
        print(f"Sending OTP to {number}")    


    def clear_otp_input4(self):
        for otp_box in self.otp4_boxes:
            otp_box.clear()  

    def reset_ui_for_new_otp(self):
        self.otp_generated4 = False
        self.clear_otp_input4()
        self.info_label4.hide()
        self.container4.hide()
        self.timer_label4.hide()
        self.sab_regenerate_otp_button.hide()
        self.saving_balance_notification_label.hide()
        self.accountnum_input.clear()
        self.accountnum_input.show()
        self.sacc_label.hide()        

    def check_otp4(self):
        entered_otp = "".join(box.text() for box in self.otp4_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input4()
           self.otp_generated4 = False
           return
           
        if entered_otp == self.otp4:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input4()
            self.update_database4()
            self.info_label4.hide()
            self.container4.hide()
            self.timer_label4.hide()
            self.sab_regenerate_otp_button.hide()
            
            self.accountnum_input.show()
            self.timer.stop() 
            
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input4()
            self.otp_generated4 = False   

        
    def mini_statement_page(self):
        self.statement_widget = QWidget()
       
        statement_label = QLabel("<html><p>Mini Statement-All Transactions<p></>", self.statement_widget)
        statement_label.setGeometry(350,50,600,80)
        statement_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        statement_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)

        account_label = QLabel("Select Account:", self)
        account_label.setGeometry(50, 150, 200, 30)
        account_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        account_label.setParent(self.statement_widget)
    
        self.account_dropdown = QComboBox(self)
        self.account_dropdown.setGeometry(250, 150, 350, 40)
        self.account_dropdown.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 14px; font-weight: bold;")
        self.account_dropdown.setParent(self.statement_widget)
    
        from_date_label = QLabel("From Date:", self)
        from_date_label.setGeometry(50, 200, 200, 30)
        from_date_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        from_date_label.setParent(self.statement_widget)
    
        self.from_date_picker = QDateEdit(self)
        self.from_date_picker.setGeometry(250, 200, 200, 30)
        self.from_date_picker.setCalendarPopup(True)
        self.from_date_picker.setDate(QDate.currentDate().addMonths(-1))
        self.from_date_picker.setStyleSheet("font-size: 14pt; font-weight: bold; border-radius: 10px; padding: 5px;")
        self.from_date_picker.setParent(self.statement_widget)
    
        to_date_label = QLabel("To Date:", self)
        to_date_label.setGeometry(50, 250, 200, 30)
        to_date_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        to_date_label.setParent(self.statement_widget)
    
        self.to_date_picker = QDateEdit(self)
        self.to_date_picker.setGeometry(250, 250, 200, 30)
        self.to_date_picker.setCalendarPopup(True)
        self.to_date_picker.setDate(QDate.currentDate())
        self.to_date_picker.setStyleSheet("font-size: 14pt; font-weight: bold; border-radius: 10px; padding: 5px;")
        self.to_date_picker.setParent(self.statement_widget)
    
        self.statement_button = QPushButton("Generate Statement", self)
        statement_button_width = 300
        statement_button_x = (self.width() - statement_button_width) // 3
        self.statement_button.setGeometry(statement_button_x, 720 ,statement_button_width, 50)
        self.statement_button.setStyleSheet("""
                                        QPushButton {
                                             background-color: blue;
                                             font-size: 14pt;
                                             border-radius: 25px;
                                                    }
                                             QPushButton:hover {
                                             background-color: #333333;
                                                               }
                                         """)
        self.statement_button.clicked.connect(self.generate_statement)
        self.statement_button.setParent(self.statement_widget)

        self.mini_widget = QWidget()
        self.mini_widget.setGeometry(50, 300, 1000, 400)
        self.mini_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.mini_widget.setParent(self.statement_widget)


        self.widget_layout =QVBoxLayout(self.mini_widget)

        mini_title = QLabel("Mini Statement")
        mini_title.setFont(QFont("Arial", 16, QFont.Bold))
        mini_title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(mini_title)

    
        self.statement_text_area = QTextEdit(self)
        self.statement_text_area.setTextColor(QColor("white"))
        self.statement_text_area.setStyleSheet("border-radius: 10px; padding: 10px; font-size: 14px;")
        self.statement_text_area.setReadOnly(True)
        
        self.widget_layout.addWidget(self.statement_text_area)
        
    
        self.download_button = QPushButton("Download Statement", self)
        download_button_width = 300
        download_button_x = (self.width() - download_button_width) // 3
        self.download_button.setGeometry(download_button_x, 800, download_button_width, 50)
        self.download_button.setStyleSheet("""
                                        QPushButton {
                                             background-color: green;
                                             font-size: 14pt;
                                             border-radius: 25px;
                                                    }
                                             QPushButton:hover {
                                             background-color: #333333;
                                                               }
                                         """)
        self.download_button.clicked.connect(self.download_statement)
        self.download_button.setParent(self.statement_widget)

        self.stacked_widget.addWidget(self.statement_widget)
        self.load_user_accounts()

    
       

        self.stacked_widget.addWidget(self.statement_widget) 
    def load_user_accounts(self):
        try:
            cursor = self.db.cursor()
            #Query for saving accounts
            cursor.execute("SELECT Account_ID FROM saving_accountdb WHERE Email = %s", (self.current_user_email,))
            saving_accounts = cursor.fetchall()



              # Query for Wallet accounts
            cursor.execute("SELECT Phonenumber FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            wallet_accounts = cursor.fetchall()



        # Clear the dropdown before adding new items
            self.account_dropdown.clear()

            for account in saving_accounts:
                self.account_dropdown.addItem(f"Saving Account: {account[0]}")
        
            for account in wallet_accounts:
                self.account_dropdown.addItem(f"My Wallet: {account[0]}")
        except mysql.connector.Error as e:

            QMessageBox.critical(self, "Database Error", f"Error loading accounts: {e}")
        finally:
            cursor.close()    
            

    def generate_statement(self):
        account_id = self.account_dropdown.currentText().split(": ")[1]
        from_date = self.from_date_picker.date().toString("yyyy-MM-dd")
        to_date = self.to_date_picker.date().toString("yyyy-MM-dd")

        from_date_time = f"{from_date} 00:00:00"
        to_date_time = f"{to_date} 23:59:59"



        
        cursor = self.db.cursor()
        
        query = """
                SELECT Date, From_Account, To_Account, Debit, Credit, Transaction_ID, Type_
                FROM transactionsdb
                WHERE (From_Account_ID = %s OR To_Account_ID = %s) AND Date BETWEEN %s AND %s
                ORDER BY Date DESC
                     """
            
           
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (account_id, account_id, from_date_time, to_date_time))
            transactions = cursor.fetchall()

            if not transactions:
                self.statement_text_area.setHtml("<p style='color: white; font-size: 20px;'>No transactions found for the given account numnber period.</p>")
                return

            # Generating the HTML for display
            statement_html = "<html><head><style>"
            statement_html += """
                body { color: white; background-color: black; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
                th { background-color: #333; color: white; }
                tr:nth-child(even) { background-color: #444; }
                tr:nth-child(odd) { background-color: #555; }
                tr:hover { background-color: #666; }
            """
            statement_html += "</style></head><body>"
          #  statement_html += "<h2>Mini Statement</h2>"
            statement_html += "<table>"
            statement_html += "<tr><th>Date</th><th>From (Account)</th><th>To (Account)</th><th>Debit</th><th>Credit</th><th>Transaction ID</th><th>Type</th></tr>"

            for transaction in transactions:
                date, from_account, to_account, debit, credit, transaction_id, type_ = transaction
                statement_html += (
                    f"<tr><td>{date}</td><td>{from_account}</td><td>{to_account}</td>"
                    f"<td>{debit:.2f}</td><td>{credit:.2f}</td><td>{transaction_id}</td><td>{type_}</td></tr>"
                )
                
            statement_html += "</table></body></html>"
            self.statement_text_area.setHtml(statement_html)

            # Option to download the mini-statement
            
        
        except mysql.connector.Error as e:
            self.statement_text_area.setHtml(f"<p>Error generating statement: {e}</p>")
        
        finally:
            cursor.close()

     
    def download_statement(self):
        statement = self.statement_text_area.toHtml()
        if not statement:
            QMessageBox.warning(self, "Download Error", "No statement to download. Please generate a statement first.")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
    
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "From Account", "To Account", "Debit", "Credit", "Transaction ID", "Type"])
                   
                    import bs4
                    soup = bs4.BeautifulSoup(statement, 'html.parser')
                    table = soup.find('table')
                    if table:
                        rows = table.find_all('tr')
                        for row in rows[1:]:  # Skip the header row
                            cells = row.find_all('td')
                            row_data = [cell.get_text(strip=True) for cell in cells]
                            writer.writerow(row_data)

                QMessageBox.information(self, "Download Complete", f"Statement successfully downloaded to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Download Error", f"Error downloading statement: {e}")






    def susu_page(self):
        susu_widget =QWidget()
        susu_label = QLabel("<html><p> Susu <p></html>", susu_widget)
        susu_label.setGeometry(350, 50, 600 , 80)
        susu_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        susu_label.setAlignment(Qt.AlignCenter)



        self.susu_table_widget = QWidget()
        self.susu_table_widget.setGeometry(400, 200, 850, 400)
        self.susu_table_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.susu_table_widget.setParent(susu_widget)

        self.widget_layout = QVBoxLayout(self.susu_table_widget)

        susu_title = QLabel("Group Details")
        susu_title.setFont(QFont("Arial", 16, QFont.Bold))
        susu_title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(susu_title)

      


        
        self.susu_table = QTableWidget()
        self.susu_table.setColumnCount(5)
        
        self.susu_table.setColumnWidth(0, 150)  
        self.susu_table.setColumnWidth(1, 190)  
        self.susu_table.setColumnWidth(2, 120)  
        self.susu_table.setColumnWidth(3, 150)  
        self.susu_table.setColumnWidth(4, 120)
        self.susu_table.setColumnWidth(5,120) 
        
        self.susu_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #333333; color: white; padding: 10px; }")
        self.susu_table.horizontalHeader().setFixedHeight(60)
        self.susu_table.horizontalHeader().setFont(QFont("Arial", 10))
        self.susu_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.susu_table.setHorizontalHeaderLabels(["Group Name", "Contribution Amount", "Interval", "Members", "Total Amount" ,"Status"])
        self.susu_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.susu_table.setAlternatingRowColors(True)
        self.susu_table.setStyleSheet("QTableWidget { background-color: #1a1a1a; color: white; }")
        self.susu_table.setStyleSheet("QTableWidget::item { background-color: #262626; }")
        self.susu_table.setParent(susu_widget)
        self.widget_layout.addWidget(self.susu_table)

           # Execute SELECT query to check login credentials
       # cursor = self.db.cursor()
       # query = "SELECT member_id FROM susu_members WHERE Email = %s"
       # cursor.execute(query,(self.current_user_email,))
       # result = cursor.fetchone()

        #if result:
        self.load_susu_groups()

                 

        
        
       

       #Investment Balance

        view_details_button = QPushButton(self)
        view_details_button.setGeometry(50, 360, 300, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        view_details_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        view_details_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("view.png")
        view_details_button.setIcon(icon)

# Set the text for the button
        view_details_button.setText(" | View Details")

        view_details_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(11))

        view_details_button.setParent(susu_widget)


               #INVESTMENT REQUEST
        create_susu_account_button = QPushButton(self)
        create_susu_account_button.setGeometry(50, 200, 300, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        create_susu_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        create_susu_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("group.png")
        create_susu_account_button.setIcon(icon)

# Set the text for the button
        create_susu_account_button.setText(" | Create Group Account")

        create_susu_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(12))

        create_susu_account_button.setParent(susu_widget)


               #INVESTMENT REQUEST
        join_susu_account_button = QPushButton(self)
        join_susu_account_button.setGeometry(50, 280, 300, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        join_susu_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        join_susu_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("add-group.png")
        join_susu_account_button.setIcon(icon)

# Set the text for the button
        join_susu_account_button.setText(" | Join Group")

        join_susu_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(33))

        join_susu_account_button.setParent(susu_widget)




        self.stacked_widget.addWidget(susu_widget)
    def join_susu_group(self):
        join_susu_widget = QWidget()

        join_susu_label = QLabel("<html><p>Join Susu Group</p></>", join_susu_widget)
        join_susu_label.setGeometry(350, 50, 600 , 80)
        join_susu_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        join_susu_label.setAlignment(Qt.AlignCenter)
        
        form_layout = QFormLayout()

        self.group_id_input = QLineEdit()
        self.group_id_input.setPlaceholderText("Enter Group ID")
        self.group_id_input.setGeometry(50, 200, 350, 50)
        self.group_id_input.setClearButtonEnabled(True)
        self.group_id_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        form_layout.addRow("Group ID:", self.group_id_input)
        self.group_id_input.setParent(join_susu_widget)

        self.session_id_input = QLineEdit()
        self.session_id_input.setPlaceholderText("Enter Session ID")
        self.session_id_input.setGeometry(50, 280, 350, 50)
        self.session_id_input.setClearButtonEnabled(True)
        self.session_id_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        form_layout.addRow("Group ID:", self.session_id_input)
        self.session_id_input.setParent(join_susu_widget)

        join_button = QPushButton("Join Susu", self)
        join_button_width = 300
        join_button_x = (self.width() - join_button_width) // 3
        join_button.setGeometry(join_button_x, 400, join_button_width, 70)
        join_button.setStyleSheet("""
                                           QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                        }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                        }
                                          """)
        join_button.clicked.connect(self.join_susu)
        form_layout.addRow(join_button)
        join_button.setParent(join_susu_widget)

        self.stacked_widget.addWidget(join_susu_widget)

    def join_susu(self):
         #Join an existing Susu group.
        group_id = self.group_id_input.text()
        session_id = self.session_id_input.text()
        mysession_id = random.randint(1000000000, 9999999999)
        
        
        

        if  group_id  == "":
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return
        if session_id == "":
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return
        
        try:
            cursor = self.db.cursor()
            
        # Check if the group ID exists
            check_group_query = "SELECT Group_name FROM susu_groups WHERE group_id = %s"
            cursor.execute(check_group_query, (group_id,))
            group = cursor.fetchone()

            if not group:
             # If group ID does not exist, show a warning message
               QMessageBox.warning(self, "Group Not Found", "The specified group ID does not exist.")
               self.group_id_input.clear()
               self.session_id_input.clear()
               cursor.close()
               return
              # If group ID exists, get the group name
            group_name = group[0]

             # Fetch the session ID from the susu_members table
            fetch_session_query = "SELECT session_id FROM susu_members WHERE session_id = %s"
            cursor.execute(fetch_session_query, (session_id,))
            session = cursor.fetchone()

            if not session:
            # If session ID does not exist for the group, show a warning message
                QMessageBox.warning(self, "Session Not Found", "No session ID found for the specified group.")
                self.group_id_input.clear()
                self.session_id_input.clear()
                cursor.close()
                return
            session_id = session[0]
        # Prompt for user confirmation
            confirmation_msg = QMessageBox.question(
            self,
            "Confirm Join Group",
            f"Do you want to join the group '{group_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
            
            if confirmation_msg == QMessageBox.No:
            # If user declines, halt the process
                
                self.group_id_input.clear()
                self.session_id_input.clear()
                return 
              
            required_member_count_query = "SELECT Number_of_Members FROM susu_groups WHERE group_id = %s"
            cursor.execute(required_member_count_query, (group_id,))
            result = cursor.fetchone() 
            required_member_count = result[0]

            current_member_count_query = "SELECT COUNT(*) FROM susu_members WHERE group_id = %s"
            cursor.execute(current_member_count_query, (group_id,))
            current_member_count = cursor.fetchone()[0]


            if current_member_count == required_member_count:
                
                self.group_id_input.clear()
                self.session_id_input.clear()
                QMessageBox.information(self, "Error", "Sorry , Susu Group is Full")
                
                return

             # Proceed with the join process if user confirms
            join_group_query = """
            INSERT INTO susu_members (Email, member_fname, member_lname, group_id, member_id, session_id, joined_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """
            values = (self.current_user_email, self.first_name, self.last_name, group_id, self.phone_number,mysession_id)
            cursor.execute(join_group_query, values)
            self.db.commit()

            message = f"You have successfully joined {group_name} savings group"

            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message, self.current_user_email,))
            self.db.commit()
            
            self.load_alert()



            contributions_query = """
            INSERT INTO contributions (session_id, member_id, Group_id, amount)
            VALUES (%s, %s, %s, %s)
        """
            values = (mysession_id, self.phone_number, group_id, 0.00)
            cursor.execute(contributions_query, values,)
            self.db.commit()

            
            QMessageBox.information(self, "Success", "Successfully joined Susu group.")
            QMessageBox.information(self, "Success", "Your Member_id is your Mobile Number.")
            
            
            

            cursor.execute("SELECT Pin FROM susu_account WHERE Email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            if result and result[0]:  # PIN is not empty
                    return
            else:
            
            
                Pin = self.get_pin()
                Balance = 0.00
                query2= """
                    INSERT INTO susu_account (Email, FirstName, LastName, Member_ID, Pin, Balance)
                    VALUES (%s, %s, %s, %s, %s,%s)
                    """
                values2 = (self.current_user_email, self.first_name, self.last_name, self.phone_number, Pin, Balance )
                cursor.execute(query2, values2)
                self.db.commit()

                message1 = "Your Susu Account has been created as you Joined the susu Group"
                sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
                cursor.execute(sql, (message1, self.current_user_email,))
                self.db.commit()
            
                self.load_alert()
            
            self.load_susu_accounts()
            self.check_and_activate_group(group_id)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to join Susu group. Error: {e}")



    def check_and_activate_group(self, group_id):
        try:
            cursor = self.db.cursor()

        # Fetch the number of members required to activate the group
            required_member_count_query = "SELECT Number_of_Members FROM susu_groups WHERE group_id = %s"
            cursor.execute(required_member_count_query, (group_id,))
            result = cursor.fetchone()

            if result is None:
                QMessageBox.warning(self, "Group Not Found", "The specified group ID does not exist.")
                cursor.close()
                return

            required_member_count = result[0]
            

        # Fetch the current number of members in the group
            current_member_count_query = "SELECT COUNT(*) FROM susu_members WHERE group_id = %s"
            cursor.execute(current_member_count_query, (group_id,))
            current_member_count = cursor.fetchone()[0]
            

        # Activate the group if the required number of members is met
            if current_member_count == required_member_count:
                activate_group_query = "UPDATE susu_groups SET status = 'Active' ,start_date =%s WHERE group_id = %s"
                start_date = datetime.now().strftime('%Y-%m-%d')
                cursor.execute(activate_group_query, (start_date, group_id,))
                self.db.commit()
                self.load_susu_accounts()
                self.load_susu_groups()
                self.send_group_activation_message(group_id)
                self.group_id_input.clear()
                self.session_id_input.clear()
            
        except mysql.connector.Error as e:
                QMessageBox.critical(self, "Database Error", f"Failed to check and activate Susu group. Error: {e}")


    def send_group_activation_message(self, group_id):

        try:
            cursor = self.db.cursor()
            message = "Congratulations! Your Susu group has been activated."

        # Fetch all members' emails in the group
            fetch_members_query = "SELECT Email FROM susu_members WHERE group_id = %s"
            cursor.execute(fetch_members_query, (group_id,))
            members = cursor.fetchall()

            if not members:
                cursor.close()
                return

        # Send message to each member
            for member in members:
                email = member[0]
                sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
                cursor.execute(sql, (message, email,))
                self.db.commit()
                
                self.load_alert
                

            
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to send activation messages. Error: {e}")


    def susu_details_page(self):

        
        susu_details_widget = QWidget()
       
        susu_details_label = QLabel(f"Susu Group Details ", susu_details_widget)
        susu_details_label.setGeometry(350,50,600,80)
        susu_details_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        susu_details_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)

        susu_group_label = QLabel("Select Group ID:", self)
        susu_group_label.setGeometry(50, 150, 200, 30)
        susu_group_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        susu_group_label.setParent(susu_details_widget)
    
        self.susu_account_dropdown = QComboBox(self)
        self.susu_account_dropdown.setGeometry(250, 150, 250, 40)
        self.susu_account_dropdown.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 14px; font-weight: bold;")
        self.susu_account_dropdown.setParent(susu_details_widget)

        view_details_button = QPushButton("View Details", self)
        view_details_button_width = 300
        view_details_button_x = (self.width() - view_details_button_width) // 2
        view_details_button.setGeometry(view_details_button_x, 150, view_details_button_width, 50)
        view_details_button.setStyleSheet("""
                                        QPushButton {
                                             background-color: green;
                                             font-size: 14pt;
                                             border-radius: 25px;
                                                    }
                                             QPushButton:hover {
                                             background-color: #333333;
                                                               }
                                         """)
        view_details_button.clicked.connect(self.fetch_and_display_susu_details)
        view_details_button.setParent(susu_details_widget)

        
       

          # Add a table for group information
        self.group_info_table_widget = QWidget()
        self.group_info_table_widget.setGeometry(50, 225, 1200, 300)
        self.group_info_table_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.group_info_table_widget.setContentsMargins(20, 20, 20, 20)
        self.group_info_table_widget.setParent(susu_details_widget)

        self.widget_layout = QVBoxLayout(self.group_info_table_widget)

        susu_title = QLabel("Group Details")
        susu_title.setFont(QFont("Arial", 16, QFont.Bold))
        susu_title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(susu_title)

          
        self.group_info_table = QTableWidget()
        
       # self.group_info_table.setStyleSheet("background-color: balck; color: black; padding: 10px; border-radius: 10px; font-size: 14pt")
        self.group_info_table.setColumnCount(10)
        self.group_info_table.setColumnWidth(0, 120)  # Group Name
        self.group_info_table.setColumnWidth(1, 170)  # Created By (Email)
        self.group_info_table.setColumnWidth(2, 120)  # First Name
        self.group_info_table.setColumnWidth(3, 120)  # Last Name
        self.group_info_table.setColumnWidth(4, 130)  # Member ID
        self.group_info_table.setColumnWidth(5, 200)  # Contribution Amount
        self.group_info_table.setColumnWidth(6, 200)  # Contribution Interval
        self.group_info_table.setColumnWidth(7, 200)  # Number of Members
        self.group_info_table.setColumnWidth(8, 100)  # Status
        self.group_info_table.setColumnWidth(9, 100)  # Start Date
        
        self.group_info_table.setRowHeight(0, 30)  # Adjust row height for header
       #Set Header Style 
        self.group_info_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #333333; color: white; padding: 12px; }")
        self.group_info_table.horizontalHeader().setFixedHeight(60)
        self.group_info_table.horizontalHeader().setFont(QFont("Arial", 10))
        #set the table to be non-editable
        self.group_info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #set the horizontal header labels
     #Set the selection behavior and style       
        self.group_info_table.setHorizontalHeaderLabels(["Group Name", "Created By (Email)", "First Name", "Last Name", "Member ID", "Contribution Amount", "Contribution Interval", "Number of Members", "Status", "Start Date"])
        self.group_info_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
       
        self.group_info_table.setAlternatingRowColors(True)
        self.group_info_table.setStyleSheet("QTableWidget { background-color: #1a1a1a; color: white; }")
        self.group_info_table.setStyleSheet("QTableWidget::item:selected { background-color: #4d4d4d; color: white; }")
        self.group_info_table.setStyleSheet("QTableWidget::item { background-color: #262626; }")
        self.widget_layout.addWidget(self.group_info_table)

    # Add a table for member contributions

        
          # Add a table for group information
        self.member_contributions_table_widget = QWidget()
        self.member_contributions_table_widget.setGeometry(50, 550, 1200, 300)
        self.member_contributions_table_widget.setStyleSheet("background-color: black; border-radius: 20px; padding: 10px;")
        self.member_contributions_table_widget.setParent(susu_details_widget)

        self.widget_layout = QVBoxLayout(self.member_contributions_table_widget)

        title = QLabel("Member Details")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("background-color: #333333; color: white; padding: 10px; border-radius: 10px; font-size: 16pt;")
        self.widget_layout.addWidget(title)

        self.member_contributions_table = QTableWidget()
        
        
        self.member_contributions_table.setColumnCount(5)
        self.member_contributions_table.setRowHeight(0, 30) 
        self.member_contributions_table.setColumnWidth(0, 200)  
        self.member_contributions_table.setColumnWidth(1, 200)  
        self.member_contributions_table.setColumnWidth(2, 200)  
        self.member_contributions_table.setColumnWidth(3, 200)  
        self.member_contributions_table.setColumnWidth(4, 200)  
        
        
        
        self.member_contributions_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #333333; color: white; padding: 12px; }")
        self.member_contributions_table.horizontalHeader().setFixedHeight(60)
        self.member_contributions_table.horizontalHeader().setFont(QFont("Arial", 10))
        self.member_contributions_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.member_contributions_table.setHorizontalHeaderLabels(["Member First Name","Member Last Name" ,"Contribution Date", "Amount", "Status"])
        self.member_contributions_table.setParent(susu_details_widget)
        self.member_contributions_table.setSelectionBehavior(QAbstractItemView.SelectRows)
                
        self.member_contributions_table.setAlternatingRowColors(True)
        self.member_contributions_table.setStyleSheet("QTableWidget { background-color: #1a1a1a; color: white; }")
        self.member_contributions_table.setStyleSheet("QTableWidget::item:selected { background-color: #4d4d4d; color: white; }")
        self.member_contributions_table.setStyleSheet("QTableWidget::item { background-color: #262626; }")
        
        self.widget_layout.addWidget(self.member_contributions_table)
        
        self.load_susu_accounts()

       


      
        self.stacked_widget.addWidget(susu_details_widget)  
    def load_susu_accounts(self):
        try:
            cursor = self.db.cursor()
            #Query for saving accounts
            cursor.execute("SELECT group_id FROM susu_members WHERE Email = %s", (self.current_user_email,))
            susu_accounts = cursor.fetchall()

            for account in susu_accounts:
                self.susu_account_dropdown.addItem(f"Group ID: {account[0]}")
        except mysql.connector.Error as e:

            QMessageBox.critical(self, "Database Error", f"Error loading accounts: {e}")
        finally:
            cursor.close() 


           

    def fetch_and_display_susu_details(self):
        group_id = self.susu_account_dropdown.currentText().split(": ")[1]
        cursor = self.db.cursor()
        

        # Fetch group information
        group_info_query = "SELECT Group_name, Email, Firstname, Lastname, member_id, Contribution_Amount, Contribution_Interval, Number_of_Members, status, start_date FROM susu_groups WHERE Group_ID = %s"
        cursor.execute(group_info_query, (group_id,))
        group_info = cursor.fetchone()

        self.group_info_table.setRowCount(0)
        if group_info:
            row_number = self.group_info_table.rowCount()
            self.group_info_table.insertRow(row_number)
            for column_number, data in enumerate(group_info):
                if isinstance(data, decimal.Decimal):
                    data = str(data)  # Convert decimal to string
                self.group_info_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


        # Fetch member contributions
        member_contributions_query = """
            SELECT m.member_fname, m.member_lname, c.Contribution_date, c.amount, c.status
            FROM contributions c
            JOIN susu_members m ON c.session_id = m.session_id
            WHERE m.group_id = %s
        """
        cursor.execute(member_contributions_query, (group_id,))
        member_contributions = cursor.fetchall()
        print("Member contributions fetched:", member_contributions)

        self.member_contributions_table.setRowCount(len(member_contributions))
        for row, (fname, lname, date, amount, status) in enumerate(member_contributions):
            self.member_contributions_table.setItem(row, 0, QTableWidgetItem(f"{fname}"))
            self.member_contributions_table.setItem(row, 1, QTableWidgetItem(f"{lname}"))
            self.member_contributions_table.setItem(row, 2, QTableWidgetItem(str(date)))
            self.member_contributions_table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.member_contributions_table.setItem(row, 4, QTableWidgetItem(str(status)))



    def create_account_page(self):
        create_susu_account_widget = QWidget()
       
        create_susu_account_label = QLabel("<html><p>Susu Group Account(s)<p></>", create_susu_account_widget)
        create_susu_account_label.setGeometry(350,50,600,80)
        create_susu_account_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        create_susu_account_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)


        form_layout = QFormLayout()

        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("Enter Group Name")
        self.group_name_input.setGeometry(50, 200, 350, 50)
        self.group_name_input.setClearButtonEnabled(True)
        self.group_name_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        form_layout.addRow("Account Name:", self.group_name_input)
        self.group_name_input.setParent(create_susu_account_widget)
           # Set an icon for the input field if needed
        # icon = QIcon("calendar.png")  # You can use a calendar icon if desired
        # self.dob_input.addAction(icon, QLineEdit.LeadingPosition)


       
      
        self.contribution_amount_input = QLineEdit()
        self.contribution_amount_input.setGeometry(50,280,350,50)
        self.contribution_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.contribution_amount_input.setPlaceholderText("Enter Contribution Amount")
        self.contribution_amount_input.setClearButtonEnabled(True)
        form_layout.addRow("Contribution Amount:", self.contribution_amount_input)
        self.contribution_amount_input.setParent(create_susu_account_widget)

        self.contribution_interval_input = QComboBox()
        self.contribution_interval_input.addItems(["Daily", "Weekly", "Monthly"])
        self.contribution_interval_input.setGeometry(50,360,350,50)
        self.contribution_interval_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        form_layout.addRow("Contribution Interval:", self.contribution_interval_input)
        self.contribution_interval_input.setParent(create_susu_account_widget)


        self.members_count_input = QLineEdit()
        self.members_count_input.setGeometry(50,430,350,50)
        self.members_count_input.setPlaceholderText("Enter Number of Members")
        self.members_count_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.members_count_input.setClearButtonEnabled(True)
        self.members_count_input.setParent(create_susu_account_widget)
        form_layout.addRow("Number of Members:", self.members_count_input)




        create_button = QPushButton("Create Group Account", self)
        create_button_width = 300
        create_button_x = (self.width() - create_button_width) // 3
        create_button.setGeometry(create_button_x, 510, create_button_width, 70)
        create_button.setStyleSheet("""
                                           QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                        }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                        }
                                          """)
        create_button.clicked.connect(self.create_susu_group)
        create_button.setParent(create_susu_account_widget)
        form_layout.addRow(create_button)
        create_button.setParent(create_susu_account_widget)

       

        

        


       

        self.stacked_widget.addWidget(create_susu_account_widget) 

    
                 
        
        

    def create_susu_group(self):
        group_name = self.group_name_input.text()
        contribution_amount = self.contribution_amount_input.text()
        contribution_interval = self.contribution_interval_input.currentText()
        members_count = self.members_count_input.text()
        group_id = random.randint(1000000000, 9999999999)
        session_id = random.randint(1000000000, 9999999999)
        message1 = f"Congratullations, You have successfully created {group_name} susu group" 
        message = f"You Have been Joined to the {group_name} saving group"

        total_funds = int(contribution_amount) * int(members_count)


        if not group_name or not contribution_amount or not members_count :
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return
        try :
            contribution_amount = Decimal(contribution_amount)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please Enter A Valid Amount.")
            return

        if contribution_amount <= 0 :
            QMessageBox.warning(self, "Input Error", "Please Enter A Valid Amount.")
            return
        try :
            members_count = int(members_count)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please Enter A Valid Amount.")
            return
        if members_count <= 1:
            QMessageBox.warning(self, "Input Error", "Please Members should be More than One.")
            return



        try:
            cursor = self.db.cursor()
            query = """
                INSERT INTO susu_groups (Email, Firstname, Lastname, member_id, Group_name, Group_ID, Contribution_Amount, Contribution_Interval, Number_of_Members, Total_amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (self.current_user_email, self.first_name, self.last_name, self.phone_number,group_name, group_id, contribution_amount, contribution_interval, members_count,total_funds)
            cursor.execute(query, values)
            self.db.commit()

            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message1, self.current_user_email,))
            self.db.commit()
            self.load_alert()

            sql = "INSERT INTO group_funds (group_id, group_name, total_funds) VALUES(%s, %s, %s)"
            cursor.execute(sql, (group_id , group_name, 0.00,))
            self.db.commit()
            

            query1 = """
                    INSERT INTO susu_members (Email, member_fname, member_lname, group_id, member_id, session_id, joined_at)
                    VALUES (%s, %s, %s, %s, %s,%s, NOW())
                """
            values1 = (self.current_user_email, self.first_name, self.last_name, group_id, self.phone_number,session_id)
            cursor.execute(query1, values1)
            self.db.commit()

           

            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message, self.current_user_email,))
            self.db.commit()
            
            self.load_alert()

            contributions_query = """
            INSERT INTO contributions (session_id, member_id, amount, Group_id)
            VALUES (%s, %s, %s, %s)
        """
            values = (session_id, self.phone_number, 0.00,  group_id,)
            cursor.execute(contributions_query, values)
            self.db.commit()
            

            self.load_susu_groups()
            self.load_susu_accounts()
            
            
            QMessageBox.information(self, "Success", "Susu group created successfully.")
            QMessageBox.information(self, "Success", f"Susu Group ID : {group_id}")
            QMessageBox.information(self, "Success", f"Susu Session ID :{session_id}")
            

            self.group_name_input.clear()
            self.contribution_amount_input.clear()
            
            self.members_count_input.clear()


            cursor.execute("SELECT Pin FROM susu_account WHERE Email = %s", (self.current_user_email,))
            result = cursor.fetchone()
            

            if result and result[0]:  # PIN is not empty
                return
            else:
        

                Pin = self.get_pin()
                Balance = 0.00
                query2= """
                    INSERT INTO susu_account (Email, FirstName, LastName, Member_ID, Pin, Balance)
                    VALUES (%s, %s, %s, %s, %s,%s)
                    """
                values2 = (self.current_user_email, self.first_name, self.last_name, self.phone_number, Pin, Balance )
                cursor.execute(query2, values2)
                self.db.commit()
            
                message2 = "Your susu Account has been created as you join the Susu Group "
                sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
                cursor.execute(sql, (message1, self.current_user_email,))
                self.db.commit()
                self.load_alert()
            
            cursor.close()
 
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to create Susu group. Error: {e}")


    def fetch_group_id_by_email(self):
        email = self.current_user_email

        
        cursor = self.db.cursor()
        cursor.execute("SELECT  Group_ID FROM susu_members WHERE Email = %s", (email,))
        accounts = [account[0] for account in cursor.fetchall()]
        cursor.close()
        return accounts
    
    def load_susu_groups(self):
        try:
            group_ids = self.fetch_group_id_by_email()
            

            cursor = self.db.cursor()

            # Clear existing rows in the table before loading new data
            self.susu_table.setRowCount(0)

            for group_id in group_ids:
                query = """
                    SELECT
                        sg.Group_name,

                        sg.Contribution_Amount,
                        sg.Contribution_Interval,
                        sg.Number_of_Members,
                        sg.Total_amount,
                        sg.status
                    FROM susu_groups sg
                    INNER JOIN susu_members sm ON sg.Group_ID = sm.Group_ID
                    WHERE sg.Group_ID = %s AND sm.Email = %s
                """
                cursor.execute(query, (group_id, self.current_user_email,))
                results = cursor.fetchall()

                for result in results:
                    row_number = self.susu_table.rowCount()
                    self.susu_table.insertRow(row_number)
                    for column_number, data in enumerate(result):
                        if isinstance(data, decimal.Decimal):
                            data = str(data)  # Convert decimal to string if needed
                        self.susu_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load Susu groups. Error: {e}")
        finally:
            if cursor:
                cursor.close()
      


        
      
        
        
    def savings_page(self):
        savings_widget =QWidget()
        savings_label = QLabel("<html><p> My Savings <p></html>", savings_widget)
        savings_label.setGeometry(350, 50, 600 , 80)
        savings_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        savings_label.setAlignment(Qt.AlignCenter)






        
            
        savings_account_button = QPushButton(self)
        savings_account_button.setGeometry(50, 200, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        savings_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        savings_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("piggy-bank.png")
        savings_account_button.setIcon(icon)

# Set the text for the button
        savings_account_button.setText(" | Edit Saving Account(s)")

        savings_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(26))

        savings_account_button.setParent(savings_widget)
        # Create account
        
        account_button = QPushButton(self)
        account_button.setGeometry(50, 280, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("piggy-bank.png")
        account_button.setIcon(icon)

# Set the text for the button
        account_button.setText(" | Create Account")

        account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(18))

        account_button.setParent(savings_widget)




        self.stacked_widget.addWidget(savings_widget)

    def my_saving_account(self):
        my_saving_account_widget = QWidget()
        my_saving_account_label = QLabel("<html><p> Edit Saving Account(s) <p></html>", my_saving_account_widget)
        my_saving_account_label.setGeometry(350, 50, 600 , 80)
        my_saving_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        my_saving_account_label.setAlignment(Qt.AlignCenter)





          
        # Create a line edit for the First Name input field

        self.saving_account_input = QLineEdit(self)
        self.saving_account_input.setGeometry(50, 200, 350, 50) 
        self.saving_account_input.setPlaceholderText("Account Number")
        self.saving_account_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.saving_account_input.setClearButtonEnabled(True)
        self.saving_account_input.setParent(my_saving_account_widget)




        self.first_name1_input = QLineEdit(self)
        self.first_name1_input.setGeometry(50, 280, 350, 50) 
        self.first_name1_input.setPlaceholderText("Enter First Name")
        self.first_name1_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.first_name1_input.setClearButtonEnabled(True)
        self.first_name1_input.setParent(my_saving_account_widget)

        self.last_name1_input = QLineEdit(self)
        self.last_name1_input.setGeometry(50, 360, 350, 50) 
        self.last_name1_input.setPlaceholderText(" Enter Last Name")
        self.last_name1_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.last_name1_input.setClearButtonEnabled(True)
        self.last_name1_input.setParent(my_saving_account_widget)

        self.goal1_input = QLineEdit(self)
        self.goal1_input.setGeometry(50, 440, 350, 50) 
        self.goal1_input.setPlaceholderText("Enter Purpose")
        self.goal1_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.goal1_input.setClearButtonEnabled(True)
        self.goal1_input.setParent(my_saving_account_widget)
        self.goal1_input.setParent(my_saving_account_widget)


        self.save_acc_button = QPushButton("Save and Submit", self)
        save_button_width = 300  # Adjust the width of the button as needed
        save_button_x = (self.width() - save_button_width) // 3  # Center the button horizontally
        self.save_acc_button.setGeometry(save_button_x, 700, save_button_width, 70)
        self.save_acc_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        
        self.save_acc_button.clicked.connect(self.save_acc)
        self.save_acc_button.setParent(my_saving_account_widget)


        
          # Create QLabel for notification messages
        self.save_notify_label = QLabel("", self)
        self.save_notify_label.setGeometry(50, 600, 600, 50)
        self.save_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.save_notify_label.setParent(my_saving_account_widget)











        self.stacked_widget.addWidget(my_saving_account_widget)
    def fetch_accounts_by_email(self):
        email = self.current_user_email

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT Account_ID FROM saving_accountdb WHERE Email = %s", (email,))
            accounts = [account[0] for account in cursor.fetchall()]
            cursor.close()
            return accounts
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            return []    
        
    def save_acc(self) :
         

        email = self.current_user_email
        acc_num = self.saving_account_input.text()
        f_name = self.first_name1_input.text()
        l_name = self.last_name1_input.text()
        Goal = self.goal1_input.text()

        acc_numbers = self. fetch_accounts_by_email()



        if acc_num not in acc_numbers:
            self.save_notify_label.setText("Please Enter A Valid Accout number")
            self.save_notify_label.show()
            return
    

        if f_name =="" :
           
            self.save_notify_label.setText("Please Enter New First Name")
            self.save_notify_label.show()
            return
        
        if l_name =="" :
           
            self.save_notify_label.setText("Please Enter New Last Name")
            self.save_notify_label.show()
            return
        
        if Goal =="" :
           
            self.save_notify_label.setText("Please Enter Your New Purpose")
            self.save_notify_label.show()
            return
        
        self.save_notify_label.hide()

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
            
            message = f"Account Details of {acc_num} has been updated successfully"
            cursor = self.db.cursor()
            # Insert the user details into the savings_accountdb
            sql  = "UPDATE saving_accountdb SET FirstName = %s, LastName = %s, Goal = %s WHERE Account_ID = %s"
            cursor.execute(sql, (f_name, l_name, Goal, acc_num,))
            self.db.commit()
            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message, self.current_user_email,))
            self.db.commit()
            cursor.close()
            self.load_alert()
            cursor.close()
           
            

        

        # Show a message with the account ID
            QMessageBox.information(self, "Account Updated", "Your account details have been Updated ")

        # Clear the input fields after successful submission
            self.saving_account_input.clear()
            self.first_name1_input.clear()
            self.last_name1_input.clear()
            self.goal1_input.clear()
            
    
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error saving account details: {e}") 




 


    def savings_account_page(self, db, current_user_email):
        
        
        saccount_widget = QWidget()
        saccount_label = QLabel("<html><p> Create Account(s) <p></html>", saccount_widget)
        saccount_label.setGeometry(350, 50, 600 , 80)
        saccount_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        saccount_label.setAlignment(Qt.AlignCenter)
        



        
        # Create a line edit for the First Name input field
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setGeometry(50, 200, 350, 50) 
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.first_name_input.setClearButtonEnabled(True)
        self.first_name_input.setParent(saccount_widget)

        self.last_name_input = QLineEdit(self)
        self.last_name_input.setGeometry(50, 280, 350, 50) 
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.last_name_input.setClearButtonEnabled(True)
        self.last_name_input.setParent(saccount_widget)

        self.goal_input = QLineEdit(self)
        self.goal_input.setGeometry(50, 360, 350, 50) 
        self.goal_input.setPlaceholderText("Purpose")
        self.goal_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.goal_input.setClearButtonEnabled(True)
        self.goal_input.setParent(saccount_widget)
        self.goal_input.setParent(saccount_widget)


        self.create_acc_button = QPushButton("Create Account", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 3  # Center the button horizontally
        self.create_acc_button.setGeometry(button_x, 700, button_width, 70)
        self.create_acc_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        
        self.create_acc_button.clicked.connect(self.create_sacc)
        self.create_acc_button.setParent(saccount_widget)


        
          # Create QLabel for notification messages
        self.notify_label = QLabel("", self)
        self.notify_label.setGeometry(50, 440, 600, 50)
        self.notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.notify_label.setParent(saccount_widget)










        self.stacked_widget.addWidget(saccount_widget)


    def generate_account_id(self):
        
    # Generate a UUID (Universally Unique Identifier)
        unique_id = uuid.uuid4().hex[:8]  # Extract the first 8 characters
    
    # Add a random number to the UUID to ensure uniqueness
        random_num = random.randint(1000, 9999)  # Generate a 4-digit random number
        account_id = f"{unique_id}-{random_num}"  # Combine UUID and random number
        
        return account_id
    
    
    
    
    def create_sacc(self):
         
        self.mysignal = pyqtSignal(str)
        
        
        
    # Get the input values from the user
        
        email = self.current_user_email
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        goal = self.goal_input.text()
    
    # Generate an account ID (you can replace this with your logic)
        
        Amount = 0.00

        if first_name =="" :
           
            self.notify_label.setText("Please Enter First Name")
            self.notify_label.show()
            return
        
        if last_name =="" :
           
            self.notify_label.setText("Please Enter Last Name")
            self.notify_label.show()
            return
        
        if goal =="" :
           
            self.notify_label.setText("Please Enter Your Purpose")
            self.notify_label.show()
            return
        
        self.notify_label.hide()
        
        
        
         

    # Save the details to the database
        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
            account_id = self.generate_account_id()
            message = f"Your Account ID for the newly created saving account is {account_id}"

            cursor = self.db.cursor()
            # Insert the user details into the savings_accountdb
            sql  = "INSERT INTO saving_accountdb (Email, FirstName, LastName, Account_ID, Goal, Amount) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ( email, first_name, last_name, account_id, goal,  Amount,))
            self.db.commit()
            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message, self.current_user_email,))
            self.db.commit()
            cursor.close()
            self.load_alert()
            

        

        # Show a message with the account ID
            QMessageBox.information(self, "Account Created", f"Your account has been created with Account ID: {account_id}")

        # Clear the input fields after successful submission
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.goal_input.clear()
            
    
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error saving account details: {e}") 

        #Own account button
    def calculate_and_update_balance(self):
        try:
            cursor = self.db.cursor()
            message = f"{account_id}  updated with interest: Gh¢ {interest:.2f}"
            # Fetch the account data
            cursor.execute("SELECT Amount, Created_at FROM saving_accountdb")
            accounts = cursor.fetchall()

            # Calculate interest for each account and update the database
            for account_id, amount, created_at in accounts:
                created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()
                elapsed_time = (current_time - created_at).days
                interest_rate = 0.02  # Example interest rate of 2%
                if elapsed_time > 0:
                    interest = amount * (1 + interest_rate) ** (elapsed_time / 365) - amount
                    new_amount = amount + interest

                    # Update the balance and creation date in the database
                    cursor.execute("UPDATE saving_accountdb SET Amount = %s, Created_at = %s WHERE Account_ID = %s",
                                   (new_amount, current_time, account_id))
                    
                    self.db.commit()
                    
                    cursor.execute("SELECT Firstname, Lastname FROM saving_accountdb WHERE Account_ID = %s", (account_id,))
                    account_info = cursor.fetchone()
                    self.db.commit()

                    sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
                    cursor.execute(sql, (message, self.current_user_email,))
                    self.db.commit()
                    cursor.close()
                    self.load_alert()
        
               
            cursor.close()
            return None
        except Exception as e:
            return str(e)
    
    
    

    def start_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)  

        




        
    def transfer_page(self):
        transfer_widget =QWidget()
        transfer_label = QLabel("<html><p> Funds Transfer <p></html>", transfer_widget)
        transfer_label.setGeometry(350, 50, 600 , 80)
        transfer_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_label.setAlignment(Qt.AlignCenter)

        #Own account button

        own_account_button = QPushButton(self)
        own_account_button.setGeometry(50, 200, 500, 50)
                       
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        own_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        own_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        own_account_button.setIcon(icon)

# Set the text for the button
        own_account_button.setText(" | To Own Account(s)")

        own_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(13))
        own_account_button.setParent(transfer_widget)

#  Another account

        another_account_button = QPushButton(self)
        another_account_button.setGeometry(50, 280, 500, 50)
                       
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        another_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        another_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        another_account_button.setIcon(icon)

# Set the text for the button
        another_account_button.setText(" | To Inter Account")

        another_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(14))
        another_account_button.setParent(transfer_widget)

         #To Wallet
        
        wallet_button = QPushButton(self)
        wallet_button.setGeometry(50, 360, 500, 50)
                       
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        wallet_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        wallet_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        wallet_button.setIcon(icon)

# Set the text for the button
        wallet_button.setText(" | Mobile Wallet")

        wallet_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(15))
        wallet_button.setParent(transfer_widget)

        
         #To Susu
        
        susu_group_button = QPushButton(self)
        susu_group_button.setGeometry(50, 430, 500, 50)
                       
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        susu_group_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        susu_group_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        susu_group_button.setIcon(icon)

# Set the text for the button
        susu_group_button.setText(" | Susu Group")

        susu_group_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(36))
        susu_group_button.setParent(transfer_widget)

        self.stacked_widget.addWidget(transfer_widget)

    def transfer_to_susu_group(self):
        transfer_to_susu_group_widget =QWidget()
        transfer_to_susu_group_label = QLabel("<html><p> Funds to Transfer-To Susu Group Account(s) <p></html>", transfer_to_susu_group_widget)
        transfer_to_susu_group_label.setGeometry(350, 50, 600 , 80)
        transfer_to_susu_group_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_to_susu_group_label.setAlignment(Qt.AlignCenter)

        self.group_acc_input = QLineEdit(self)
        self.group_acc_input.setGeometry(50, 200, 350, 50)
        self.group_acc_input.setPlaceholderText("Enter Group ID")
        self.group_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.group_acc_input.setClearButtonEnabled(True)
        self.group_acc_input.setParent(transfer_to_susu_group_widget)

        self.transfer_amount8_input = QLineEdit(self)
        self.transfer_amount8_input.setGeometry(50, 280, 350, 50)
        self.transfer_amount8_input.setPlaceholderText("Amount to Transfer")
        self.transfer_amount8_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer_amount8_input.setClearButtonEnabled(True)
        self.transfer_amount8_input.setParent(transfer_to_susu_group_widget)

        self.transfer8_button = QPushButton("Transfer", self)
        transfer8_button_width = 300
        transfer8_button_x = (self.width() - transfer8_button_width) // 3
        self.transfer8_button.setGeometry(transfer8_button_x, 450, transfer8_button_width, 70)
        self.transfer8_button.setStyleSheet("""
                                      QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                  }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                             }
                                           """)
        self.transfer8_button.clicked.connect(self.perform_susu_account_to_susu_group_transfer)
        self.transfer8_button.setParent(transfer_to_susu_group_widget)


        self.transfer8_notify_label = QLabel("", self)
        self.transfer8_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer8_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer8_notify_label.setParent(transfer_to_susu_group_widget)

        self.transfer8_regenerate_otp_button = QPushButton(self)
        self.transfer8_regenerate_otp_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.transfer8_regenerate_otp_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.transfer8_regenerate_otp_button.setGeometry(410, 335, 40, 40)
        self.transfer8_regenerate_otp_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.transfer8_regenerate_otp_button.hide()
        self.transfer8_regenerate_otp_button.clicked.connect(self.generate_otp8)  # Connect the clicked signal
        self.transfer8_regenerate_otp_button.setParent(transfer_to_susu_group_widget)
        
        self.otp_generated8 = False
        self.otp8= ""

        #Create a QLabel for the information display 
        self.info_label8_widget = QWidget()
        self.info_label8 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label8_widget)
        self.info_label8.setAlignment(Qt.AlignCenter)
        self.info_label8.setGeometry(50,200,400,40)
        self.info_label8.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label8.hide() # Hide the info label initially
        self.info_label8.setParent(transfer_to_susu_group_widget)

        #create a container widget for the otp input
        self.container8 = QWidget()
        self.container8.setGeometry(50,235,400,100)
        self.container8.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container8.hide()
        self.container8.setParent(transfer_to_susu_group_widget)

        # Create a QVBoxLayout for the container
        self.container_layout8 = QVBoxLayout(self.container8)
        self.container_layout8.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp8_boxes = []
        for _ in range(6):
            otp8_box = QLineEdit(self.container8)
            otp8_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp8_box.setMaxLength(1)  # Limit input to one character
            otp8_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp8_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp8_box)
            self.otp8_boxes.append(otp8_box)
             # Connect textChanged signal to handle_otp_input slot
            otp8_box.textChanged.connect(self.handle_otp_input8)


        self.container_layout8.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label8_widget = QWidget()
        self.timer_label8 = QLabel("<html><p>Time remaining....60 seconds<p></html> ", self.timer_label8_widget)
        self.timer_label8.setAlignment(Qt.AlignCenter)
        self.timer_label8.setGeometry(50,335,360,40)
        self.timer_label8.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label8.hide()
        self.timer_label8.setParent(transfer_to_susu_group_widget)


        self.stacked_widget.addWidget(transfer_to_susu_group_widget)

    def handle_otp_input8(self, text):
        current_box = self.sender()  # Get the sender QLineEdit
        index = self.otp8_boxes.index(current_box)
        if len(text) == 1 and index < len(self.otp8_boxes) - 1:
            self.otp8_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp8_boxes) - 1:
            self.check_otp8()
               

    def update_timer8(self):
        self.time_left -= 1
        self.timer_label8.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input8()
            self.otp_generated8
            self.otp_generated8 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         

    def fecth_group_id_by_email(self):
        cursor = self.db.cursor()
            #Query for saving accounts
        cursor.execute("SELECT group_id FROM susu_members WHERE Email = %s", (self.current_user_email,))
        susu_accounts = [id [0] for id in cursor.fetchall() ]
        cursor.close()
        return susu_accounts
    
    
       
       

    def perform_susu_account_to_susu_group_transfer(self):
        group_acc = self.group_acc_input.text()
        transfer_amount8 = self.transfer_amount8_input.text()
        group_ids = self.fecth_group_id_by_email()

        


          # Validate inputs
        if not group_acc or not transfer_amount8:
            self.transfer8_notify_label.setText("Please fill in all fields.")
            self.transfer8_notify_label.show()
            return

        try:
            transfer_amount8= Decimal(transfer_amount8)
        except ValueError:
            self.transfer8_notify_label.setText("Please enter a valid amount.")
            self.transfer8_notify_label.show()
            return

        if transfer_amount8 <= 0:
            self.transfer8_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer8_notify_label.show()
            return
        
        if group_acc not in group_ids:
            self.transfer8_notify_label.setText("Please Enter A Valid Group ID")
            self.transfer8_notify_label.show()
            return
        
        if transfer_amount8 != "":
            self.generate_otp8()
            self.otp_generated8 = True
            self.info_label8.show()
            self.container8.show()
            self.timer_label8.show()
            self.transfer8_regenerate_otp_button.show()
            self.transfer8_notify_label.setText("")
            self.group_acc_input.hide()
            self.transfer_amount8_input.hide()
      
            self.start_timer8()

        self.transfer8_notify_label.hide()  

    def perform_transaction8(self):    

        group_acc = self.group_acc_input.text()
        transfer_amount8 = self.transfer_amount8_input.text()

        transfer_amount8 = Decimal(transfer_amount8)

        


        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account1_result = cursor.fetchone()

            if not account1_result or account1_result[0] is None:
                QMessageBox.information(self, "Accout Not Found", "Please activate your account by setting a PIN.")
                self.group_acc_input.clear()
                self.transfer_amount8_input.clear()
                return
          

            # Check if susu group account exists 
            cursor.execute("SELECT Balance FROM susu_account WHERE Email= %s", (self.current_user_email,))
            sender_result = cursor.fetchone()

            if not sender_result:
               
               QMessageBox.information(self, "Failed", "Account not Found")
               self.group_acc_input.clear()
               self.transfer_amount8_input.clear()
               return

            
            sender_balance = sender_result[0]


            
            cursor.execute("SELECT total_funds FROM group_funds WHERE group_id= %s", (group_acc,))
            result = cursor.fetchone()

            if not result:
               QMessageBox.information(self, "Failed", "Account not Found")
               self.group_acc_input.clear()
               self.transfer_amount8_input.clear()
               return


            funds_balance = result[0]
            
            
               
            cursor.execute("SELECT amount FROM contributions WHERE member_id = %s AND group_id = %s " ,(self.phone_number, group_acc,))
            account1_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            account1_balance = account1_result[0]

            cursor.execute("SELECT status FROM susu_groups WHERE group_id = %s", (group_acc,))
            group_status = cursor.fetchone()[0]

            if group_status == 'Inactive':
                QMessageBox.information(self, "Account Inactive", " Account is inactive")
                self.group_acc_input.clear()
                self.transfer_amount8_input.clear()
                return

            # Get all active Susu groups and their intervals
            cursor.execute("SELECT Contribution_Amount FROM susu_groups WHERE Group_ID = %s ", (group_acc,))
            amount = cursor.fetchone()

            amount = amount[0]

            if transfer_amount8 != amount:
                QMessageBox.information(self, "Amount Not Up To", "Enter Amount to be Paid")
                self.group_acc_input.clear()
                self.transfer_amount8_input.clear()
                return



            if sender_balance < transfer_amount8:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    self.transfer_amount8_input.clear()
                    self.group_acc_input.clear()
                    return
            

                
            
         

            # Perform the transfer
            new_sender1_balance = sender_balance - transfer_amount8
            new_account1_balance = account1_balance + transfer_amount8
            total_funds = funds_balance + transfer_amount8

            check_group_query = "SELECT Group_name FROM susu_groups WHERE group_id = %s"
            cursor.execute(check_group_query, (group_acc,))
            group = cursor.fetchone()

            if not group:
             # If group ID does not exist, show a warning message
                QMessageBox.warning(self, "Group Not Found", "The specified group ID does not exist.")
                cursor.close()
                self.transfer_amount8_input.clear()
                self.group_acc_input.clear()
                return
              # If group ID exists, get the group name
            group_name = group[0]

           
        # Prompt for user confirmation
            confirmation_msg = QMessageBox.question(
            self,
            "Confirm Transaction",
            f"Do you want to send money to  '{group_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
            
            if confirmation_msg == QMessageBox.No:
            # If user declines, halt the process
                cursor.close()
                self.transfer_amount8_input.clear()
                self.group_acc_input.clear()
                return 

            cursor.execute("UPDATE contributions SET amount = %s , status = %s WHERE member_id = %s AND group_id = %s", (new_account1_balance, 'Completed', self.phone_number, group_acc))
            self.db.commit()
            cursor.execute("UPDATE susu_account SET Balance = %s WHERE Email = %s", (new_sender1_balance, self.current_user_email))
            self.db.commit()
            cursor.execute("UPDATE group_funds SET total_funds = %s WHERE group_id = %s", (total_funds, group_acc))
            self.db.commit()


            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount8:.2f} from susu account: {self.phone_number} to susu_group,  completed successfully.")

            from_account = "Susu Account"
            to_account = "Susu Group"
            from_account_id = self.phone_number
            to_account_id = group_acc
            Type = "External"
            
             # Generate unique transaction ID
            contribution_id = str(uuid.uuid4())
            contribution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (contribution_date, from_account, to_account, from_account_id, transfer_amount8, to_account_id, transfer_amount8, contribution_id, Type, self.current_user_email,))
            self.load_transactions()

            self.db.commit()

            cursor.execute("UPDATE contributions SET Contribution_ID = %s, Contribution_date = %s WHERE member_id = %s AND Group_id = %s", (contribution_id,contribution_date,self.phone_number, group_acc,))
            self.db.commit()

        # Clear the input fields after successful transfer
            self.transfer_amount1_input.clear()
            self.sender1_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from saving Account to Wallet")    

    def start_timer8(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer8)
        self.timer.start(1000)  # Update timer every  


    def generate_otp8(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp8 = str(random.randint(100000, 999999))
        QMessageBox.information(self,"OTP", f"Sending OTP to {email}")
        QMessageBox.information(self,"OTP", f"""Your Verification code: {self.otp8}
For security reasons, do not share
this code with anyone. Enter this code 
to perform the transaction""") 
        QMessageBox.information(self,"OTP", f"Sending OTP to {number}")
        QMessageBox.information(self,"OTP", f"""Your Verification code: {self.otp8}
For security reasons, do not share
this code with anyone. Enter this code 
to the transaction""") # Print the generated OTP
        self.start_timer8()

    

    def clear_otp_input8(self):
        for otp_box in self.otp8_boxes:
            otp_box.clear()  
       
        

    

    def check_otp8(self):
        entered_otp = "".join(box.text() for box in self.otp8_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input8()
           self.otp_generated8 = False
           return
           
        if entered_otp == self.otp8:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input8()
            
            self.info_label8.hide()
            self.container8.hide()
            self.timer_label8.hide()
            self.transfer8_regenerate_otp_button.hide()
            self.timer.stop() 
            self.group_acc_input.show()
            self.transfer_amount8_input.show()
            self.perform_transaction8()
            
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input8()
            self.otp_generated8 = False   
          


    

    def own_account_page(self):
        own_account_widget =QWidget()
        own_account_label = QLabel("<html><p> Funds to Transfer-To Own Account<p></html>", own_account_widget)
        own_account_label.setGeometry(350, 50, 600 , 80)
        own_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        own_account_label.setAlignment(Qt.AlignCenter)



        
        self.own_source_account_label = QLabel('<U> Select Account Account to be Credited</>',own_account_widget)
        self.own_source_account_label.setGeometry(50, 180, 600, 80)
        self.own_source_account_label.setStyleSheet("background-color: transparent; color: white; padding: 20px; border-radius: 40px; font-size: 20pt;")
        self.own_source_account_label.setParent(own_account_widget)


        my_account_button = QPushButton(self)
        my_account_button.setGeometry(50, 250, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        my_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        my_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        my_account_button.setIcon(icon)

# Set the text for the button
        my_account_button.setText(" | Wallet")

        my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(27))

        my_account_button.setParent(own_account_widget)

      
        
        from_saving_account_button = QPushButton(self)
        from_saving_account_button.setGeometry(50, 330, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        from_saving_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        from_saving_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        from_saving_account_button.setIcon(icon)

# Set the text for the button
        from_saving_account_button.setText(" | Saving Account")

        from_saving_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(31))

        from_saving_account_button.setParent(own_account_widget)


        
        from_investment_button = QPushButton(self)
        from_investment_button.setGeometry(50, 410, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        from_investment_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        from_investment_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        from_investment_button.setIcon(icon)

# Set the text for the button
        from_investment_button.setText(" | Susu Account")

        from_investment_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(32))

        from_investment_button.setParent(own_account_widget)
        
        '''loan_account_button = QPushButton(self)
        loan_account_button.setGeometry(50, 490, 500, 50)
                         
         Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        loan_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        loan_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("financial.png")
        loan_account_button.setIcon(icon)

# Set the text for the button
        loan_account_button.setText(" | Loan Account ")

      #  my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))

        loan_account_button.setParent(balance_widget)'''

        self.stacked_widget.addWidget(own_account_widget)

    def transfer_to_my_saving_account(self) :
        transfer_to_my_saving_account_widget =QWidget()
        transfer_to_my_saving_account_label = QLabel("<html><p> Funds to Transfer Saving Account<p></html>", transfer_to_my_saving_account_widget)
        transfer_to_my_saving_account_label.setGeometry(350, 50, 600 , 80)
        transfer_to_my_saving_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_to_my_saving_account_label.setAlignment(Qt.AlignCenter)

        self.receiver_acc_input = QLineEdit(self)
        self.receiver_acc_input.setGeometry(50, 200, 350, 50)
        self.receiver_acc_input.setPlaceholderText("Enter Saving Account Number")
        self.receiver_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.receiver_acc_input.setClearButtonEnabled(True)
        self.receiver_acc_input.setParent(transfer_to_my_saving_account_widget)


        self.transfer4_amount_input = QLineEdit(self)
        self.transfer4_amount_input.setGeometry(50, 280, 350, 50)
        self.transfer4_amount_input.setPlaceholderText("Amount to Transfer")
        self.transfer4_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer4_amount_input.setClearButtonEnabled(True)
        self.transfer4_amount_input.setParent(transfer_to_my_saving_account_widget)

        self.transfer4_button = QPushButton("Transfer", self)
        transfer4_button_width = 300
        transfer4_button_x = (self.width() - transfer4_button_width) // 3
        self.transfer4_button.setGeometry(transfer4_button_x, 450, transfer4_button_width, 70)
        self.transfer4_button.setStyleSheet("""
                                           QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                        }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                        }
                                          """)
        self.transfer4_button.clicked.connect(self.perform_wallet_to_saving_account_transfer)
        self.transfer4_button.setParent(transfer_to_my_saving_account_widget)

        self.transfer4_notify_label = QLabel("", self)
        self.transfer4_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer4_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer4_notify_label.setParent(transfer_to_my_saving_account_widget)

        self.stacked_widget.addWidget(transfer_to_my_saving_account_widget)


       

        #Create a QLabel for the information display 
        self.pin_info_label_widget = QWidget()
        self.pin_info_label = QLabel("<html><p>Enter Your Pin<p></html> ", self.pin_info_label_widget)
        self.pin_info_label.setAlignment(Qt.AlignCenter)
        self.pin_info_label.setGeometry(50,200,400,40)
        self.pin_info_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_info_label.hide() # Hide the info label initially
        self.pin_info_label.setParent(transfer_to_my_saving_account_widget)

        #create a container widget for the otp input
        self.pin_container = QWidget()
        self.pin_container.setGeometry(50,235,400,100)
        self.pin_container.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.pin_container.hide()
        self.pin_container.setParent(transfer_to_my_saving_account_widget)

        # Create a QVBoxLayout for the container
        self.pin_container_layout = QVBoxLayout(self.pin_container)
        self.pin_container_layout.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.pin_boxes = []
        for _ in range(4):
            pin_box = QLineEdit(self.pin_container)
            pin_box.setFixedSize(50, 50)  # Set fixed size for each box
            pin_box.setMaxLength(1)  # Limit input to one character
            pin_box.setAlignment(Qt.AlignCenter)  # Center align text
            pin_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(pin_box)
            self.pin_boxes.append(pin_box)
             # Connect textChanged signal to handle_otp_input slot
            pin_box.textChanged.connect(self.handle_pin_input)


        self.pin_container_layout.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.pin_label_widget = QWidget()
        self.pin_label = QLabel("", self.pin_label_widget)
        self.pin_label.setAlignment(Qt.AlignCenter)
        self.pin_label.setGeometry(50,335,400,40)
        self.pin_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_label.hide()
        self.pin_label.setParent(transfer_to_my_saving_account_widget)




        self.stacked_widget.addWidget(transfer_to_my_saving_account_widget)
     
          
    def handle_pin_input(self, text):
        current_pin = self.sender()  # Get the sender QLineEdit
        index = self.pin_boxes.index(current_pin)
        if len(text) == 1 and index < len(self.pin_boxes) - 1:
            self.pin_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.pin_boxes) - 1:
            self.check_pin()
               

       
       
    def perform_wallet_to_saving_account_transfer(self):   
    
        receiver_acc = self.receiver_acc_input.text()
        transfer_amount4 = self.transfer4_amount_input.text()


          # Validate inputs
        if not receiver_acc or not transfer_amount4:
            self.transfer4_notify_label.setText("Please fill in all fields.")
            self.transfer4_notify_label.show()
            return

        try:
            transfer_amount4 = Decimal(transfer_amount4)
        except ValueError:
            self.transfer4_notify_label.setText("Please enter a valid amount.")
            self.transfer4_notify_label.show()
            return

        if transfer_amount4 <= 0:
            self.transfer4_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer4_notify_label.show()
            return
        
        if transfer_amount4 != "":
            
            self.pin_info_label.show()
            self.pin_container.show()
            self.pin_label.show()
            self.receiver_acc_input.hide()
            self.transfer4_amount_input.hide()
      
            

        self.transfer4_notify_label.hide()  

    def perform_transaction2(self):    
        receiver_acc = self.receiver_acc_input.text()
        transfer_amount4 = self.transfer4_amount_input.text()
        

        transfer_amount4 = Decimal(transfer_amount4)

        


        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account2_result = cursor.fetchone()

            if not account2_result or account2_result[0] is None:
                QMessageBox.information(self, "Failed", "Please Activate Your Account By Setting Pin")

                return


            # Check if receiver account exists and has sufficient funds
            cursor.execute("SELECT Amount FROM saving_accountdb WHERE Account_ID =%s  AND Email = %s ",  (receiver_acc,self.current_user_email,))
            receiver_result = cursor.fetchone()

            if not receiver_result:
               
               QMessageBox.information(self, "Failed", "Account not Found")

               return
            
            receiver_balance = receiver_result[0]



            # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            wallet_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            wallet_balance = wallet_result[0]





            if wallet_balance < transfer_amount4:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    
                    self.transfer4_amount_input.clear()
                    self.receiver_acc_input.clear()
                    return
            


            # Perform the transfer
            new_wallet_balance = wallet_balance - transfer_amount4
            new_receiver_balance = receiver_balance + transfer_amount4

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_wallet_balance, self.current_user_email))
            self.db.commit()
            cursor.execute("UPDATE saving_accountdb SET Amount = %s WHERE Email = %s", (new_receiver_balance, self.current_user_email))
            self.db.commit()

            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount4:.2f} To  {receiver_acc},  completed successfully.")
            from_account = "Wallet"
            to_account = "Saving Acount"
            from_account_id = self.phone_number
            Type = "Internal"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (transaction_date, from_account, to_account, from_account_id, transfer_amount4, receiver_acc, transfer_amount4, transaction_id, Type, self.current_user_email,))
            self.load_transactions()
            self.db.commit()
            

        # Clear the input fields after successful transfer
            self.transfer4_amount_input.clear()
            self.receiver_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from saving Account to Wallet")    



    

    def clear_pin_input(self):
        for otp_box in self.pin_boxes:
            otp_box.clear()  
       
        

    

    def check_pin(self):
        entered_pin = "".join(box.text() for box in self.pin_boxes)
        entered_pin = self.sha512_64_hash(entered_pin)

        
        
        if entered_pin == self.get_pin():
            
            
            self.clear_pin_input()
            
            self.pin_info_label.hide()
            self.pin_container.hide()
            self.pin_label.hide() 
            self.receiver_acc_input.show()
            self.transfer4_amount_input.show()
            self.perform_transaction2()
            
        else:
            QMessageBox.warning(self, "Error", "Wrong Pin, Please try again")
            self.clear_pin_input()
            
              




    def transfer_to_susu_account(self) :

        transfer_to_susu_group_account_widget =QWidget()
        transfer_to_susu_group_account_label = QLabel("<html><p> Funds to Transfer to Susu Account<p></html>", transfer_to_susu_group_account_widget)
        transfer_to_susu_group_account_label.setGeometry(350, 50, 600 , 80)
        transfer_to_susu_group_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_to_susu_group_account_label.setAlignment(Qt.AlignCenter)

        self.receiver1_acc_input = QLineEdit(self)
        self.receiver1_acc_input.setGeometry(50, 200, 350, 50)
        self.receiver1_acc_input.setPlaceholderText("Member ID")
        self.receiver1_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.receiver1_acc_input.setClearButtonEnabled(True)
        self.receiver1_acc_input.setParent(transfer_to_susu_group_account_widget)


        self.transfer5_amount_input = QLineEdit(self)
        self.transfer5_amount_input.setGeometry(50, 280, 350, 50)
        self.transfer5_amount_input.setPlaceholderText("Amount to Transfer")
        self.transfer5_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer5_amount_input.setClearButtonEnabled(True)
        self.transfer5_amount_input.setParent(transfer_to_susu_group_account_widget)

        self.transfer5_button = QPushButton("Transfer", self)
        transfer5_button_width = 300
        transfer5_button_x = (self.width() - transfer5_button_width) // 3
        self.transfer5_button.setGeometry(transfer5_button_x, 450, transfer5_button_width, 70)
        self.transfer5_button.setStyleSheet("""
                                           QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                        }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                        }
                                          """)
        self.transfer5_button.clicked.connect(self.perform_wallet_to_susu_group_account_transfer)
        self.transfer5_button.setParent(transfer_to_susu_group_account_widget)

        self.transfer5_notify_label = QLabel("", self)
        self.transfer5_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer5_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer5_notify_label.setParent(transfer_to_susu_group_account_widget)

        

            #Create a QLabel for the information display 
        self.pin_info_label3_widget = QWidget()
        self.pin_info_label3 = QLabel("<html><p>Enter Your Pin<p></html> ", self.pin_info_label3_widget)
        self.pin_info_label3.setAlignment(Qt.AlignCenter)
        self.pin_info_label3.setGeometry(50,200,400,40)
        self.pin_info_label3.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_info_label3.hide() # Hide the info label initially
        self.pin_info_label3.setParent(transfer_to_susu_group_account_widget)

        #create a container widget for the otp input
        self.pin_container3 = QWidget()
        self.pin_container3.setGeometry(50,235,400,100)
        self.pin_container3.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.pin_container3.hide()
        self.pin_container3.setParent(transfer_to_susu_group_account_widget)

        # Create a QVBoxLayout for the container
        self.pin_container_layout3 = QVBoxLayout(self.pin_container3)
        self.pin_container_layout3.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

           #Create Six QLineEDIT Boxes for the otp
        self.pin3_boxes = []
        for _ in range(4):
            pin3_box = QLineEdit(self.pin_container3)
            pin3_box.setFixedSize(50, 50)  # Set fixed size for each box
            pin3_box.setMaxLength(1)  # Limit input to one character
            pin3_box.setAlignment(Qt.AlignCenter)  # Center align text
            pin3_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(pin3_box)
            self.pin3_boxes.append(pin3_box)
             # Connect textChanged signal to handle_otp_input slot
            pin3_box.textChanged.connect(self.handle_pin_input3)


        self.pin_container_layout3.addLayout(self.layout)

          # Create a QLabel for time remaining display (initially hidden)
        self.pin_label3_widget = QWidget()
        self.pin_label3 = QLabel("", self.pin_label3_widget)
        self.pin_label3.setAlignment(Qt.AlignCenter)
        self.pin_label3.setGeometry(50,335,400,40)
        self.pin_label3.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_label3.hide()
        self.pin_label3.setParent(transfer_to_susu_group_account_widget)



        self.stacked_widget.addWidget(transfer_to_susu_group_account_widget)

        
    def handle_pin_input3(self, text):
        current_pin = self.sender()  # Get the sender QLineEdit
        index = self.pin3_boxes.index(current_pin)
        if len(text) == 1 and index < len(self.pin3_boxes) - 1:
            self.pin3_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.pin3_boxes) - 1:
            self.check_pin3()
               
    
       
       

    def perform_wallet_to_susu_group_account_transfer(self):
        receiver_acc1 = self.receiver1_acc_input.text()
        transfer_amount5 = self.transfer5_amount_input.text()


          # Validate inputs
        if not receiver_acc1 or not transfer_amount5:
            self.transfer5_notify_label.setText("Please fill in all fields.")
            self.transfer5_notify_label.show()
            return

        
        transfer_amount5 = Decimal(transfer_amount5)
        
            

        if transfer_amount5 <= 0:
            self.transfer5_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer5_notify_label.show()
            return
        
        if transfer_amount5 != "":
            
            self.pin_info_label3.show()
            self.pin_container3.show()
            self.pin_label3.show()
            self.receiver1_acc_input.hide()
            self.transfer5_amount_input.hide()
    
        self.transfer5_notify_label.hide()  

    
    def check_pin3(self):

        entered_pin3 = "".join(box.text() for box in self.pin3_boxes)
        entered_pin3 = self.sha512_64_hash(entered_pin3)
        print(f"Entered PIN: {entered_pin3}")
        print(f"Stored PIN: {self.get_susu_pin()}")
        stored_pin = self.get_susu_pin()
        receiver_acc1 = self.receiver1_acc_input.text()
        transfer_amount5 = self.transfer5_amount_input.text()
        transfer_amount5 = Decimal(transfer_amount5)

        cursor = self.db.cursor()

       
        if entered_pin3 == stored_pin:
            

            cursor.execute("SELECT Balance FROM susu_account WHERE Member_ID =%s  AND Email = %s ",  (receiver_acc1, self.current_user_email,))
            receiver_result = cursor.fetchone()

            receiver_balance = receiver_result[0]

              # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            wallet_result = cursor.fetchone()
            
      
            # Convert the fetched amount to Decimal
            wallet_balance = wallet_result[0]


            
            if wallet_balance < transfer_amount5:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    
                    self.transfer5_amount_input.clear()
                    self.receiver1_acc_input.clear()
                    return
            


            # Perform the transfer
            new_wallet_balance = wallet_balance - transfer_amount5
            new_receiver_balance = receiver_balance + transfer_amount5

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_wallet_balance, self.current_user_email))
            self.db.commit()
            cursor.execute("UPDATE susu_account SET Balance = %s WHERE Email = %s", (new_receiver_balance, self.current_user_email))
            self.db.commit()

            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount5:.2f} To  {receiver_acc1},  completed successfully.")
            from_account = "Wallet"
            to_account = "Susu Account"
            from_account_id = self.phone_number
            Type = "Internal"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (transaction_date, from_account, to_account, from_account_id, transfer_amount5, receiver_acc1, transfer_amount5, transaction_id, Type, self.current_user_email,))
            self.load_transactions()
            self.db.commit()
            

        # Clear the input fields after successful transfer
            self.transfer5_amount_input.clear()
            self.receiver1_acc_input.clear()
            self.clear_pin_input3()  
            self.pin_info_label3.hide()
            self.pin_container3.hide()
            self.pin_label3.hide() 
            self.receiver1_acc_input.show()
            self.transfer5_amount_input.show()
            
        
        else:
        

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account2_result = cursor.fetchone()
            

            if not account2_result or account2_result[0] is None:
                QMessageBox.information(self, "Failed", "Please Activate Your Account By Setting Pin")
                self.clear_pin_input3()  
                return
            
            cursor.execute("SELECT Pin FROM susu_account WHERE Email = %s", (self.current_user_email ,))
            result = cursor.fetchone()
            
            
            if not result or not result[0]:  # PIN exists and is not empty
            # Account is activated, proceed to verify PIN
        
            # Account is not activated (PIN is empty), show appropriate message
                QMessageBox.warning(self, "Account Not Activated", "Please join a susu group to activate your account.")
                self.clear_pin_input3()  
                return
            
            # Check if receiver account exists and has sufficient funds
            cursor.execute("SELECT Balance FROM susu_account WHERE Member_ID =%s  AND Email = %s ",  (receiver_acc1, self.current_user_email,))
            receiver_result = cursor.fetchone()
            
            if not receiver_result:
               
               QMessageBox.information(self, "Failed", "Account not Found")
               self.clear_pin_input3()  
    
               return
            
            else :
                QMessageBox.warning(self, "Error", "Wrong Pin, Please try again")
                self.clear_pin_input3()
                
    

    def clear_pin_input3(self):
        for otp_box in self.pin3_boxes:
            otp_box.clear()  
       

   


    def transfer_to_my_account(self):   
        transfer_to_my_account_widget =QWidget()
        transfer_to_my_account_label = QLabel("<html><p> Funds to Transfer-To Own Account<p></html>", transfer_to_my_account_widget)
        transfer_to_my_account_label.setGeometry(350, 50, 600 , 80)
        transfer_to_my_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_to_my_account_label.setAlignment(Qt.AlignCenter)



        
        self.my_source_account_label = QLabel('<U> Select Source Account</>',transfer_to_my_account_widget)
        self.my_source_account_label.setGeometry(50, 180, 600, 80)
        self.my_source_account_label.setStyleSheet("background-color: transparent; color: white; padding: 20px; border-radius: 40px; font-size: 20pt;")
        self.my_source_account_label.setParent(transfer_to_my_account_widget) 


         
        from_saving_account_to_my_account_button = QPushButton(self)
        from_saving_account_to_my_account_button.setGeometry(50, 250, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        from_saving_account_to_my_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        from_saving_account_to_my_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        from_saving_account_to_my_account_button.setIcon(icon)

# Set the text for the button
        from_saving_account_to_my_account_button.setText(" | Saving Account")

        from_saving_account_to_my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(28))

        from_saving_account_to_my_account_button.setParent(transfer_to_my_account_widget)
        from_investment_account_to_my_account_button = QPushButton(self)
        from_investment_account_to_my_account_button.setGeometry(50, 330, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        from_investment_account_to_my_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        from_investment_account_to_my_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        from_investment_account_to_my_account_button.setIcon(icon)

# Set the text for the button
        from_investment_account_to_my_account_button.setText(" | Susu Account")

        from_investment_account_to_my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(29))

        from_investment_account_to_my_account_button.setParent(transfer_to_my_account_widget)

        mobile_wallet_to_my_account_button = QPushButton(self)
        mobile_wallet_to_my_account_button.setGeometry(50, 410, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        mobile_wallet_to_my_account_button.setIconSize(icon_size)
         # Set the icon position to the left side of the button
        mobile_wallet_to_my_account_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("money.png")
        mobile_wallet_to_my_account_button.setIcon(icon)

# Set the text for the button
        mobile_wallet_to_my_account_button.setText(" | Mobile Wallet")

        mobile_wallet_to_my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(30))

        mobile_wallet_to_my_account_button.setParent(transfer_to_my_account_widget)



        self.stacked_widget.addWidget(transfer_to_my_account_widget)

    def saving_to_my_account_transfer(self):

        saving_to_my_account_transfer_widget =QWidget()
        saving_to_my_account_transfer_label = QLabel("<html><p> Saving To Account Transfer<p></html>", saving_to_my_account_transfer_widget)
        saving_to_my_account_transfer_label.setGeometry(350, 50, 600 , 80)
        saving_to_my_account_transfer_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        saving_to_my_account_transfer_label.setAlignment(Qt.AlignCenter)

        
        self.sender1_acc_input = QLineEdit(self)
        self.sender1_acc_input.setGeometry(50, 200, 350, 50)
        self.sender1_acc_input.setPlaceholderText("Enter Account Number")
        self.sender1_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.sender1_acc_input.setClearButtonEnabled(True)
        self.sender1_acc_input.setParent(saving_to_my_account_transfer_widget)

        self.transfer_amount1_input = QLineEdit(self)
        self.transfer_amount1_input.setGeometry(50, 280, 350, 50)
        self.transfer_amount1_input.setPlaceholderText("Amount to Transfer")
        self.transfer_amount1_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer_amount1_input.setClearButtonEnabled(True)
        self.transfer_amount1_input.setParent(saving_to_my_account_transfer_widget)

        self.transfer1_button = QPushButton("Transfer", self)
        transfer1_button_width = 300
        transfer1_button_x = (self.width() - transfer1_button_width) // 3
        self.transfer1_button.setGeometry(transfer1_button_x, 450, transfer1_button_width, 70)
        self.transfer1_button.setStyleSheet("""
                                      QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                  }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                             }
                                           """)
        self.transfer1_button.clicked.connect(self.perform_saving_account_to_account_transfer)
        self.transfer1_button.setParent(saving_to_my_account_transfer_widget)


        self.transfer1_notify_label = QLabel("", self)
        self.transfer1_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer1_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer1_notify_label.setParent(saving_to_my_account_transfer_widget)

        self.transfer1_regenerate_otp_button = QPushButton(self)
        self.transfer1_regenerate_otp_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.transfer1_regenerate_otp_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.transfer1_regenerate_otp_button.setGeometry(410, 335, 40, 40)
        self.transfer1_regenerate_otp_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.transfer1_regenerate_otp_button.hide()
        self.transfer1_regenerate_otp_button.clicked.connect(self.generate_otp5)  # Connect the clicked signal
        self.transfer1_regenerate_otp_button.setParent(saving_to_my_account_transfer_widget)
        
        self.otp_generated5 = False
        self.otp5= ""

        #Create a QLabel for the information display 
        self.info_label5_widget = QWidget()
        self.info_label5 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label5_widget)
        self.info_label5.setAlignment(Qt.AlignCenter)
        self.info_label5.setGeometry(50,200,400,40)
        self.info_label5.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label5.hide() # Hide the info label initially
        self.info_label5.setParent(saving_to_my_account_transfer_widget)

        #create a container widget for the otp input
        self.container5 = QWidget()
        self.container5.setGeometry(50,235,400,100)
        self.container5.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container5.hide()
        self.container5.setParent(saving_to_my_account_transfer_widget)

        # Create a QVBoxLayout for the container
        self.container_layout5 = QVBoxLayout(self.container5)
        self.container_layout5.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp5_boxes = []
        for _ in range(6):
            otp5_box = QLineEdit(self.container5)
            otp5_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp5_box.setMaxLength(1)  # Limit input to one character
            otp5_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp5_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp5_box)
            self.otp5_boxes.append(otp5_box)
             # Connect textChanged signal to handle_otp_input slot
            otp5_box.textChanged.connect(self.handle_otp_input5)


        self.container_layout5.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label5_widget = QWidget()
        self.timer_label5 = QLabel("<html><p>Time remaining....60 seconds<p></html> ", self.timer_label5_widget)
        self.timer_label5.setAlignment(Qt.AlignCenter)
        self.timer_label5.setGeometry(50,335,360,40)
        self.timer_label5.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label5.hide()
        self.timer_label5.setParent(saving_to_my_account_transfer_widget)




        self.stacked_widget.addWidget(saving_to_my_account_transfer_widget)

        
    def handle_otp_input5(self, text):
        current_box5 = self.sender()  # Get the sender QLineEdit
        index = self.otp5_boxes.index(current_box5)
        if len(text) == 1 and index < len(self.otp5_boxes) - 1:
            self.otp5_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp5_boxes) - 1:
            self.check_otp5()
               

    def update_timer5(self):
        self.time_left -= 1
        self.timer_label5.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input5()
            self.otp_generated5
            self.otp_generated5 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         

       
       

    def perform_saving_account_to_account_transfer(self):
        sender_acc1 = self.sender1_acc_input.text()
        transfer_amount1 = self.transfer_amount1_input.text()


          # Validate inputs
        if not sender_acc1 or not transfer_amount1:
            self.transfer1_notify_label.setText("Please fill in all fields.")
            self.transfer1_notify_label.show()
            return

        try:
            transfer_amount1 = Decimal(transfer_amount1)
        except ValueError:
            self.transfer1_notify_label.setText("Please enter a valid amount.")
            self.transfer1_notify_label.show()
            return

        if transfer_amount1 <= 0:
            self.transfer1_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer1_notify_label.show()
            return
        
        if transfer_amount1 != "":
            self.generate_otp5()
            self.otp_generated5 = True
            self.info_label5.show()
            self.container5.show()
            self.timer_label5.show()
            self.transfer1_regenerate_otp_button.show()
            self.transfer1_notify_label.setText("")
            self.sender1_acc_input.hide()
            self.transfer_amount1_input.hide()
      
            self.start_timer5()

        self.transfer1_notify_label.hide()  

    def perform_transaction1(self):    
        sender_acc1 = self.sender1_acc_input.text()
        transfer_amount1 = self.transfer_amount1_input.text()

        transfer_amount1 = Decimal(transfer_amount1)

        


        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account1_result = cursor.fetchone()

            if not account1_result or account1_result[0] is None:
                self.transfer1_notify_label.setText("Please activate your account by setting a PIN.")
                self.transfer1_notify_label.show()
                return


            # Check if sender account exists and has sufficient funds
            cursor.execute("SELECT Amount FROM saving_accountdb WHERE Account_ID = %s", (sender_acc1,))
            sender_result = cursor.fetchone()

            if not sender_result:
               
               QMessageBox.information(self, "Failed", "Account not Found")

               return
            
            sender1_balance = sender_result[0]

            if sender1_balance < transfer_amount1:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    self.transfer_amount1_input.clear()
                    self.sender1_acc_input.clear()
                    return
            

                
            
            
            # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account1_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            account1_balance = account1_result[0]


            # Perform the transfer
            new_sender1_balance = sender1_balance - transfer_amount1
            new_account1_balance = account1_balance + transfer_amount1

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_account1_balance, self.current_user_email))
            self.db.commit()
            cursor.execute("UPDATE saving_accountdb SET Amount = %s WHERE Email = %s", (new_sender1_balance, self.current_user_email))
            self.db.commit()

            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount1:.2f} from  {sender_acc1} to Wallet,  completed successfully.")

            from_account = "Saving Account"
            to_account = "Wallet"
            to_account_id = self.phone_number
            Type = "Internal"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (transaction_date, from_account, to_account, sender_acc1, transfer_amount1, to_account_id, transfer_amount1, transaction_id, Type,self.current_user_email,))
            self.load_transactions()
            self.db.commit()

        # Clear the input fields after successful transfer
            self.transfer_amount1_input.clear()
            self.sender1_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from saving Account to Wallet")    

    def start_timer5(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer5)
        self.timer.start(1000)  # Update timer every  


    def generate_otp5(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp5 = str(random.randint(100000, 999999))
        QMessageBox.information(self, "OTP", f"Sending OTP to {email}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp5}
For security reasons, do not share
this code with anyone. Enter this code 
to perform the transaction""")
        
        QMessageBox.information(self, "OTP", f"Sending OTP to {number}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp5}
For security reasons, do not share
this code with anyone. Enter this code 
to perform the transaction""") # Print the generated OTP
        self.start_timer5()

    

    def clear_otp_input5(self):
        for otp_box in self.otp5_boxes:
            otp_box.clear()  
       
        

    

    def check_otp5(self):
        entered_otp = "".join(box.text() for box in self.otp5_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input5()
           self.otp_generated5 = False
           return
           
        if entered_otp == self.otp5:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input5()
            
            self.info_label5.hide()
            self.container5.hide()
            self.timer_label5.hide()
            self.transfer1_regenerate_otp_button.hide()
            self.timer.stop() 
            self.sender1_acc_input.show()
            self.transfer_amount1_input.show()
            self.perform_transaction1()
            
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input5()
            self.otp_generated4 = False   



    def susu_to_my_wallet_transfer(self):


        susu_to_my_wallet_transfer_widget =QWidget()
        susu_to_my_wallet_transfer_label = QLabel("<html><p> Susu To Wallet Transfer<p></html>", susu_to_my_wallet_transfer_widget)
        susu_to_my_wallet_transfer_label.setGeometry(350, 50, 600 , 80)
        susu_to_my_wallet_transfer_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        susu_to_my_wallet_transfer_label.setAlignment(Qt.AlignCenter)

        
        self.sender2_acc_input = QLineEdit(self)
        self.sender2_acc_input.setGeometry(50, 200, 350, 50)
        self.sender2_acc_input.setPlaceholderText("Member ID")
        self.sender2_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.sender2_acc_input.setClearButtonEnabled(True)
        self.sender2_acc_input.setParent(susu_to_my_wallet_transfer_widget)

        self.transfer_amount2_input = QLineEdit(self)
        self.transfer_amount2_input.setGeometry(50, 280, 350, 50)
        self.transfer_amount2_input.setPlaceholderText("Amount to Transfer")
        self.transfer_amount2_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer_amount2_input.setClearButtonEnabled(True)
        self.transfer_amount2_input.setParent(susu_to_my_wallet_transfer_widget)

        self.transfer2_button = QPushButton("Transfer", self)
        transfer2_button_width = 300
        transfer2_button_x = (self.width() - transfer2_button_width) // 3
        self.transfer2_button.setGeometry(transfer2_button_x, 450, transfer2_button_width, 70)
        self.transfer2_button.setStyleSheet("""
                                      QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                  }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                             }
                                           """)
        self.transfer2_button.clicked.connect(self.perform_susu_account_to_wallet_transfer)
        self.transfer2_button.setParent(susu_to_my_wallet_transfer_widget)

        self.transfer2_notify_label = QLabel("", self)
        self.transfer2_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer2_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer2_notify_label.setParent(susu_to_my_wallet_transfer_widget)

        self.transfer2_regenerate_otp_button = QPushButton(self)
        self.transfer2_regenerate_otp_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.transfer2_regenerate_otp_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.transfer2_regenerate_otp_button.setGeometry(410, 335, 40, 40)
        self.transfer2_regenerate_otp_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.transfer2_regenerate_otp_button.hide()
        self.transfer2_regenerate_otp_button.clicked.connect(self.generate_otp7)  # Connect the clicked signal
        self.transfer2_regenerate_otp_button.setParent(susu_to_my_wallet_transfer_widget)
        
        self.otp_generated7 = False
        self.otp7= ""

        #Create a QLabel for the information display 
        self.info_label7_widget = QWidget()
        self.info_label7 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label7_widget)
        self.info_label7.setAlignment(Qt.AlignCenter)
        self.info_label7.setGeometry(50,200,400,40)
        self.info_label7.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label7.hide() # Hide the info label initially
        self.info_label7.setParent(susu_to_my_wallet_transfer_widget)

        #create a container widget for the otp input
        self.container7 = QWidget()
        self.container7.setGeometry(50,235,400,100)
        self.container7.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container7.hide()
        self.container7.setParent(susu_to_my_wallet_transfer_widget)

        # Create a QVBoxLayout for the container
        self.container_layout7 = QVBoxLayout(self.container7)
        self.container_layout7.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp7_boxes = []
        for _ in range(6):
            otp7_box = QLineEdit(self.container7)
            otp7_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp7_box.setMaxLength(1)  # Limit input to one character
            otp7_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp7_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp7_box)
            self.otp7_boxes.append(otp7_box)
             # Connect textChanged signal to handle_otp_input slot
            otp7_box.textChanged.connect(self.handle_otp_input7)


        self.container_layout7.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label7_widget = QWidget()
        self.timer_label7 = QLabel("<html><p>Time remaining....60 seconds<p></html> ", self.timer_label7_widget)
        self.timer_label7.setAlignment(Qt.AlignCenter)
        self.timer_label7.setGeometry(50,335,360,40)
        self.timer_label7.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label7.hide()
        self.timer_label7.setParent(susu_to_my_wallet_transfer_widget)


        self.stacked_widget.addWidget(susu_to_my_wallet_transfer_widget)

    def handle_otp_input7(self, text):
        current_box = self.sender()  # Get the sender QLineEdit
        index = self.otp7_boxes.index(current_box)
        if len(text) == 1 and index < len(self.otp7_boxes) - 1:
            self.otp7_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp7_boxes) - 1:
            self.check_otp7()
               

    def update_timer7(self):
        self.time_left -= 1
        self.timer_label7.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input7()
            self.otp_generated7
            self.otp_generated7 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         

       
       

    def perform_susu_account_to_wallet_transfer(self):
        sender_acc2 = self.sender2_acc_input.text()
        transfer_amount2 = self.transfer_amount2_input.text()


          # Validate inputs
        if not sender_acc2 or not transfer_amount2:
            self.transfer2_notify_label.setText("Please fill in all fields.")
            self.transfer2_notify_label.show()
            return

        try:
            transfer_amount2 = Decimal(transfer_amount2)
        except ValueError:
            self.transfer2_notify_label.setText("Please enter a valid amount.")
            self.transfer2_notify_label.show()
            return

        if transfer_amount2 <= 0:
            self.transfer2_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer2_notify_label.show()
            return
        
        if transfer_amount2 != "":
            self.generate_otp7()
            self.otp_generated7 = True
            self.info_label7.show()
            self.container7.show()
            self.timer_label7.show()
            self.transfer2_regenerate_otp_button.show()
            self.transfer2_notify_label.setText("")
            self.sender2_acc_input.hide()
            self.transfer_amount2_input.hide()
      
            self.start_timer7()

        self.transfer2_notify_label.hide()  

    def perform_transaction6(self):    
        sender_acc2 = self.sender2_acc_input.text()
        transfer_amount2 = self.transfer_amount2_input.text()

        transfer_amount2 = Decimal(transfer_amount2)

        


        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account2_result = cursor.fetchone()

            if not account2_result or account2_result[0] is None:
                QMessageBox.information(self, "Error","Please activate your account by setting a PIN.")
                
                return


            # Check if sender account exists and has sufficient funds
            cursor.execute("SELECT Balance FROM susu_account WHERE member_id = %s", (sender_acc2,))
            sender_result = cursor.fetchone()

            if not sender_result:
               
               QMessageBox.information(self, "Failed", "Account not Found")
               self.sender2_acc_input.clear()
               self.transfer_amount2_input.clear()
               return
            
            sender2_balance = sender_result[0]

            if sender2_balance < transfer_amount2:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    self.transfer_amount2_input.clear()
                    self.sender2_acc_input.clear()
                    return
            

                
            
            
            # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account1_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            account1_balance = account1_result[0]


            # Perform the transfer
            new_sender2_balance = sender2_balance - transfer_amount2
            new_account1_balance = account1_balance + transfer_amount2

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_account1_balance, self.current_user_email))
            self.db.commit()
            cursor.execute("UPDATE susu_account SET Balance = %s WHERE Email = %s", (new_sender2_balance, self.current_user_email))
            self.db.commit()

            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount2:.2f} from  {sender_acc2} to Wallet,  completed successfully.")

            from_account = "Susu Account"
            to_account = "Wallet"
            to_account_id = self.phone_number
            Type = "Internal"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (transaction_date, from_account, to_account, sender_acc2, transfer_amount2, to_account_id, transfer_amount2, transaction_id, Type,self.current_user_email,))
            self.load_transactions()
            self.db.commit()

        # Clear the input fields after successful transfer
            self.transfer_amount2_input.clear()
            self.sender2_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from saving Account to Wallet")    

    def start_timer7(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer7)
        self.timer.start(1000)  # Update timer every  


    def generate_otp7(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp7 = str(random.randint(100000, 999999))
        QMessageBox.information( self, "OTP", f"Sending OTP to {email}")
        QMessageBox.information( self, "OTP", f"""Your Verification code: {self.otp7}
For security reasons, do not share
this code with anyone. Enter this code 
to perform the transaction""") 
        QMessageBox.information( self, "OTP", f"Sending OTP to {number}")
        QMessageBox.information( self, "OTP", f"""Your Verification code: {self.otp7}
For security reasons, do not share
this code with anyone. Enter this code 
to perform the transaction""") # Print the generated OTP
        self.start_timer7()

    

    def clear_otp_input7(self):
        for otp_box in self.otp7_boxes:
            otp_box.clear()  
       
        

    

    def check_otp7(self):
        entered_otp = "".join(box.text() for box in self.otp7_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input7()
           self.otp_generated7 = False
           return
           
        if entered_otp == self.otp7:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input7()
            
            self.info_label7.hide()
            self.container7.hide()
            self.timer_label7.hide()
            self.transfer2_regenerate_otp_button.hide()
            self.timer.stop() 
            self.sender2_acc_input.show()
            self.transfer_amount2_input.show()
            self.perform_transaction6()
            
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input5()
            self.otp_generated4 = False   

    def mobile_wallet_to_account_transfer(self):


    
        mobile_wallet_to_account_transfer_widget =QWidget()
        mobile_wallet_to_account_transfer_label = QLabel("<html><p> Mobile Wallet To Account Transfer<p></html>", mobile_wallet_to_account_transfer_widget)
        mobile_wallet_to_account_transfer_label.setGeometry(350, 50, 600 , 80)
        mobile_wallet_to_account_transfer_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        mobile_wallet_to_account_transfer_label.setAlignment(Qt.AlignCenter)

        
        self.sender3_acc_input = QLineEdit(self)
        self.sender3_acc_input.setGeometry(50, 200, 350, 50)
        self.sender3_acc_input.setPlaceholderText("Enter Mobile Number")
        self.sender3_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.sender3_acc_input.setClearButtonEnabled(True)
        self.sender3_acc_input.setParent(mobile_wallet_to_account_transfer_widget)

        self.transfer_amount3_input = QLineEdit(self)
        self.transfer_amount3_input.setGeometry(50, 280, 350, 50)
        self.transfer_amount3_input.setPlaceholderText("Amount to Transfer")
        self.transfer_amount3_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer_amount3_input.setClearButtonEnabled(True)
        self.transfer_amount3_input.setParent(mobile_wallet_to_account_transfer_widget)

        self.transfer3_button = QPushButton("Transfer", self)
        transfer3_button_width = 300
        transfer3_button_x = (self.width() - transfer3_button_width) // 3
        self.transfer3_button.setGeometry(transfer3_button_x, 450, transfer3_button_width, 70)
        self.transfer3_button.setStyleSheet("""
                                      QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                  }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                             }
                                           """)
        self.transfer3_button.clicked.connect(self.perform_mobile_wallet_to_account_transfer)
        self.transfer3_button.setParent(mobile_wallet_to_account_transfer_widget)

        self.transfer3_notify_label = QLabel("", self)
        self.transfer3_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer3_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer3_notify_label.setParent(mobile_wallet_to_account_transfer_widget)

        self.stacked_widget.addWidget(mobile_wallet_to_account_transfer_widget)
    

    def perform_mobile_wallet_to_account_transfer(self):
        mobile_number3 = self.sender3_acc_input.text()
        transfer_amount3 = self.transfer_amount3_input.text()


          # Validate inputs
        if not mobile_number3 or not transfer_amount3:
            self.transfer3_notify_label.setText("Please fill in all fields.")
            self.transfer3_notify_label.show()
            return

        try:
            transfer_amount3 = Decimal(transfer_amount3)
        except ValueError:
            self.transfer3_notify_label.setText("Please enter a valid amount.")
            self.transfer3_notify_label.show()
            return

        if transfer_amount3 <= 0:
            self.transfer3_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer3_notify_label.show()
            return

        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT Pin FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account_result = cursor.fetchone()

            if not account_result or account_result[0] is None:
                self.transfer3_notify_label.setText("Please activate your account by setting a PIN.")
                self.transfer3_notify_label.show()
                return
            
            # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            account_balance = account_result[0]


            # Perform the transfer
            new_account_balance = account_balance + transfer_amount3

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_account_balance, self.current_user_email))
            self.db.commit()

            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount3:.2f} from mobile wallet to Account completed successfully.")
    
            from_account = "Mobile Wallet"
            to_account = "Wallet"
            to_account_id = self.phone_number
            Type = "External"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (transaction_date, from_account, to_account, mobile_number3, transfer_amount3, to_account_id, transfer_amount3, transaction_id, Type,self.current_user_email,))
            self.load_transactions()
            self.db.commit()
            

        # Clear the input fields after successful transfer
            self.transfer_amount3_input.clear()
            self.sender3_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from mobile wallet to Account")



    def another_account_page(self):
        another_account_widget =QWidget()
        another_account_label = QLabel("<html><p> Funds to Transfer-To Inter Account<p></html>", another_account_widget)
        another_account_label.setGeometry(350, 50, 600 , 80)
        another_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        another_account_label.setAlignment(Qt.AlignCenter)


        self.receiver3_acc_input = QLineEdit(self)
        self.receiver3_acc_input.setGeometry(50, 200, 350, 50)
        self.receiver3_acc_input.setPlaceholderText("Enter Mobile Number")
        self.receiver3_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.receiver3_acc_input.setClearButtonEnabled(True)
        self.receiver3_acc_input.setParent(another_account_widget)


        self.transfer7_amount_input = QLineEdit(self)
        self.transfer7_amount_input.setGeometry(50, 280, 350, 50)
        self.transfer7_amount_input.setPlaceholderText("Amount to Transfer")
        self.transfer7_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer7_amount_input.setClearButtonEnabled(True)
        self.transfer7_amount_input.setParent(another_account_widget)

        self.transfer7_button = QPushButton("Transfer", self)
        transfer7_button_width = 300
        transfer7_button_x = (self.width() - transfer7_button_width) // 3
        self.transfer7_button.setGeometry(transfer7_button_x, 450, transfer7_button_width, 70)
        self.transfer7_button.setStyleSheet("""
                                           QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                        }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                        }
                                          """)
        self.transfer7_button.clicked.connect(self.perform_wallet_to_inter_wallet_transfer)
        self.transfer7_button.setParent(another_account_widget)

        self.transfer7_notify_label = QLabel("", self)
        self.transfer7_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer7_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer7_notify_label.setParent(another_account_widget)


        #Create a QLabel for the information display 
        self.pin_info_label1_widget = QWidget()
        self.pin_info_label1 = QLabel("<html><p>Enter Your Pin<p></html> ", self.pin_info_label1_widget)
        self.pin_info_label1.setAlignment(Qt.AlignCenter)
        self.pin_info_label1.setGeometry(50,200,400,40)
        self.pin_info_label1.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_info_label1.hide() # Hide the info label initially
        self.pin_info_label1.setParent(another_account_widget)

        #create a container widget for the otp input
        self.pin_container1 = QWidget()
        self.pin_container1.setGeometry(50,235,400,100)
        self.pin_container1.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.pin_container1.hide()
        self.pin_container1.setParent(another_account_widget)

        # Create a QVBoxLayout for the container
        self.pin_container_layout1 = QVBoxLayout(self.pin_container1)
        self.pin_container_layout1.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.pin1_boxes = []
        for _ in range(4):
            pin1_box = QLineEdit(self.pin_container1)
            pin1_box.setFixedSize(50, 50)  # Set fixed size for each box
            pin1_box.setMaxLength(1)  # Limit input to one character
            pin1_box.setAlignment(Qt.AlignCenter)  # Center align text
            pin1_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(pin1_box)
            self.pin1_boxes.append(pin1_box)
             # Connect textChanged signal to handle_otp_input slot
            pin1_box.textChanged.connect(self.handle_pin_input1)


        self.pin_container_layout1.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.pin_label1_widget = QWidget()
        self.pin_label1 = QLabel("", self.pin_label1_widget)
        self.pin_label1.setAlignment(Qt.AlignCenter)
        self.pin_label1.setGeometry(50,335,400,40)
        self.pin_label1.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_label1.hide()
        self.pin_label1.setParent(another_account_widget)

        
        self.stacked_widget.addWidget(another_account_widget)


         
    def handle_pin_input1(self, text):
        current_pin = self.sender()  # Get the sender QLineEdit
        index = self.pin1_boxes.index(current_pin)
        if len(text) == 1 and index < len(self.pin1_boxes) - 1:
            self.pin1_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.pin1_boxes) - 1:
            self.check_pin1()
               

       
       
    def perform_wallet_to_inter_wallet_transfer(self):   
    
        receiver_acc3 = self.receiver3_acc_input.text()
        transfer_amount7 = self.transfer7_amount_input.text()


          # Validate inputs
        if not receiver_acc3 or not transfer_amount7:
            self.transfer7_notify_label.setText("Please fill in all fields.")
            self.transfer7_notify_label.show()
            return

        try:
            transfer_amount7 = Decimal(transfer_amount7)
        except ValueError:
            self.transfer7_notify_label.setText("Please enter a valid amount.")
            self.transfer7_notify_label.show()
            return

        if transfer_amount7 <= 0:
            self.transfer7_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer7_notify_label.show()
            return
        
        if transfer_amount7 != "":
            
            self.pin_info_label1.show()
            self.pin_container1.show()
            self.pin_label1.show()
            self.receiver3_acc_input.hide()
            self.transfer7_amount_input.hide()
      
            

        self.transfer7_notify_label.hide()  

    def perform_transaction3(self):    
        receiver_acc3 = self.receiver3_acc_input.text()
        transfer_amount7 = self.transfer7_amount_input.text()

        transfer_amount7 = Decimal(transfer_amount7)

        


        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account3_result = cursor.fetchone()

            if not account3_result or account3_result[0] is None:
                QMessageBox.information(self, "Failed", "Please Activate Your Account By Setting Pin")

                return


            # Check if receiver account exists and has sufficient funds
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Phonenumber=%s",  (receiver_acc3,))
            receiver_result = cursor.fetchone()

            if not receiver_result:
               
               QMessageBox.information(self, "Failed", "Account not Found")

               return
            
            receiver_balance = receiver_result[0]



            # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            wallet_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            wallet_balance = wallet_result[0]





            if wallet_balance < transfer_amount7:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    
                    self.transfer7_amount_input.clear()
                    self.receiver3_acc_input.clear()
                    return
            


            # Perform the transfer
            new_wallet_balance = wallet_balance - transfer_amount7
            new_receiver_balance = receiver_balance + transfer_amount7

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_wallet_balance, self.current_user_email))
            self.db.commit()
            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Phonenumber = %s", (new_receiver_balance, receiver_acc3))
            self.db.commit()

            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount7:.2f} To  {receiver_acc3},  completed successfully.")

            from_account = "Wallet"
            to_account = "Inter-Wallet"
            from_account_id = self.phone_number
            Type = "External"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (transaction_date, from_account, to_account, from_account_id, transfer_amount7, receiver_acc3, transfer_amount7, transaction_id, Type,self.current_user_email,))
            self.load_transactions()
            self.db.commit()

        # Clear the input fields after successful transfer
            self.transfer7_amount_input.clear()
            self.receiver3_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from saving Account to Wallet")    


    def clear_pin_input1(self):
        for otp_box in self.pin1_boxes:
            otp_box.clear()  
       
    

    def check_pin1(self):
        entered_pin1 = "".join(box.text() for box in self.pin1_boxes)
        entered_pin1 = self.sha512_64_hash(entered_pin1)

        
        
        if entered_pin1 == self.get_pin():
            
            
            self.clear_pin_input1()
            
            self.pin_info_label1.hide()
            self.pin_container1.hide()
            self.pin_label1.hide() 
            self.receiver3_acc_input.show()
            self.transfer7_amount_input.show()
            self.perform_transaction3()
            
        else:
            QMessageBox.warning(self, "Error", "Wrong Pin, Please try again")
            self.clear_pin_input1()    
    


    def wallet_page(self):
        wallet_widget =QWidget()
        wallet_label = QLabel("<html><p> Funds Transfer-To Wallet<p></html>", wallet_widget)
        wallet_label.setGeometry(350, 50, 600 , 80)
        wallet_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        wallet_label.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(wallet_widget)

        

        self.receiver2_acc_input = QLineEdit(self)
        self.receiver2_acc_input.setGeometry(50, 200, 350, 50)
        self.receiver2_acc_input.setPlaceholderText("Mobile Number")
        self.receiver2_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.receiver2_acc_input.setClearButtonEnabled(True)
        self.receiver2_acc_input.setParent(wallet_widget)


        self.transfer6_amount_input = QLineEdit(self)
        self.transfer6_amount_input.setGeometry(50, 280, 350, 50)
        self.transfer6_amount_input.setPlaceholderText("Amount to Transfer")
        self.transfer6_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer6_amount_input.setClearButtonEnabled(True)
        self.transfer6_amount_input.setParent(wallet_widget)

        self.transfer6_button = QPushButton("Transfer", self)
        transfer6_button_width = 300
        transfer6_button_x = (self.width() - transfer6_button_width) // 3
        self.transfer6_button.setGeometry(transfer6_button_x, 450, transfer6_button_width, 70)
        self.transfer6_button.setStyleSheet("""
                                           QPushButton {
                                           background-color: blue;
                                           font-size: 18pt;
                                           border-radius: 35px;
                                                        }
                                           QPushButton:hover {
                                           background-color: #333333;
                                                        }
                                          """)
        self.transfer6_button.clicked.connect(self.perform_wallet_to_mobile_wallet_transfer)
        self.transfer6_button.setParent(wallet_widget)

        self.transfer6_notify_label = QLabel("", self)
        self.transfer6_notify_label.setGeometry(50, 380, 600, 50)
        self.transfer6_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer6_notify_label.setParent(wallet_widget)

         #Create a QLabel for the information display 
        self.pin_info_label2_widget = QWidget()
        self.pin_info_label2 = QLabel("<html><p>Enter Your Pin<p></html> ", self.pin_info_label2_widget)
        self.pin_info_label2.setAlignment(Qt.AlignCenter)
        self.pin_info_label2.setGeometry(50,200,400,40)
        self.pin_info_label2.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_info_label2.hide() # Hide the info label initially
        self.pin_info_label2.setParent(wallet_widget)

        #create a container widget for the otp input
        self.pin_container2 = QWidget()
        self.pin_container2.setGeometry(50,235,400,100)
        self.pin_container2.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.pin_container2.hide()
        self.pin_container2.setParent(wallet_widget)

        # Create a QVBoxLayout for the container
        self.pin_container_layout2 = QVBoxLayout(self.pin_container2)
        self.pin_container_layout2.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.pin2_boxes = []
        for _ in range(4):
            pin2_box = QLineEdit(self.pin_container2)
            pin2_box.setFixedSize(50, 50)  # Set fixed size for each box
            pin2_box.setMaxLength(1)  # Limit input to one character
            pin2_box.setAlignment(Qt.AlignCenter)  # Center align text
            pin2_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(pin2_box)
            self.pin2_boxes.append(pin2_box)
             # Connect textChanged signal to handle_otp_input slot
            pin2_box.textChanged.connect(self.handle_pin_input2)


        self.pin_container_layout2.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.pin_label2_widget = QWidget()
        self.pin_label2 = QLabel("", self.pin_label2_widget)
        self.pin_label2.setAlignment(Qt.AlignCenter)
        self.pin_label2.setGeometry(50,335,400,40)
        self.pin_label2.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.pin_label2.hide()
        self.pin_label2.setParent(wallet_widget)


        self.stacked_widget.addWidget(wallet_widget)
    
    def handle_pin_input2(self, text):
        current_pin = self.sender()  # Get the sender QLineEdit
        index = self.pin2_boxes.index(current_pin)
        if len(text) == 1 and index < len(self.pin2_boxes) - 1:
            self.pin2_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.pin2_boxes) - 1:
            self.check_pin2()
               

       
       
    def perform_wallet_to_mobile_wallet_transfer(self):   
    
        receiver_acc2 = self.receiver2_acc_input.text()
        transfer_amount6 = self.transfer6_amount_input.text()


          # Validate inputs
        if not receiver_acc2 or not transfer_amount6:
            self.transfer6_notify_label.setText("Please fill in all fields.")
            self.transfer6_notify_label.show()
            return

        try:
            transfer_amount6 = Decimal(transfer_amount6)
        except ValueError:
            self.transfer6_notify_label.setText("Please enter a valid amount.")
            self.transfer6_notify_label.show()
            return

        if transfer_amount6 <= 0:
            self.transfer6_notify_label.setText("Transfer amount must be greater than zero.")
            self.transfer6_notify_label.show()
            return
        
        if transfer_amount6 != "":
            
            self.pin_info_label2.show()
            self.pin_container2.show()
            self.pin_label2.show()
            self.receiver2_acc_input.hide()
            self.transfer6_amount_input.hide()
      
            

        self.transfer6_notify_label.hide()  

    def perform_transaction4(self):    
        receiver_acc2 = self.receiver2_acc_input.text()
        transfer_amount6 = self.transfer6_amount_input.text()

        transfer_amount6 = Decimal(transfer_amount6)

        


        try:
            cursor = self.db.cursor()

        # Check if the account has a PIN set
            cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            account3_result = cursor.fetchone()

            if not account3_result or account3_result[0] is None:
                QMessageBox.information(self, "Failed", "Please Activate Your Account By Setting Pin")

                return




            # Check if the user's bank account exists and get the current balance
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s", (self.current_user_email,))
            wallet_result = cursor.fetchone()

            # Convert the fetched amount to Decimal
            wallet_balance = wallet_result[0]





            if wallet_balance < transfer_amount6:
                    QMessageBox.information(self, "Failed", "Insufficient Balance")
                    
                    self.transfer6_amount_input.clear()
                    self.receiver2_acc_input.clear()
                    return
            


            # Perform the transfer
            new_wallet_balance = wallet_balance - transfer_amount6
            

            cursor.execute("UPDATE my_accountdb SET Balance = %s WHERE Email = %s", (new_wallet_balance, self.current_user_email))
            self.db.commit()
            
            QMessageBox.information(self, "Success", f"Transfer of Gh¢ {transfer_amount6:.2f} To  {receiver_acc2},  completed successfully.")

            from_account = "Wallet"
            to_account = "Mobile Wallet"
            from_account_id = self.phone_number
            Type = "External"
            
             # Generate unique transaction ID
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
               # Insert the transaction record
            cursor.execute("""
                         INSERT INTO transactionsdb (Date, From_Account, To_Account, From_Account_ID, Debit, To_Account_ID, Credit, Transaction_ID, Type_, Email)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s. %s)
            """, (transaction_date, from_account, to_account, from_account_id, transfer_amount6, receiver_acc2, transfer_amount6, transaction_id, Type, self.current_user_email,))
            self.load_transactions()
            self.db.commit()

        # Clear the input fields after successful transfer
            self.transfer6_amount_input.clear()
            self.receiver2_acc_input.clear()

        except mysql.connector.Error as e:
            QMessageBox.information(self, "Failed", "Error tranfering from saving Account to Wallet")    



    

    def clear_pin_input2(self):
        for otp_box in self.pin2_boxes:
            otp_box.clear()  
       
        

    

    def check_pin2(self):
        entered_pin2 = "".join(box.text() for box in self.pin2_boxes)
        entered_pin2 = self.sha512_64_hash(entered_pin2)

       
        if entered_pin2 == self.get_pin():
            
            
            self.clear_pin_input2()
            
            self.pin_info_label2.hide()
            self.pin_container2.hide()
            self.pin_label2.hide() 
            self.receiver2_acc_input.show()
            self.transfer6_amount_input.show()
            self.perform_transaction4()
            
        else:
            QMessageBox.warning(self, "Error", "Wrong Pin, Please try again")
            self.clear_pin_input2()    
   

                    
        
    def loan_page(self):
        loan_widget =QWidget()
        loan_label = QLabel("<html><p> Loan <p></html>", loan_widget)
        loan_label.setGeometry(350, 50, 600 , 80)
        loan_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        loan_label.setAlignment(Qt.AlignCenter)


        
        loan_balance_button = QPushButton(self)
        loan_balance_button.setGeometry(50, 200, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        loan_balance_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        loan_balance_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("payment.png")
        loan_balance_button.setIcon(icon)

# Set the text for the button
        loan_balance_button.setText(" | Check Loan Account Balance")

        loan_balance_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(16))

        loan_balance_button.setParent(loan_widget)


        loan_request_button = QPushButton(self)
        loan_request_button.setGeometry(50, 280, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        loan_request_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        loan_request_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("payment.png")
        loan_request_button.setIcon(icon)

# Set the text for the button
        loan_request_button.setText(" | Loan Request")

        loan_request_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(17))

        loan_request_button.setParent(loan_widget)




        self.stacked_widget.addWidget(loan_widget)


    def loan_balance_page(self):
        loan_balance_widget = QWidget()
       
        loan_balance_label = QLabel("<html><p>Check Loan Account Balance<p></>", loan_balance_widget)
        loan_balance_label.setGeometry(350,50,600,80)
        loan_balance_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        loan_balance_label.setAlignment(Qt.AlignCenter)

       # profile_layout.addWidget(welcome_label)


        loan_balance_label1 = QLabel("<html><p>You are not eligible for loan<p></>", loan_balance_widget)
        loan_balance_label1.setGeometry(350,350,600,200)
        loan_balance_label1.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        loan_balance_label1.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
       

        self.stacked_widget.addWidget(loan_balance_widget)    


    def loan_request_page(self):
        loan_request_widget = QWidget()
       
        loan_request_label = QLabel("<html><p>Loan Request<p></>", loan_request_widget)
        loan_request_label.setGeometry(350,50,600,80)
        loan_request_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        loan_request_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)


        loan_request_label1 = QLabel("<html><p>You are not eligible for loan<p></>", loan_request_widget)
        loan_request_label1.setGeometry(350,350,600,200)
        loan_request_label1.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        loan_request_label1.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
       
       

        self.stacked_widget.addWidget(loan_request_widget)      
    


    def profile_page(self):
        profile_widget =QWidget()
        profile_label = QLabel("<html><p> My Profile <p></html>", profile_widget)
        profile_label.setGeometry(350, 50, 600 , 80)
        profile_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        profile_label.setAlignment(Qt.AlignCenter)

        
#         Add an edit profile button

        edit_profile_button = QPushButton(self)
        edit_profile_button.setGeometry(50, 200, 500, 50)
        icon = QIcon("user.png")                  
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        edit_profile_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        edit_profile_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("user.png")
        edit_profile_button.setIcon(icon)

# Set the text for the button
        edit_profile_button.setText(" | Edit Profile")

        edit_profile_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))
        edit_profile_button.setParent(profile_widget)

        self.stacked_widget.addWidget(profile_widget)

# Change Password

        password_button = QPushButton(self)
        password_button.setGeometry(50, 280, 500, 50)
        icon = QIcon("padlock.png")                  
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        password_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        password_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("padlock.png")
        password_button.setIcon(icon)

# Set the text for the button
        password_button.setText(" | Change Login Password")

        password_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(8))
        password_button.setParent(profile_widget)



                    
        change_pin_button = QPushButton(self)
        change_pin_button.setGeometry(50, 360, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        change_pin_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        change_pin_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("padlock.png")
        change_pin_button.setIcon(icon)

# Set the text for the button
        change_pin_button.setText(" | Change Pin ")

        change_pin_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(24))

        change_pin_button.setParent(profile_widget)



        # Notification 

        notification_button = QPushButton(self)
        notification_button.setGeometry(50, 440, 500, 50)
                   
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        notification_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        notification_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("notification-bell.png")
        notification_button.setIcon(icon)

# Set the text for the button
        notification_button.setText(" | Notification Option")

        notification_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(19))
        notification_button.setParent(profile_widget)


        self.stacked_widget.addWidget(profile_widget)

    def change_pin_page(self, db, current_user_email, Phonenumber):
        self.current_user_email = current_user_email
        self.phone_number = Phonenumber
        self.db = db

        change_pin_widget = QWidget()
        change_pin_label = QLabel("<html><p> Change pin <p></html>", change_pin_widget)
        change_pin_label.setGeometry( 350, 50, 600 , 80)
        change_pin_label.setStyleSheet( "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        change_pin_label.setAlignment(Qt.AlignCenter)





        self.current_pin_input = QLineEdit(self)
        self.current_pin_input.setGeometry(50, 200, 350, 50)
        # Set placeholder text for the password input field
        self.current_pin_input.setPlaceholderText("Enter Current Pin")
        # Appply styling to the password input field
        self.current_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.current_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.current_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.current_pin_input.setEchoMode(QLineEdit.Password)
        self.current_pin_input.editingFinished.connect(self.reset_current_pin_input_style)
        self.current_pin_input.setParent(change_pin_widget)


        # Create checkbox to toggle password visibility
        self.show_current_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_current_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_current_pin_checkbox.setGeometry(50, 247, 150 , 30)
        self.show_current_pin_checkbox.stateChanged.connect(self.toggle_current_pin_visibility)

        self.show_current_pin_checkbox.setParent(change_pin_widget)




          # Create a line edit for password input field
        self.new_update_pin_input = QLineEdit(self)
        self.new_update_pin_input.setGeometry(50, 300, 350, 50)
        # Set placeholder text for the password input field
        self.new_update_pin_input.setPlaceholderText("Enter New Pin")
        # Appply styling to the password input field
        self.new_update_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.new_update_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.new_update_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.new_update_pin_input.setEchoMode(QLineEdit.Password)
        self.new_update_pin_input.textChanged.connect(self.validate_new_update_pin)
        self.new_update_pin_input.editingFinished.connect(self.reset_new_update_pin_input_style)
        self.new_update_pin_input.setParent(change_pin_widget)


        # Create checkbox to toggle password visibility
        self.show_new_update_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_new_update_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_new_update_pin_checkbox.setGeometry(50, 347, 150 , 30)
        self.show_new_update_pin_checkbox.stateChanged.connect(self.toggle_new_update_pin_visibility)

        self.show_new_update_pin_checkbox.setParent(change_pin_widget)


            # Create a line edit for password input field
        self.confirm_update_pin_input = QLineEdit(self)
        self.confirm_update_pin_input.setGeometry(50, 400, 350, 50)
        # Set placeholder text for the password input field
        self.confirm_update_pin_input.setPlaceholderText("Confirm New Pin")
        # Appply styling to the password input field
        self.confirm_update_pin_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.confirm_update_pin_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.confirm_update_pin_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_update_pin_input.setEchoMode(QLineEdit.Password)
        self.confirm_update_pin_input.textChanged.connect(self.validate_confirm_update_pin)
        self.confirm_update_pin_input.editingFinished.connect(self.reset_confirm_update_pin_input_style)
        self.confirm_update_pin_input.setParent(change_pin_widget)


        # Create checkbox to toggle password visibility
        self.show_confirm_update_pin_checkbox = QCheckBox("Show Pin", self)
        self.show_confirm_update_pin_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_confirm_update_pin_checkbox.setGeometry(50, 447, 150 , 30)
        self.show_confirm_update_pin_checkbox.stateChanged.connect(self.toggle_confirm_update_pin_visibility)

        self.show_confirm_update_pin_checkbox.setParent(change_pin_widget)

           # Create QLabel for notification messages
        self.pin_notification_label = QLabel("", self)
        self.pin_notification_label.setGeometry(50, 520, 650, 50)
        self.pin_notification_label.setStyleSheet("color: red; font-size: 25px;")
        self.pin_notification_label.setParent(change_pin_widget)



        self.save_and_submit_button3 = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 3  # Center the button horizontally
        self.save_and_submit_button3.setGeometry(button_x, 700, button_width, 70)
        self.save_and_submit_button3.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.save_and_submit_button3.clicked.connect(self.save_and_submit3)
        self.save_and_submit_button3.setParent(change_pin_widget)



        
# Inside your initialization method or where you create the widgets
        self.regenerate_otp_button3 = QPushButton(self)
        self.regenerate_otp_button3.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.regenerate_otp_button3.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.regenerate_otp_button3.setGeometry(760, 335, 40, 40)
        self.regenerate_otp_button3.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.regenerate_otp_button3.hide()
        self.regenerate_otp_button3.clicked.connect(self.generate_otp3)  # Connect the clicked signal
        self.regenerate_otp_button3.setParent(change_pin_widget)
        
     

        self.otp_generated3 = False
        self.otp3 = ""

        #Create a QLabel for the information display 
        self.info_label3_widget = QWidget()
        self.info_label3 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label3_widget)
        self.info_label3.setAlignment(Qt.AlignCenter)
        self.info_label3.setGeometry(400,200,400,40)
        self.info_label3.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label3.hide() # Hide the info label initially
        self.info_label3.setParent(change_pin_widget)

        #create a container widget for the otp input
        self.container3 = QWidget()
        self.container3.setGeometry(400,235,400,100)
        self.container3.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container3.hide()
        self.container3.setParent(change_pin_widget)

        # Create a QVBoxLayout for the container
        self.container_layout3 = QVBoxLayout(self.container3)
        self.container_layout3.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp3_boxes = []
        for _ in range(6):
            otp3_box = QLineEdit(self.container3)
            otp3_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp3_box.setMaxLength(1)  # Limit input to one character
            otp3_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp3_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp3_box)
            self.otp3_boxes.append(otp3_box)
             # Connect textChanged signal to handle_otp_input slot
            otp3_box.textChanged.connect(self.handle_otp_input3)


        self.container_layout3.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label3_widget = QWidget()
        self.timer_label3 = QLabel("<html><p>Time remaining....180 seconds<p></html> ", self.timer_label3_widget)
        self.timer_label3.setAlignment(Qt.AlignCenter)
        self.timer_label3.setGeometry(400,335,360,40)
        self.timer_label3.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label3.hide()
        self.timer_label3.setParent(change_pin_widget)


          #  self.save_and_submit_button.clicked.connect(self.save_user_details)
        self.stacked_widget.addWidget(change_pin_widget)

        
      


    def handle_otp_input3(self, text):
        current_box3 = self.sender()  # Get the sender QLineEdit
        index = self.otp3_boxes.index(current_box3)
        if len(text) == 1 and index < len(self.otp3_boxes) - 1:
            self.otp3_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp3_boxes) - 1:
            self.check_otp3()
               

    def update_timer3(self):
        self.time_left -= 1
        self.timer_label3.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input3()
            self.otp_generated3
            self.otp_generated3 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
                



    


    def save_and_submit3(self):
        email = self.current_user_email
        number = self.phone_number

        current_pin = self.current_pin_input.text()
        new_update_pin = self.new_update_pin_input.text()
        confirm_update_pin = self.confirm_update_pin_input.text()
        entered_otp = self.otp3 # Get the entered OTP

        PIN = self.get_pin()
        
        
        hash_pin = self.sha512_64_hash(current_pin)
 
 
        if hash_pin != PIN:
            self.pin_notification_label.setText("Current Pin does not match.")
            self.pin_notification_label.show()
           

            return
        

        if current_pin == "":
            self.pin_notification_label.setText("Please Enter Current Pin.")
            self.pin_notification_label.show()
            
            return

        if new_update_pin == "":
            self.pin_notification_label.setText("Please Enter New Pin.")
            self.pin_notification_label.show()
           
            return  
        if len(new_update_pin) != 4 :
            QMessageBox.warning(self, "Invalid PIN", "PIN must be exactly 4 digits.")
            return


        if confirm_update_pin == "":
            self.pin_notification_label.setText("Please Confirm Pin.")
            self.pin_notification_label.show()
            
            return  
        
        if len(confirm_update_pin) != 4:
            QMessageBox.warning(self, "Invalid PIN", "Confirmation PIN must be exactly 4 digits.")
            return
        
        if new_update_pin != confirm_update_pin:
           self.pin_notification_label.setText("New Pin and Confirm Pin do not match.")
           self.pin_notification_label.show()
           return

        if entered_otp =="":
            self.generate_otp3()
            self.otp_generated3 = True
            self.info_label3.show()
            self.container3.show()
            self.timer_label3.show()
            self.regenerate_otp_button3.show()
            self.pin_notification_label.setText("")
            self.current_pin_input.hide()
            
            self.show_current_pin_checkbox.hide()
            self.show_new_update_pin_checkbox.hide()
            self.show_confirm_update_pin_checkbox.hide()
            self.new_update_pin_input.hide()
            
            self.confirm_update_pin_input.hide()
            self.start_timer3()
           
          

        self.pin_notification_label.hide()



    def get_pin(self):
        email = self.current_user_email
             # Fetch and return the PIN from your database based on the user's email
        cursor = self.db.cursor()
        cursor.execute("SELECT PIN FROM my_accountdb WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()

        return result[0] if result else None  # Assuming PIN is the first column in the result
    
    def get_susu_pin(self):
               # Fetch and return the PIN from your database based on the user's email
        cursor = self.db.cursor()
        cursor.execute("SELECT Pin FROM susu_account WHERE Email = %s", (self.current_user_email,))
        result = cursor.fetchone()
        cursor.close()

        return result[0] if result else None  # Assuming PIN is the first column in the result



        
     
    def start_timer3(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer3)
        self.timer.start(1000)  # Update timer every second

    def update_database3(self):

        new_update_pin = self.new_update_pin_input.text()
        message = "Your Pin has been Changed successfully."    
        email = self.current_user_email
        hash_updated_pin = self.sha512_64_hash(new_update_pin)

        cursor = self.db.cursor()
        sql = "UPDATE  my_accountdb SET PIN = %s WHERE Email = %s"
        cursor.execute (sql, (hash_updated_pin, email,))
        self.db.commit()

        cursor = self.db.cursor()
        sql = "UPDATE  susu_account SET Pin = %s WHERE Email = %s"
        cursor.execute (sql, (hash_updated_pin, email,))
        self.db.commit()

        QMessageBox.information(self, "Pin Changed", "You have successfully changed your Pin.")


        sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
        cursor.execute(sql, (message, self.current_user_email,))
        self.db.commit()

        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
        
        self.load_alert()


        
        
        
        

    
           

        
       
    def generate_otp3(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp3 = str(random.randint(100000, 999999))
        QMessageBox.information(self, "OTP", f"Sending OTP to {email}")
        
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp3}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Pin""")  # Print the generated OTP
        QMessageBox.information(self, "OTP", f"Sending OTP to {number}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp3}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Pin""") # Print the generated OTP
        self.start_timer3()

 

    def clear_otp_input3(self):
        for otp_box in self.otp3_boxes:
            otp_box.clear()  

    def check_otp3(self):
        entered_otp = "".join(box.text() for box in self.otp3_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input3()
           self.otp_generated3 = False
           return
           
        if entered_otp == self.otp3:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input3()
            self.update_database3()
            self.generate_otp3 = False
            self.info_label3.hide()
            self.container3.hide()
            self.timer_label3.hide()
            self.regenerate_otp_button3.hide()
            self.timer.stop() 
            self.update_database3()
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input3()
            self.otp_generated3 = False    


     
       

        

    def toggle_current_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.current_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.current_pin_input.setEchoMode(QLineEdit.Password) 

    def toggle_new_update_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.new_update_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.new_update_pin_input.setEchoMode(QLineEdit.Password)

    def toggle_confirm_update_pin_visibility(self, state):
        if state == Qt.Checked:
            # Show pin
            self.confirm_new_pin_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide pin
            self.confirm_new_pin_input.setEchoMode(QLineEdit.Password)
                    
            
            

        
    @pyqtSlot()
    def reset_current_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.current_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
     
    @pyqtSlot()

    def reset_new_update_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.new_update_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
    
    @pyqtSlot()

    def reset_confirm_update_pin_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.confirm_update_pin_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")


    def validate_new_update_pin(self,text):
        new_update_pin_pattern = r'^[0-9]{4}$'  # Assuming a 10-digit phone number

        new_update_pin_regex = re.compile(new_update_pin_pattern)

        if new_update_pin_regex.match(text):
            # Valid email format
            self.new_update_pin_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.new_update_pin_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.new_update_pin_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.new_update_pin_input.setFont(font)  
            
    def validate_confirm_update_pin(self,text):
            confirm_update_pin_pattern = r'^[0-9]{4}$'  # Assuming a 10-digit phone number

            confirm_update_pin_regex = re.compile(confirm_update_pin_pattern)

            if confirm_update_pin_regex.match(text):
            # Valid email format
                self.confirm_update_pin_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
            else:
            # Invalid email format
                self.confirm_update_pin_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
                font = self.confirm_update_pin_input.font()
                font.setPointSize(10)  # Adjust the font size as needed
                self.confirm_update_pin_input.setFont(font)   
          


    def notification_page(self):
        notification_widget = QWidget()
        notification_label = QLabel("<html><p> Notification <p></html>", notification_widget)
        notification_label.setGeometry( 350, 50, 600 , 80)
        notification_label.setStyleSheet( "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        notification_label.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(notification_widget)

    def edit_profile_page(self):
        edit_profile_widget = QWidget()
       
        edit_profile_label = QLabel("<html><p>Edit Profile<p></>", edit_profile_widget)
        edit_profile_label.setGeometry(350,50,600,80)
        edit_profile_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        edit_profile_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)




          #Add an edit email change button

        change_email_button = QPushButton(self)
        change_email_button.setGeometry(50, 200, 500, 50)
        icon = QIcon("user.png")                  
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        change_email_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        change_email_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("user.png")
        change_email_button.setIcon(icon)

# Set the text for the button
        change_email_button.setText(" | Change Email Address")

        change_email_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(20))
        change_email_button.setParent(edit_profile_widget)



          #Add an edit Mobile Number change button

        change_number_button = QPushButton(self)
        change_number_button.setGeometry(50, 280, 500, 50)
        icon = QIcon("user.png")                  
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        change_number_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        change_number_button.setStyleSheet("""
                        QPushButton {
                                     background-color: white;
                                     font-size: 12pt; 
                                     border-radius: 35px;
                                     text-align: left;  /* Align text to the left */
                                     padding-left: 40px;  /* Space for the icon */
                                               
                                     }          
                        
                        QPushButton::icon {
                                     padding-right: 15px;  /* Space between icon and text */
                                    }
                        QPushButton:hover{
                                     background-color:#333333
                                    } 
                                    
                                                """)

# Set the icon to the left of the button text
        icon = QIcon("phone-call.png")
        change_number_button.setIcon(icon)

# Set the text for the button
        change_number_button.setText(" | Change Mobile Number")

        change_number_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(21))
        change_number_button.setParent(edit_profile_widget)

        self.stacked_widget.addWidget(edit_profile_widget)


    def email_page(self,db , current_user_email) :   

        self.current_user_email = current_user_email 
        self.db = db

        email_widget = QWidget()
       
        emai_label = QLabel("<html><p>Change Email Address<p></>", email_widget)
        emai_label.setGeometry(350,50,600,80)
        emai_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        emai_label.setAlignment(Qt.AlignCenter)
         
       
        # Create a line edit for the email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(50, 200, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.email_input.setPlaceholderText(" Current Email Address ")
        # Apply styling to the email input field
        self.email_input.setStyleSheet("background-color: white; border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.email_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        self.email_input.addAction(icon, QLineEdit.LeadingPosition)
               # Connect textChanged signal to validate_email slot
        self.email_input.textChanged.connect(self.validate_email)
        self.email_input.editingFinished.connect(self.reset_email_input_style)
        self.email_input.setParent(email_widget)


         
        # Create a line edit for the email input field
        self.new_email_input = QLineEdit(self)
        self.new_email_input.setGeometry(50, 280, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.new_email_input.setPlaceholderText("  New Email Address ")
        # Apply styling to the email input field
        self.new_email_input.setStyleSheet("background-color: white; border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.new_email_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        self.new_email_input.addAction(icon, QLineEdit.LeadingPosition)
               # Connect textChanged signal to validate_email slot
        self.new_email_input.textChanged.connect(self.validate_new_email)
        self.new_email_input.editingFinished.connect(self.reset_new_email_input_style)
        self.new_email_input.setParent(email_widget)

          # Create a line edit for the email input field
        self.confirm_email_input = QLineEdit(self)
        self.confirm_email_input.setGeometry(50, 360, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.confirm_email_input.setPlaceholderText(" Confirm New Email Address ")
        # Apply styling to the email input field
        self.confirm_email_input.setStyleSheet("background-color: white; border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.confirm_email_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        self.confirm_email_input.addAction(icon, QLineEdit.LeadingPosition)
               # Connect textChanged signal to validate_email slot
        self.confirm_email_input.textChanged.connect(self.validate_confirm_email)
        self.confirm_email_input.editingFinished.connect(self.reset_confirm_email_input_style)
        self.confirm_email_input.setParent(email_widget)

              
        # Create QLabel for notification messages
        self.notification_label = QLabel("", self)
        self.notification_label.setGeometry(50, 440, 600, 50)
        self.notification_label.setStyleSheet("color: red; font-size: 25px;")
        self.notification_label.setParent(email_widget)



        
        self.save_and_submit_button = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 3  # Center the button horizontally
        self.save_and_submit_button.setGeometry(button_x, 700, button_width, 70)
        self.save_and_submit_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.save_and_submit_button.clicked.connect(self.save_and_submit)
           
        self.save_and_submit_button.setParent(email_widget)

   
# Inside your initialization method or where you create the widgets
        self.regenerate_otp_button = QPushButton(self)
        self.regenerate_otp_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.regenerate_otp_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.regenerate_otp_button.setGeometry(760, 335, 40, 40)
        self.regenerate_otp_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.regenerate_otp_button.hide()
        self.regenerate_otp_button.clicked.connect(self.generate_otp)  # Connect the clicked signal
        self.regenerate_otp_button.setParent(email_widget)
        
     

        self.otp_generated = False
        self.otp = ""

        #Create a QLabel for the information display 
        self.info_label_widget = QWidget()
        self.info_label = QLabel("<html><p>Enter the OTP....You have 3 minutes<p></html> ", self.info_label_widget)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setGeometry(400,200,400,40)
        self.info_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label.hide() # Hide the info label initially
        self.info_label.setParent(email_widget)

        #create a container widget for the otp input
        self.container = QWidget()
        self.container.setGeometry(400,235,400,100)
        self.container.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container.hide()
        self.container.setParent(email_widget)

        # Create a QVBoxLayout for the container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp_boxes = []
        for _ in range(6):
            otp_box = QLineEdit(self.container)
            otp_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp_box.setMaxLength(1)  # Limit input to one character
            otp_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp_box)
            self.otp_boxes.append(otp_box)
             # Connect textChanged signal to handle_otp_input slot
            otp_box.textChanged.connect(self.handle_otp_input)


        self.container_layout.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label_widget = QWidget()
        self.timer_label = QLabel("<html><p>Time remaining....180 seconds<p></html> ", self.timer_label_widget)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setGeometry(400,335,360,40)
        self.timer_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label.hide()
        self.timer_label.setParent(email_widget)


          #  self.save_and_submit_button.clicked.connect(self.save_user_details)
        self.stacked_widget.addWidget(email_widget)


    def handle_otp_input(self, text):
        current_box = self.sender()  # Get the sender QLineEdit
        index = self.otp_boxes.index(current_box)
        if len(text) == 1 and index < len(self.otp_boxes) - 1:
            self.otp_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp_boxes) - 1:
            self.check_otp()
               

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input()
            self.otp_generated
            self.otp_generated = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
                



    


    def save_and_submit(self):
        
        email = self.email_input.text()
        new_email = self.new_email_input.text()
        confirm_email = self.confirm_email_input.text()
        entered_otp = self.otp # Get the entered OTP
 
        if email != self.current_user_email:
            self.notification_label.setText("Current email does not match.")
            self.notification_label.show()
            return
        

        if email == "":
            self.notification_label.setText("Please Enter Current Email.")
            self.notification_label.show()
            
            return

        if new_email == "":
            self.notification_label.setText("Please Enter New Email.")
            self.notification_label.show()
           
            return  


        if confirm_email == "":
            self.notification_label.setText("Please Confirn Email.")
            self.notification_label.show()
            
            return  
        
        if new_email != confirm_email:
           self.notification_label.setText("New Email and Confirm Email do not match.")
           self.notification_label.show()
           return

        if entered_otp =="":
            self.generate_otp()
            self.generate_otp = True
            
            self.info_label.show()
            self.container.show()
            self.timer_label.show()
            self.regenerate_otp_button.show()
            self.notification_label.setText("")
            self.email_input.hide()
            
            self.new_email_input.hide()
            self.confirm_email_input.hide()
            self.start_timer()
           
          

        self.notification_label.hide()
        
     
    def start_timer(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update timer every second

    def update_database(self,):

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
            cursor = self.db.cursor()
            new_email = self.new_email_input.text()
            email = self.email_input.text()
            message = "Your Email has been Changed successfully."
            
            
            # Check if the user already exists using a parameterized query
            query = "SELECT * FROM registerdb WHERE Email = %s"
            cursor.execute(query,(new_email,))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, " Failed", "The Email is already registered.")
                
            else:    
        # Update the email in the database
                sql = "UPDATE registerdb SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                sql_update_edit = "INSERT INTO edit_db (email, action1) VALUES (%s,%s)"
                action = f"Changed Email from {email} to {new_email}"
                cursor.execute(sql_update_edit, (new_email, action))
                self.db.commit()

                sql = "UPDATE my_accountdb SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                self.db.commit()

                
                sql = "UPDATE susu_account SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                self.db.commit()

                
                sql = "UPDATE susu_members SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                self.db.commit()

                sql = "UPDATE login_logs SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                self.db.commit()

                sql = "UPDATE susu_groups SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                self.db.commit()



                sql = "UPDATE saving_accountdb SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                
                self.db.commit()

                sql = "UPDATE alertdb SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                
                self.db.commit()

                sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
                cursor.execute(sql, (message, self.current_user_email,))
                self.db.commit()
                cursor.close()
                self.load_alert()
                    
                    
                


                QMessageBox.information(self, "Email Changed", "You have successfully changed your email.")
        
       
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
           
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
        finally:
            cursor.close()

         
        
        
       
    def generate_otp(self):
        email = self.current_user_email
        self.otp = str(random.randint(100000, 999999))
        QMessageBox.information(self, "OTP", f"Sending OTP to {email}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Email Address""")  # Print the generated OTP
        self.start_timer1()

      


    def clear_otp_input(self):
        for otp_box in self.otp_boxes:
            otp_box.clear()  

    def check_otp(self):
        entered_otp = "".join(box.text() for box in self.otp_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input()
           self.otp_generated = False
           return
           
        if entered_otp == self.otp:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input()
            self.update_database()
            self.info_label.hide()
            self.container.hide()
            self.timer_label.hide()
            self.regenerate_otp_button.hide()
            self.new_email_input.clear()
            self.email_input.clear()
            self.email_input.show()
            self.confirm_email_input.clear()
            self.new_email_input.show()
            self.confirm_email_input.show()
            self.timer.stop() 
            
          

        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input()
            self.otp_generated = False    





    def mobile_number_page(self, db, Phonenumber):
        self.phone_number = Phonenumber 
        self.db = db

        number_widget = QWidget()
        number_label = QLabel("<html><p>Edit Profile<p></>", number_widget)
        number_label.setGeometry(350,50,600,80)
        number_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        number_label.setAlignment(Qt.AlignCenter)
         

         # Create a line edit for the Phone Number input field
        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(50, 200, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.number_input.setPlaceholderText(" Enter Current Phone Number ")
        # Apply styling to the email input field
        self.number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.number_input.setClearButtonEnabled(True)
        icon =QIcon("phone-call")
        self.number_input.addAction(icon,QLineEdit.LeadingPosition)


        self.number_input.textChanged.connect(self.validate_number)
        self.number_input.editingFinished.connect(self.reset_number_input_style)
        self.number_input.setParent(number_widget)


         # Create a line edit for the New Phone Number input field
        self.new_number_input = QLineEdit(self)
        self.new_number_input.setGeometry(50, 280, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.new_number_input.setPlaceholderText(" Enter New Phone Number ")
        # Apply styling to the email input field
        self.new_number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.new_number_input.setClearButtonEnabled(True)
        icon =QIcon("phone-call")
        self.new_number_input.addAction(icon,QLineEdit.LeadingPosition)


        self.new_number_input.textChanged.connect(self.validate_new_number)
        self.new_number_input.editingFinished.connect(self.reset_new_number_input_style)
        self.new_number_input.setParent(number_widget) 

        
         # Create a line edit for the Confirm new Phone Number input field
        self.confirm_number_input = QLineEdit(self)
        self.confirm_number_input.setGeometry(50, 360, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.confirm_number_input.setPlaceholderText(" Enter Confirm Phone Number ")
        # Apply styling to the email input field
        self.confirm_number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.confirm_number_input.setClearButtonEnabled(True)
        icon =QIcon("phone-call")
        self.confirm_number_input.addAction(icon,QLineEdit.LeadingPosition)

        self.confirm_number_input.textChanged.connect(self.validate_confirm_number)
        self.confirm_number_input.editingFinished.connect(self.reset_confirm_number_input_style)


        self.confirm_number_input.setParent(number_widget)
        # Set an icon for the input field
        #icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        #self.number_input.addAction(icon, QLineEdit.LeadingPosition)

         # Create QLabel for notification messages
        self.notification_label1 = QLabel("", self)
        self.notification_label1.setGeometry(50, 440, 600, 50)
        self.notification_label1.setStyleSheet("color: red; font-size: 25px;")
        self.notification_label1.setParent(number_widget)



        self.save_and_submit_button1 = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 3  # Center the button horizontally
        self.save_and_submit_button1.setGeometry(button_x, 700, button_width, 70)
        self.save_and_submit_button1.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.save_and_submit_button1.clicked.connect(self.save_and_submit1)
        self.save_and_submit_button1.setParent(number_widget)



        
# Inside your initialization method or where you create the widgets
        self.regenerate_otp_button1 = QPushButton(self)
        self.regenerate_otp_button1.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.regenerate_otp_button1.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.regenerate_otp_button1.setGeometry(760, 335, 40, 40)
        self.regenerate_otp_button1.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.regenerate_otp_button1.hide()
        self.regenerate_otp_button1.clicked.connect(self.generate_otp1)  # Connect the clicked signal
        self.regenerate_otp_button1.setParent(number_widget)
        
     

        self.otp_generated1 = False
        self.otp1 = ""

        #Create a QLabel for the information display 
        self.info_label1_widget = QWidget()
        self.info_label1 = QLabel("<html><p>Enter the OTP....You have 3 minutes<p></html> ", self.info_label1_widget)
        self.info_label1.setAlignment(Qt.AlignCenter)
        self.info_label1.setGeometry(400,200,400,40)
        self.info_label1.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label1.hide() # Hide the info label initially
        self.info_label1.setParent(number_widget)

        #create a container widget for the otp input
        self.container1 = QWidget()
        self.container1.setGeometry(400,235,400,100)
        self.container1.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container1.hide()
        self.container1.setParent(number_widget)

        # Create a QVBoxLayout for the container
        self.container_layout1 = QVBoxLayout(self.container1)
        self.container_layout1.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp1_boxes = []
        for _ in range(6):
            otp1_box = QLineEdit(self.container1)
            otp1_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp1_box.setMaxLength(1)  # Limit input to one character
            otp1_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp1_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp1_box)
            self.otp1_boxes.append(otp1_box)
             # Connect textChanged signal to handle_otp_input slot
            otp1_box.textChanged.connect(self.handle_otp_input1)


        self.container_layout1.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label1_widget = QWidget()
        self.timer_label1 = QLabel("<html><p>Time remaining....180 seconds<p></html> ", self.timer_label1_widget)
        self.timer_label1.setAlignment(Qt.AlignCenter)
        self.timer_label1.setGeometry(400,335,360,40)
        self.timer_label1.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label1.hide()
        self.timer_label1.setParent(number_widget)


          #  self.save_and_submit_button.clicked.connect(self.save_user_details)
        self.stacked_widget.addWidget(number_widget)

        
      


    def handle_otp_input1(self, text):
        current_box1 = self.sender()  # Get the sender QLineEdit
        index = self.otp1_boxes.index(current_box1)
        if len(text) == 1 and index < len(self.otp1_boxes) - 1:
            self.otp1_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp1_boxes) - 1:
            self.check_otp1()
               

    def update_timer1(self):
        self.time_left -= 1
        self.timer_label1.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input1()
            self.otp_generated1
            self.otp_generated1 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
                



    


    def save_and_submit1(self):

        number = self.number_input.text()
        new_number = self.new_number_input.text()
        confirm_numnber = self.confirm_number_input.text()
        entered_otp = self.otp1 # Get the entered OTP
 
        if number != self.phone_number:
            self.notification_label1.setText("Current Number does not match.")
            self.notification_label1.show()
            return
        

        if number == "":
            self.notification_label1.setText("Please Enter Current Number.")
            self.notification_label1.show()
            
            return

        if new_number == "":
            self.notification_label1.setText("Please Enter New Number.")
            self.notification_label1.show()
           
            return  


        if confirm_numnber == "":
            self.notification_label1.setText("Please Confirn Number.")
            self.notification_label1.show()
            
            return  
        
        if new_number != confirm_numnber:
           self.notification_label1.setText("New Number and Confirm Number do not match.")
           self.notification_label1.show()
           return

        if entered_otp =="":
            self.generate_otp1()
            self.otp_generated1 = True
            self.info_label1.show()
            self.container1.show()
            self.timer_label1.show()
            self.regenerate_otp_button1.show()
            self.notification_label1.setText("")
            self.number_input.hide()
            
            
            self.new_number_input.hide()
            self.confirm_number_input.hide()
            self.start_timer1()
           
          

        self.notification_label1.hide()
        
     
    def start_timer1(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer1)
        self.timer.start(1000)  # Update timer every second

    def update_database1(self):

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
            message = " Your Mobile Number has been Successfully  Changed. "
            cursor = self.db.cursor()
            new_number = self.new_number_input.text()
            number = self.number_input.text()
           
            cursor.execute("SELECT * FROM registerdb WHERE Phonenumber = %s", (new_number,))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, " Failed", "The Mobile Number is already registered.")
                return
            else:    
               

        # Update the email in the database
                sql = "UPDATE registerdb SET Phonenumber = %s WHERE Phonenumber = %s"
                cursor.execute(sql, (new_number, number))
                
                    
                self.db.commit()

                # Update the edit database with the change
                sql_update_edit = "INSERT INTO edit_db (phone_number, action2) VALUES (%s, LEFT(%s, 255))"
                action = f"Changed Phone Number from {number} to {new_number}"
                cursor.execute(sql_update_edit, (new_number, action))
                self.db.commit()

                sql = "UPDATE login_logs SET PhoneNumber = %s WHERE PhoneNumber = %s"
                cursor.execute(sql, (new_number, number))
                
                    
                self.db.commit()

                sql = "UPDATE susu_groups SET member_id = %s WHERE member_id = %s"
                cursor.execute(sql, (new_number, number))
               
                    
                self.db.commit()

                sql = "UPDATE susu_members SET member_id = %s WHERE member_id = %s"
                cursor.execute(sql, (new_number, number))
                
                    
                self.db.commit()

                sql = "UPDATE contributions SET member_id = %s WHERE member_id = %s"
                cursor.execute(sql, (new_number, number))
                
                    
                self.db.commit()

                sql = "UPDATE susu_account SET Member_ID = %s WHERE Member_ID = %s"
                cursor.execute(sql, (new_number, number))
                
                    
                self.db.commit()

                sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
                cursor.execute(sql, (message, self.current_user_email,))
                self.db.commit()
                cursor.close()
                self.load_alert()
                cursor.close()


                QMessageBox.information(self, "Number Changed", "You have successfully changed your Number.")

        # Close the window or perform other actions as needed
        # Go back to the profile page
         #   profile_page_index = 6  # Set the index of the profile page in your stacked widget
            self.main_window = MainWindow()
            self.main_window.show()
            self.close() 
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
    
        
        
        
       
    def generate_otp1(self):
        number = self.phone_number
        self.otp1 = str(random.randint(100000, 999999))
        QMessageBox.information(self, "OTP", f"Sending OTP to {number}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp1}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Phone Number""")  # Print the generated OTP
        self.start_timer1()


    def clear_otp_input1(self):
        for otp_box in self.otp1_boxes:
            otp_box.clear()  

    def check_otp1(self):
        entered_otp = "".join(box.text() for box in self.otp1_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input1()
           self.otp_generated1 = False
           return
           
        if entered_otp == self.otp1:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input1()
            self.update_database1()
            
            self.info_label1.hide()
            self.container1.hide()
            self.timer_label1.hide()
            self.regenerate_otp_button1.hide()
            self.number_input.show()
            self.number_input.clear()
            self.new_number_input.clear()
            self.confirm_number_input.clear()
            self.new_number_input.show()
            self.confirm_number_input.show()
            self.timer.stop() 
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input1()
            self.otp_generated1 = False    


    
       


    def validate_number(self,text):
        number_pattern = r'^[0-9]{10}$'  # Assuming a 10-digit phone number

        number_regex = re.compile(number_pattern)

        if number_regex.match(text):
            # Valid email format
            self.number_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.number_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.number_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.number_input.setFont(font)   

    def validate_new_number(self,text):
        number_pattern = r'^[0-9]{10}$'  # Assuming a 10-digit phone number

        number_regex = re.compile(number_pattern)

        if number_regex.match(text):
            # Valid email format
            self.new_number_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.new_number_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.number_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.new_number_input.setFont(font)   

    def validate_confirm_number(self,text):
        number_pattern = r'^[0-9]{10}$'  # Assuming a 10-digit phone number

        number_regex = re.compile(number_pattern)

        if number_regex.match(text):
            # Valid email format
            self.confirm_number_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.confirm_number_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.number_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.confirm_number_input.setFont(font)   

         

        



    def validate_email(self, text):
        # Regular expression pattern for validating email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern)

        # Use match method to check if the input text matches the pattern
        if regex.match(text):
            # Valid email format
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.email_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.email_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.email_input.setFont(font) 

    def validate_new_email(self, text):
        # Regular expression pattern for validating email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern)

        # Use match method to check if the input text matches the pattern
        if regex.match(text):
            # Valid email format
            self.new_email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.new_email_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.new_email_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.new_email_input.setFont(font)   

    def validate_confirm_email(self, text):
        email = self.new_email_input.text()
        confirmation_email = self.confirm_email_input.text()

        # Check if the confirmation password matches the original password
        if email == confirmation_email:
            # Matching passwords, apply green border
                       self.confirm_email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Non-matching passwords, apply red border
                  self.confirm_email_input.setStyleSheet("border-radius: 25px; border: 2px solid red;")
   
            # Set font size back to normal
        font = self.confirm_email_input.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.confirm_email_input.setFont(font)   


    @pyqtSlot()
    def reset_number_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")


    @pyqtSlot()
    def reset_new_number_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.new_number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    @pyqtSlot()
    def reset_confirm_number_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.confirm_number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    

    @pyqtSlot()
    def reset_email_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    

    @pyqtSlot()
    def reset_new_email_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.new_email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    

    @pyqtSlot()
    def reset_confirm_email_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.confirm_email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
                  
         


    def change_password_page(self, db, current_password, current_user_email):
        self.current_user_email = current_user_email
        self.current_password = current_password
        self.db = db
        

        change_password_widget = QWidget()
       
        change_password_label = QLabel("<html><p>Change Password<p></>", change_password_widget)
        change_password_label.setGeometry(300,50,600,80)
        change_password_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        change_password_label.setAlignment(Qt. AlignCenter)
       # profile_layout.addWidget(welcome_label)

       
        # Create a line edit for password input field
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(50, 200, 350, 50)
        # Set placeholder text for the password input field
        self.password_input.setPlaceholderText("Enter Current Password")
        # Appply styling to the password input field
        self.password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.password_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.validate_password)
        self.password_input.editingFinished.connect(self.reset_password_input_style)
        self.password_input.setParent(change_password_widget)


        # Create checkbox to toggle password visibility
        self.show_password_checkbox1 = QCheckBox("Show Password", self)
        self.show_password_checkbox1.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox1.setGeometry(40, 247, 200, 30)
        self.show_password_checkbox1.stateChanged.connect(self.toggle_password_visibility)

        self.show_password_checkbox1.setParent(change_password_widget)


          # Create a line edit for New password input field
        self.new_password_input = QLineEdit(self)
        self.new_password_input.setGeometry(50, 300, 350, 50)
        # Set placeholder text for the password input field
        self.new_password_input.setPlaceholderText("Enter New  Password")
        # Appply styling to the password input field
        self.new_password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.new_password_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.new_password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.textChanged.connect(self.validate_new_password)
        self.new_password_input.editingFinished.connect(self.reset_new_password_input_style)
        self.new_password_input.setParent(change_password_widget)

           # Create checkbox to toggle password visibility
        self.show_password_checkbox2 = QCheckBox("Show Password", self)
        self.show_password_checkbox2.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox2.setGeometry(40, 347, 200, 30)
        self.show_password_checkbox2.stateChanged.connect(self.toggle_password_visibility1)



        self.show_password_checkbox2.setParent(change_password_widget)


        
          # Create a line edit for Confirmpassword input field
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setGeometry(50, 400, 350, 50)
        # Set placeholder text for the password input field
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        # Appply styling to the password input field
        self.confirm_password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.confirm_password_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.confirm_password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.textChanged.connect(self.validate_confirm_password)
        self.confirm_password_input.setParent(change_password_widget)

               # Create checkbox to toggle password visibility
        self.show_password_checkbox3 = QCheckBox("Show Password", self)
        self.show_password_checkbox3.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox3.setGeometry(40, 447, 200, 30)
        self.show_password_checkbox3.stateChanged.connect(self.toggle_password_visibility2)
        self.show_password_checkbox3.setParent(change_password_widget)



        # Create QLabel for notification messages
        self.notification_label2 = QLabel("", self)
        self.notification_label2.setGeometry(50, 500, 600, 50)
        self.notification_label2.setStyleSheet("color: red; font-size: 25px;")
        self.notification_label2.setParent(change_password_widget)



        


        self.save_and_submit_button2 = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 3  # Center the button horizontally
        self.save_and_submit_button2.setGeometry(button_x, 700, button_width, 70)
        self.save_and_submit_button2.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        
        self.save_and_submit_button2.clicked.connect(self.save_and_submit2)
        self.save_and_submit_button2.setParent(change_password_widget)



        
# Inside your initialization method or where you create the widgets
        self.regenerate_otp_button2 = QPushButton(self)
        self.regenerate_otp_button2.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.regenerate_otp_button2.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.regenerate_otp_button2.setGeometry(760, 335, 40, 40)
        self.regenerate_otp_button2.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.regenerate_otp_button2.hide()
        self.regenerate_otp_button2.clicked.connect(self.generate_otp2)  # Connect the clicked signal
        self.regenerate_otp_button2.setParent(change_password_widget)
        
     

        self.otp_generated2 = False
        self.otp2 = ""

        #Create a QLabel for the information display 
        self.info_label2_widget = QWidget()
        self.info_label2 = QLabel("<html><p>Enter the OTP....You have 3 minutes<p></html> ", self.info_label2_widget)
        self.info_label2.setAlignment(Qt.AlignCenter)
        self.info_label2.setGeometry(400,200,400,40)
        self.info_label2.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label2.hide() # Hide the info label initially
        self.info_label2.setParent(change_password_widget)

        #create a container widget for the otp input
        self.container2 = QWidget()
        self.container2.setGeometry(400,235,400,100)
        self.container2.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container2.hide()
        self.container2.setParent(change_password_widget)

        # Create a QVBoxLayout for the container
        self.container_layout2 = QVBoxLayout(self.container2)
        self.container_layout2.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp2_boxes = []
        for _ in range(6):
            otp2_box = QLineEdit(self.container2)
            otp2_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp2_box.setMaxLength(1)  # Limit input to one character
            otp2_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp2_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp2_box)
            self.otp2_boxes.append(otp2_box)
             # Connect textChanged signal to handle_otp_input slot
            otp2_box.textChanged.connect(self.handle_otp_input2)


        self.container_layout2.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        self.timer_label2_widget = QWidget()
        self.timer_label2 = QLabel("<html><p>Time remaining....180 seconds<p></html> ", self.timer_label2_widget)
        self.timer_label2.setAlignment(Qt.AlignCenter)
        self.timer_label2.setGeometry(400,335,360,40)
        self.timer_label2.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label2.hide()
        self.timer_label2.setParent(change_password_widget)


          #  self.save_and_submit_button.clicked.connect(self.save_user_details)
        self.stacked_widget.addWidget(change_password_widget)

        
      


    def handle_otp_input2(self, text):
        current_box2 = self.sender()  # Get the sender QLineEdit
        index = self.otp2_boxes.index(current_box2)
        if len(text) == 1 and index < len(self.otp2_boxes) - 1:
            self.otp2_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp2_boxes) - 1:
            self.check_otp2()
               

    def update_timer2(self):
        self.time_left -= 1
        self.timer_label2.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input2()
            self.otp_generated2
            self.otp_generated2 = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP."),
         
                



    


    def save_and_submit2(self):

        email = self.current_user_email
        password = self.password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        entered_otp = self.otp2 # Get the entered OTP

        hash_password = hashlib.sha256(password.encode()).hexdigest()
        
        if hash_password != self.current_password:
            self.notification_label2.setText("Current Password does not match.")
            self.notification_label2.show()
            print(hash_password)
            print(self.current_password)
            print(password)
            return
        

        if password== "":
            self.notification_label2.setText("Please Enter Current Password.")
            self.notification_label2.show()
            
            return

        if new_password == "":
            self.notification_label2.setText("Please Enter New Password.")
            self.notification_label2.show()
           
            return  


        if confirm_password == "":
            self.notification_label2.setText("Please Confirn Password.")
            self.notification_label2.show()
            
            return  
        
        if new_password != confirm_password:
           self.notification_label2.setText("New Password and Confirm Password do not match.")
           self.notification_label2.show()
           return

        if entered_otp =="":
            self.generate_otp2()
            self.otp_generated2 = True
            self.info_label2.show()
            self.container2.show()
            self.timer_label2.show()
            self.regenerate_otp_button2.show()
            self.notification_label2.setText("")
            self.password_input.hide()
            
            
            self.new_password_input.hide()
            self.confirm_password_input.hide()
            self.show_password_checkbox1.hide()
            self.show_password_checkbox2.hide()
            self.show_password_checkbox3.hide()
            self.start_timer2()
           
          

        self.notification_label2.hide()
        
     
    def start_timer2(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer2)
        self.timer.start(1000)  # Update timer every second

    def update_database2(self):

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return
            
            cursor = self.db.cursor()
            new_password = self.new_password_input.text()
            password = self.password_input.text()
            email = self.current_user_email
            hash_password = hashlib.sha256(new_password.encode()).hexdigest()
            message = "Your Password has been Successfully Changed"
          
           
               

        # Update the email in the database
            sql = "UPDATE registerdb SET Password = %s, PasswordHash = %s WHERE Email = %s"
            cursor.execute(sql, (new_password, hash_password, email))
            print(new_password)
                    
            self.db.commit()
            sql_update_edit = "INSERT INTO edit_db (email, password, action3, hashed_password) VALUES (%s, %s, %s, %s)"
            action = f"Changed Password from {password} to {new_password}"
            cursor.execute(sql_update_edit, (email, new_password, action, hash_password))
            self.db.commit()

            sql = "INSERT INTO alertdb (message, created_at, Email) VALUES(%s, NOW(), %s)"
            cursor.execute(sql, (message, self.current_user_email,))
            self.db.commit()
            cursor.close()
            self.load_alert()
            cursor.close()


            QMessageBox.information(self, "Password Changed", "You have successfully changed your Password.")

        # Close the window or perform other actions as needed
        # Go back to the profile page
         #   profile_page_index = 6  # Set the index of the profile page in your stacked widget
            self.main_window = MainWindow()
            self.main_window.show()
            self.close() 
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
    
        
        
        
       
    def generate_otp2(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp2 = str(random.randint(100000, 999999))
        QMessageBox.information(self, "OTP", f"Sending OTP to {email}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp2}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Password""") 
        QMessageBox.information(self, "OTP", f"Sending OTP to {number}")
        QMessageBox.information(self, "OTP", f"""Your Verification code: {self.otp2}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Password""") # Print the generated OTP
        self.start_timer2()

   

    def clear_otp_input2(self):
        for otp_box in self.otp2_boxes:
            otp_box.clear()  

    def check_otp2(self):
        entered_otp = "".join(box.text() for box in self.otp2_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input2()
           self.otp_generated2 = False
           return
           
        if entered_otp == self.otp2:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            
            self.clear_otp_input2()
            self.update_database2()
            self.generate_otp2 = False
            self.info_label2.hide()
            self.container2.hide()
            self.timer_label2.hide()
            self.regenerate_otp_button2.hide()
            self.password_input.show()
            self.password_input.clear()
            self.confirm_password_input.clear()
            self.new_password_input.clear()
            self.new_password_input.show()
            self.confirm_password_input.show()
            self.show_password_checkbox1.show()
            self.show_password_checkbox2.show()
            self.show_password_checkbox3.show()
            self.timer.stop() 
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input2()
            self.otp_generated2 = False    


    

       


    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            # Show password
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.password_input.setEchoMode(QLineEdit.Password)

    def toggle_password_visibility1(self, state):
        if state == Qt.Checked:
            # Show password
            self.new_password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.new_password_input.setEchoMode(QLineEdit.Password)

    def toggle_password_visibility2(self, state):
        if state == Qt.Checked:
            # Show password
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
        


    def validate_password(self, password):
       
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(password_pattern)

        # Use match method to check if the input password matches the pattern
        if regex.match(password):
            self.password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.password_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")



            # Set font size back to normal
        font = self.password_input.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.password_input.setFont(font)


    def validate_new_password(self, password):
       
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(password_pattern)

        # Use match method to check if the input password matches the pattern
        if regex.match(password):
            self.new_password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.new_password_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")



            # Set font size back to normal
        font = self.new_password_input.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.new_password_input.setFont(font)

    def validate_confirm_password(self, password):
       

            # Get the content of both password fields
        password = self.new_password_input.text()
        confirmation_password = self.confirm_password_input.text()

        # Check if the confirmation password matches the original password
        if password == confirmation_password:
            # Matching passwords, apply green border
            self.confirm_password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Non-matching passwords, apply red border
            self.confirm_password_input.setStyleSheet("border-radius: 25px; border: 2px solid red;")
   

            # Set font size back to normal
        font = self.confirm_password_input.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.confirm_password_input.setFont(font)
    
    
    @pyqtSlot()
    def reset_password_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.password_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    @pyqtSlot()
    def reset_new_password_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.new_password_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    def start(self):
        self.show()

    def sha512_64_hash(self,key):
        
        #SHA-512 hash function truncated to 64 bits.
    
        hash_object = hashlib.sha512(str(key).encode())
        hash_value = int(hash_object.hexdigest(), 16)
        return f"{hash_value:016x}"    
    

    def handle_page_change(self, index):
        print(index)
        # When the current page changes, hide specific widgets as needed
        if index != 8:

            self.clear_otp_input2()
            
            self.info_label2.hide()
            self.container2.hide()
            self.timer_label2.hide()
            self.regenerate_otp_button2.hide()



            self.password_input.clear()
            self.notification_label2.hide()
            self.password_input.show()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
            
            self.new_password_input.show()
            self.confirm_password_input.show()
            self.show_password_checkbox1.show()
            self.show_password_checkbox2.show()
            self.show_password_checkbox3.show()
            
           
            

        if index != 14 :
            self.clear_pin_input1()
            
            self.pin_info_label1.hide()
            self.pin_container1.hide()
            self.pin_label1.hide() 
            self.receiver3_acc_input.show()
            self.transfer7_amount_input.show()
            self.transfer7_notify_label.hide()

        if index != 15 :
            self.clear_pin_input2()
            
            self.pin_info_label2.hide()
            self.pin_container2.hide()
            self.pin_label2.hide() 
            self.receiver2_acc_input.show()
            self.transfer6_amount_input.show()
            self.transfer7_notify_label.hide()

        if index != 20 :
            self.clear_otp_input()
            
            self.info_label.hide()
            self.container.hide()
            self.timer_label.hide()
            self.regenerate_otp_button.hide()
            self.notification_label.hide()

           
            self.email_input.show()
            
            self.new_email_input.show()
            self.confirm_email_input.show()
            self.email_input.clear()
            
            self.new_email_input.clear()
            self.confirm_email_input.clear()
          


        if index != 21 :    

            self.clear_otp_input1()
            
            self.info_label1.hide()
            self.container1.hide()
            self.timer_label1.hide()
            self.regenerate_otp_button1.hide()
            self.notification_label1.hide()
            self.number_input.clear()
            self.number_input.show    
            self.new_number_input.show()
            self.new_number_input.clear()
            self.confirm_number_input.clear()
            self.confirm_number_input.show()
            
            
              
               
            
        if index != 22:
            # Hide specific widgets in page 2 when leaving that page
            self.acc_label.hide()    
            self.pin_input.clear()

        if index != 23:
            self.new_pin_input.clear()
            self.confirm_new_pin_input.clear()
            self.notification_label4.hide()    
            
        if index != 18:
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.goal_input.clear()
            self.notify_label.hide()

        if index != 24:
            self.clear_otp_input3()
            
            self.info_label3.hide()
            self.container3.hide()
            self.timer_label3.hide()
            self.regenerate_otp_button3.hide()



            self.pin_notification_label.hide()
            self.current_pin_input.show()
            self.current_pin_input.clear()
            
            self.show_current_pin_checkbox.show()
            self.show_new_update_pin_checkbox.show()
            self.show_confirm_update_pin_checkbox.show()
            self.new_update_pin_input.show()
            self.new_update_pin_input.clear()
            
            self.confirm_update_pin_input.show()
            
            self.confirm_update_pin_input.clear()
        
                

        if index != 25:
            
            self.reset_ui_for_new_otp() 
            self.clear_otp_input4()
            self.accountnum_input.clear()
            self.info_label4.hide()
            self.container4.hide()
            self.timer_label4.hide()
            self.sab_regenerate_otp_button.hide()
            
            self.accountnum_input.show()
              

        if index != 26 :
            self.saving_account_input.clear()
            self.first_name1_input.clear()
            self.last_name1_input.clear()
            self.goal1_input.clear()   
            self.save_notify_label.hide()

        if index != 28:
            self.sender1_acc_input.clear()
            self.transfer_amount1_input.clear()
            self.transfer1_notify_label.hide()

        if index !=29 :

            self.clear_otp_input7()
            
            self.info_label7.hide()
            self.container7.hide()
            self.timer_label7.hide()
            self.transfer2_regenerate_otp_button.hide()
            self.transfer2_notify_label.hide()
             
            self.sender2_acc_input.show()
            self.transfer_amount2_input.show()

        if index != 30:
            self.transfer_amount3_input.clear()
            self.sender3_acc_input.clear()    
            self.transfer3_notify_label.hide()
             
        if index != 31 :

            self.pin_info_label.hide()
            self.pin_container.hide()
            self.pin_label.hide() 
            self.receiver_acc_input.show()
            self.transfer4_amount_input.show()
            self.receiver_acc_input.clear()
            self.transfer4_amount_input.clear()
            self.transfer4_notify_label.hide()

        if index != 32 :
            self.transfer5_amount_input.clear()
            self.receiver1_acc_input.clear()
            self.clear_pin_input3()  
            self.pin_info_label3.hide()
            self.pin_container3.hide()
            self.pin_label3.hide() 
            self.receiver1_acc_input.show()
            self.transfer5_amount_input.show()   
            
    
            self.transfer5_notify_label.hide()  


        if index != 34:
            self.susu_pin_input.clear()   
            self.susu_acc_label.hide()

        if index != 35 :
            self.info_label6.hide()
            self.container6.hide()
            self.timer_label6.hide()
            self.regenerate_otp_for_forgot_pin_button.hide()
            self.email_input_for_forgot_pin.show()
            self.forgot_pin_input.show()
            self.forgot_pin_checkbox.show()
            self.show_confirm_forgot_pin_checkbox.show()
            self.confirm_forgot_pin_input.show()
            self.forgot_pin_notification_label.hide()
            
            

        if index != 36 :
            self.clear_otp_input8()
            
            self.info_label8.hide()
            self.container8.hide()
            self.timer_label8.hide()
            self.transfer8_regenerate_otp_button.hide()
            
            self.group_acc_input.show()
            self.transfer_amount8_input.show()
            
            self.transfer8_notify_label.hide()
            
            
                

        if index != 12 :
            self.group_name_input.clear()
            self.contribution_amount_input.clear()
            
            self.members_count_input.clear()

        if index != 33 :
            self.group_id_input.clear()
            self.session_id_input.clear()    


       


       



    def load1_image(self):
        pixmap = QPixmap(self.image_path[0])
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)


    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.SessionId = str(uuid.uuid4())  # Generate a unique session ID
        
        self.first_name = ""
        self.last_name = ""
        self.dob = ""
        self.gender = ""
        self.phone_number =""
        self.email = ""

        self.setWindowTitle("Register Window")
        self.setGeometry(100, 100, 1500, 900)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 1500, 900)

        # Loading a list of images
        self.image_paths = ["desk.jpg"]

        # Load intial image
        self.load_image()

        # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Create New</><p> Account</>", self)
        label_height = 200  # Adjust the width of the label as needed
        label_width = 900
        # label_x = (self.width() - label_width) // 2  # Center the label horizontally
        # label_y = 20
        self.welcome_label.setGeometry(300, 10,  label_width, label_height)
        self.welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 20px; font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignCenter)




        # Create a line edit for the First Name input field
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setGeometry(575, 285, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the date of birth input field
        self.first_name_input.setPlaceholderText("First Name")
        # Apply styling to the date of birth input field
        self.first_name_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.first_name_input.setClearButtonEnabled(True)
        # Set an icon for the input field if needed
        # icon = QIcon("calendar.png")  # You can use a calendar icon if desired
        # self.dob_input.addAction(icon, QLineEdit.LeadingPosition)

        # Create a line edit for the Last Name input field
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setGeometry(575, 345, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the date of birth input field
        self.last_name_input.setPlaceholderText("Last Name")
        # Apply styling to the date of birth input field
        self.last_name_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.last_name_input.setClearButtonEnabled(True)
        # Set an icon for the input field if needed
        # icon = QIcon("calendar.png")  # You can use a calendar icon if desired
        # self.dob_input.addAction(icon, QLineEdit.LeadingPosition)

         # Create a line edit for date of birth
        self.dob_input = QLineEdit(self)
        self.dob_input.setGeometry(575, 405, 350, 50)  # Adjust position and size
        self.dob_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.dob_input.setPlaceholderText("Date Of Birth")  # Placeholder text for format
        self.dob_input.setReadOnly(True)
        self.dob_input.setCursorPosition(0)
       # self.dob_input.setAlignment(Qt.AlignCenter)  # Center align text
      #  self.dob_input.setInputMask("9999-99-99")  # Input mask for date format

         # Add dropdown arrow button
        self.dropdown_button3 = QToolButton(self)
        self.dropdown_button3.setText("▼")
        self.dropdown_button3.setStyleSheet("font-size: 16px; color : black; border : none")
        self.dropdown_button3.setGeometry(900, 405, 20, 50)
        self.dropdown_button3.clicked.connect(self.showCalendar)
       # self.dob_input.setCalendarPopup(True) 
        #self.dob_input.setButtonSymbols(QDateEdit.CalendarButton)


        # Calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGeometry(900, 550, 350, 250)  # Adjust position and size
        self.calendar.setWindowFlags(Qt.Popup)
        self.calendar.selectionChanged.connect(self.updateDate)

        
        # Line edit for Gender Selection
        self.gender_line_edit = QLineEdit(self)
        self.gender_line_edit.setGeometry(575, 470, 350, 50)
        self.gender_line_edit.setPlaceholderText("Gender")
        self.gender_line_edit.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.gender_line_edit.setReadOnly(True)
        self.gender_line_edit.setCursorPosition(0)

        # Add dropdown arrow button
        self.dropdown_button1 = QToolButton(self)
        self.dropdown_button1.setText("▼")
        self.dropdown_button1.setStyleSheet("font-size: 16px; color : black; border : none")
        self.dropdown_button1.setGeometry(900, 470, 20, 50)
        self.dropdown_button1.clicked.connect(self.show_menu2)

        # Create a menu for Gender selection
        self.menu1 = QMenu(self)
        self.menu1.addAction("Male").triggered.connect(lambda: self.update_gender_line_edit(" Male "))
        self.menu1.addAction("Female").triggered.connect(lambda: self.update_gender_line_edit("Female"))
        self.menu1.addAction("").triggered.connect(lambda: self.update_gender_line_edit(""))

        # Create a line edit for the Phone Number input field
        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(575, 530, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.number_input.setPlaceholderText(" Phone Number ")
        # Apply styling to the email input field
        self.number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.number_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        #icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        #self.number_input.addAction(icon, QLineEdit.LeadingPosition)
        icon =QIcon("phone-call")
        self.number_input.addAction(icon,QLineEdit.LeadingPosition)

        self.number_input.textChanged.connect(self.validate_number)
        self.number_input.editingFinished.connect(self.reset_number_input_style)


        # Create a line edit for the email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(575, 590, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.email_input.setPlaceholderText(" Enter Email ")
        # Apply styling to the email input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.email_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        self.email_input.addAction(icon, QLineEdit.LeadingPosition)

        # Connect textChanged signal to validate_email slot
        self.email_input.textChanged.connect(self.validate_email)
        self.email_input.editingFinished.connect(self.reset_email_input_style)

    
        self.login_button = QPushButton("login", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.login_button.setGeometry(button_x, 700, button_width, 70)
        self.login_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        self.login_button.clicked.connect(self.open_login_window)


        self.continue_button = QPushButton("Continue", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.continue_button.setGeometry(button_x, 800, button_width, 70)
        self.continue_button.setStyleSheet("""
                 QPushButton {
                 background-color: blue;
                  font-size: 18pt; 
                  border-radius: 35px;
                  }
                   QPushButton:hover{
                      background-color:brown
                  }
              """)
        self.continue_button.clicked.connect(self.validate_inputs)


            
        # Create QLabel for notification messages
        self.notification_label = QLabel("", self)
        self.notification_label.setGeometry(575, 650, 400, 50)
        self.notification_label.setStyleSheet("color: red; font-size: 25px;")


    def showCalendar(self):
        # Show a calendar popup for date selection
       self.calendar.show()

    
    def updateDate(self):
        # Get the selected date from the calendar and format it
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        # Update the text in the input field with the selected date
        self.dob_input.setText(selected_date)   

 

    def validate_inputs(self):
        # Check if any of the required fields are empty
       

        if self.first_name_input.text().strip() == "":
            self.notification_label.setText("Please enter your first name.")
            self.notification_label.show()
            return

        if self.last_name_input.text().strip() == "":
            self.notification_label.setText("Please enter your last name.")
            self.notification_label.show()
            return

        if self.dob_input.text().strip() == "":
            self.notification_label.setText("Please enter your date of birth.")
            self.notification_label.show()
            return

        if self.gender_line_edit.text().strip() == "":
            self.notification_label.setText("Please select your gender.")
            self.notification_label.show()
            return
        
        if self.number_input.text().strip() == "":
            self.notification_label.setText("Please enter your phone number.")
            self.notification_label.show()
            return

        if self.email_input.text().strip() == "":
            self.notification_label.setText("Please enter your email.")
            self.notification_label.show()
            return

        # If all required fields are filled, hide the notification and proceed
        self.notification_label.hide()
        # Proceed with the registration process
        self.open_continue_window()



    
    # Instantiate your window class and call the register_user method as needed

    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel







    def validate_number(self, text):
        number_pattern = r'^[0-9]{10}$'  # Assuming a 10-digit phone number

        number_regex = re.compile(number_pattern)

        if number_regex.match(text):
            # Valid email format
            self.number_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.number_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.number_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.number_input.setFont(font)


    def validate_email(self, text):
        # Regular expression pattern for validating email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern)

        # Use match method to check if the input text matches the pattern
        if regex.match(text):
            # Valid email format
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.email_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.email_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.email_input.setFont(font)


    @pyqtSlot()
    def reset_number_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")





    @pyqtSlot()
    def reset_email_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")



    def update_gender_line_edit(self,gender_type):
        self.gender_line_edit.setText(gender_type)
    def show_menu2(self):
        self.menu1.exec_(self.dropdown_button1.mapToGlobal(QtCore.QPoint(0, self.dropdown_button1.height())))



    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel

    def open_continue_window(self):
      # Check if SessionId is available before creating the continueWindow instance
        if hasattr(self, 'SessionId') and self.SessionId:
            self.continue_window = continueWindow(self.SessionId,self.first_name,self.last_name,self.dob,self.gender,self.phone_number,self.email)
            self.continue_window.show()
        else:
            QMessageBox.critical(self, "Error", "SessionId not available.")

        # Retrieve user details from input fields
        
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        dob= self.dob_input.text()
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
    # Handle invalid date format
         QMessageBox.warning(self, "Error", "Invalid date format. Please enter in YYYY-MM-DD format.")
        
        gender = self.gender_line_edit.text()
        phone_number = self.number_input.text()
        email = self.email_input.text()
        

        try:
            # Connect to the MySQL database
            db = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="S3cR3tUs3R",
                database="desktopdb"
            )

            # Create a cursor object
            cursor = db.cursor()

            # Check if the user already exists using a parameterized query
            cursor.execute("SELECT * FROM registerdb WHERE Email = %s", (email,))
            result = cursor.fetchone()

            if result:
                QMessageBox.information(self, "Registration Failed",
                                        "The user is already registered. Please login.")
            else:
                # Insert the new user into the database using a parameterized query
                insert_query = "INSERT INTO registerdb (SessionId, Firstname, Lastname, Dob, Gender, Email, Phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                user_data = (self.SessionId, first_name, last_name, dob, gender, email, phone_number)
               # cursor.execute(insert_query, user_data)
                #db.commit()
                cursor.close()
                print(user_data)
                db.close()

            # Close the current window (RegisterWindow)
                self.close()

            # Open the next window (ContinueWindow)
                self.continue_window = continueWindow(SessionId= self.SessionId, first_name=first_name, last_name= last_name, dob= dob, gender=gender, email=email, phone_number=phone_number)
                self.continue_window.show()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to register user. Error: {e}")

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()        
    

class continueWindow(QMainWindow):
    def __init__(self, SessionId, first_name, last_name,  dob, gender, email ,phone_number):
        super().__init__()
        self.setWindowTitle("Continue Window")
        self.setGeometry(100, 100, 1500, 900)
        self.SessionId = SessionId
        self.first_name = first_name  # Inherit first_name from parent class
        self.last_name = last_name  # Inherit last_name from parent class
        self.gender = gender  # Inherit gender from parent class
        self.dob = dob  # Inherit dob from parent class
        self.phone_number = phone_number  # Inherit phone_number from parent class
        self.email = email 

        
        
        

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 1500, 900)

        # Loading a list of images
        self.image_paths = ["desk.jpg"]

        # Load intial image
        self.load_image()

        # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Create New</><p> Account</>", self)
        label_height= 200  # Adjust the width of the label as needed
        label_width = 900
        # label_x = (self.width() - label_width) // 2  # Center the label horizontally
        # label_y = 20
        self.welcome_label.setGeometry(300, 10, label_width, label_height)
        self.welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 20px; font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignCenter)



        # Create a line edit for password input field
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(575, 225, 350, 50)
        # Set placeholder text for the password input field
        self.password_input.setPlaceholderText("Enter Password")
        # Appply styling to the password input field
        self.password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.password_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Create a line edit for confirming password input field
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setGeometry(575, 320, 350, 50)
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        self.confirm_password_input.setClearButtonEnabled(True)
        icon = QIcon("padlock.png")
        self.confirm_password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)



        # Create checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(570, 280, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Create checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(570, 375, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility2)

        self.password_input.textChanged.connect(self.validate_password)
        self.password_input.editingFinished.connect(self.reset_password_input_style)
        self.confirm_password_input.textChanged.connect(self.validate_confirmation_password)
        self.confirm_password_input.editingFinished.connect(self.reset_confirm_password_input_style)

        # Create QLabel for notification messages
        self.notification_label = QLabel("", self)
        self.notification_label.setGeometry(575, 700, 350, 50)
        self.notification_label.setStyleSheet("color: blue; font-size: 25px;")

        #login

        self.login_button = QPushButton("login", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.login_button.setGeometry(button_x, 800, button_width, 70)
        self.login_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        self.login_button.clicked.connect(self.validate_inputs)


                #Save and Submit

        self.save_and_submit_button = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.save_and_submit_button.setGeometry(button_x, 700, button_width, 70)
        self.save_and_submit_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        self.save_and_submit_button.clicked.connect(self.save_user_details)



        self.back_button = QPushButton("<----", self)
        button_width = 100  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 50  # Center the button horizontally
        self.back_button.setGeometry(button_x, 800, button_width, 70)
        self.back_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        self.back_button.clicked.connect(self.open_register_window)


        # Create QLabel to display password rules
        self.password_rules_label = QLabel(self)
        self.password_rules_label.setGeometry(575, 400, 600, 50)
        self.password_rules_label.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label.setText(
            "<html>Password must contain : <br> ✓ At least 8 characters </html>" )
        self.password_rules_label1 = QLabel(self)
        self.password_rules_label1.setGeometry(575, 425, 600, 50)
        self.password_rules_label1.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label1.setText(
            "<html> ✓ 1 Uppercase[A-Z] </html>")
        self.password_rules_label2 = QLabel(self)
        self.password_rules_label2.setGeometry(575, 445, 600, 50)
        self.password_rules_label2.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label2.setText(
            "<html> ✓ 1 Lowercase [a-z] </html>" )
        self.password_rules_label3 = QLabel(self)
        self.password_rules_label3.setGeometry(575, 465, 600, 50)
        self.password_rules_label3.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label3.setText(    
            "<html> ✓ 1 Numeric value [0-9]</html>")
        self.password_rules_label4 = QLabel(self)
        self.password_rules_label4.setGeometry(575, 485, 600, 50)
        self.password_rules_label4.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label4.setText(    
            "<html> ✓ 1 Special characters[#,$, etc ] </html>")


    def validate_inputs(self):
        # Check if any of the required fields are empty
        if self.password_input.text().strip() == "":
            self.notification_label.setText("Please Enter Password.")
            self.notification_label.show()
            self.notification_label.setGeometry(575,600,350,50)
            return

            # If all required fields are filled, hide the notification and proceed
        self.notification_label.hide()
            # Proceed with the registration process
        self.open_login_window()
        self.close()

    
       

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            # Show password
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.password_input.setEchoMode(QLineEdit.Password)



    def toggle_password_visibility2(self, state):
        if state == Qt.Checked:
            # Show password
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.confirm_password_input.setEchoMode(QLineEdit.Password)


    def validate_password(self, password):
       
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(password_pattern)

        # Use match method to check if the input password matches the pattern
        if regex.match(password):
            self.password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.password_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")



            # Set font size back to normal
        font = self.password_input.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.password_input.setFont(font)


    def validate_confirmation_password(self):
        # Get the content of both password fields
        password = self.password_input.text()
        confirmation_password = self.confirm_password_input.text()

        # Check if the confirmation password matches the original password
        if password == confirmation_password:
            # Matching passwords, apply green border
            self.confirm_password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Non-matching passwords, apply red border
            self.confirm_password_input.setStyleSheet("border-radius: 25px; border: 2px solid red;")

            # Set font size back to normal
            font = self.password_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.confirm_password_input.setFont(font)




    @pyqtSlot()
    def reset_password_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.password_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    @pyqtSlot()
    def reset_confirm_password_input_style(self):
        self.confirm_password_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")



    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def save_user_details(self):

        if self.password_input.text().strip() == "":
            self.notification_label.setText("Please Enter Password.")
            self.notification_label.show()
            self.notification_label.setGeometry(575,600,350,50)
            return

            # If all required fields are filled, hide the notification and proceed
        self.notification_label.hide()
            # Proceed with the registration process
         # Retrieve user details from input fields
        password_input = self.password_input.text()
        confirmation_password = self.confirm_password_input.text()


        

       

    # Check if SessionId is available before creating the continueWindow instance
        if hasattr(self, 'SessionId') and self.SessionId:
            self.continue_window = continueWindow(
                self.SessionId, self.first_name, self.last_name,
                self.dob, self.gender, self.phone_number, self.email
        )
            
        else:
            QMessageBox.critical(self, "Error", "SessionId not available.")
        

        try:
            # Connect to the database
            with mysql.connector.connect(host="localhost", port=3307, user="root", password="S3cR3tUs3R",
                                         db="desktopdb") as db:
                # Create a cursor object
                with db.cursor() as cursor:
                    # Hash the password before storing it
                    hashed_password = hashlib.sha256(password_input.encode()).hexdigest()

                   
                        # Insert the hashed password into the database
                    insert_query="INSERT INTO registerdb (SessionId, Firstname, Lastname, Dob, Gender, Phonenumber,Email, Password, PasswordHash) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s )" 
                    new_user_data = (self.SessionId, self.first_name, self.last_name, self.dob, self.gender, self.email, password_input, hashed_password)  
                    #update_query = "UPDATE registerdb SET column1 = %s, column2 = %s, ... WHERE SessionId = %s"
                    new_user_data = (self.SessionId, self.first_name, self.last_name, self.dob, self.gender, self.phone_number, self.email, password_input,hashed_password)   
                        
        # Execute the update query with the complete user data and session ID

        # Optionally, you can delete the temporary data associated with the session ID
                      #  delete_query = "DELETE FROM registerdb WHERE SessionId = %s"
        
        # Execute the delete query to clean up temporary data
                    if password_input!= confirmation_password:
            # Display a message box indicating password mismatch
                        QMessageBox.warning(self, "Password Mismatch", "Password and confirm password do not match.")
                        return
            

              
                    cursor.execute(insert_query,new_user_data)
                    db.commit()

                       # cursor.execute(update_query, (self.SessionId))
                       # db.commit() 
                       # cursor.execute(new_user_data)
                       # cursor.execute(delete_query, (self.SessionId,))
                        #db.commit() 
                    QMessageBox.information(self, "Registration Successful",
                                                "The user has been registered successfully.")
                        
                        
                    cursor.close()
                        
                    db.close()
           

            

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to register user. Error: {e}")

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
           
        
        


    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel

class Forgot_PasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Forgot Password Window")
        self.setGeometry(100, 100, 1500, 900)

        self.db = self.create_db_connection()  # Initialize db attribute during object creation

        
        

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 1500, 900)

        # Loading a list of images
        self.image_paths = ["desk.jpg"]

        # Load intial image
        self.load_image()

           # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Forgot My</><p> Password </>", self)
        label_height= 200  # Adjust the width of the label as needed
        label_width = 900
        # label_x = (self.width() - label_width) // 2  # Center the label horizontally
        # label_y = 20
        self.welcome_label.setGeometry(300, 10, label_width, label_height)
        self.welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 20px; font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Create a line edit for the email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(575, 280, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.email_input.setPlaceholderText(" Enter Current Email ")
        # Apply styling to the email input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.email_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        self.email_input.addAction(icon, QLineEdit.LeadingPosition)

        # Connect textChanged signal to validate_email slot
        self.email_input.textChanged.connect(self.validate_email)
        self.email_input.editingFinished.connect(self.reset_email_input_style)

        # Create a line edit for password input field
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(575, 360, 350, 50)
        # Set placeholder text for the password input field
        self.password_input.setPlaceholderText("Enter New Password")
        # Appply styling to the password input field
        self.password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        # Enable the clear button to the clear input
        self.password_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        icon = QIcon("padlock.png")
        self.password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.validate_password)
        self.password_input.editingFinished.connect(self.reset_password_input_style)

         # Create checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(570, 415, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Create a line edit for confirming password input field
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setGeometry(575, 455, 350, 50)
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        self.confirm_password_input.setClearButtonEnabled(True)
        icon = QIcon("padlock.png")
        self.confirm_password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.textChanged.connect(self.validate_confirmation_password)
        self.confirm_password_input.editingFinished.connect(self.reset_confirm_password_input_style)



       

         # Create checkbox to toggle password visibility for confirm password
        self.show_confirm_password_checkbox = QCheckBox("Show Password", self)
        self.show_confirm_password_checkbox.setStyleSheet("color: black; font-size: 16px")
        self.show_confirm_password_checkbox.setGeometry(570, 510, 200, 30)
        self.show_confirm_password_checkbox.stateChanged.connect(self.toggle_confirm_password_visibility)

        
        

        # Create QLabel for notification messages
        self.notification_label = QLabel("", self)
        self.notification_label.setGeometry(575, 600, 600, 50)
        self.notification_label.setStyleSheet("color: red; font-size: 25px;")

        #login

        self.login_button = QPushButton("login", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.login_button.setGeometry(button_x, 800, button_width, 70)
        self.login_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        self.login_button.clicked.connect(self.open_login_window)


                #Save and Submit

        self.save_and_submit_button = QPushButton("Save and Submit", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.save_and_submit_button.setGeometry(button_x, 700, button_width, 70)
        self.save_and_submit_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:brown
                      }
                  """)
        self.save_and_submit_button.clicked.connect(self.change_password)

        self.regenerate_otp_button = QPushButton(self)
        self.regenerate_otp_button.setIcon(QIcon("refresh-page-option.png"))  # Set the icon for the button
        self.regenerate_otp_button.setToolTip("Regenerate OTP")  # Optional tooltip for the button
        # Adjust the position and size of the button as needed
        self.regenerate_otp_button.setGeometry(935, 500, 40, 40)
        self.regenerate_otp_button.setStyleSheet("""
                     QPushButton {
                     background-color: blue;
                      font-size: 18pt; 
                      border-radius: 35px;
                      }
                       QPushButton:hover{
                          background-color:#333333
                      }
                  """)
        self.regenerate_otp_button.hide()
        self.regenerate_otp_button.clicked.connect(self.generate_otp)  # Connect the clicked signal
        
        
     

        self.otp_generated = False
        self.otp = ""

        #Create a QLabel for the information display 
        
        self.info_label = QLabel("<html><p>Enter the OTP....You have 3 minutes<p></html> ", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setGeometry(575,360,400,40)
        self.info_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.info_label.hide() # Hide the info label initially
        

        #create a container widget for the otp input
        self.container = QWidget(self)
        self.container.setGeometry(575,400,400,100)
        self.container.setStyleSheet("background-color: blue; border-radius: 5px; padding: 5px;")
        self.container.hide()
        

        # Create a QVBoxLayout for the container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)  # No margins
       # self.container_layout.setParent(email_widget)


       

        #Create a QHBoxlayout for the OTP boxes 
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10,10,10,10) #set Margins
      #  self.layout.setParent(email_widget)

        #Create Six QLineEDIT Boxes for the otp
        self.otp_boxes = []
        for _ in range(6):
            otp_box = QLineEdit(self.container)
            otp_box.setFixedSize(50, 50)  # Set fixed size for each box
            otp_box.setMaxLength(1)  # Limit input to one character
            otp_box.setAlignment(Qt.AlignCenter)  # Center align text
            otp_box.setStyleSheet(
                "background-color: white; border: 1px solid black; border-radius: 10px; font-size: 18px;")
            self.layout.addWidget(otp_box)
            self.otp_boxes.append(otp_box)
             # Connect textChanged signal to handle_otp_input slot
            otp_box.textChanged.connect(self.handle_otp_input)


        self.container_layout.addLayout(self.layout)


           # Create a QLabel for time remaining display (initially hidden)
        
        self.timer_label = QLabel("<html><p>Time remaining....180 seconds<p></html> ", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setGeometry(575,500,360,40)
        self.timer_label.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 100px; font-size: 10pt;")
        self.timer_label.hide()


    
    def handle_otp_input(self, text):
        current_box = self.sender()  # Get the sender QLineEdit
        index = self.otp_boxes.index(current_box)
        if len(text) == 1 and index < len(self.otp_boxes) - 1:
            self.otp_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp_boxes) - 1:
            self.check_otp()
               

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time remaining: {self.time_left} seconds")
        if self.time_left == 0:
            self.timer.stop()
            self.clear_otp_input()
            self.otp_generated
            self.otp_generated = False
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
    
    
       
           
          

        
        
     
    def start_timer(self):

         # Check if timer is already running, stop it first
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
           # Initialize timer
        self.time_left = 60 # 3 minutes (180 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update timer every second
    




        

    def create_db_connection(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                password="S3cR3tUs3R",
                database="desktopdb"
            )
            return db
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to connect to the database. Error: {e}")
            return None
        
    def fetch_email(self):
        

        

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT Email FROM registerdb")
            Email = [Email[0] for Email in cursor.fetchall()]
            cursor.close()
            return Email
        except Exception as e:
            print(f"Error fetching Email: {e}")
            return []     


    def change_password(self):
        email = self.email_input.text()
        new_password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        entered_otp = self.otp


        email_list = self. fetch_email()



        if email not in email_list:
            self.notification_label.setText("Please Enter A Valid Email Address")
            self.notification_label.show()
            return
        
        if new_password == "":
            self.notification_label.setText("Please Enter Your New Password")
            self.notification_label.show()
            return
        
        if confirm_password == " ":
            self.notification_label.setText("Please Confirm Your Password")
            self.notification_label.show()
            return
        
        

        if entered_otp =="":
            self.generate_otp()
            self.email_input.hide()
            
            self.password_input.hide()
            
            self.confirm_password_input.hide()
            
            self.show_password_checkbox.hide()
            self.show_confirm_password_checkbox.hide()
            
            
            
            self.otp_generated = True
            
            self.info_label.show()
            self.container.show()
            self.timer_label.show()
            self.regenerate_otp_button.show()
            self.notification_label.setText("")
            self.start_timer()
            

        self.notification_label.hide()    

    def update_database(self):
        email = self.email_input.text()
        new_password = self.password_input.text()
        
        try:
            if self.db is None:
                return
            
            #Create Cursor:
            cursor = self.db.cursor()
            hash_password = hashlib.sha256(new_password.encode()).hexdigest()
        
            
            # Execute SELECT query to check login credentials
            sql = "UPDATE registerdb SET Password = %s, PasswordHash = %s WHERE Email = %s"
            cursor.execute(sql, (new_password, hash_password, email))

            self.db.commit()
            cursor.close()


            QMessageBox.information(self, "Password Changed", "You have successfully changed your Password.")
            self.email_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
      

    def generate_otp(self):
        email = self.email_input.text()
        self.otp = str(random.randint(100000, 999999))
        QMessageBox.information(self,"OTP", f"Sending OTP to {email}")
        QMessageBox.information(self,"OTP", f"""Your Verification code: {self.otp}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Pin""")
        

        
        self.start_timer()

   

    def clear_otp_input(self):
        for otp_box in self.otp_boxes:
            otp_box.clear()  

    def check_otp(self):
        entered_otp = "".join(box.text() for box in self.otp_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input()
           self.otp_generated = False
           return
           
        if entered_otp == self.otp:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input()
            
            self.info_label.hide()
            self.container.hide()
            self.timer_label.hide()
            self.regenerate_otp_button.hide()
            self.email_input.show()
            self.password_input.show()
            self.show_password_checkbox.show()
            self.show_confirm_password_checkbox.show()
            self.confirm_password_input.show()
            
            self.timer.stop() 

            self.update_database()
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input()
            self.otp_generated = False  
                 
           





    def validate_email(self, text):
        # Regular expression pattern for validating email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(pattern)

        # Use match method to check if the input text matches the pattern
        if regex.match(text):
            # Valid email format
            self.email_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.email_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")

            # Set font size back to normal
            font = self.email_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.email_input.setFont(font)




    @pyqtSlot()
    def reset_email_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.email_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")

    def validate_inputs(self):
        # Check if any of the required fields are empty
        if self.password_input.text().strip() == "":
            self.notification_label.setText("Please Enter Password.")
            self.notification_label.show()
            self.notification_label.setGeometry(575,600,350,50)
            return

            # If all required fields are filled, hide the notification and proceed
        self.notification_label.hide()
            # Proceed with the registration process
        self.open_login_window()
        self.close()

    
       

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            # Show password
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.password_input.setEchoMode(QLineEdit.Password)



    def toggle_confirm_password_visibility(self, state):
        if state == Qt.Checked:
            # Show password
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
        else:
            # Hide password
            self.confirm_password_input.setEchoMode(QLineEdit.Password)


    def validate_password(self, password):
       
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?!.*\s).{8,}$'

        # Compile the pattern into a regular expression object
        regex = re.compile(password_pattern)

        # Use match method to check if the input password matches the pattern
        if regex.match(password):
            self.password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Invalid email format
            self.password_input.setStyleSheet("border-radius: 25px;  border: 5px solid red;")



            # Set font size back to normal
        font = self.password_input.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.password_input.setFont(font)


    def validate_confirmation_password(self):
        # Get the content of both password fields
        password = self.password_input.text()
        confirmation_password = self.confirm_password_input.text()

        # Check if the confirmation password matches the original password
        if password == confirmation_password:
            # Matching passwords, apply green border
            self.confirm_password_input.setStyleSheet("border-radius: 25px; border: 2px solid green;")
        else:
            # Non-matching passwords, apply red border
            self.confirm_password_input.setStyleSheet("border-radius: 25px; border: 2px solid red;")

            # Set font size back to normal
            font = self.password_input.font()
            font.setPointSize(10)  # Adjust the font size as needed
            self.confirm_password_input.setFont(font)




    @pyqtSlot()
    def reset_password_input_style(self):
        # Reset the stylesheet when the user leaves the input field
        self.password_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;") 

    @pyqtSlot()
    def reset_confirm_password_input_style(self):
        self.confirm_password_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
     


    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()         

    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel
    



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Savings and Loans App")
        self.setGeometry(100,100,1500,900)



        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)



        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 1500, 900)



        # Loading a list of images
        self.image_paths = ["image.jpg", "image5.png", "image6.png"]


        self.current_image_index = 0

        # Load intial image
        self.load_image()




        #Setting up timer to change image every 3 secs
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(4000)




        # Button for "LOGIN"
        self.login_button = QPushButton("LOGIN", self)
        button_width = 300  # Adjust the width of the button as needed
        button_x = (self.width() - button_width) // 2  # Center the button horizontally
        self.login_button.setGeometry(button_x, 350, button_width, 70)
        self.login_button.setStyleSheet("""
           QPushButton {
           background-color: blue;
            font-size: 18pt; 
            border-radius: 35px;
            }
             QPushButton:hover{
                background-color:brown
            }
        """)
        self.login_button.clicked.connect(self.open_login_window)



        # Button for "REGISTER"
        self.register_button = QPushButton("REGISTER", self)
        button_width = 300
        button_x = (self.width() - button_width ) // 2
        self.register_button.setGeometry(button_x, 450 , button_width,  70) # Adjusted position and size
        self.register_button.setStyleSheet("""
                 QPushButton {
                     background-color: blue;
                     font-size: 18pt;
                     border-radius: 35px;
                     color: white;
                 }
                 QPushButton:hover {
                     background-color: brown; /* Change color when hovered */
                 }
             """)
        self.register_button.clicked.connect(self.open_register_window)

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

       

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    def load_image(self):
        pixmap = QPixmap(self.image_paths[self.current_image_index])
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel




    def change_image(self):
        #Change the current image indec and reload the image
        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
        self.load_image()

if __name__ == "__main__":
    start_scheduler()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
