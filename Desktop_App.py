import sys
import uuid
import hashlib
import re
import random
import datetime
import schedule
import time
import mysql.connector
from datetime import datetime, timedelta
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QPixmap,QPalette,QBrush,QPen,QPainter, QColor
from PyQt5.QtCore import QRectF, QPoint, QObject,pyqtSignal, Qt, QPropertyAnimation, QRect, QTimer, QSize,QDate ,QCalendar ,QDateTime# Qt core manages the alignment, and the Qpropertyanimation, with the Qreact handles the animation
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QStyle, QAction, QToolBar,QToolButton, QCheckBox, QMenu, QDateEdit, QMessageBox,QCalendarWidget,QStackedWidget,QFrame,QHBoxLayout


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
        self.email_input.setPlaceholderText("Enter Email, Phone, or  Account no")


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
                self.log_login(Firstname, Lastname, email)
                self.my_accountdb(Firstname, Lastname, email)
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

    def log_login(self, Firstname, Lastname, email):
        try:
           cursor = self.db.cursor()
           login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           sql = "INSERT INTO login_logs (Firstname, Lastname, Email, login_time) VALUES (%s,%s, %s, %s)"
           values = (Firstname, Lastname, email, login_time,)
           cursor.execute(sql, values)
           self.db.commit()
           cursor.close() 
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error logging login: {e}")

    def my_accountdb(self, Firstname, Lastname,email):
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
                sql1 = "INSERT INTO my_accountdb (Firstname, Lastname, Email, Balance) VALUES (%s,%s, %s, %s)"
                values = (Firstname, Lastname, email, Balance)
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
    update_home_page = pyqtSignal(str)
    
  
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
        self.update_home_page.connect(self.update_home_page_slot)

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
        self.investment_page() #2
        self.savings_page() #3
        self.transfer_page() #4
        self.loan_page() #5
        self.profile_page() #6
        self.edit_profile_page() #7
        self.change_password_page(db, current_password, current_user_email) #8
        self.check_balance_page() #9
        self.mini_statement_page() # 10
        self.invest_page() #11
        self.invest_request_page() #12
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
        self.investment_to_my_account_transfer() #29
        self.mobile_wallet_to_account_transfer() #30
        self.transfer_to_my_saving_account() #31
        self.transfer_to_investment_account() #32
        self.transfer_to_mobile_wallet() #33
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
       
        Home_button.setGeometry(10, 100, 150, 30)
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
        account_button.setGeometry(-7,180,150,30)
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
        

        investment_button = QPushButton("Investment", self.frame)
        investment_button.setGeometry(10,260,150,30)
        self.set_button_icon2(investment_button, "investment.png")
        investment_button.setStyleSheet("""
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
        investment_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))  # Switch to home page


        savings_button = QPushButton("Savings", self.frame)
        savings_button.setGeometry(-7,340,150,30)
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
        transfer_button.setGeometry(-7,420,150,30)
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
        loan_button.setGeometry(-25,500,150,30)
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
        profile_button.setGeometry(-15,580,150,30)
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
    
    def set_button_icon2(self, investment_button, icon_path):
        icon = QIcon(icon_path)
        investment_button.setIcon(icon)
        investment_button.setIconSize(investment_button.size())  # Set icon size to button size
    

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
    def home_page(self, db , current_user_email,Firstname):
        self.current_user_email = current_user_email
        self.db = db
        self.first_name = Firstname
        
        

        home_widget = QWidget()
        self.icon_label = QLabel(self.central_widget)
        self.setCircularIcon(self.icon_label, "user.png", size = 130, position= (50,10))  # Set your icon path
        self.layout.addWidget(self.icon_label)
        self.icon_label.setParent(home_widget)

        
        home_label = QLabel(f"Welcome, {Firstname} ",home_widget)
        home_label.setGeometry(200,48,500,80)
        home_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home_label.setAlignment(Qt.AlignCenter)

        home1_widget = QWidget()
        home1_label = QLabel("""
            <html>
                <body>
                    
                        <div style=' font-size: 30px; font-weight: bold; color: red;'>Transaction</div>
                      
                    
                </body>
            </html>
        """, home1_widget)
        home1_label.setGeometry(50,150,800,500)
        home1_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home1_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        home1_label.setParent(home_widget)

        
        self.home2_widget = QWidget()
        self.home2_label = QLabel("""
            <html>
                <body>
                    
                        <div style=' font-size: 30px; font-weight: bold; color: red;'>Accounts</div>
                        <div style='text-align:center; font-size: 24px; color: white;'>No Account Created</div>
                    </div>
                </body>
            </html>
        """, self.home2_widget)
        self.home2_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Set alignment to top-left
        self.home2_label.setGeometry(50, 680, 800, 200)
        self.home2_label.setStyleSheet(
            """
            QLabel {
                background-color: black;
                color: red;
                font-size: 24px;
                padding: 20px;
                border-radius: 40px;
            }
            """
        )

        self.home2_label.setParent(home_widget)
        

        self.home3_widget = QWidget()
        self.home3_label = QLabel("""
            <html>
                <body>
                    
                        <div style=' font-size: 30px; font-weight: bold; color: red;'>Alerts</div>
                        <div style='text-align:center; font-size: 24px; color: white;'>No Alerts</div>
                    </div>
                </body>
            </html>
        """, self.home3_widget)
        self.home3_label.setGeometry(900,150,350,300)
        self.home3_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        self.home3_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.home3_label.setParent(home_widget)

        home4_widget = QWidget()
        home4_label = QLabel(" <html><p> Home<p></>", home4_widget)
        home4_label.setGeometry(900,480,350,300)
        home4_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home4_label.setAlignment(Qt.AlignCenter)
        home4_label.setParent(home_widget)


        
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

        logout_button.setParent(home_widget)

        
        
        
        self.stacked_widget.addWidget(home_widget)
        

        
        
        
        
    def update_home_page_slot(self, account_id):

       # Load circular icon
        pixmap = QPixmap("user.png")  # Replace with your circular icon path

        # Create HTML for icon and account ID
        account_info_html = f"""
            <div style='display: flex; align-items: center;'>
                <img src='user.png' width='50' height='50' style='border-radius: 50%; margin-right: 10px;'>
                <div style='font-size: 18px; color: white;'>{account_id}</div>
            </div>
        """
        

        # Update the QLabel's HTML content
        self.home2_label.setText(f"""
            <html>
                <body>
                    <div style='font-size: 30px; font-weight: bold; color: red;'>Accounts</div>
                    {account_info_html}
                </body>
            </html>
        """)
        
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
        my_account_button.setText(" | My Account")

        my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(22))

        my_account_button.setParent(balance_widget)


        
        investment_account_button = QPushButton(self)
        investment_account_button.setGeometry(50, 330, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        investment_account_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        investment_account_button.setStyleSheet("""
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
        investment_account_button.setIcon(icon)

# Set the text for the button
        investment_account_button.setText(" | Investment Account")

      #  my_account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(9))

        investment_account_button.setParent(balance_widget)


        
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
       # self.forgot_pin_button.clicked.connect(self.open_forgot_password_window)
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
            PIN = hashlib.sha256(pin.encode()).hexdigest()
            cursor = self.db.cursor()
            print(pin)
            print(PIN)
            cursor.execute("SELECT Balance FROM my_accountdb WHERE Email = %s AND PIN = %s", (email, PIN))
            result = cursor.fetchone()

            if result:
                balance = result[0]
                self.acc_label.setText(f"Gh¢{balance}.")
                self.acc_label.show()
                print(PIN + " For checking balance")
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

        hash_new_pin = hashlib.sha256(new_pin.encode()).hexdigest()
        


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
             new_pin = self.new_pin_input.text()
             hash_new_pin = hashlib.sha256(new_pin.encode()).hexdigest()
             print(new_pin)
             print(hash_new_pin + "Create pin Hash")


           

             sql = "UPDATE my_accountdb SET PIN = %s WHERE Email = %s"
             cursor.execute(sql, (hash_new_pin, email))
             print(hash_new_pin + " Update pin its still the created pin")
                                
             self.db.commit()
            
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
        self.info_label4 = QLabel("<html><p>Enter the OTP....You have 1 minutes<p></html> ", self.info_label1_widget)
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
        self.timer_label4 = QLabel("<html><p>Time remaining....60 seconds<p></html> ", self.timer_label1_widget)
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
            self.saving_balance_notification_label.setText("Please Enter Account Number.")
            self.saving_balance_notification_label.show()
            
            return
        
          # Reset UI and state for a new OTP process if OTP is already generated
        if self.otp_generated4:
            self.reset_ui_for_new_otp()
        self.calculate_and_update_balance(account_number)    


      

     

        if not self.otp_generated4:
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
        print(f"Sending OTP to {email}")
        print(f"""Your Verification code: {self.otp4}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Email Address""") 
        print(f"Sending OTP to {number}")
        print(f"""Your Verification code: {self.otp4}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Email Address""") # Print the generated OTP
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
            
            self.info_label4.hide()
            self.container4.hide()
            self.timer_label4.hide()
            self.sab_regenerate_otp_button.hide()
            self.timer.stop() 
            self.update_database4()
            
          
           


        else:
            QMessageBox.warning(self, "Error", "Invalid OTP, Please try again")
            self.clear_otp_input4()
            self.otp_generated4 = False   

        
    def mini_statement_page(self):
        statement_widget = QWidget()
       
        statement_label = QLabel("<html><p>Mini Statement-All Transactions<p></>", statement_widget)
        statement_label.setGeometry(350,50,600,80)
        statement_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        statement_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
       

        self.stacked_widget.addWidget(statement_widget) 






    def investment_page(self):
        investment_widget =QWidget()
        investment_label = QLabel("<html><p> Investment <p></html>", investment_widget)
        investment_label.setGeometry(350, 50, 600 , 80)
        investment_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        investment_label.setAlignment(Qt.AlignCenter)
       

       #Investment Balance

        investment_balance_button = QPushButton(self)
        investment_balance_button.setGeometry(50, 200, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        investment_balance_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        investment_balance_button.setStyleSheet("""
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
        icon = QIcon("investment.png")
        investment_balance_button.setIcon(icon)

# Set the text for the button
        investment_balance_button.setText(" | Check Investment Account Balance")

        investment_balance_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(11))

        investment_balance_button.setParent(investment_widget)


               #INVESTMENT REQUEST
        investment_request_button = QPushButton(self)
        investment_request_button.setGeometry(50, 280, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        investment_request_button.setIconSize(icon_size)

         # Set the icon position to the left side of the button
        investment_request_button.setStyleSheet("""
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
        icon = QIcon("investment.png")
        investment_request_button.setIcon(icon)

# Set the text for the button
        investment_request_button.setText(" | Investment Request")

        investment_request_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(12))

        investment_request_button.setParent(investment_widget)


        self.stacked_widget.addWidget(investment_widget)


    def invest_page(self):
        invest_widget = QWidget()
       
        invest_label = QLabel("<html><p>Check Investment Account Balance<p></>", invest_widget)
        invest_label.setGeometry(350,50,600,80)
        invest_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        invest_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
       

        self.stacked_widget.addWidget(invest_widget)     


    def invest_request_page(self):
        request_widget = QWidget()
       
        request_label = QLabel("<html><p>Check Investment Request<p></>", request_widget)
        request_label.setGeometry(350,50,600,80)
        request_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        request_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
       

        self.stacked_widget.addWidget(request_widget)     
        
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
            

            cursor = self.db.cursor()
            # Insert the user details into the savings_accountdb
            sql  = "UPDATE saving_accountdb SET FirstName = %s, LastName = %s, Goal = %s WHERE EMAIL = %s"
            cursor.execute(sql, (f_name, l_name, Goal, email,))
            self.db.commit()
            cursor.close()
            self.home3_label.setText(f"""
               <html>
                <body style='background-color: black; color: white; padding: 20px;'>
                    <div style='font-size: 30px; font-weight: bold; color: red; text-align: center;'>Alerts</div>
                    <div style='text-align: center; font-size: 24px; color: white;'>
                        Your account {acc_num} details<br>have been updated
                    </div>
                </body>
            </html>
        """)
            

        

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

            cursor = self.db.cursor()
            # Insert the user details into the savings_accountdb
            sql  = "INSERT INTO saving_accountdb (Email, FirstName, LastName, Account_ID, Goal, Amount) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ( email, first_name, last_name, account_id, goal,  Amount,))
            self.db.commit()
            cursor.close()
            self.update_home_page.emit(account_id)

        

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
        
               
            cursor.close()
            return None
        except Exception as e:
            return str(e)
    
    
    

    def start_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)  

    def handle_alert(self, account_id, interest):
        cursor = self.db.cursor()
        cursor.execute("SELECT Firstname, Lastname FROM saving_accountdb WHERE Account_ID = %s", (account_id,))
        account_info = cursor.fetchone()
        cursor.close()

        if account_info:
            firstname, lastname = account_info
            alert_message = f"""
            <html>
                <body>
                    <div style='font-size: 30px; font-weight: bold; color: red;'>Alerts</div>
                    <div style='text-align: center; font-size: 24px; color: white;'>
                        Account {account_id} ({firstname} {lastname}) balance updated with interest: Gh¢ {interest:.2f}
                    </div>
                </body>
            </html>
        """
        else:
            alert_message = f"""
            <html>
                <body>
                    <div style='font-size: 30px; font-weight: bold; color: red;'>Alerts</div>
                    <div style='text-align: center; font-size: 24px; color: white;'>
                        Account {account_id} balance updated with interest: Gh¢ {interest:.2f}
                    </div>
                </body>
            </html>
        """

        self.home3_label.setText(alert_message)
        




        
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
        own_account_button.setText(" | To Own Account")

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
        another_account_button.setText(" | To other Account")

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
        wallet_button.setText(" | To Wallet")

        wallet_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(15))
        wallet_button.setParent(transfer_widget)








        self.stacked_widget.addWidget(transfer_widget)

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
        my_account_button.setText(" | My Account")

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
        from_investment_button.setText(" | Investment Account")

        from_investment_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(32))

        from_investment_button.setParent(own_account_widget)

        mobile_wallet_button = QPushButton(self)
        mobile_wallet_button.setGeometry(50, 490, 500, 50)
                         
        # Set the icon size explicitly
        icon_size = QSize(30, 30)  # Adjust the size as needed
        mobile_wallet_button.setIconSize(icon_size)
         # Set the icon position to the left side of the button
        mobile_wallet_button.setStyleSheet("""
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
        mobile_wallet_button.setIcon(icon)

# Set the text for the button
        mobile_wallet_button.setText(" | Mobile Wallet")

        mobile_wallet_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(33))

        mobile_wallet_button.setParent(own_account_widget)


        

        
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
        #self.transfer_button.clicked.connect(self.perform_own_account_transfer)
        self.transfer4_button.setParent(transfer_to_my_saving_account_widget)

        self.transfer4_notify_label = QLabel("", self)
        self.transfer4_notify_label.setGeometry(50, 550, 600, 50)
        self.transfer4_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer4_notify_label.setParent(transfer_to_my_saving_account_widget)

        self.stacked_widget.addWidget(transfer_to_my_saving_account_widget)

    def transfer_to_investment_account(self) :

        transfer_to_investment_account_widget =QWidget()
        transfer_to_investment_account_label = QLabel("<html><p> Funds to Transfer to Investment Account<p></html>", transfer_to_investment_account_widget)
        transfer_to_investment_account_label.setGeometry(350, 50, 600 , 80)
        transfer_to_investment_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_to_investment_account_label.setAlignment(Qt.AlignCenter)

        self.receiver1_acc_input = QLineEdit(self)
        self.receiver1_acc_input.setGeometry(50, 200, 350, 50)
        self.receiver1_acc_input.setPlaceholderText("Investment Account Number")
        self.receiver1_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.receiver1_acc_input.setClearButtonEnabled(True)
        self.receiver1_acc_input.setParent(transfer_to_investment_account_widget)


        self.transfer5_amount_input = QLineEdit(self)
        self.transfer5_amount_input.setGeometry(50, 280, 350, 50)
        self.transfer5_amount_input.setPlaceholderText("Amount to Transfer")
        self.transfer5_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer5_amount_input.setClearButtonEnabled(True)
        self.transfer5_amount_input.setParent(transfer_to_investment_account_widget)

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
        #self.transfer_button.clicked.connect(self.perform_own_account_transfer)
        self.transfer5_button.setParent(transfer_to_investment_account_widget)

        self.transfer5_notify_label = QLabel("", self)
        self.transfer5_notify_label.setGeometry(50, 550, 600, 50)
        self.transfer5_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer5_notify_label.setParent(transfer_to_investment_account_widget)

        self.stacked_widget.addWidget(transfer_to_investment_account_widget)


    def transfer_to_mobile_wallet(self):

        
        transfer_to_mobile_wallet_widget =QWidget()
        transfer_to_mobile_wallet_label = QLabel("<html><p> Funds to Transfer to Mobile Wallet<p></html>", transfer_to_mobile_wallet_widget)
        transfer_to_mobile_wallet_label.setGeometry(350, 50, 600 , 80)
        transfer_to_mobile_wallet_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        transfer_to_mobile_wallet_label.setAlignment(Qt.AlignCenter)

        self.receiver2_acc_input = QLineEdit(self)
        self.receiver2_acc_input.setGeometry(50, 200, 350, 50)
        self.receiver2_acc_input.setPlaceholderText("Mobile Number")
        self.receiver2_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.receiver2_acc_input.setClearButtonEnabled(True)
        self.receiver2_acc_input.setParent(transfer_to_mobile_wallet_widget)


        self.transfer6_amount_input = QLineEdit(self)
        self.transfer6_amount_input.setGeometry(50, 280, 350, 50)
        self.transfer6_amount_input.setPlaceholderText("Amount to Transfer")
        self.transfer6_amount_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer6_amount_input.setClearButtonEnabled(True)
        self.transfer6_amount_input.setParent(transfer_to_mobile_wallet_widget)

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
        #self.transfer_button.clicked.connect(self.perform_own_account_transfer)
        self.transfer6_button.setParent(transfer_to_mobile_wallet_widget)

        self.transfer6_notify_label = QLabel("", self)
        self.transfer6_notify_label.setGeometry(50, 550, 600, 50)
        self.transfer6_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer6_notify_label.setParent(transfer_to_mobile_wallet_widget)

        self.stacked_widget.addWidget(transfer_to_mobile_wallet_widget)


    








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
        from_investment_account_to_my_account_button.setText(" | Investment Account")

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
      #  self.transfer_button.clicked.connect(self.perform_own_account_transfer)
        self.transfer1_button.setParent(saving_to_my_account_transfer_widget)

        self.transfer1_notify_label = QLabel("", self)
        self.transfer1_notify_label.setGeometry(50, 550, 600, 50)
        self.transfer1_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer1_notify_label.setParent(saving_to_my_account_transfer_widget)

       
        self.stacked_widget.addWidget(saving_to_my_account_transfer_widget)

    def investment_to_my_account_transfer(self):


        investment_to_my_account_transfer_widget =QWidget()
        investment_to_my_account_transfer_label = QLabel("<html><p> Investment To Account Transfer<p></html>", investment_to_my_account_transfer_widget)
        investment_to_my_account_transfer_label.setGeometry(350, 50, 600 , 80)
        investment_to_my_account_transfer_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        investment_to_my_account_transfer_label.setAlignment(Qt.AlignCenter)

        
        self.sender2_acc_input = QLineEdit(self)
        self.sender2_acc_input.setGeometry(50, 200, 350, 50)
        self.sender2_acc_input.setPlaceholderText("Enter Account Number")
        self.sender2_acc_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.sender2_acc_input.setClearButtonEnabled(True)
        self.sender2_acc_input.setParent(investment_to_my_account_transfer_widget)

        self.transfer_amount2_input = QLineEdit(self)
        self.transfer_amount2_input.setGeometry(50, 280, 350, 50)
        self.transfer_amount2_input.setPlaceholderText("Amount to Transfer")
        self.transfer_amount2_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.transfer_amount2_input.setClearButtonEnabled(True)
        self.transfer_amount2_input.setParent(investment_to_my_account_transfer_widget)

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
      #  self.transfer_button.clicked.connect(self.perform_own_account_transfer)
        self.transfer2_button.setParent(investment_to_my_account_transfer_widget)

        self.transfer2_notify_label = QLabel("", self)
        self.transfer2_notify_label.setGeometry(50, 550, 600, 50)
        self.transfer2_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer2_notify_label.setParent(investment_to_my_account_transfer_widget)

        self.stacked_widget.addWidget(investment_to_my_account_transfer_widget)


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
      #  self.transfer_button.clicked.connect(self.perform_own_account_transfer)
        self.transfer3_button.setParent(mobile_wallet_to_account_transfer_widget)

        self.transfer3_notify_label = QLabel("", self)
        self.transfer3_notify_label.setGeometry(50, 550, 600, 50)
        self.transfer3_notify_label.setStyleSheet("color: red; font-size: 25px;")
        self.transfer3_notify_label.setParent(mobile_wallet_to_account_transfer_widget)

        self.stacked_widget.addWidget(mobile_wallet_to_account_transfer_widget)
    

     
    


    def another_account_page(self):
        another_account_widget =QWidget()
        another_account_label = QLabel("<html><p> Funds to Transfer-To Other Account<p></html>", another_account_widget)
        another_account_label.setGeometry(350, 50, 600 , 80)
        another_account_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        another_account_label.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(another_account_widget)
    


    def wallet_page(self):
        wallet_widget =QWidget()
        wallet_label = QLabel("<html><p> Funds to Transfer-To Wallet<p></html>", wallet_widget)
        wallet_label.setGeometry(350, 50, 600 , 80)
        wallet_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        wallet_label.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(wallet_widget)
    

                    
        
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
       

        self.stacked_widget.addWidget(loan_balance_widget)    


    def loan_request_page(self):
        loan_request_widget = QWidget()
       
        loan_request_label = QLabel("<html><p>Loan Request<p></>", loan_request_widget)
        loan_request_label.setGeometry(350,50,600,80)
        loan_request_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        loan_request_label.setAlignment(Qt.AlignCenter)
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



        
        hash_pin = hashlib.sha256(current_pin.encode()).hexdigest()
 
    

 
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
            self.current_pin_input.clear()
            self.show_current_pin_checkbox.hide()
            self.show_new_update_pin_checkbox.hide()
            self.show_confirm_update_pin_checkbox.hide()
            self.new_update_pin_input.hide()
            self.new_update_pin_input.clear()
            self.confirm_update_pin_input.clear()
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
            
        email = self.current_user_email
        hash_updated_pin = hashlib.sha256(new_update_pin.encode()).hexdigest()

        cursor = self.db.cursor()
        sql = "UPDATE  my_accountdb SET PIN = %s WHERE Email = %s"
        cursor.execute (sql, (hash_updated_pin, email,))
        self.db.commit()
        cursor.close()
        print(hash_updated_pin + " Updated pin")

        QMessageBox.information(self, "Pin Changed", "You have successfully changed your Pin.")

        self.main_window = MainWindow()
        self.main_window.show()
        self.close() 

    
           
          
 



        
       
    def generate_otp3(self):
        email = self.current_user_email
        number = self.phone_number
        self.otp3 = str(random.randint(100000, 999999))
        print(f"Sending OTP to {email}")
        print(f"""Your Verification code: {self.otp3}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Pin""")  # Print the generated OTP
        print(f"Sending OTP to {number}")
        print(f"""Your Verification code: {self.otp3}
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
            
            self.otp_generated = False
            self.generate_otp()
            self.info_label.show()
            self.container.show()
            self.timer_label.show()
            self.regenerate_otp_button.show()
            self.notification_label.setText("")
            self.email_input.hide()
            self.email_input.clear()
            self.new_email_input.clear()
            self.confirm_email_input.clear()
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

                sql = "UPDATE saving_accountdb SET Email = %s WHERE Email = %s"
                cursor.execute(sql, (new_email, email))

                
                self.db.commit()
                    
                    
                


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
        print(f"Sending OTP to {email}")
        print(f"""Your Verification code: {self.otp}
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
            self.generate_otp = False
            self.info_label.hide()
            self.container.hide()
            self.timer_label.hide()
            self.regenerate_otp_button.hide()
            self.timer.stop() 
            self.update_database()
          

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
            self.number_input.clear()
            self.new_number_input.clear()
            self.confirm_number_input.clear()
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
                print(new_number)
                    
                self.db.commit()

                # Update the edit database with the change
                sql_update_edit = "INSERT INTO edit_db (phone_number, action2) VALUES (%s, LEFT(%s, 255))"
                action = f"Changed Phone Number from {number} to {new_number}"
                cursor.execute(sql_update_edit, (new_number, action))
                self.db.commit()
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
        print(f"Sending OTP to {number}")
        print(f"""Your Verification code: {self.otp1}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Phone Number""")  # Print the generated OTP
        self.start_timer1()

    def send_otp1(self,number):
        print(f"Sending OTP to {number}")    


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
            self.generate_otp1 = False
            self.info_label1.hide()
            self.container1.hide()
            self.timer_label1.hide()
            self.regenerate_otp_button1.hide()
            self.timer.stop() 
            self.update_database1()
          
           


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
            QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
         
                



    


    def save_and_submit2(self):

        email = self.current_user_email
        password = self.password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        entered_otp = self.otp2 # Get the entered OTP

        hash_password = hashlib.sha256(password.encode()).hexdigest()
        hash_password1 = hashlib.sha256(new_password.encode()).hexdigest()
        hash_password2 = hashlib.sha256(confirm_password.encode()).hexdigest()
 
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
        
        if hash_password1 != hash_password2:
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
            self.password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
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

           
               

        # Update the email in the database
            sql = "UPDATE registerdb SET Password = %s, PasswordHash = %s WHERE Email = %s"
            cursor.execute(sql, (new_password, hash_password, email))
            print(new_password)
                    
            self.db.commit()
            sql_update_edit = "INSERT INTO edit_db (password, action3, hashed_password) VALUES (%s, %s, %s)"
            action = f"Changed Password from {password} to {new_password}"
            cursor.execute(sql_update_edit, (new_password, action, hash_password))
            self.db.commit()
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
        print(f"Sending OTP to {email}")
        print(f"""Your Verification code: {self.otp2}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Password""") 
        print(f"Sending OTP to {number}")
        print(f"""Your Verification code: {self.otp2}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Password""") # Print the generated OTP
        self.start_timer2()

    def send_otp2(self,number):
        print(f"Sending OTP to {number}")    


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
            self.generate_otp2 = False
            self.info_label2.hide()
            self.container2.hide()
            self.timer_label2.hide()
            self.regenerate_otp_button2.hide()
            self.timer.stop() 
            self.update_database2()
          
           


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


    
    

    def handle_page_change(self, index):
        print(index)
        # When the current page changes, hide specific widgets as needed
        if index != 22:
            # Hide specific widgets in page 2 when leaving that page
            self.acc_label.hide()    
            
        if index != 18:
            self.first_name_input.clear()
            self.last_name_input.clear()
            self.goal_input.clear()
            self.notify_label.hide()
        if index != 25:
            
            self.reset_ui_for_new_otp()   
    



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
        self.account_type = ""
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



        # Line edit for account selection
        self.account_line_edit = QLineEdit(self)
        self.account_line_edit.setGeometry(575, 225, 350, 50)
        self.account_line_edit.setPlaceholderText("Select account type...")
        self.account_line_edit.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.account_line_edit.setReadOnly(True)
        self.account_line_edit.setCursorPosition(0)

        # Add dropdown arrow button
        self.dropdown_button = QToolButton(self)
        self.dropdown_button.setText("▼")
        self.dropdown_button.setStyleSheet("font-size: 16px; color : black; border : none")
        self.dropdown_button.setGeometry(900, 225, 20, 50)
        self.dropdown_button.clicked.connect(self.show_menu)


        # Create a menu for account selection
        self.menu = QMenu(self)
        self.menu.addAction("Savings Account").triggered.connect(lambda: self.update_account_line_edit("Savings Account"))
        self.menu.addAction("Loan Account").triggered.connect(lambda: self.update_account_line_edit("Loan Account"))
        self.menu.addAction("Investment Account").triggered.connect(lambda: self.update_account_line_edit("Investment Account"))
        self.menu.addAction("").triggered.connect (lambda: self.update_account_line_edit(""))

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
        if self.account_line_edit.text().strip() == "":
            self.notification_label.setText("Please select an account type.")
            self.notification_label.show()
            return

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




    def update_account_line_edit(self, account_type):
        self.account_line_edit.setText(account_type)
    def show_menu(self):
        self.menu.exec_(self.dropdown_button.mapToGlobal(QtCore.QPoint(0, self.dropdown_button.height())))


    def load_image(self):
        pixmap = QPixmap(self.image_paths[0])  # Assuming there's only one image in the list
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Ensure the image fits into the QLabel

    def open_continue_window(self):
      # Check if SessionId is available before creating the continueWindow instance
        if hasattr(self, 'SessionId') and self.SessionId:
            self.continue_window = continueWindow(self.SessionId, self.account_type,self.first_name,self.last_name,self.dob,self.gender,self.phone_number,self.email)
            self.continue_window.show()
        else:
            QMessageBox.critical(self, "Error", "SessionId not available.")

        # Retrieve user details from input fields
        account_type = self.account_line_edit.text()
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
                insert_query = "INSERT INTO registerdb (SessionId, Accounttype, Firstname, Lastname, Dob, Gender, Email, Phonenumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                user_data = (self.SessionId, account_type, first_name, last_name, dob, gender, email, phone_number)
               # cursor.execute(insert_query, user_data)
                #db.commit()
                cursor.close()
                print(user_data)
                db.close()

            # Close the current window (RegisterWindow)
                self.close()

            # Open the next window (ContinueWindow)
                self.continue_window = continueWindow(SessionId= self.SessionId,account_type=account_type, first_name=first_name, last_name= last_name, dob= dob, gender=gender, email=email, phone_number=phone_number)
                self.continue_window.show()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to register user. Error: {e}")

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()        
    

class continueWindow(QMainWindow):
    def __init__(self, SessionId, account_type, first_name, last_name,  dob, gender, email ,phone_number):
        super().__init__()
        self.setWindowTitle("Continue Window")
        self.setGeometry(100, 100, 1500, 900)
        self.SessionId = SessionId
        self.account_type = account_type  # Inherit account_type from parent class
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
                self.SessionId, self.account_type, self.first_name, self.last_name,
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

                    # Check if the hashed password already exists
                    cursor.execute("SELECT * FROM registerdb WHERE PasswordHash = %s", (hashed_password,))
                    result = cursor.fetchone()

                    if result:
                        QMessageBox.information(self, "Registration Failed",
                                                "The password is already used. Please use another password.")
                    else:
                        # Insert the hashed password into the database
                        insert_query="INSERT INTO registerdb (SessionId,Accounttype, Firstname, Lastname, Dob, Gender, Phonenumber,Email, Password, PasswordHash) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s )" 
                        new_user_data = (self.SessionId,self.account_type, self.first_name, self.last_name, self.dob, self.gender, self.email, password_input, hashed_password)  
                        #update_query = "UPDATE registerdb SET column1 = %s, column2 = %s, ... WHERE SessionId = %s"
                        new_user_data = (self.SessionId, self.account_type, self.first_name, self.last_name, self.dob, self.gender, self.phone_number, self.email, password_input,hashed_password)   
                        
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
                        print(new_user_data)
                       # print(new_user_data)
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
        self.setGeometry(100, 100, 900, 900)



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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
