from tkinter import *
import urllib.request
import pymysql
from re import findall
import datetime

class GTTrains:

    def __init__(self,win):
        self.win = win
        self.image = PhotoImage(file="Buzz.gif")
        self.canvas = Canvas(self.win, width = 100, height = 100)
        self.canvas.pack()
        self.canvas.create_image(50,50, anchor=CENTER, image=self.image)
        self.frame = Frame(self.win)
        self.frame.pack(side=BOTTOM)
        self.username = StringVar()
        self.password = StringVar()
        #self.username.set("A")
        #self.password.set("A1")
        self.win.title("Login")

        lb0 = Label(self.frame, text = "Username:")
        lb0.grid(row=1,column=0, sticky=W)

        e0 = Entry(self.frame, textvariable = self.username)
        e0.grid(row=1,column=1, columnspan=2)

        lb1 = Label(self.frame, text = "Password:")
        lb1.grid(row=2,column=0, sticky=W)

        e1 = Entry(self.frame, textvariable = self.password, show ="*")
        e1.grid(row=2,column=1, columnspan=2)

        b1 = Button(self.frame, text = "Register", command = self.register)
        b1.grid(row=3,column=0, sticky=EW)

        b2 = Button(self.frame, text = "Login", command = self.login)
        b2.grid(row=3,column=1, sticky=EW)

    def register(self):
        self.win.withdraw()
        self.winregister = Toplevel()
        canvas = Canvas(self.winregister, width = 100, height = 100)
        canvas.pack()
        canvas.create_image(50,50, anchor=CENTER, image=self.image)
        win2 = Frame(self.winregister)

        self.name = StringVar()
        self.user = StringVar()
        self.pass1 = StringVar()
        self.pass2 = StringVar()
        self.entrys = [self.name, self.user, self.pass1, self.pass2]

        lb0 = Label(win2, text = "Last Name:")
        lb0.grid(row=0,column=0, sticky=W)

        e0 = Entry(win2, textvariable = self.name)
        e0.grid(row=0,column=1, columnspan=4)

        lb1 = Label(win2, text = "Username:")
        lb1.grid(row=1,column=0, sticky=W)

        e1 = Entry(win2, textvariable = self.user)
        e1.grid(row=1,column=1, columnspan=4)

        lb2 = Label(win2, text = "Password:")
        lb2.grid(row=2,column=0, sticky=W)

        e2 = Entry(win2, textvariable = self.pass1, show ="*")
        e2.grid(row=2,column=1, columnspan=4)

        lb2 = Label(win2, text = "Confirm Password:")
        lb2.grid(row=3,column=0, sticky=W)

        e2 = Entry(win2, textvariable = self.pass2, show ="*")
        e2.grid(row=3,column=1, columnspan=4)

        b1 = Button(win2, text = "Cancel", command = self.cancel)
        b1.grid(row=4,column=2, sticky=EW)

        b2 = Button(win2, text = "Register", command = self.checkRegistration)
        b2.grid(row=4,column=3,columnspan=2, sticky=EW)

        win2.pack()

    def cancel(self):
        print("hi")

    def checkRegistration(self):
        print("hi")


    def login(self):
        data = self.Connect()
        cursor = data.cursor()
        cursor.execute('SELECT Password FROM Customer WHERE Username ="{}"'.format(self.username.get()))
        userpass = cursor.fetchone()
        cursor.close()
        data.close()
        if (userpass != () and userpass != None):
            if (self.password.get() == userpass[0]):
                messagebox.showinfo("Login Successful!", "You are now logged in")
                self.win.withdraw()
                #calls the big window with the user data
                self.personalUserData()
            else:
                messagebox.showerror("Invalid Password","Please check that the password is correct!")
        else:
            messagebox.showerror("Invalid Username","Please Enter A Valid Username Or Try Registering")

    def Connect(self):
        try:
            connection = pymysql.connect(host = 'academic-mysql.cc.gatech.edu', passwd = "k7E1wfyD", user = "cs4400_Team_73", db = "cs4400_Team_73")
            cursor = connection.cursor()
            return connection
        except:
            print("Cannot connect to database")

window = Tk()
rankObj = GTTrains(window)
window.mainloop()
