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

        title = Label(frame, text = "Choose Functionality",fg="Blue",font="TkDefaultFont 24 bold")
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
        giveReview.grid(row = 6, column = 0)

        viewReview = Button(frame, text = "View Review", command = self.viewReview)
        viewReview.grid(row = 5, column = 0)

        addInfo = Button(frame, text = "Add School Information (student discount)", command = self.addInformation)
        addInfo.grid(row = 7, column = 0)

        logoutManager = Button(frame, text = "Logout", command = self.logout)
        logoutManager.grid(row = 8, column = 0)

        frame.pack()

    def managerFunctionality(self):
        self.win.withdraw()
        self.funcScreenManager = Toplevel()
        frame = Frame(self.funcScreenManager)

        title = Label(frame, text = "Choose Functionality",fg="Blue",font="TkDefaultFont 24 bold")
        title.grid(row = 0, column = 0, columnspan = 2)

        viewTrain = Button(frame, text = "View revenue report", command = self.viewRevenueReport)
        viewTrain.grid(row = 1, column = 0)

        makeNew = Button(frame, text = "View popular route report", command = self.viewPopularRouteReport)
        makeNew.grid(row = 2, column = 0)

        logoutManager = Button(frame, text = "Logout", command = self.logout)
        logoutManager.grid(row = 3, column = 0)

        frame.pack()

    def viewTrainSchedule(self):
        self.funcScreen.withdraw()
        self.trainView = Toplevel()
        frame = Frame(self.trainView)

        self.trainNumber = StringVar()

        title = Label(frame, text= "View Train Schedule", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan = 2)

        trainNum = Label(frame, text = "Train Number: ")
        trainNum.grid(row=1,column=0, sticky=W)

        trainNumEntry = Entry(frame, textvariable = self.trainNumber)
        trainNumEntry.grid(row=1, column=1)

        spaceLabel = Label(frame, text="")
        spaceLabel.grid(row=2,column=0)

        searchButton = Button(frame, text="Search", command=self.getTrainSchedule)
        searchButton.grid(row=3, column=0, sticky=W)

        frame.pack()

    def getTrainSchedule(self):
        print("From my point of view, the CS majors are evil!")

    def makeNewReservation(self):
        self.funcScreen.withdraw()
        self.searchTrains = Toplevel()
        frame = Frame(self.searchTrains)

        self.chosenDeparture = StringVar()
        self.chosenArrival = StringVar()
        self.departDate = StringVar()

        title = Label(frame, text = "Search Trains", fg="Blue",font="TkDefaultFont 24 bold")
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
        self.searchTrains.withdraw()

        self.trainsTable = Toplevel()
        frame = Frame(self.trainsTable)

        self.trainChosen = IntVar()

        self.listofTrains = [["Hogwarts Express", "3:30 a.m.", "$220", "$100"],
                        ["Jon Snowmobile", "1:00 a.m.", "$100", "$10"],
                        ["Thomas the Tank", "12:00 p.m.", "$200", "$150"],
                        ["Dragon Wing", "2:00 p.m.", "FREE", "FREE"],
                        ]

        label = Label(frame, text = "Train")
        label.grid(row = 0, column = 0)

        label1 = Label(frame, text = "Time")
        label1.grid(row = 0, column = 1)

        label2 = Label(frame, text = "1st Class Price")
        label2.grid(row = 0, column = 2)

        label3 = Label(frame, text = "2nd Class Price")
        label3.grid(row = 0, column = 3)

        rowCount = 1
        colCount = 0

        self.classType = 0

        self.trainChoice = 0

        for trainLists in self.listofTrains:
            temp = Label(frame, text = trainLists[0])
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = trainLists[1])
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            rb = Radiobutton(frame, text = trainLists[2], variable = self.trainChosen, value = self.classType, command = self.test)
            rb.grid(row = rowCount, column = colCount)
            colCount = colCount + 1
            self.classType = self.classType + 1

            rb = Radiobutton(frame, text = trainLists[3], variable = self.trainChosen, value = self.classType, command = self.test)
            rb.grid(row = rowCount, column = colCount)
            self.trainChoice = self.trainChoice + 1
            self.classType = self.classType + 1

            colCount = 0
            rowCount = rowCount + 1

        nextB = Button(frame, text = "Next", command = self.goToTravelExtras)
        nextB.grid(row = rowCount + 1, column = 0, sticky = E)

        backB = Button(frame, text = "Back")
        backB.grid(row = rowCount + 1, column = 1, sticky = W)

        frame.pack()

    def test(self):
        print(self.listofTrains[self.trainChosen.get()])

    def goToTravelExtras(self):
        print("hi")

    def goToConfirmation(self):
        self.confirmScreen = Toplevel()
        frame = Frame(self.confirmScreen)

        title = Label(frame, text = "Confirmation")
        title.grid(row = 0, column = 0, columnspan = 2)

        reLabel = Label(frame, text = "Reservaton ID")
        reLabel = grid(row = 1, column = 0)

        entry = Entry(frame, width = 50)
        entry.grid(row = 1, column = 1)



    def updateReservation(self):
        self.funcScreen.withdraw()
        self.reserveView = Toplevel()
        frame = Frame(self.reserveView)

        self.idNum = StringVar()

        title = Label(frame, text= "Update Reservation", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan = 3)

        idNum = Label(frame, text = "Reservation ID: ")
        idNum.grid(row=1,column=0)

        idNumEntry = Entry(frame, textvariable = self.idNum)
        idNumEntry.grid(row=1, column=1)

        searchButton = Button(frame, text="Search", command=self.setReservationUpdate)
        searchButton.grid(row=1, column=2)

        frame.pack()

    def setReservationUpdate(self):
        print("Dost thou arthen an illiterate lethrblaka farmer?")

    def cancelReservation(self):
        self.cancelReservationID = StringVar()
        self.funcScreen.withdraw()
        self.cancelReservationWin = Toplevel()
        frame = Frame(self.cancelReservationWin)

        title = Label(frame, text = "Cancel Reservation", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row = 0, column = 1, columnspan = 1)

        reservationLabel = Label(frame, text = "Reservation ID")
        reservationLabel.grid(row=1,column=0, sticky=W)

        reservationIDEntry = Entry(frame, textvariable = self.cancelReservationID)
        reservationIDEntry.grid(row=1, column=1)

        searchButton = Button(frame, text="Search", command=self.cancelReservationSearch)
        searchButton.grid(row=1, column=2)

        frame.pack()

    def cancelReservationSearch(self):
        if True:
            self.cancelReservationWin.withdraw()
            self.cancelReservationWin2 = Toplevel()

            self.cancelTotalCost = StringVar()
            self.cancelDate = StringVar()
            self.cancelRefund = StringVar()

            frame = Frame(self.cancelReservationWin2)
            trainsDict = {"2163 Express" : ["3:30 a.m.", "Boston(BBY)", "New York(Penn)", "2nd Class", "$115", "3", "Alier Hu"],
                        "2543 Regional" : ["3:30 a.m.", "Boston(BBY)", "New York(Penn)", "2nd Class", "$115", "3", "Alier Hu"]
                        }

            title = Label(frame, text = "Cancel Reservation", fg="Blue", font="TkDefaultFont 24 bold")
            title.grid(row = 0, column = 3, columnspan = 2)

            label = Label(frame, text = "Train \n (Train Number)")
            label.grid(row = 1, column = 0)

            label1 = Label(frame, text = "Time \n (Duration)")
            label1.grid(row = 1, column = 1)

            label2 = Label(frame, text = "Departs From")
            label2.grid(row = 1, column = 2)

            label3 = Label(frame, text = "Arrives At")
            label3.grid(row = 1, column = 3)

            label4 = Label(frame, text = "Class")
            label4.grid(row = 1, column = 4)

            label5 = Label(frame, text = "Price")
            label5.grid(row = 1, column = 5)

            label6 = Label(frame, text = "# of Baggages")
            label6.grid(row = 1, column = 6)

            label7 = Label(frame, text = "Passengar Name")
            label7.grid(row = 1, column = 7)

            rowCount = 2
            colCount = 0

            for key in trainsDict:
                temp = Label(frame, text = key)
                print(key)
                temp.grid(row = rowCount, column = colCount)
                colCount = colCount + 1
                items = trainsDict.get(key)
                for i in range(len(trainsDict.get(key))):
                    print(items[i])
                    temp1 = Label(frame, text = items[i])
                    temp1.grid(row = rowCount, column = colCount)
                    colCount = colCount + 1
                colCount = 0
                rowCount = rowCount + 1

            label8 = Label(frame, text = "Total Cost of Reservation")
            label8.grid(row=rowCount+1,column=0, sticky=W)

            entry8 = Entry(frame, textvariable = self.cancelTotalCost)
            entry8.grid(row=rowCount+1, column=1)

            label9 = Label(frame, text = "Date of Cancellation")
            label9.grid(row=rowCount+2,column=0, sticky=W)

            entry9 = Entry(frame, textvariable = self.cancelDate)
            entry9.grid(row=rowCount+2, column=1)

            label10 = Label(frame, text = "Amount to be Refunded")
            label10.grid(row=rowCount+3,column=0, sticky=W)

            entry10 = Entry(frame, textvariable = self.cancelRefund)
            entry10.grid(row=rowCount+3, column=1)

            buttonBack = Button(frame, text = "Back", command = self.back)
            buttonBack.grid(row = rowCount+4, column = 0, stick=EW)

            submitCancelB = Button(frame, text = "Submit", command = None)
            submitCancelB.grid(row= rowCount+4, column=1, sticky=EW)

            frame.pack()

        else:
            messagebox.showerror("Error", "Enter the correct ReservationID")
            return

    def giveReview(self):
        self.funcScreen.withdraw()
        self.reviewWin = Toplevel()
        frame = Frame(self.reviewWin)

        self.trainNumber = StringVar()
        self.ratingVar = StringVar()
        self.comment = StringVar()

        self.reviewEntry = [self.trainNumber, self.ratingVar, self.comment]

        title = Label(frame, text = "Give Review")
        title.grid(row = 0, column = 0, columnspan = 2)

        trainNum = Label(frame, text = "Train Number: ")
        trainNum.grid(row=1,column=0, sticky=W)

        trainNumEntry = Entry(frame, textvariable = self.trainNumber)
        trainNumEntry.grid(row=1, column=1)

        ratingLabel = Label(frame, text = "Rating: ")
        ratingLabel.grid(row=2, column=0, sticky=W)

        ratingBox = ttk.Combobox(frame, textvariable=self.ratingVar)
        ratingBox['values'] = ["Very Good" , "Good" , "Neutral" , "Bad" , "Very Bad"]
        ratingBox.grid(row=2, column=1)

        commentBox = Label(frame, text = "Comment: ")
        commentBox.grid(row=3, column=0, sticky=W)

        commentBoxEntry = Entry(frame, textvariable = self.comment)
        commentBoxEntry.grid(row=3, column=1)

        subReview = Button(frame, text = "Submit", command = self.submitReview)
        subReview.grid(row = 4, column = 0, columnspan = 2)

        frame.pack()

    def submitReview(self):
        ratingDict = {"Very Good":"1","Good":"2","Neutral":"3","Bad":"4","Very Bad":"5"}
        for item in self.reviewEntry:
            if item.get() == "":
                messagebox.showerror("Invalid Input", "All Fields Must Be Filled")
                return
        data = self.Connect()
        cursor = data.cursor()
        cursor.execute('SELECT Train_Number FROM Train_Name WHERE Name ="{}"'.format(self.trainNumber.get()))
        trainNum = cursor.fetchone()
        cursor.close()
        data.close()
        data = self.Connect()
        cursor = data.cursor()
        if(trainNum != () and trainNum != None):
            query = 'INSERT INTO Review(Comment,Rating,Train_Number,C_Username)VALUES("{0}","{1}","{2}","{3}")'.format(self.comment.get(),ratingDict.get(self.ratingVar.get()),trainNum[0],self.username.get())
            cursor.execute(query)
            data.commit()
        else:
            messagebox.showerror("Incorrect Train Name", "Please type the correct train name.")
            return
        cursor.close()
        data.close()
        messagebox.showerror("Review Submitted", "Thank you for submitting a review.")
        self.reviewWin.destroy()
        self.funcScreen.deiconify()

    def viewReview(self):
        self.trainName = StringVar()
        self.funcScreen.withdraw()
        self.viewReviewWin = Toplevel()
        frame = Frame(self.viewReviewWin)

        title = Label(frame, text = "View Review", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row = 0, column = 0, columnspan = 2)

        reviewLabel = Label(frame, text = "Train Number")
        reviewLabel.grid(row=1,column=0, sticky=W)

        reviewEntry = Entry(frame, textvariable = self.trainName)
        reviewEntry.grid(row=1, column=1)

        nextButton = Button(frame, text="Next", command=self.viewReviewNext)
        nextButton.grid(row=2, column=1, sticky=EW)

        backB = Button(frame, text = "Back", command = self.back)
        backB.grid(row=2,column=0, sticky=EW)

        frame.pack()

    def viewReviewNext(self):
        ratingDict = {1:"Very Good",2:"Good",3:"Neutral",4:"Bad",5:"Very Bad"}
        if(self.trainName.get() == ""):
            messagebox.showerror("Invalid Input", "All Fields Must Be Filled")
            return
        data = self.Connect()
        cursor = data.cursor()
        cursor.execute('SELECT Train_Number FROM Train_Name WHERE Name ="{}"'.format(self.trainName.get()))
        trainNum = cursor.fetchone()
        cursor.close()
        data.close()
        data = self.Connect()
        cursor = data.cursor()
        if(trainNum != () and trainNum != None):
            cursor.execute('SELECT Comment,Rating FROM Review WHERE Train_Number ="{}" ORDER BY Rating ASC'.format(trainNum[0]))
            reviews = cursor.fetchall()
        else:
            messagebox.showerror("Incorrect Train Name", "Please type the correct train name.")
            return
        cursor.close()
        data.close()

        reviewDict = []
        for x in range(len(reviews)):
            reviewDict.append([ratingDict.get(reviews[x][1]),reviews[x][0]])

        self.viewReviewWin.destroy()
        self.viewReviewWin2 = Toplevel()
        frame = Frame(self.viewReviewWin2)

        title = Label(frame, text = "View Review", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row = 0, column = 0, columnspan = 2)

        label = Label(frame, text = "Rating", font="TkDefaultFont 16 bold")
        label.grid(row = 1, column = 0, sticky=W)

        label1 = Label(frame, text = "Comment", font="TkDefaultFont 16 bold")
        label1.grid(row = 1, column = 1, sticky=W)

        rowCount = 2
        colCount = 0

        for trainLists in reviewDict:
            temp = Label(frame, text = trainLists[0])
            temp.grid(row = rowCount, column = colCount, sticky=W)
            colCount = colCount + 1

            temp = Label(frame, text = trainLists[1])
            temp.grid(row = rowCount, column = colCount, sticky=W)
            colCount = colCount + 1

            colCount = 0
            rowCount = rowCount + 1

        backB = Button(frame, text = "Back", command = self.back)
        backB.grid(row=rowCount + 1,column=1, sticky=EW)

        frame.pack()

    def addInformation(self):
        self.funcScreen.withdraw()
        self.addInfo = Toplevel()
        frame = Frame(self.addInfo)

        self.schoolEmail = StringVar()

        title = Label(frame, text = "Add School Info", fg="Blue",font="TkDefaultFont 24 bold")
        title.grid(row = 0, column = 0, columnspan = 2)

        schoolInfoLabel = Label(frame, text = "School Email Address")
        schoolInfoLabel.grid(row=1,column=0, sticky=W)

        schoolInfoText = Entry(frame, textvariable = self.schoolEmail)
        schoolInfoText.grid(row=1,column=1, columnspan=2)

        schoolReq = Label(frame, text = "Your school email address ends with .edu")
        schoolReq.grid(row = 2, column = 0, columnspan = 2)

        backEmail = Button(frame, text = "Back", command = self.back)
        backEmail.grid(row=3,column=0, sticky=EW)

        submitEmail = Button(frame, text = "Submit", command = self.addStudentInfo)
        submitEmail.grid(row=3,column=1, sticky=EW)

        frame.pack()

    def addStudentInfo(self):
        if(findall("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.edu$)",self.schoolEmail.get()) != []):
            data = self.Connect()
            cursor = data.cursor()
            query = 'UPDATE Customer SET Is_Student = "1" WHERE Username ="{}"'.format(self.username.get())
            cursor.execute(query)
            data.commit()
            cursor.close()
            data.close()
            messagebox.showerror("Successful", "Successfully added student discount")
            self.addInfo.destroy()
            self.funcScreen.deiconify()
        else:
            messagebox.showerror("Invalid Email", "Please enter a .edu email address")
            return


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

    def back(self):
        print("if only")

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
