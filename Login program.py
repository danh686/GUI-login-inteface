from tkinter import *
from tkinter import messagebox
import hashlib

class LoginWindow:
    def __init__(self):
        root= Tk()
        root.geometry("300x300")
        root.resizable(False, False)
        root.title("Login")
        root.configure(bg= "light blue")
        frameHeading= Frame(root)
        frameHeading.grid(row= 0, column= 0,columnspan= 2,padx= 30, pady=10)
        frameHeading.configure(bg= "light blue")
        frameEntry= Frame(root)
        frameEntry.grid(row= 1, column=1, columnspan=2, padx= 30, pady=10)
        frameEntry.configure(bg= "light blue")
        Label(frameHeading, text= "Login", font= ("Arial",14)).grid(row= 0, column= 0, padx= 10, pady= 10)
        Label(frameEntry, text= "Username").grid(row= 0, column=0, padx= 10, pady= 10)
        Label(frameEntry, text= "Password").grid(row= 1, column=0, padx= 10, pady= 10)
        usernameEntry= Entry(frameEntry, width= 15)
        usernameEntry.grid(row= 0, column= 1, padx= 10, pady= 10)
        passwordEntry= Entry(frameEntry, width= 15, show= "*")
        passwordEntry.grid(row= 1, column= 1, padx= 10, pady= 10)
        Button(root, text= "Register", width= 7, command= RegisterWindow).grid(row= 2, column= 1, padx=10, pady=10)
        Button(root, text= "Login", width= 7, command= lambda : self.login(root, usernameEntry, passwordEntry)).grid(row= 2, column= 2, padx= 10, pady= 10)
        usernameEntry.focus_set()
        root.mainloop()
    
    def login(self,root, usernameEntry, passwordEntry):
        attempts= 0
        usernameGet= usernameEntry.get()
        passwordGet= passwordEntry.get()
        if not self.valid_credentials(usernameGet, passwordGet):
            messagebox.showinfo(title= "Error", message= "Incorrect username or password")
            usernameEntry.delete(0,END)
            passwordEntry.delete(0,END)
            usernameEntry.focus_set()
            attempts += 1
        if attempts > 3: 
            messagebox.showinfo(message= "Too many attempts, press ok to exit")
            root.destroy()
        elif self.valid_credentials(usernameGet, passwordGet):
            messagebox.showinfo(message= "Username and password accepted, press ok to exit")
            root.destroy()

    def valid_credentials(self,username, password): 
        with open("Login data.txt", "r") as file:
            for row in file:
                field= row.split(",")
                hash= hashlib.sha256(password.encode('UTF-8'))
                if username == field[0].strip() and hash.hexdigest() == field[1].strip():
                    return True 
        return False 

class RegisterWindow:
    def __init__(self):
        root= Tk()
        root.resizable(False, False)
        root.title("Register")
        root.configure(bg= "light blue")
        root.attributes("-topmost", True)
        root.geometry("300x300")
        frameHeading= Frame(root)
        frameHeading.grid(row= 0, column=0, columnspan=2, padx=10, pady=10)
        frameHeading.configure(bg= "light blue")
        frameEntry= Frame(root)
        frameEntry.grid(row= 1, column=1, columnspan=2, padx= 10, pady=10)
        frameEntry.configure(bg= "light blue")
        usernameEntry= Entry(frameEntry, width= 15)
        usernameEntry.grid(row= 0, column= 1, padx= 10, pady= 10)
        passwordEntry= Entry(frameEntry, width= 15, show= "*")
        passwordEntry.grid(row= 1, column= 1, padx= 10, pady= 10)
        Label(frameHeading, text= "Register", font= ("Arial",14)).grid(row= 0, column= 0, padx= 10, pady= 10)
        Label(frameEntry, text= "Confirm password").grid(row= 2, column= 0, padx=10, pady=10)
        Label(frameEntry, text= "Enter a username").grid(row= 0, column=0, padx= 10, pady= 10)
        Label(frameEntry, text= "Enter a password").grid(row= 1, column=0, padx= 10, pady= 10)
        passwordConfirm= Entry(frameEntry, width=15, show= "*")
        passwordConfirm.grid(row= 2, column= 1, padx=10, pady=10)
        confirmRegisterButton= Button(root, text= "Register", width= 7, command= lambda : self.confirmRegister(root,passwordConfirm, usernameEntry, passwordEntry))
        confirmRegisterButton.grid(row= 3, column= 2, padx= 10, pady=10)
        usernameEntry.focus_set()
        root.mainloop()

    def confirmRegister(self, root, passwordConfirm, usernameEntry, passwordEntry): 
        if passwordConfirm.get() == "" or usernameEntry.get() == "" or passwordEntry.get() == "":
            messagebox.showinfo(message= "Error: Please fill out all fields")
        elif passwordConfirm.get() != passwordEntry.get():
            messagebox.showinfo(message= "Error: Password could not be confirmed")
            passwordEntry.delete(0,END)
            passwordConfirm.delete(0,END)
            usernameEntry.focus_set()
        elif self.already_exists(usernameEntry.get()):
            messagebox.showinfo(message= "Error: Username already exists")
            usernameEntry.delete(0,END)
            usernameEntry.focus_set()
        else:
            with open("Login data.txt", "a") as file:
                hash= hashlib.sha256(passwordEntry.get().encode('UTF-8'))
                file.write("\n"+usernameEntry.get()+","+hash.hexdigest())
            messagebox.showinfo(message= "New account confirmed, press ok to exit")
            root.destroy()
        
    def already_exists(self,username):
        with open("Login data.txt", "r") as file:
            for row in file:
                field= row.split(",")
                if username == field[0].strip():
                    return True
        return False

if __name__ == "__main__":
    LoginWindow()

