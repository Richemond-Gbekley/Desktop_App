import sys
import uuid
import hashlib
import re
import datetime
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QPixmap,QPalette,QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QSize,QDate ,QCalendar # Qt core manages the alignment, and the Qpropertyanimation, with the Qreact handles the animation
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QStyle, QAction, QToolBar,QToolButton, QCheckBox, QMenu, QDateEdit, QMessageBox,QCalendarWidget,QStackedWidget,QFrame,QHBoxLayout


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        self.setGeometry(100, 100, 900, 900)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)


        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 900, 900)

        # Loading a list of images
        self.image_paths = ["image10.jpg"]


        # Load intial image
        self.load_image()

        # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Log into your</><p> account</>", self)
        label_width = 200  # Adjust the width of the label as needed
        label_height =900
        self.welcome_label.setGeometry(0, 10, label_height, label_width)
        self.welcome_label.setStyleSheet("background-color: white; color: black; padding: 20px; border-radius: 20px; font-size: 18pt;")
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
        button_x = 400  # Center the button horizontally
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
        self.email_input.setGeometry(280, 290, 350, 50)  # Adjust the position and size of the input field

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
        self.password_input.setGeometry(280, 350, 350, 50)

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
        self.show_password_checkbox.setGeometry(280, 410, 200, 30)
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

   
    

    # Compare the hashed passwords
              

    def open_Main1_window(self):
        self.Main1_window = Main1Window()
        self.Main1_window.show()

    '''
        email = self.email_input.text()
        password = self.password_input.text()


        try:
            with mysql.connector.connect(host="localhost", port=3307, user= "root", password="S3cR3tUs3R", db="desktopdb") as db:

            #Create Cursor:
                with db.cursor() as cursor:
                 hash_password = hashlib.sha256(password.encode()).hexdigest()
        
            
            # Execute SELECT query to check login credentials
                 query = "SELECT * FROM registerdb WHERE Email = %s AND PasswordHash = %s"
                 
                 cursor.execute(query, (email, hash_password))
                 result = cursor.fetchone()
                 print(hash_password)
                 print(password)
            

            if result:


                # Assuming the login is successful and you have retrieved user details
                Firstname, Lastname = self.get_user_details(email)
                self.log_login(Firstname, Lastname, email)


                

                self.Main1_window = Main1Window()
                self.Main1_window.show()

                
                cursor.close()
                
                db.close()


            # Close the current window (RegisterWindow)
                self.close()
                QMessageBox.information(self, "Login Successful", "You have successfully logged in.")

                
               
            else:
                
                self.Main1_window = Main1Window()
                self.Main1_window.close()

                QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
       
        except mysql.connector.Error as e :
            QMessageBox.critical(self,"Error",f"Failed to register user. Error:{e}")

    def get_user_details(self, email):
        # Fetch user details from the database based on the email
        # Modify this according to your database structure and query method
        db = mysql.connector.connect(host="localhost", port=3307, user="root", password="S3cR3tUs3R", database="desktopdb")
        cursor = db.cursor()

        # Execute the SELECT query to fetch user details based on email
        sql = "SELECT FirstName, LastName FROM registerdb WHERE Email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()  # Assuming there's only one user with the email

        # Check if a user with the provided email exists
        if result:
            Firstname, Lastname = result
            return Firstname, Lastname

    def log_login(self, Firstname, Lastname, email):
        try:
            # Your code for database connection, cursor, and inserting log entry here
            db = mysql.connector.connect(host="localhost",port=3307, user="root", password="S3cR3tUs3R", database="desktopdb")
            cursor = db.cursor()

            # Get current login time
            login_time = datetime.now()

            # Insert login log into the database
            sql = "INSERT INTO login_logs (Firstname, Lastname, Email, login_time) VALUES (%s, %s, %s, %s)"
            values = (Firstname, Lastname, email, login_time)
            cursor.execute(sql, values)

            # Commit changes and close connection
            db.commit()
            db.close()
        except mysql.connector.Error as e:
            print("Error logging login:", e)        
  '''

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    def open_forgot_password_window(self):
        self.forgot_password_window = Forgot_PasswordWindow()
        self.forgot_password_window.show()
        self.close()


class Main1Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Main  Window")
        self.setGeometry(100, 100, 900, 900)

        # Create central widget and layout
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 900, 900)

        # Loading a list of images
        self.image_paths = ["image10.jpg"]

        # Load intial image
        self.load_image()



            
        

        # Create a frame
        self.frame = QFrame(self.centralWidget())
       # self.frame.setFrameShape(QFrame.StyledPanel)  # Set the frame shape
        self.frame.setStyleSheet("background-color: #333333;")  # Set background color
             
       # frame.setGeometry(280,300,50,50)
        self.frame.setGeometry(0,0,200,900)   


         # Create a stacked widget to hold multiple pages
        self.stacked_widget = QStackedWidget(self.centralWidget())
        self.stacked_widget.setStyleSheet("background-color:white")
        self.stacked_widget.setGeometry(200, 0, 700, 900)  # Adjust size and position as needed
        # Create a QLabel to display the image
       # image_label = QLabel()
      #  image_path = "path/to/your/image.jpg"  # Replace with the actual path to your image file
     #   pixmap = QPixmap(image_path)
    #    image_label.setPixmap(pixmap)

# Add the QLabel to the stacked widget
   #     self.stacked_widget.addWidget(image_label)

        # Add pages to the stacked widget
        self.create_home_page() #0
        self.account_page() #1
        self.investment_page() #2
        self.saving_page() #3
        self.fundstransfer_page #4
        self.loan_page() #5
        self.create_profile_page() #6
        
        


        
        # Create a layout for the frame
       # frame_layout = QVBoxLayout(self.frame)    

        Home_button = QPushButton("HOME", self.frame)
       
        Home_button.setGeometry(10, 100, 100, 30)
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
       
        account_button.setGeometry(-7, 180, 150, 30)
        self.set_button_icon1(account_button, "user.png")  # Set button icon
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
        account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))  # Switch to account page

        investment_button = QPushButton("Investment", self.frame)
       
        investment_button.setGeometry(10, 260, 150, 30)
        self.set_button_icon2(investment_button, "investment.png")  # Set button icon
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
        investment_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))  # Switch to investment page
        


                   
        saving_button = QPushButton("Savings", self.frame)
       
        saving_button.setGeometry(-7, 340, 150, 30)
        self.set_button_icon3(saving_button, "piggy-bank.png")  # Set button icon
        saving_button.setStyleSheet("""
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
        saving_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))  # Switch to savings page

      
        fundstransfer_button = QPushButton("Transfer", self.frame)
        fundstransfer_button.setGeometry(-7, 420, 150, 30)
        self.set_button_icon4(fundstransfer_button, "money.png")  # Set button icon
        fundstransfer_button.setStyleSheet("""
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
        fundstransfer_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))  # Switch to Funds Transfer page


            
        loan_button= QPushButton("Loan", self.frame)
       
        loan_button.setGeometry(-25, 500, 150, 30)
        self.set_button_icon5(loan_button, "payment.png")  # Set button icon
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
        loan_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))  # Switch to loan page





        Profile_button = QPushButton("Profile", self.frame)
       
        Profile_button.setGeometry(-16, 580, 150, 30)
        self.set_button_icon6(Profile_button, "user.png")  # Set button icon
        Profile_button.setStyleSheet("""
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
        Profile_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(6))  # Switch to profile page

        
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
    
    def set_button_icon3(self, saving_button, icon_path):
        icon = QIcon(icon_path)
        saving_button.setIcon(icon)
        saving_button.setIconSize(saving_button.size())  # Set icon size to button size
    

    
    def set_button_icon4(self, fundstransfer_button, icon_path):
        icon = QIcon(icon_path)
        fundstransfer_button.setIcon(icon)
        fundstransfer_button.setIconSize(fundstransfer_button.size())  # Set icon size to button size
    
    def set_button_icon5(self, loan_button, icon_path):
        icon = QIcon(icon_path)
        loan_button.setIcon(icon)
        loan_button.setIconSize(loan_button.size())  # Set icon size to button size
    

    def set_button_icon6(self, profile_button, icon_path):
        icon = QIcon(icon_path)
        profile_button.setIcon(icon)
        profile_button.setIconSize(profile_button.size())  # Set icon size to button size
    
#Page index 0
    def create_home_page(self):
        home_widget = QWidget()
        #profile_layout = QVBoxLayout(profile_widget)
              # Label for "My Profile"
        welcome_label = QLabel("<html><p>Home<p></>")
        welcome_label.setGeometry(50,50,600,80)
        welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        welcome_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
        welcome_label.setParent(home_widget)
        
      

        
        
        self.stacked_widget.addWidget(home_widget)

#Page index 1
    def account_page(self):
        account_widget = QWidget()
          #profile_layout = QVBoxLayout(profile_widget)
              # Label for "My Profile"
        welcome_label = QLabel("<html><p>My Account<p></>")
        welcome_label.setGeometry(50,50,600,80)
        welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        welcome_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
        welcome_label.setParent(account_widget)
        
        self.stacked_widget.addWidget(account_widget)  

#Page Index 2
    def investment_page(self):
        investment_widget = QWidget()
          #profile_layout = QVBoxLayout(profile_widget)
              # Label for "My Profile"
        welcome_label = QLabel("<html><p>Investment<p></>")
        welcome_label.setGeometry(50,50,600,80)
        welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        welcome_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
        welcome_label.setParent(investment_widget)
        
      

        
        
        self.stacked_widget.addWidget(investment_widget)  

#Page Index 3
    def saving_page(self):
        savings_widget = QWidget()
          #profile_layout = QVBoxLayout(profile_widget)
              # Label for "My Profile"
        welcome_label = QLabel("<html><p>Savings<p></>")
        welcome_label.setGeometry(50,50,600,80)
        welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        welcome_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
        welcome_label.setParent(savings_widget)
        
        self.stacked_widget.addWidget(savings_widget) 

#Page Index 4
    def fundstransfer_page(self):
        fundstransfer_widget = QWidget()
   
        
        
        self.stacked_widget.addWidget(fundstransfer_widget) 



#Page Index 5
    def loan_page(self):
        loan_widget = QWidget()

        self.stacked_widget.addWidget(loan_widget) 




#Page index 6

    def create_profile_page(self):
        profile_widget = QWidget()
    


        welcome_label = QLabel("<html><p>My Profile<p></>")
        welcome_label.setGeometry(50,50,600,80)
        welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        welcome_label.setAlignment(Qt.AlignCenter)
       

        welcome_label.setParent(profile_widget)

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
                                     background-color: grey;
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
        edit_profile_button.setText("Edit Profile|")

        


        edit_profile_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(7))

        edit_profile_button.setParent(profile_widget)

        self.stacked_widget.addWidget(profile_widget)


        
       

    def editprofile_page(self):
        editprofile_widget = QWidget()
       
        welcome_label = QLabel("<html><p>Edit Profile<p></>")
        welcome_label.setGeometry(50,50,600,80)
        welcome_label.setStyleSheet(
            "background-color: black; color: white; padding: 20px; border-radius: 40px; font-size: 18pt;")
        welcome_label.setAlignment(Qt.AlignCenter)
       # profile_layout.addWidget(welcome_label)
        welcome_label.setParent(editprofile_widget)

        self.stacked_widget.addWidget(editprofile_widget)



        

    
        
        
      

        
        
        






      

    
        
              

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
        self.email = ""
        self.phone_number =""

        self.setWindowTitle("Register Window")
        self.setGeometry(100, 100, 900, 900)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 900, 900)

        # Loading a list of images
        self.image_paths = ["image10.jpg"]

        # Load intial image
        self.load_image()

        # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Create New</><p> Account</>", self)
        label_width = 200  # Adjust the width of the label as needed
        label_height = 900
        # label_x = (self.width() - label_width) // 2  # Center the label horizontally
        # label_y = 20
        self.welcome_label.setGeometry(0, 10, label_height, label_width)
        self.welcome_label.setStyleSheet(
            "background-color: white; color: black; padding: 20px; border-radius: 20px; font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignCenter)



        # Line edit for account selection
        self.account_line_edit = QLineEdit(self)
        self.account_line_edit.setGeometry(280, 225, 350, 50)
        self.account_line_edit.setPlaceholderText("Select account type...")
        self.account_line_edit.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.account_line_edit.setReadOnly(True)
        self.account_line_edit.setCursorPosition(0)

        # Add dropdown arrow button
        self.dropdown_button = QToolButton(self)
        self.dropdown_button.setText("▼")
        self.dropdown_button.setStyleSheet("font-size: 16px; color : black; border : none")
        self.dropdown_button.setGeometry(600, 225, 20, 50)
        self.dropdown_button.clicked.connect(self.show_menu)


        # Create a menu for account selection
        self.menu = QMenu(self)
        self.menu.addAction("Savings Account").triggered.connect(lambda: self.update_account_line_edit("Savings Account"))
        self.menu.addAction("Loan Account").triggered.connect(lambda: self.update_account_line_edit("Loan Account"))
        self.menu.addAction("Investment Account").triggered.connect(lambda: self.update_account_line_edit("Investment Account"))
        self.menu.addAction("").triggered.connect (lambda: self.update_account_line_edit(""))

        # Create a line edit for the First Name input field
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setGeometry(280, 285, 350, 50)  # Adjust the position and size of the input field
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
        self.last_name_input.setGeometry(280, 345, 350, 50)  # Adjust the position and size of the input field
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
        self.dob_input.setGeometry(280, 405, 350, 50)  # Adjust position and size
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
        self.dropdown_button3.setGeometry(600, 405, 20, 50)
        self.dropdown_button3.clicked.connect(self.showCalendar)
       # self.dob_input.setCalendarPopup(True) 
        #self.dob_input.setButtonSymbols(QDateEdit.CalendarButton)


        # Calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGeometry(600, 550, 350, 250)  # Adjust position and size
        self.calendar.setWindowFlags(Qt.Popup)
        self.calendar.selectionChanged.connect(self.updateDate)

        
        # Line edit for Gender Selection
        self.gender_line_edit = QLineEdit(self)
        self.gender_line_edit.setGeometry(280, 470, 350, 50)
        self.gender_line_edit.setPlaceholderText("Gender")
        self.gender_line_edit.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        self.gender_line_edit.setReadOnly(True)
        self.gender_line_edit.setCursorPosition(0)

        # Add dropdown arrow button
        self.dropdown_button1 = QToolButton(self)
        self.dropdown_button1.setText("▼")
        self.dropdown_button1.setStyleSheet("font-size: 16px; color : black; border : none")
        self.dropdown_button1.setGeometry(600, 470, 20, 50)
        self.dropdown_button1.clicked.connect(self.show_menu2)

        # Create a menu for Gender selection
        self.menu1 = QMenu(self)
        self.menu1.addAction("Male").triggered.connect(lambda: self.update_gender_line_edit(" Male "))
        self.menu1.addAction("Female").triggered.connect(lambda: self.update_gender_line_edit("Female"))
        self.menu1.addAction("").triggered.connect(lambda: self.update_gender_line_edit(""))

        # Create a line edit for the Phone Number input field
        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(280, 530, 350, 50)  # Adjust the position and size of the input field
        # Set placeholder text for the email input field
        self.number_input.setPlaceholderText(" Phone Number ")
        # Apply styling to the email input field
        self.number_input.setStyleSheet("border-radius: 25px; padding: 10px; font-size: 16px;")
        # Enable the clear button to clear the input
        self.number_input.setClearButtonEnabled(True)
        # Set an icon for the input field
        #icon = QIcon("message.png")  # Replace "icon.png" with the path to your icon file
        #self.number_input.addAction(icon, QLineEdit.LeadingPosition)

        self.number_input.textChanged.connect(self.validate_number)
        self.number_input.editingFinished.connect(self.reset_number_input_style)


        # Create a line edit for the email input field
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(280, 590, 350, 50)  # Adjust the position and size of the input field
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

        
        # Create QLabel for notification messages
        self.notification_label = QLabel("", self)
        self.notification_label.setGeometry(280, 650, 350, 50)
        self.notification_label.setStyleSheet("color: blue; font-size: 25px;")

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

        if self.email_input.text().strip() == "":
            self.notification_label.setText("Please enter your email.")
            self.notification_label.show()
            return

        if self.number_input.text().strip() == "":
            self.notification_label.setText("Please enter your phone number.")
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
        dob_raw = self.dob_input.text()
        try:
            dob = datetime.datetime.strptime(dob_raw, "%Y-%m-%d").strftime("%Y-%m-%d")
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
        self.setGeometry(100, 100, 900, 900)
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
        self.image_label.setGeometry(0, 0, 900, 900)

        # Loading a list of images
        self.image_paths = ["image10.jpg"]

        # Load intial image
        self.load_image()

        # Label for "WELCOME"
        self.welcome_label = QLabel("<html><p>Create New</><p> Account</>", self)
        label_width = 200  # Adjust the width of the label as needed
        label_height = 900
        # label_x = (self.width() - label_width) // 2  # Center the label horizontally
        # label_y = 20
        self.welcome_label.setGeometry(0, 10, label_height, label_width)
        self.welcome_label.setStyleSheet(
            "background-color: white; color: black; padding: 20px; border-radius: 20px; font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignCenter)



        # Create a line edit for password input field
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(280, 225, 350, 50)
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
        self.confirm_password_input.setGeometry(280, 320, 350, 50)
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setStyleSheet("border-radius: 25; padding : 10px; font-size: 16px; ")
        self.confirm_password_input.setClearButtonEnabled(True)
        icon = QIcon("padlock.png")
        self.confirm_password_input.addAction(icon, QLineEdit.LeadingPosition)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)



        # Create checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(280, 280, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Create checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("color: black; font-size : 16px")
        self.show_password_checkbox.setGeometry(280, 375, 200, 30)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility2)

        self.password_input.textChanged.connect(self.validate_password)
        self.password_input.editingFinished.connect(self.reset_password_input_style)
        self.confirm_password_input.textChanged.connect(self.validate_confirmation_password)

        # Create QLabel for notification messages
        self.notification_label = QLabel("", self)
        self.notification_label.setGeometry(280, 700, 350, 50)
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
        self.password_rules_label.setGeometry(280, 400, 600, 50)
        self.password_rules_label.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label.setText(
            "<html>Password must contain : <br> ✓ At least 8 characters </html>" )
        self.password_rules_label1 = QLabel(self)
        self.password_rules_label1.setGeometry(280, 425, 600, 50)
        self.password_rules_label1.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label1.setText(
            "<html> ✓ 1 Uppercase[A-Z] </html>")
        self.password_rules_label2 = QLabel(self)
        self.password_rules_label2.setGeometry(280, 445, 600, 50)
        self.password_rules_label2.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label2.setText(
            "<html> ✓ 1 Lowercase [a-z] </html>" )
        self.password_rules_label3 = QLabel(self)
        self.password_rules_label3.setGeometry(280, 465, 600, 50)
        self.password_rules_label3.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label3.setText(    
            "<html> ✓ 1 Numeric value [0-9]</html>")
        self.password_rules_label4 = QLabel(self)
        self.password_rules_label4.setGeometry(280, 485, 600, 50)
        self.password_rules_label4.setStyleSheet("color: black; font-size: 16px;")
        self.password_rules_label4.setText(    
            "<html> ✓ 1 Special characters[#,$, etc ] </html>")


    def validate_inputs(self):
        # Check if any of the required fields are empty
        if self.password_input.text().strip() == "":
            self.notification_label.setText("Please Enter Password.")
            self.notification_label.show()
            self.notification_label.setGeometry(280,600,350,50)
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
            self.notification_label.setGeometry(280,600,350,50)
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
        self.setGeometry(100,100,900,900)



        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)



        # Create a QLabel to hold the image
        self.image_label = QLabel(self.central_widget)
        self.image_label.setGeometry(0, 0, 900, 900)



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
