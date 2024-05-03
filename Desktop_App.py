import sys
import uuid
import hashlib
import re
import random
import datetime
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QPixmap,QPalette,QBrush,QPen,QPainter
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QSize,QDate ,QCalendar ,QDateTime# Qt core manages the alignment, and the Qpropertyanimation, with the Qreact handles the animation
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
                Firstname, Lastname, Phonenumber, PasswordHash= self.get_user_details(email)
                self.log_login(Firstname, Lastname, Phonenumber, PasswordHash, email)
                self.current_user_email = email #Sets the session variable
                cursor.close()
                self.Main1_window = Main1Window(db=self.db, Firstname=Firstname, Phonenumber=Phonenumber,PasswordHash=PasswordHash, current_user_email=self.current_user_email)
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
        sql = "SELECT FirstName, LastName, Phonenumber,PasswordHash FROM registerdb WHERE Email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()  # Assuming there's only one user with the email
        cursor.close()
        return result if result else (None, None)

    def log_login(self, Firstname, Lastname,Phonenumber ,PasswordHash, email):
        try:
           cursor = self.db.cursor()
           login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           sql = "INSERT INTO login_logs (Firstname, Lastname, Email, login_time) VALUES (%s, %s, %s, %s)"
           values = (Firstname, Lastname, email, login_time)
           cursor.execute(sql, values)
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
    def __init__(self, db, current_user_email,Firstname, Phonenumber, PasswordHash):
        super().__init__()
        self.setWindowTitle(" Main  Window")
        self.setGeometry(100, 100, 1500, 900)
        self.current_user_email = current_user_email 
        self.db = db
        self.first_name = Firstname
        self.phone_number = Phonenumber
        self.pass_hash = PasswordHash
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
        self.phone_number = Phonenumber
        self.pass_hash = PasswordHash

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
        self.change_password_page() #8
        self.check_balance_page() #9
        self.mini_statement_page() # 10
        self.invest_page() #11
        self.invest_request_page() #12
        self.own_account_page() #13
        self.another_account_page()# 14
        self.wallet_page() # 15
        self.loan_balance_page() #16
        self.loan_request_page() #17
        self.savings_account_page() #18
        self.notification_page() #19
        self.email_page(db, current_user_email) # 20
        self.mobile_number_page(db, Phonenumber) #21
      


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
        home1_label = QLabel(" <html><p> Home<p></>", home1_widget)
        home1_label.setGeometry(50,150,800,500)
        home1_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home1_label.setAlignment(Qt.AlignCenter)
        home1_label.setParent(home_widget)

        
        home2_widget = QWidget()
        home2_label = QLabel(" <html><p> Home<p></>", home2_widget)
        home2_label.setGeometry(50,680,800,200)
        home2_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home2_label.setAlignment(Qt.AlignCenter)
        home2_label.setParent(home_widget)
        

        home3_widget = QWidget()
        home3_label = QLabel(" <html><p> Home<p></>", home3_widget)
        home3_label.setGeometry(900,150,350,300)
        home3_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        home3_label.setAlignment(Qt.AlignCenter)
        home3_label.setParent(home_widget)

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

        bal_label = QLabel("<html><p>Current Balance: $0.00<p></html>", balance_widget)
        
       

        self.stacked_widget.addWidget(balance_widget)    
        
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



        # Create account
        
        account_button = QPushButton(self)
        account_button.setGeometry(50, 200, 500, 50)
                         
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


    def savings_account_page(self):
        saccount_widget =QWidget()
        saccount_label = QLabel("<html><p> Create Account <p></html>", saccount_widget)
        saccount_label.setGeometry(350, 50, 600 , 80)
        saccount_label.setStyleSheet("background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")    
        saccount_label.setAlignment(Qt.AlignCenter)
        self.stacked_widget.addWidget(saccount_widget)

        #Own account button





        
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
        self.stacked_widget.addWidget(own_account_widget)

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


        # Notification 

        notification_button = QPushButton(self)
        notification_button.setGeometry(50, 360, 500, 50)
        icon = QIcon("padlock.png")                  
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

    def update_database(self):

        try:
            if self.db is None:
                QMessageBox.critical(self, "Database Error", "Database connection not established.")
                return

            cursor = self.db.cursor()
            new_email = self.new_email_input.text()
            email = self.email_input.text()

        # Update the email in the database
            sql = "UPDATE registerdb SET Email = %s WHERE Email = %s"
            cursor.execute(sql, (new_email, email))
                    
            self.db.commit()
            cursor.close()


            QMessageBox.information(self, "Email Changed", "You have successfully changed your email.")

        # Close the window or perform other actions as needed
        # Go back to the profile page
         #   profile_page_index = 6  # Set the index of the profile page in your stacked widget
            self.main_window = MainWindow()
            self.main_window.show()
            self.close() 
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
    
        
        
        
       
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

        
        self.stacked_widget.addWidget(number_widget)


    def handle_otp_input1(self, text):
        current_box = self.sender()  # Get the sender QLineEdit
        index = self.otp_boxes.index(current_box)
        if len(text) == 1 and index < len(self.otp_boxes) - 1:
            self.otp_boxes[index + 1].setFocus()  # Move focus to the next box
        elif len(text) == 1 and index == len(self.otp_boxes) - 1:
            self.check_otp1()
               

    def update_timer1(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time remaining: {self.time_left} seconds")
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
        entered_otp = self.otp # Get the entered OTP
 
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
            self.generate_otp1(number)
            self.send_otp1(number)
            print(f"""Your Verification code: {self.otp}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Email Address""")  # Print the generated OTP
            self.otp_generated1 = True
            self.info_label1.show()
            self.container.show()
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

            cursor = self.db.cursor()
            new_number = self.new_number_input.text()
            number = self.number_input.text()

        # Update the email in the database
            sql = "UPDATE registerdb SET Email = %s WHERE Email = %s"
            cursor.execute(sql, (new_number, number))
                    
            self.db.commit()
            cursor.close()


            QMessageBox.information(self, "Number Changed", "You have successfully changed your email.")

        # Close the window or perform other actions as needed
        # Go back to the profile page
         #   profile_page_index = 6  # Set the index of the profile page in your stacked widget
            self.main_window = MainWindow()
            self.main_window.show()
            self.close() 
        
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error updating logout time: {e}")
    
        
        
        
       
    def generate_otp1(self, number):
        self.otp = str(random.randint(100000, 999999))
        print(f"Sending OTP to {number}")
        print(f"""Your Verification code: {self.otp1}
For security reasons, do not share
this code with anyone. Enter this code 
to successfully change your Email Address""")  # Print the generated OTP
        self.start_timer1()

    def send_otp1(self,number):
        print(f"Sending OTP to {number}")    


    def clear_otp_input1(self):
        for otp_box in self.otp_boxes:
            otp_box.clear()  

    def check_otp1(self):
        entered_otp = "".join(box.text() for box in self.otp_boxes)

        if self.time_left <= 0:
           QMessageBox.warning(self, "OTP Expired", "Your OTP has expired. Please request a new OTP.")
           self.clear_otp_input1()
           self.otp_generated1 = False
           return
           
        if entered_otp == self.otp1:
            QMessageBox.information(self, "Success", "OTP Matched Successfully")
            self.clear_otp_input1()
            self.generate_otp1 = False
            self.info_label.hide()
            self.container.hide()
            self.timer_label.hide()
            self.regenerate_otp_button.hide()
            self.timer.stop() 
            self.update_database1()
          
           


        else:
            QMessageBox(self, "Error", "Invalid OTP, Please try again")
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
                  
         


    def change_password_page(self):
        change_password_widget = QWidget()
       
        change_password_label = QLabel("<html><p>Change Password<p></>", change_password_widget)
        change_password_label.setGeometry(300,50,600,80)
        change_password_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        change_password_label.setAlignment(Qt.AlignCenter)
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
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(40, 247, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.show_password_checkbox.setParent(change_password_widget)


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
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(40, 347, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility1)



        self.show_password_checkbox.setParent(change_password_widget)


        
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
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(40, 447, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility2)
        self.show_password_checkbox.setParent(change_password_widget)


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
                          background-color:brown
                      }
                  """)
        self.save_and_submit_button.setParent(change_password_widget)
      #  self.save_and_submit_button.clicked.connect(self.save_user_details)

    

        self.stacked_widget.addWidget(change_password_widget)  



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
