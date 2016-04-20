from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
        self.userstate = None
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

        self.user = StringVar()
        self.email = StringVar()
        self.pass1 = StringVar()
        self.pass2 = StringVar()
        self.entrys = [self.user, self.email, self.pass1, self.pass2]

        lb0 = Label(win2, text = "Username:")
        lb0.grid(row=0,column=0, sticky=W)

        e0 = Entry(win2, textvariable = self.user)
        e0.grid(row=0,column=1, columnspan=4)

        lb1 = Label(win2, text = "Email:")
        lb1.grid(row=1,column=0, sticky=W)

        e0 = Entry(win2, textvariable = self.email)
        e0.grid(row=1,column=1, columnspan=4)

        lb2 = Label(win2, text = "Password:")
        lb2.grid(row=2,column=0, sticky=W)

        e2 = Entry(win2, textvariable = self.pass1, show ="*")
        e2.grid(row=2,column=1, columnspan=4)

        lb2 = Label(win2, text = "Confirm Password:")
        lb2.grid(row=3,column=0, sticky=W)

        e2 = Entry(win2, textvariable = self.pass2, show ="*")
        e2.grid(row=3,column=1, columnspan=4)

        b2 = Button(win2, text = "Create", command = self.checkRegistration)
        b2.grid(row=4,column=2,columnspan=2, sticky=EW)

        win2.pack()

    def checkRegistration(self):
        for item in self.entrys:
            if item.get() == "":
                messagebox.showerror("Invalid Input", "All Fields Must Be Filled")
                return
        data = self.Connect()
        cursor = data.cursor()
        cursor.execute('SELECT Username,Email FROM Customer NATURAL LEFT JOIN Manager UNION SELECT Username,Email FROM Customer NATURAL RIGHT JOIN Manager')
        usernames = cursor.fetchall()
        cursor.close()
        data.close()
        for name in usernames:
            if self.user.get() == name[0]:
                messagebox.showerror("Invalid Username", "The username already exists. Please try again with a unique username!")
                return
            if self.email.get() == name[1]:
                messagebox.showerror("Invalid Email", "The email already exists. Please try again with a unique email!")
                return
        if findall("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",self.email.get()) == []:
            messagebox.showerror("Invalid Email","This email is improperly formatted")
            return
        if findall("((?=.*\d)(?=.*[A-Z]))",self.pass1.get()) == []:
            messagebox.showerror("Invalid Password","The password must contain at least one number and at least one uppercase letter.")
            return
        if self.pass1.get() != self.pass2.get():
            messagebox.showerror("Passwords Do Not Match","Please make sure the passwords match!")
            return
        data = self.Connect()
        cursor = data.cursor()
        query = 'INSERT INTO Customer(Username,Password,Email)VALUES("{0}","{1}","{2}")'.format(self.user.get(),self.pass1.get(),self.email.get())
        cursor.execute(query)
        data.commit()
        cursor.close()
        data.close()
        messagebox.showinfo("Welcome!", "Registration was sucessful!")
        self.winregister.destroy()
        self.win.deiconify()

    def login(self):
        userpass = [(),()]
        data = self.Connect()
        cursor = data.cursor()
        cursor.execute('SELECT Password FROM Customer WHERE Username ="{}"'.format(self.username.get()))
        userpass[0] = cursor.fetchone()
        cursor.execute('SELECT Password FROM Manager WHERE Username ="{}"'.format(self.username.get()))
        userpass[1] = cursor.fetchone()
        cursor.close()
        data.close()
        if (userpass[0] != () and userpass[0] != None):
            if (self.password.get() == userpass[0][0]):
                messagebox.showinfo("Login Successful!", "You are now logged in")
                self.win.withdraw()
                #calls the functionality window with the user data
                self.customerFunctionality()
                self.userstate = 0
            else:
                messagebox.showerror("Invalid Password","Please check that the password is correct!")
        elif (userpass[1] != () and userpass[1] != None):
            if (self.password.get() == userpass[1][0]):
                messagebox.showinfo("Login Successful!", "You are now logged in as a manager")
                self.win.withdraw()
                #calls the functionality window with the manager data
                self.managerFunctionality()
                self.userstate = 1
            else:
                messagebox.showerror("Invalid Password","Please check that the password is correct!")
        else:
            messagebox.showerror("Invalid Username","Please Enter A Valid Username Or Try Registering")

    def customerFunctionality(self):
        self.win.withdraw()
        self.funcScreen = Toplevel()
        frame = Frame(self.funcScreen)

        title = Label(frame, text = "Choose Functionality")
        title.grid(row = 0, column = 0, columnspan = 2)

        viewTrain = Button(frame, text = "View Train Schedule", command = self.viewTrainSchedule)
        viewTrain.grid(row = 1, column = 0)

        makeNew = Button(frame, text = "Make a new Reservation", command = self.makeNewReservation)
        makeNew.grid(row = 2, column = 0)

        updateRes = Button(frame, text = "Update a Reservation", command = self.updateReservation)
        updateRes.grid(row = 3, column = 0)

        cancel = Button(frame, text = "Cancel a Reservation", command = self.cancelReservation)
        cancel.grid(row = 4, column = 0)

        giveReview = Button(frame, text = "Give Review", command = self.giveReview)
        giveReview.grid(row = 5, column = 0)

        addInfo = Button(frame, text = "Add School Information (student discount)", command = self.addInformation)
        addInfo.grid(row = 6, column = 0)

        frame.pack()

    def managerFunctionality(self):
        self.win.withdraw()
        self.funcScreenManager = Toplevel()
        frame = Frame(self.funcScreenManager)

        title = Label(frame, text = "Choose Functionality")
        title.grid(row = 0, column = 0, columnspan = 2)

        viewTrain = Button(frame, text = "View revenue report", command = self.viewRevenueReport)
        viewTrain.grid(row = 1, column = 0)

        makeNew = Button(frame, text = "View popular route report", command = self.viewPopularRouteReport)
        makeNew.grid(row = 2, column = 0)

        logoutManager = Button(frame, text = "Logout", command = self.logout)
        logoutManager.grid(row = 3, column = 0)

        frame.pack()

    def viewTrainSchedule(self):
        print("hi")

    def makeNewReservation(self):
        self.funcScreen.withdraw()
        self.searchTrains = Toplevel()
        frame = Frame(self.searchTrains)

        self.chosenDeparture = StringVar()
        self.chosenArrival = StringVar()
        self.departDate = StringVar()

        title = Label(frame, text = "Search Trains")
        title.grid(row = 0, column = 0, columnspan = 2)

        departFrom = Label(frame, text = "Departs from")
        departFrom.grid(row = 1, column = 0)

        departBox = ttk.Combobox(frame, textvariable = self.chosenDeparture)
        departBox['values'] = ["Winterfell", "King's Landing", "Harrenhall"]
        departBox.grid(row = 1, column = 1)

        arrive = Label(frame, text = "Arrives at");
        arrive.grid(row = 2, column = 0)

        arriveBox = ttk.Combobox(frame, textvariable = self.chosenArrival)
        arriveBox['values'] = ["Hogwarts", "Markarth", "Winterhold", "The Reach"]
        arriveBox.grid(row = 2, column = 1)

        date = Label(frame, text = "Departure Date")
        date.grid(row = 3, column = 0)

        dateBox = ttk.Combobox(frame, textvariable = self.departDate)
        dateBox['values'] = ["7/16/1996"]
        dateBox.grid(row = 3, column = 1)

        findTrains = Button(frame, text = "Find Trains", command = self.findTrains)
        findTrains.grid(row = 4, column = 0, sticky = E)

        frame.pack()

    def findTrains(self):
        print("trololol")

    def updateReservation(self):
        print("hi")

    def cancelReservation(self):
        print("hi")

    def giveReview(self):
        print("hi")

    def addInformation(self):
        print("hi")

    def cancel(self):
        print("hi")

    def viewRevenueReport(self):
        print("hi")

    def viewPopularRouteReport(self):
        print("hi")

    def logout(self):
        if self.userstate == 0:
            self.funcScreen.destroy()
        elif self.userstate == 1:
            self.funcScreenManager.destroy()
        self.win.deiconify()
        self.username.set("")
        self.password.set("")
        self.userstate = None

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