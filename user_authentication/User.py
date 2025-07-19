import re
import getpass
import random
import smtplib
from email.mime.text import MIMEText

class User:
    def __init__ (self):
        self.email = ''
        self.password = ''
        self.username = ''
        self.country = ''
    
    def is_email_valid(self,email):
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$",email)

    def is_password_valid(self,password):
        if len(password) < 8 :
            return "WEAK : strong password length should be atleast 8"
        if not re.search("[a-z]",password):
            return "WEAK : should contain atleast one lowercase "
        if not re.search("[A-Z]",password):
            return "WEAK : should contain atleast one uppercase"
        if not re.search("[0-9]",password):
            return "WEAK : should contain numbers"
        if not re.search("[!@$%^&*_]",password):
            return "WEAK : should contain speacial characters"
        common_passwords = ['password','123456789','acdef']
        if password.lower() in common_passwords:
            return "WEAK : avoid using common password"
        else:
            return "STRONG : your password is stronger "

    def register(self):
        while True:
            self.email = input("Email : ")
            if self.is_email_valid(self.email):
                break
            else:
                print("Invalid email format")
        while True:            
            self.password = getpass.getpass("Password : ")
            result = self.is_password_valid(self.password)
            print(result)
            if "STRONG" in result:
                break
        self.username = input("Username : ")
        self.country = input("Country : ")

        with open("User_account.txt","a")as file:
            file.write(f"{self.email}|{self.password}|{self.username}|{self.country}\n")
            print("Registered Successfully")

    def login(self):
        self.email = input("Email : ")
        self.password = getpass.getpass("Password : ")

        with open("User_account.txt",'r') as file:
            for line in file:
                s_email, s_password, s_user, s_country = line.strip().split('|')
                if s_email == self.email and s_password == self.password:
                    print("Login Successful ")
                    print("Wellcom",s_user)
                    return True
        print("Invalid credentials")
        return False
    
    def send_otp(self,email):
        otp = str(random.randint(10000,99999))

        sender_email = 'jayasuriya2002@gmail.com'
        mail_password = 'ycudlqqnupctxkgk'
        msg = MIMEText(f"Your OTP for password reset is: {otp}")
        msg['Subject'] = 'Password Reset OTP'
        msg['From'] = sender_email
        msg['To'] = email

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(sender_email,mail_password)
            smtp.send_message(msg)
        print("otp sent,Please check email")
        
        return otp

    def forgot_password(self):
        reset_email = input("Registered Email : ")
        found = False

        with open("User_account.txt",'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            s_email, s_passowrd, s_user, s_country = line.strip().split('|')
            if reset_email == s_email:
                found = True
                otp_gen = self.send_otp(reset_email)
                otp_rec = input("OTP : ")
                if otp_rec == otp_gen:
                    print("OTP verified. reset Password")
                else:
                    print("invalid OTP")

                while True:
                    new_password = getpass.getpass("New Password : ")
                    result = self.is_password_valid(new_password)
                    print(result)
                    if "STRONG" in result:
                        con_password = getpass.getpass("Confirm Password : ")
                        if new_password == con_password :
                            print("Password changed successfully")
                            new_line = f"{s_email}|{new_password}|{s_user}|{s_country}\n"
                            new_lines.append(new_line)
                            break
                        else:
                            print("Not a Match, Try Agian")
            else:
                new_lines.append(line)
                        
        if found:
            with open("User_account.txt",'w') as file:
                file.writelines(new_lines)
        else:
            print("email not found")
                            
                    
                    

