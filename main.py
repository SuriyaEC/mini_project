from User import User

print("Wellcome")
print("1. Register\n2. Login\n3. Forgot password")
ch = input("choose : ")

if ch == '1':
    u = User()
    u.register()
    print("To continue Please Login here")
    u.login()
elif ch == '2':
    u = User()
    u.login()
elif ch == '3':
    u = User()
    u.forgot_password()
else:
    print("Invalid choose")