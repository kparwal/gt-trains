from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import urllib.request
import pymysql
from re import findall
import datetime
import random


class GTTrains:
    def __init__(self, win):
        self.getMonthDict = {"01" : "January", "02" : "February", "03" : "March",
                                "04" : "April", "05" : "May", "06" : "June",
                                "07" : "July", "08" : "August", "09" : "September",
                                "10" : "October", "11" : "November", "12" : "December"}

        self.win = win
        self.image = PhotoImage(file="Buzz.gif")
        self.canvas = Canvas(self.win, width=100, height=100)
        self.canvas.pack()
        self.canvas.create_image(50, 50, anchor=CENTER, image=self.image)
        self.frame = Frame(self.win)
        self.frame.pack(side=BOTTOM)
        self.username = StringVar()
        self.password = StringVar()
        self.userstate = None
        self.winList = []
        #self.username.set("A")
        #self.password.set("A1")
        self.win.title("Login")

        lb0 = Label(self.frame, text="Username:")
        lb0.grid(row=1, column=0, sticky=W)

        e0 = Entry(self.frame, textvariable=self.username)
        e0.grid(row=1, column=1, columnspan=2)

        lb1 = Label(self.frame, text="Password:")
        lb1.grid(row=2, column=0, sticky=W)

        e1 = Entry(self.frame, textvariable=self.password, show="*")
        e1.grid(row=2, column=1, columnspan=2)

        b1 = Button(self.frame, text="Register", command=self.register)
        b1.grid(row=3, column=0, sticky=EW)

        b2 = Button(self.frame, text="Login", command=self.login)
        b2.grid(row=3, column=1, sticky=EW)

    def register(self):
        self.win.withdraw()
        self.winregister = Toplevel()
        self.winregister.title("Register")
        canvas = Canvas(self.winregister, width=100, height=100)
        canvas.pack()
        canvas.create_image(50, 50, anchor=CENTER, image=self.image)
        win2 = Frame(self.winregister)

        self.user = StringVar()
        self.email = StringVar()
        self.pass1 = StringVar()
        self.pass2 = StringVar()
        self.entrys = [self.user, self.email, self.pass1, self.pass2]

        lb0 = Label(win2, text="Username:")
        lb0.grid(row=0, column=0, sticky=W)

        e0 = Entry(win2, textvariable=self.user)
        e0.grid(row=0, column=1, columnspan=4)

        lb1 = Label(win2, text="Email:")
        lb1.grid(row=1, column=0, sticky=W)

        e0 = Entry(win2, textvariable=self.email)
        e0.grid(row=1, column=1, columnspan=4)

        lb2 = Label(win2, text="Password:")
        lb2.grid(row=2, column=0, sticky=W)

        e2 = Entry(win2, textvariable=self.pass1, show="*")
        e2.grid(row=2, column=1, columnspan=4)

        lb2 = Label(win2, text="Confirm Password:")
        lb2.grid(row=3, column=0, sticky=W)

        e2 = Entry(win2, textvariable=self.pass2, show="*")
        e2.grid(row=3, column=1, columnspan=4)

        b2 = Button(win2, text="Create", command=self.checkRegistration)
        b2.grid(row=4, column=2, columnspan=2, sticky=EW)

        win2.pack()

    def checkRegistration(self):
        for item in self.entrys:
            if item.get() == "":
                messagebox.showerror("Invalid Input", "All Fields Must Be Filled")
                return
        data = self.Connect()
        cursor = data.cursor()
        cursor.execute(
            'SELECT Username,Email FROM Customer NATURAL LEFT JOIN Manager UNION SELECT Username,Email FROM Customer NATURAL RIGHT JOIN Manager')
        usernames = cursor.fetchall()
        cursor.close()
        data.close()
        for name in usernames:
            if self.user.get() == name[0]:
                messagebox.showerror("Invalid Username",
                                     "The username already exists. Please try again with a unique username!")
                return
            if self.email.get() == name[1]:
                messagebox.showerror("Invalid Email", "The email already exists. Please try again with a unique email!")
                return
        if findall("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email.get()) == []:
            messagebox.showerror("Invalid Email", "This email is improperly formatted")
            return
        if findall("((?=.*\d)(?=.*[A-Z]))", self.pass1.get()) == []:
            messagebox.showerror("Invalid Password",
                                 "The password must contain at least one number and at least one uppercase letter.")
            return
        if self.pass1.get() != self.pass2.get():
            messagebox.showerror("Passwords Do Not Match", "Please make sure the passwords match!")
            return
        data = self.Connect()
        cursor = data.cursor()
        query = 'INSERT INTO Customer(Username,Password,Email)VALUES("{0}","{1}","{2}")'.format(self.user.get(),
                                                                                                self.pass1.get(),
                                                                                                self.email.get())
        cursor.execute(query)
        data.commit()
        cursor.close()
        data.close()
        messagebox.showinfo("Welcome!", "Registration was sucessful!")
        self.winregister.destroy()
        self.win.deiconify()

    def login(self):
        userpass = [(), ()]
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
                # calls the functionality window with the user data
                self.customerFunctionality()
                self.userstate = 0
            else:
                messagebox.showerror("Invalid Password", "Please check that the password is correct!")
        elif (userpass[1] != () and userpass[1] != None):
            if (self.password.get() == userpass[1][0]):
                messagebox.showinfo("Login Successful!", "You are now logged in as a manager")
                self.win.withdraw()
                # calls the functionality window with the manager data
                self.managerFunctionality()
                self.userstate = 1
            else:
                messagebox.showerror("Invalid Password", "Please check that the password is correct!")
        else:
            messagebox.showerror("Invalid Username", "Please Enter A Valid Username Or Try Registering")

    def customerFunctionality(self):
        self.fullTrainList = [] # will track a single customer's full train list. Reset at this point since coming back to this screen indicates "new"
        self.win.withdraw()
        self.funcScreen = Toplevel()
        self.funcScreen.title("Customer Functionality")
        self.winList.append(self.funcScreen)
        frame = Frame(self.funcScreen)

        title = Label(frame, text="Choose Functionality", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        viewTrain = Button(frame, text="View Train Schedule", command=self.viewTrainSchedule)
        viewTrain.grid(row=1, column=0)

        makeNew = Button(frame, text="Make a new Reservation", command=self.makeNewReservation)
        makeNew.grid(row=2, column=0)

        updateRes = Button(frame, text="Update a Reservation", command=self.updateReservation)
        updateRes.grid(row=3, column=0)

        cancel = Button(frame, text="Cancel a Reservation", command=self.cancelReservation)
        cancel.grid(row=4, column=0)

        giveReview = Button(frame, text="Give Review", command=self.giveReview)
        giveReview.grid(row=6, column=0)

        viewReview = Button(frame, text="View Review", command=self.viewReview)
        viewReview.grid(row=5, column=0)

        addInfo = Button(frame, text="Add School Information (student discount)", command=self.addInformation)
        addInfo.grid(row=7, column=0)

        logoutManager = Button(frame, text="Logout", command=self.logout)
        logoutManager.grid(row=8, column=0)

        frame.pack()

    def managerFunctionality(self):
        self.win.withdraw()
        self.funcScreenManager = Toplevel()
        self.funcScreenManager.title("Manager Functionality")
        self.winList.append(self.funcScreenManager)
        frame = Frame(self.funcScreenManager)

        title = Label(frame, text="Choose Functionality", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        viewTrain = Button(frame, text="View revenue report", command=self.viewRevenueReport)
        viewTrain.grid(row=1, column=0)

        makeNew = Button(frame, text="View popular route report", command=self.viewPopularRouteReport)
        makeNew.grid(row=2, column=0)

        logoutManager = Button(frame, text="Logout", command=self.logout)
        logoutManager.grid(row=3, column=0)

        frame.pack()

    def viewTrainSchedule(self):
        self.funcScreen.withdraw()
        self.trainView = Toplevel()
        self.trainView.title("View Train Schedule")
        self.winList.append(self.trainView)
        frame = Frame(self.trainView)

        self.trainNumber = StringVar()

        title = Label(frame, text="View Train Schedule", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        trainNum = Label(frame, text="Train Number: ")
        trainNum.grid(row=1, column=0, sticky=W)

        trainNumEntry = Entry(frame, textvariable=self.trainNumber)
        trainNumEntry.grid(row=1, column=1)

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=2, column=0, sticky=EW)

        searchButton = Button(frame, text="Search", command=self.getTrainSchedule)
        searchButton.grid(row=2, column=1, sticky=EW)

        frame.pack()

    def getTrainSchedule(self):
        data = self.Connect()
        cursor = data.cursor()
        nameQuery = "SELECT Train_Number FROM Train_Name WHERE Name = '{}'".format(self.trainNumber.get())
        cursor.execute(nameQuery)
        train = cursor.fetchone()
        if train is not None or train == ():
            train = train[0]
        else:
            messagebox.showerror("Incorrect Train Name", "Please type an existing Train name")
            return
        query = "SELECT * FROM Train_Stop WHERE Train_Number = '{}' ORDER BY Arrival_Time ASC".format(train)
        schedule = cursor.execute(query)
        schedule = cursor.fetchall()
        cursor.close()
        data.close()

        self.trainView.withdraw()
        self.scheduleView = Toplevel()
        self.winList.append(self.scheduleView)
        self.scheduleView.title("View Train Schedule")
        frame = Frame(self.scheduleView)

        dataSet = []
        for index, row in enumerate(schedule):
            rowlist = []
            for idx, item in enumerate(row):
                if item is None:
                    item = ""
                if idx == 0 and index == 0:
                    rowlist.append(self.trainNumber.get())
                elif idx == 0:
                    rowlist.append("")
                else:
                    rowlist.append(item)
            dataSet.append(rowlist)

        trainsDict = {}
        count = 0
        for row in dataSet:
            tableList = []
            for col in row[1:]:
                tableList.append(col)
            trainsDict[self.trainNumber.get() + " " * count] = tableList
            count += 1


        # trainsDict = {self.trainNumber.get() : [str(dataSet[0][2]), str(dataSet[0][3]), dataSet[0][1]]}

        title = Label(frame, text="View Train Schedule", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=3)

        label = Label(frame, text="Train \n (Train Number)")
        label.grid(row=1, column=0)

        label1 = Label(frame, text="Station")
        label1.grid(row=1, column=1)

        label2 = Label(frame, text="Arrival Time")
        label2.grid(row=1, column=2)

        label3 = Label(frame, text="Departure Time")
        label3.grid(row=1, column=3)

        rowCount = 2
        colCount = 0

        # for key in trainsDict:
        #    temp = Label(frame, text = key)
        #    print(key)
        #    temp.grid(row = rowCount, column = colCount)
        #    colCount = colCount + 1
        #    items = trainsDict.get(key)
        #    for i in range(len(trainsDict.get(key))):
        #        print(items[i])
        #        temp1 = Label(frame, text = items[i])
        #        temp1.grid(row = rowCount, column = colCount)
        #        colCount = colCount + 1
        #    colCount = 0
        #    rowCount = rowCount + 1

        for row in dataSet:
            colCount = 0
            for col in row:
                temp = Label(frame, text=col)
                temp.grid(row=rowCount, column=colCount)
                colCount += 1
            rowCount += 1

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=rowCount+1, column=0, sticky=EW)

        frame.pack()

    def nested_tuple_to_list(self, tuple_struct, flat=True):
        if flat:
            flat_list = []
            for i in tuple_struct:
                for j in i:
                    flat_list.append(j)
            return flat_list
        else:
            deep_list = []
            for i in tuple_struct:
                inlist = []
                for j in i:
                    inlist.append(j)
                deep_list.append(inlist)
            return deep_list

    def makeNewReservation(self):
        try:
            self.funcScreen.withdraw()
        except:
            print("WHAT DO YOU MEAN WHEN YOU NOD YOUR HEAD YES")

        self.searchTrains = Toplevel()
        self.searchTrains.title("Make New Reservation")
        self.winList.append(self.searchTrains)
        frame = Frame(self.searchTrains)
        data = self.Connect()
        cursor = data.cursor()
        nameQuery = "SELECT DISTINCT Station_Name FROM Station"
        cursor.execute(nameQuery)
        location_list = self.nested_tuple_to_list(cursor.fetchall())
        cursor.close()
        data.close()
        self.chosenDeparture = StringVar()
        self.chosenArrival = StringVar()
        self.departDate = StringVar()

        title = Label(frame, text="Search Trains", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        departFrom = Label(frame, text="Departs from")
        departFrom.grid(row=1, column=0)

        departBox = ttk.Combobox(frame, textvariable=self.chosenDeparture)
        departBox['values'] = location_list
        departBox.grid(row=1, column=1)

        arrive = Label(frame, text="Arrives at");
        arrive.grid(row=2, column=0)

        arriveBox = ttk.Combobox(frame, textvariable=self.chosenArrival)
        arriveBox['values'] = location_list
        arriveBox.grid(row=2, column=1)

        date = Label(frame, text = "Departure Date(YYYY-MM-DD)")
        date.grid(row = 3, column = 0)

        dateBox = Entry(frame, textvariable=self.departDate)
        dateBox.grid(row=3, column=1)

        findTrains = Button(frame, text="Find Trains", command=self.findTrains)
        findTrains.grid(row=4, column=1, sticky=EW)

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=4, column=0, sticky=EW)

        frame.pack()

    def parseDate(self, userDate):
        try:
            # userDate = self.departDate.get()
            userDate = userDate.split('-')

            userDate = datetime.date(int(userDate[0]), int(userDate[1]), int(userDate[2]))

            return(userDate)
        except:
            messagebox.showerror("Incorrect Date", "Please enter date in correct format.")
            return(False)



    def findTrains(self):
        if (self.chosenDeparture.get() == self.chosenArrival.get()):
            messagebox.showerror("Invalid Entry", "Cannot have the same arrival and departure stations")
            return

        temp = [self.chosenDeparture,self.chosenArrival,self.departDate]
        for item in temp:
            if item.get() == "":
                messagebox.showerror("Invalid Input", "All Fields Must Be Filled")
                return

        self.userDate = self.parseDate(self.departDate.get())
        try:
            if (not self.userDate):
                return
        except:
            pass
        self.dateForSQL = self.parseDate(self.departDate.get())

        try:
            if (self.userDate < datetime.date.today()):
                messagebox.showerror("Incorrect Date", "Please enter future date.")
                return
        except:
                pass

        self.trainChosen = IntVar()

        self.listofTrains = []

        data = self.Connect()
        cursor = data.cursor()
        query = """
                SELECT `Name`, `Depart From`, `Arrive At`, `Departure_Time`, `Arrival_Time`, `First_Class_Price`, `Second_Class_Price`
                FROM
                (SELECT `Name`, `Depart From`, `Arrive At`, `Departure_Time`, `Arrival_Time`, `C`.`Train_Number`
                FROM
                (SELECT `A`.`Station_Name` AS `Depart From` , `B`.`Station_Name` AS `Arrive At` , `A`.`Train_Number` , `A`.`Departure_Time` , `B`.`Arrival_Time`
                FROM (

                SELECT *
                FROM `Train_Stop`
                NATURAL JOIN `Station`
                WHERE `Station_Name` = '{}'
                AND `Departure_Time` IS NOT NULL
                ORDER BY `Station_Name` ASC
                ) AS A
                INNER JOIN (

                SELECT *
                FROM `Train_Stop`
                NATURAL JOIN `Station`
                WHERE `Station_Name` = '{}'
                AND `Arrival_Time` IS NOT NULL
                ORDER BY `Station_Name` ASC
                ) AS B ON `A`.`Train_Number` = `B`.`Train_Number`) AS C INNER JOIN `Train_Name` AS D ON `C`.`Train_Number`=`D`.`Train_Number`)
                AS E INNER JOIN `Train_Route` AS F ON `E`.`Train_Number`=`F`.`Train_Number`
                """.format(self.chosenDeparture.get(), self.chosenArrival.get())
        cursor.execute(query)
        datalist = self.nested_tuple_to_list(cursor.fetchall(), False)
        # datalist = cursor.fetchall()
        cursor.close()
        data.close()
        # print("I am in the right filed")
        #  print(datalist)
        self.listofTrains = datalist

        if(self.listofTrains==[] or self.listofTrains == None):
            messagebox.showerror("Train Route Not Available", "There is no train route avaliable for those two stations.")
            return

        self.searchTrains.withdraw()
        self.trainsTable = Toplevel()
        self.trainsTable.title("Make New Reservation")
        self.winList.append(self.trainsTable)
        frame = Frame(self.trainsTable)

        label = Label(frame, text="Train")
        label.grid(row=0, column=0)

        label1 = Label(frame, text="Leaves From")
        label1.grid(row=0, column=1)

        label2 = Label(frame, text="Arrives At")
        label2.grid(row=0, column=2)

        label3 = Label(frame, text="Departure Time")
        label3.grid(row=0, column=3)

        label4 = Label(frame, text="Arrival Time")
        label4.grid(row=0, column=4)

        label5 = Label(frame, text="1st Class Price")
        label5.grid(row=0, column=5)

        label6 = Label(frame, text="2nd Class Price")
        label6.grid(row=0, column=6)

        rowCount = 1
        colCount = 0

        rowCol = 0

        for trainLists in self.listofTrains:
            temp = Label(frame, text=trainLists[0])
            temp.grid(row=rowCount, column=colCount)
            colCount = colCount + 1

            temp = Label(frame, text=trainLists[1])
            temp.grid(row=rowCount, column=colCount)
            colCount = colCount + 1

            temp = Label(frame, text=trainLists[2])
            temp.grid(row=rowCount, column=colCount)
            colCount = colCount + 1

            temp = Label(frame, text=trainLists[3])
            temp.grid(row=rowCount, column=colCount)
            colCount = colCount + 1

            temp = Label(frame, text=trainLists[4])
            temp.grid(row=rowCount, column=colCount)
            colCount = colCount + 1

            rb = Radiobutton(frame, text=trainLists[5], variable=self.trainChosen, value=rowCol)
            rb.grid(row=rowCount, column=colCount)
            colCount = colCount + 1
            rowCol = rowCol + 1

            rb = Radiobutton(frame, text=trainLists[6], variable=self.trainChosen, value=rowCol)
            rb.grid(row=rowCount, column=colCount)

            rowCol = rowCol + 9

            colCount = 0
            rowCount = rowCount + 1

        nextB = Button(frame, text="Next", command=self.goToTravelExtras)
        nextB.grid(row=rowCount + 1, column=1, sticky=EW)

        backB = Button(frame, text="Back", command=self.back)
        backB.grid(row=rowCount + 1, column=0, sticky=EW)

        frame.pack()

    def getTrainChosen(self):
        train = self.trainChosen.get()

        self.classChosen = ""

        trainIndex = train // 10
        indicator = train % 10

        self.fullTrainList = self.fullTrainList + [self.listofTrains[trainIndex]]

        if (indicator == 0):
            del self.fullTrainList[len(self.fullTrainList) - 1][6]
            self.classChosen = "First"

            self.fullTrainList[len(self.fullTrainList) - 1].append(self.classChosen)
        elif (indicator == 1):
            del self.fullTrainList[len(self.fullTrainList) - 1][5]
            self.classChosen = "Second"

            self.fullTrainList[len(self.fullTrainList) - 1].append(self.classChosen)

    def goToTravelExtras(self):
        self.getTrainChosen()
        self.trainsTable.withdraw()
        self.travelInfo = Toplevel()
        self.travelInfo.title("Make New Reservation")
        self.winList.append(self.travelInfo)
        frame = Frame(self.travelInfo)

        self.baggageNum = IntVar()
        self.passengerName = StringVar()

        title = Label(frame, text = "Travel Extras & Passenger Info", fg="Blue",font="TkDefaultFont 24 bold")
        title.grid(row = 0, column = 0, columnspan = 2)

        spaceLabel = Label(frame)
        spaceLabel.grid(row=1, column=0, columnspan=2)

        numBagLabel = Label(frame, text = "Number of Baggage", font="TkDefaultFont 13")
        numBagLabel.grid(row = 2, column = 0)

        bagEntryBox = Spinbox(frame, from_= 0, to = 4, increment = 1, textvariable = self.baggageNum, state='readonly', font="TkDefaultFont 13")
        bagEntryBox.grid(row = 2, column =1)

        bagInfo = Label(frame, text = "Passengers can bring 4 bags max (2 free of charge and 2 extra for $30 per bag)")
        bagInfo.grid(row=3, column=0, columnspan = 2)

        spaceLabel2 = Label(frame)
        spaceLabel2.grid(row=4, column=0, columnspan=2)

        passNameLabel = Label(frame, text= "Passenger Name", font="TkDefaultFont 13")
        passNameLabel.grid(row=5, column=0)

        passName = Entry(frame, textvariable = self.passengerName)
        passName.grid(row=5, column=1)

        spaceLabel3 = Label(frame)
        spaceLabel3.grid(row=6, column=0, columnspan=2)

        nextB = Button(frame, text = "Next", command = self.updateFullList)
        nextB.grid(row =7 , column = 1, sticky=EW)

        backB = Button(frame, text = "Back", command=self.back)
        backB.grid(row = 7, column = 0, sticky=EW)

        frame.pack()


    def updateFullList(self):
        if(self.passengerName.get()==""):
            messagebox.showerror("Name Missing","Please input a Passenger Name.")

            return

        self.fullTrainList[len(self.fullTrainList) - 1] = self.fullTrainList[len(self.fullTrainList) - 1] + [self.passengerName.get(), self.baggageNum.get()]
        self.makeReservation()

    def makeReservation(self):
        data = self.Connect()
        cursor = data.cursor()

        flag = self.isStudent()
        cost = IntVar()
        cost.set(self.calcCost(flag))
        self.cardChosen = StringVar()

        try:
            self.travelInfo.withdraw()
        except:
            pass

        self.make1 = Toplevel()
        self.make1.title("Make New Reservation")
        self.winList.append(self.make1)
        frame = Frame(self.make1)

        query ="SELECT Card_Num FROM Payment_Info WHERE C_Username = '{}'".format(self.username.get())
        self.datalist1 = cursor.execute(query)
        self.datalist1 = cursor.fetchall()

        cursor.close()
        data.close()

        self.cardList=[]
        for item in self.datalist1:
            self.cardList.append(item[0])


        self.fullCardList={}
        for item in range(len(self.cardList)):
            self.fullCardList[self.cardList[item][12:]] = self.cardList[item]

        discLabel = ""
        if (flag):
            discLabel = "Student Discount Added!"
        else:
            discLabel = "No discount added :("

        title = Label(frame, text = "Make Reservation")
        title.grid(row = 0, column = 0, columnspan = 2)

        discountLabel = Label(frame, text = discLabel)
        discountLabel.grid(row = 1, column = 0, sticky = EW)

        cLabel = Label(frame, text = "Total cost")
        cLabel.grid(row = 2, column = 0)

        cEntry = Entry(frame, width = 30, textvariable = cost)
        cEntry.grid(row = 2, column = 1)
        cEntry.configure(state='disabled')

        cardLabel = Label(frame, text = "Use Card")
        cardLabel.grid(row = 3, column = 0)

        cardBox = ttk.Combobox(frame, textvariable = self.cardChosen, state = 'readonly')
        cardBox['values'] = list(self.fullCardList.keys())
        self.cardChosen.set("Select Card Number")
        cardBox.grid(row = 3, column = 1)

        addCardButton = Button(frame, text = "Add a card", command = self.addCardScreen)
        addCardButton.grid(row = 3, column = 2)

        cont = Button(frame, text = "Continue adding trains", command = self.addMore)
        cont.grid(row = 4, column = 0)

        back = Button(frame, text = "Back", command=self.back)
        back.grid(row = 5, column = 0, sticky=EW)

        next = Button(frame, text = "Submit", command = self.goToConfirmation)
        next.grid(row = 5, column = 1, sticky=EW)

        currLabel = Label(frame, text = "Currently Selected")
        currLabel.grid(row = 6, column = 0, columnspan = 2, sticky = W)

        label1 = Label(frame, text = "Train")
        label1.grid(row = 7, column = 0)

        label2 = Label(frame, text = "Time (Duration)")
        label2.grid(row = 7, column = 1)

        label3 = Label(frame, text = "Departs from")
        label3.grid(row = 7, column = 2)

        label4 = Label(frame, text = "Arrives at")
        label4.grid(row = 7, column = 3)

        label5 = Label(frame, text = "Class")
        label5.grid(row = 7, column = 4)

        label6 = Label(frame, text = "Price")
        label6.grid(row = 7, column = 5)

        label7 = Label(frame, text = "Number of baggages")
        label7.grid(row = 7, column = 6)

        label8 = Label(frame, text = "Passenger Name")
        label8.grid(row = 7, column = 7)

        label9 = Label(frame, text = "Departure Date")
        label9.grid(row = 7, column = 8)

        label10 = Label(frame, text = "Remove")
        label10.grid(row = 7, column = 9)


        rowCount = 8
        colCount = 0

        self.removeTracker = IntVar()
        removeIndex = 0

        for indi in self.fullTrainList:
            temp = Radiobutton(frame, text = indi[0], variable = self.removeTracker, value = removeIndex)
            temp.grid(row = rowCount, column = colCount)    # col 0 has the train name
            colCount = colCount + 1
            removeIndex = removeIndex + 1

            start = indi[3]
            end = indi[4]
            duration = end - start

            hours = duration.total_seconds() // 3600
            minutes = (duration.total_seconds() - (hours * 3600)) // 60
            strDuration = str(hours) + " hours " + str(minutes) + "minutes "

            temp = Label(frame, text = strDuration) # col 1 has the duration
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = indi[1]) # col 2 has the departure station
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = indi[2]) # col 3 has the arrival station
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = indi[6]) # col 4 has the class type
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = indi[5]) # col 5 has the price
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = indi[8]) # col 6 has baggage num
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Label(frame, text = indi[7]) # col 7 has the name
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            finalFormat = str(self.userDate).split("-")
            month = self.getMonthDict[finalFormat[1]]
            year = finalFormat[0]
            day = finalFormat[2]
            temp = Label(frame, text = month + " " + day + " " + year)
            temp.grid(row = rowCount, column = colCount)
            colCount = colCount + 1

            temp = Button(frame, text = "Remove", command = self.removeTrain)
            temp.grid(row = rowCount, column = colCount)

            colCount = 0
            rowCount = rowCount + 1

        frame.pack()

    def removeTrain(self):
        self.make1.withdraw()
        removeIndex = self.removeTracker.get()

        del self.fullTrainList[removeIndex]
        self.makeReservation()

    def addMore(self):
        self.make1.withdraw()
        self.makeNewReservation()

    def addCardScreen(self):
        self.make1.withdraw()
        self.addCards = Toplevel()
        frame = Frame(self.addCards)

        self.cardName = StringVar()
        self.cardNum = IntVar()
        self.cvv = IntVar()
        self.expDate = StringVar()
        self.cardChosen1 = StringVar()

        """
        data = self.Connect()
        cursor = data.cursor()
        query = "SELECT Card_Num FROM Payment_Info WHERE C_Username = '{}'".format(self.username.get())
        self.datalist1 = cursor.execute(query)
        self.datalist1 = cursor.fetchall()
        cursor.close()
        data.close()

        self.cardList=[]
        for item in self.datalist1:
            self.cardList.append(item[0])


        self.fullCardList={}
        for item in range(len(self.cardList)):
            self.fullCardList[self.cardList[item][12:]] = self.cardList[item]
        """



        title = Label(frame, text= "Payment Information", fg="Blue",font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=5)

        cardAdd = Label(frame, text = "Add Card", font= "TkDefaultFont 13")
        cardAdd.grid(row=1, column=0)

        cardName = Label(frame, text = "Name on Card")
        cardName.grid(row=2, column=0)

        cardNameEntry = Entry(frame, textvariable = self.cardName)
        cardNameEntry.grid(row=2, column=1)

        cardNum = Label(frame, text= "Card Number")
        cardNum.grid(row=3, column=0)

        cardNumEntry = Entry(frame, textvariable = self.cardNum)
        cardNumEntry.grid(row=3, column=1)

        cvv = Label(frame, text="CVV")
        cvv.grid(row=4, column=0)

        cvvEntry = Entry(frame, textvariable = self.cvv)
        cvvEntry.grid(row=4, column=1)

        expDate = Label(frame, text="Expiration Date (YYYY-MM)")
        expDate.grid(row=5, column=0)

        expDateEntry = Entry(frame, textvariable = self.expDate)
        expDateEntry.grid(row=5, column=1)

        spaceLabel = Label(frame)
        spaceLabel.grid(row=6, column=0)

        submitButton = Button(frame, text = "Submit", command = self.submitCard)
        submitButton.grid(row = 7, column = 0, columnspan=2)

        middleSpace = Label(frame)
        middleSpace.grid(row=1, column=2, rowspan=6)

        cardDelete = Label(frame, text = "Delete Card", font= "TkDefaultFont 13")
        cardDelete.grid(row=1, column=3)

        cardNum2 = Label(frame, text= "Card Number")
        cardNum2.grid(row=2, column=3)

        cardBox = ttk.Combobox(frame, textvariable = self.cardChosen1, state = 'readonly')
        cardBox['values'] = list(self.fullCardList.keys())
        cardBox.grid(row = 2, column = 4)

        spaceLabel2 = Label(frame)
        spaceLabel2.grid(row=3, column=0, columnspan=2, rowspan=4)

        submitButton2 = Button(frame, text = "Submit", command = self.removeCard)
        submitButton2.grid(row = 7, column = 3, columnspan=2)

        frame.pack()

    def submitCard(self):
        self.expireDate = self.expDate.get()
        self.expireDate = self.expireDate.split('-')
        self.expireDate = datetime.date(int(self.expireDate[0]), int(self.expireDate[1]), 1)

        self.cardInfos = [self.cardName, self.cardNum, self.cvv, self.expDate]

        for item in self.cardInfos:
            if item.get() == "":
                messagebox.showerror("Invalid Input", "All Fields Must Be Filled")
                return

        if (self.expireDate < datetime.date.today()):
            messagebox.showerror("Invalid Input", "Expiration Date Must Be Greater Than Today")
            return

        data = self.Connect()
        cursor = data.cursor()
        query ="INSERT INTO Payment_Info (Card_Num,CVV,Exp_Date,Name_on_card,C_Username) VALUES ('{}','{}','{}','{}','{}')".format(self.cardNum.get(),self.cvv.get(),self.expireDate,self.cardName.get(),self.username.get())
        cursor.execute(query)
        data.commit()
        cursor.close()
        data.close()

        messagebox.showinfo("Success!", "Your Card was Added")

        self.addCards.withdraw()
        #self.make1.deiconify()
        self.makeReservation()

    def removeCard(self):
        cardSelect = self.fullCardList[self.cardChosen1.get()]

        data = self.Connect()
        cursor = data.cursor()
        valid = True
        check = "SELECT `Departure_Date` FROM `Reserve_Train` NATURAL JOIN `Reservation` WHERE `Card_Num`='{}'".format(cardSelect)
        cursor.execute(check)
        checklist = self.nested_tuple_to_list(cursor.fetchall(), False)
        cursor.close()
        data.close()
        for result in checklist:
            date = self.parseDate(result[0])
            advance = int(str(date - datetime.date.today()).split(' ')[0])
            if advance > -1:
                valid = False
        if valid:
            data = self.Connect()
            cursor = data.cursor()
            query ="DELETE FROM Payment_Info WHERE Card_Num = '{}'".format(cardSelect)
            cursor.execute(query)
            data.commit()
            cursor.close()
            data.close()

            messagebox.showinfo("Success!", "Your Card was Removed")

            self.addCards.withdraw()
            #self.make1.deiconify()
            self.makeReservation()
        else:
            messagebox.showerror("Failed!", "This card has outstanding reservations")
    def calcCost(self, flag):
        db = self.Connect()
        cursor = db.cursor()

        sql = "SELECT Student_Discount FROM System_Info"
        r = cursor.execute(sql)
        disc = cursor.fetchone()[0]

        cursor.close()
        db.close()

        cost = 0

        for items in self.fullTrainList:
            if (items[8] > 2):
                cost = cost + (30 * (items[8] - 2))
            cost = cost + items[5]

        if (flag):
            cost = float(cost) * float(disc)

        return(cost)

    def isStudent(self):
        data = self.Connect()
        cursor = data.cursor()

        sql = "SELECT Is_Student FROM Customer WHERE Username  = '{}'".format(self.username.get())
        r = cursor.execute(sql)

        flag = cursor.fetchone()

        data.close()
        cursor.close()

        if (flag[0] == 1):
            return (True)

        return(False)

    def goToConfirmation(self):
        self.make1.withdraw()

        data = self.Connect()

        cursor = data.cursor()

        flag = self.isStudent()
        finalCost = self.calcCost(flag)

        if(len(self.fullTrainList) == 0):
            messagebox.showerror("Empty Reservation", "Cannot submit empty reservations!")
            self.funcBack()

        sql = "INSERT INTO `Reservation` (`Is_Cancelled`, `C_Username`, `Card_Num`, `Total_Cost`) VALUES ('{}', '{}', '{}', '{}')".format(0, self.username.get(), self.fullCardList[self.cardChosen.get()], finalCost)
        cursor.execute(sql)
        data.commit()

        self.travelInfo.withdraw()
        self.confirmScreen = Toplevel()
        self.winList.append(self.confirmScreen)
        frame = Frame(self.confirmScreen)

        sql = "SELECT MAX(`ReservationID`) FROM `Reservation`"
        cursor.execute(sql)
        aList = cursor.fetchall()[0][0]

        for lists in self.fullTrainList:
            fetchNumber = "SELECT `Train_Number` from `Train_Name` WHERE `Name` = '{}'".format(lists[0])
            cursor.execute(fetchNumber)
            num = cursor.fetchall()[0][0]
            insert = "INSERT INTO `Reserve_Train` (`ReservationID`, `Username`, `Passenger_Name`, `Departure_Date`, `First_Class`, `Departs_From`, `Arrives_At`, `Train_Number`, `Num_Baggage`) VALUES ('{}'," \
                     "'{}', '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(aList, self.username.get(), lists[-2], self.dateForSQL, lists[6], lists[1], lists[2], num, lists[-1])
            cursor.execute(insert)
            data.commit()

        cursor.close()
        data.close()
        num = IntVar()

        title = Label(frame, text = "Confirmation")
        title.grid(row = 0, column = 0, columnspan = 2)

        reLabel = Label(frame, text = "Reservation ID")
        reLabel.grid(row = 1, column = 0)
        reLabel.configure(state='disabled')

        entry = Entry(frame, width = 50, textvariable = num)
        entry.grid(row = 1, column = 1)
        entry.configure(state='disabled')

        backB = Button(frame, text = "Continue", command = self.funcBack)
        backB.grid(row = 1, column = 2)

        num.set(aList)
        frame.pack()

        self.fullTrainList = []


    def updateReservation(self):
        self.funcScreen.withdraw()
        self.reserveView = Toplevel()
        self.reserveView.title("Update Reservation")
        self.winList.append(self.reserveView)
        frame = Frame(self.reserveView)

        self.idNum = StringVar()

        title = Label(frame, text="Update Reservation", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=3)

        idNum = Label(frame, text="Reservation ID: ")
        idNum.grid(row=1, column=0)

        idNumEntry = Entry(frame, textvariable=self.idNum)
        idNumEntry.grid(row=1, column=1)

        searchButton = Button(frame, text="Search", command=self.setReservationUpdate)
        searchButton.grid(row=1, column=2)

        buttonBack = Button(frame, text="Back", command=self.funcBack)
        buttonBack.grid(row=2, column=1)

        frame.pack()

    def setReservationUpdate(self):
        print("Dost thou arthen an illiterate lethrblaka farmer?")

    def cancelReservation(self):
        self.cancelReservationID = StringVar()
        self.funcScreen.withdraw()
        self.cancelReservationWin = Toplevel()
        self.cancelReservationWin.title("Cancel Reservation")
        self.winList.append(self.cancelReservationWin)
        frame = Frame(self.cancelReservationWin)

        title = Label(frame, text="Cancel Reservation", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=1, columnspan=1)

        reservationLabel = Label(frame, text="Reservation ID")
        reservationLabel.grid(row=1, column=0, sticky=W)

        reservationIDEntry = Entry(frame, textvariable=self.cancelReservationID)
        reservationIDEntry.grid(row=1, column=1)

        searchButton = Button(frame, text="Search", command=self.cancelReservationSearch)
        searchButton.grid(row=1, column=2)

        buttonBack = Button(frame, text="Back", command=self.funcBack)
        buttonBack.grid(row=2, column=1)

        frame.pack()

    def cancelReservationSearch(self):
        data = self.Connect()
        cursor = data.cursor()

        sql = "SELECT ReservationID FROM Reservation WHERE Is_Cancelled='0'"
        cursor.execute(sql)

        aList = self.nested_tuple_to_list(cursor.fetchall(), True)

        if (int(self.cancelReservationID.get()) not in aList):
            messagebox.showerror("Error", "ReservationID does not exist")
            return

        if (self.cancelReservationID.get()==""):
            messagebox.showerror("Error", "Enter a valid ReservationID")
            return

        self.cancelReservationWin.withdraw()
        self.cancelReservationWin2 = Toplevel()
        self.cancelReservationWin2.title("Cancel Reservation")
        self.winList.append(self.cancelReservationWin2)

        self.cancelTotalCost = StringVar()
        self.cancelDate = StringVar()
        self.cancelRefund = StringVar()

        frame = Frame(self.cancelReservationWin2)
        # trainsDict = {
        #     "2163 Express": ["3:30 a.m.", "Boston(BBY)", "New York(Penn)", "2nd Class", "$115", "3", "Alier Hu"],
        #     "2543 Regional": ["3:30 a.m.", "Boston(BBY)", "New York(Penn)", "2nd Class", "$115", "3", "Alier Hu"]
        # }


        search_sql = """
                        SELECT `Name`, `Departure_Date`, `Departure_Time`, `Departs_From`, `Arrives_At`, `First_Class`, `Num_Baggage`, `Passenger_Name`, `Total_Cost` FROM (
                        SELECT * FROM
                            (SELECT * FROM `Reservation` NATURAL JOIN `Reserve_Train` WHERE `Reserve_Train`.`ReservationID` = {} AND `Reservation`.`Is_Cancelled` != '1')
                        AS A NATURAL JOIN `Train_Name`) AS B INNER JOIN `Train_Stop` ON `B`.`Departs_From` = `Train_Stop`.`Station_Name` WHERE `B`.`Train_Number`=`Train_Stop`.`Train_Number` AND `Username` = '{}'
                     """.format(self.cancelReservationID.get(), self.username.get())
        cursor.execute(search_sql)
        searchlist = self.nested_tuple_to_list(cursor.fetchall(), False)
        cursor.close()
        data.close()

        trainsDict = {}
        if len(searchlist) == 0:
            messagebox.showerror("Error", "Enter a valid Reservation ID")
            self.cancelReservationWin2.withdraw()
            self.cancelReservation()
        days_before = 9 ** 9
        self.refund_percentage = 0.0
        for result in searchlist:
            date = self.parseDate(result[1])
            advance = int(str(date - datetime.date.today()).split(' ')[0])
            if advance < days_before:
                days_before = advance
            trainsDict[result[0]] = result[1:8]
            self.cancelTotalCost = str(result[8])
        if days_before<= 0:
            messagebox.showerror("Error", "Too late to cancel!")
            self.cancelReservationWin2.withdraw()
            self.cancelReservation()
        elif days_before < 7 and days_before >=1:
            self.refund_percentage = .5
        else:
            self.refund_percentage = .8

        self.cancelRefund = round(self.refund_percentage * round(float(self.cancelTotalCost)) - 50, 2)
        if self.cancelRefund < 0:
            self.cancelRefund = 0
        title = Label(frame, text="Cancel Reservation", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=3, columnspan=2)

        label = Label(frame, text="Train \n (Train Number)")
        label.grid(row=1, column=0)

        label1 = Label(frame, text="Departure Date")
        label1.grid(row=1, column=1)

        label2 = Label(frame, text="Departure Time")
        label2.grid(row=1, column=2)

        label3 = Label(frame, text="Departs From")
        label3.grid(row=1, column=3)

        label4 = Label(frame, text="Arrives At")
        label4.grid(row=1, column=4)

        label5 = Label(frame, text="Class")
        label5.grid(row=1, column=5)

        label6 = Label(frame, text="# of Baggages")
        label6.grid(row=1, column=6)

        label7 = Label(frame, text="Passenger Name")
        label7.grid(row=1, column=7)

        rowCount = 2
        colCount = 0

        for key in trainsDict:
            temp = Label(frame, text=key)
            temp.grid(row=rowCount, column=colCount)
            colCount = colCount + 1
            items = trainsDict.get(key)
            for i in range(len(trainsDict.get(key))):
                temp1 = Label(frame, text=items[i])
                temp1.grid(row=rowCount, column=colCount)
                colCount = colCount + 1
            colCount = 0
            rowCount = rowCount + 1

        label8 = Label(frame, text="Total Cost of Reservation")
        label8.grid(row=rowCount + 1, column=0, sticky=W)

        entry8 = Label(frame, text=self.cancelTotalCost)
        entry8.grid(row=rowCount + 1, column=1)

        label9 = Label(frame, text="Date of Cancellation")
        label9.grid(row=rowCount + 2, column=0, sticky=W)

        entry9 = Label(frame, text=str(datetime.date.today()))
        entry9.grid(row=rowCount + 2, column=1)

        label10 = Label(frame, text="Amount to be Refunded")
        label10.grid(row=rowCount + 3, column=0, sticky=W)

        entry10 = Label(frame, text=self.cancelRefund)
        entry10.grid(row=rowCount + 3, column=1)

        label11 = Label(frame, text="Refund Percent")
        label11.grid(row=rowCount + 4, column=0, sticky=W)

        entry11 = Label(frame, text=str(self.refund_percentage))
        entry11.grid(row=rowCount + 4, column=1)

        buttonBack = Button(frame, text="Back", command=self.funcBack)
        buttonBack.grid(row=rowCount + 5, column=0, stick=EW)

        submitCancelB = Button(frame, text="Submit", command=self.setCancelled)
        submitCancelB.grid(row=rowCount + 5, column=1, sticky=EW)

        frame.pack()

    def setCancelled(self):
        # data = self.Connect()
        # cursor = data.cursor()
        # query =  "UPDATE `cs4400_Team_73`.`Reservation` SET `Is_Cancelled` = 1 WHERE `Reservation`.`ReservationID` = {}".format(self.cancelReservationID.get())
        # cursor.execute(query)
        # data.commit()
        # cursor.close()
        # data.close()
        refund_percentage = self.refund_percentage
        if round(refund_percentage * round(float(self.cancelTotalCost)) - 50, 2) < 0:
            self.cancelRefund = 0
        self.cancelRefund = round(refund_percentage * round(float(self.cancelTotalCost)) - 50, 2)
        refund_percentage *= 100
        self.cancelTotalCost = str(float(self.cancelTotalCost) - self.cancelRefund)

        data = self.Connect()
        cursor = data.cursor()
        query = "UPDATE `cs4400_Team_73`.`Reservation` SET `Is_Cancelled` = 1, `Total_Cost` = {} WHERE `ReservationID` = {} AND `C_Username`='{}'".format(float(self.cancelTotalCost), self.cancelReservationID.get(), self.username.get())
        cursor.execute(query)
        data.commit()
        cursor.close()
        data.close()
        self.cancelRefund = str(self.cancelRefund)
        messagebox.showinfo("Success", "Successfully cancelled reservation!")
        self.funcBack()

    def giveReview(self):
        self.funcScreen.withdraw()
        self.reviewWin = Toplevel()
        self.reviewWin.title("Give Review")
        self.winList.append(self.reviewWin)
        frame = Frame(self.reviewWin)

        self.trainNumber = StringVar()
        self.ratingVar = StringVar()
        self.comment = StringVar()

        self.reviewEntry = [self.trainNumber, self.ratingVar, self.comment]

        title = Label(frame, text="Give Review")
        title.grid(row=0, column=0, columnspan=2)

        trainNum = Label(frame, text="Train Number: ")
        trainNum.grid(row=1, column=0, sticky=W)

        trainNumEntry = Entry(frame, textvariable=self.trainNumber)
        trainNumEntry.grid(row=1, column=1)

        ratingLabel = Label(frame, text="Rating: ")
        ratingLabel.grid(row=2, column=0, sticky=W)

        ratingBox = ttk.Combobox(frame, textvariable=self.ratingVar)
        ratingBox['values'] = ["Very Good", "Good", "Neutral", "Bad", "Very Bad"]
        ratingBox.grid(row=2, column=1)

        commentBox = Label(frame, text="Comment: ")
        commentBox.grid(row=3, column=0, sticky=W)

        commentBoxEntry = Entry(frame, textvariable=self.comment)
        commentBoxEntry.grid(row=3, column=1)

        subReview = Button(frame, text="Submit", command=self.submitReview)
        subReview.grid(row=4, column=1, stick=EW)

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=4, column=0, sticky=EW)

        frame.pack()

    def submitReview(self):
        ratingDict = {"Very Good": "1", "Good": "2", "Neutral": "3", "Bad": "4", "Very Bad": "5"}
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
        if (trainNum != () and trainNum != None):
            query = 'INSERT INTO Review(Comment,Rating,Train_Number,C_Username)VALUES("{0}","{1}","{2}","{3}")'.format(
                self.comment.get(), ratingDict.get(self.ratingVar.get()), trainNum[0], self.username.get())
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
        self.viewReviewWin.title("View Review")
        self.winList.append(self.viewReviewWin)
        frame = Frame(self.viewReviewWin)

        title = Label(frame, text="View Review", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        reviewLabel = Label(frame, text="Train Number")
        reviewLabel.grid(row=1, column=0, sticky=W)

        reviewEntry = Entry(frame, textvariable=self.trainName)
        reviewEntry.grid(row=1, column=1)

        nextButton = Button(frame, text="Next", command=self.viewReviewNext)
        nextButton.grid(row=2, column=1, sticky=EW)

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=2, column=0, sticky=EW)

        frame.pack()

    def viewReviewNext(self):
        ratingDict = {1: "Very Good", 2: "Good", 3: "Neutral", 4: "Bad", 5: "Very Bad"}
        if (self.trainName.get() == ""):
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
        if (trainNum != () and trainNum != None):
            cursor.execute(
                'SELECT Comment,Rating FROM Review WHERE Train_Number ="{}" ORDER BY Rating ASC'.format(trainNum[0]))
            reviews = cursor.fetchall()
        else:
            messagebox.showerror("Incorrect Train Name", "Please type the correct train name.")
            return
        cursor.close()
        data.close()

        reviewDict = []
        for x in range(len(reviews)):
            reviewDict.append([ratingDict.get(reviews[x][1]), reviews[x][0]])

        self.viewReviewWin.withdraw()
        self.viewReviewWin2 = Toplevel()
        self.viewReviewWin2.title("View Review")
        self.winList.append(self.viewReviewWin2)

        frame = Frame(self.viewReviewWin2)

        title = Label(frame, text="View Review", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        label = Label(frame, text="Rating", font="TkDefaultFont 16 bold")
        label.grid(row=1, column=0, sticky=W)

        label1 = Label(frame, text="Comment", font="TkDefaultFont 16 bold")
        label1.grid(row=1, column=1, sticky=W)

        rowCount = 2
        colCount = 0

        for trainLists in reviewDict:
            temp = Label(frame, text=trainLists[0])
            temp.grid(row=rowCount, column=colCount, sticky=W)
            colCount = colCount + 1

            temp = Label(frame, text=trainLists[1])
            temp.grid(row=rowCount, column=colCount, sticky=W)
            colCount = colCount + 1

            colCount = 0
            rowCount = rowCount + 1

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=rowCount + 1, column=1, sticky=EW)

        frame.pack()

    def addInformation(self):
        self.funcScreen.withdraw()
        self.addInfo = Toplevel()
        self.winList.append(self.addInfo)
        self.addInfo.title("Get Student Discount")
        frame = Frame(self.addInfo)

        self.schoolEmail = StringVar()

        title = Label(frame, text="Add School Info", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        schoolInfoLabel = Label(frame, text="School Email Address")
        schoolInfoLabel.grid(row=1, column=0, sticky=W)

        schoolInfoText = Entry(frame, textvariable=self.schoolEmail)
        schoolInfoText.grid(row=1, column=1, columnspan=2)

        schoolReq = Label(frame, text="Your school email address ends with .edu")
        schoolReq.grid(row=2, column=0, columnspan=2)

        backEmail = Button(frame, text="Back", command=self.funcBack)
        backEmail.grid(row=3, column=0, sticky=EW)

        submitEmail = Button(frame, text="Submit", command=self.addStudentInfo)
        submitEmail.grid(row=3, column=1, sticky=EW)

        frame.pack()

    def addStudentInfo(self):
        if (findall("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.edu$)", self.schoolEmail.get()) != []):
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

    def viewRevenueReport(self):
        self.funcScreenManager.withdraw()
        self.viewRevenueWin = Toplevel()
        self.winList.append(self.viewRevenueWin)
        self.viewRevenueWin.title("Revenue Report")
        revDict = []
        data = self.Connect()
        cursor = data.cursor()
        query = "SELECT Month, SUM(Total_Cost) FROM (SELECT MIN(MONTH(`Departure_Date`)) as Month, Total_Cost FROM Reservation JOIN Reserve_Train ON Reservation.`ReservationID`=Reserve_Train.`ReservationID` WHERE `Departure_Date` BETWEEN DATE_FORMAT(NOW() - INTERVAL 3 MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59') GROUP BY Reserve_Train.`ReservationID` ORDER BY Month) AS A GROUP BY Month"
        cursor.execute(query)
        datalist = cursor.fetchall()
        cursor.close()
        data.close()
        frame = Frame(self.viewRevenueWin)

        title = Label(frame, text="View Revenue Report", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=0, columnspan=2)

        label = Label(frame, text="Month", font="TkDefaultFont 16 bold")
        label.grid(row=1, column=0, sticky=EW)

        label1 = Label(frame, text="Revenue", font="TkDefaultFont 16 bold")
        label1.grid(row=1, column=1, sticky=EW)

        rowCount = 2
        colCount = 0

        for data in datalist:
            revDict.append([datetime.date(1900, data[0], 1).strftime('%B'),"$"+str(data[1])])

        for lists in revDict:
            temp = Label(frame, text=lists[0])
            temp.grid(row=rowCount, column=colCount, sticky=EW)
            colCount = colCount + 1

            temp = Label(frame, text=lists[1])
            temp.grid(row=rowCount, column=colCount, sticky=EW)
            colCount = colCount + 1

            colCount = 0
            rowCount = rowCount + 1

        space = Label(frame)
        space.grid(row=rowCount + 1, column=0, sticky=W)

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=rowCount + 2, column=0, sticky=W)

        frame.pack()

    def viewPopularRouteReport(self):
        self.funcScreenManager.withdraw()
        self.viewPopularRouteWin = Toplevel()
        self.winList.append(self.viewPopularRouteWin)
        self.viewPopularRouteWin.title("Popular Route Report")
        revDict = []
        data = self.Connect()
        cursor = data.cursor()
        query = """
                    SELECT MONTH(Departure_Date) AS
                    MONTH , Train_Name.Name, COUNT( Reserve_Train.ReservationID ) AS Number
                    FROM Reservation
                    JOIN Reserve_Train ON Reservation.`ReservationID` = Reserve_Train.`ReservationID`
                    JOIN Train_Name ON Train_Name.Train_Number = Reserve_Train.Train_Number
                    WHERE  `Departure_Date`
                    BETWEEN DATE_FORMAT( NOW( ) - INTERVAL 3
                    MONTH ,  '%Y-%m-01 00:00:00' )
                    AND DATE_FORMAT( LAST_DAY( NOW( ) - INTERVAL 1
                    MONTH ) ,  '%Y-%m-%d 23:59:59' )
                    AND  `Is_Cancelled` =0
                    GROUP BY MONTH , Train_Name.Name
                    ORDER BY MONTH , Number DESC, Train_Name.Name"""
        cursor.execute(query)
        datalist = cursor.fetchall()
        cursor.close()
        data.close()
        frame = Frame(self.viewPopularRouteWin)

        title = Label(frame, text="View Popular Route Report", fg="Blue", font="TkDefaultFont 24 bold")
        title.grid(row=0, column=1)

        label = Label(frame, text="Month", font="TkDefaultFont 16 bold")
        label.grid(row=1, column=0, sticky=EW)

        label1 = Label(frame, text="Train Number", font="TkDefaultFont 16 bold")
        label1.grid(row=1, column=1, sticky=EW)

        label1 = Label(frame, text="# of Reservations", font="TkDefaultFont 16 bold")
        label1.grid(row=1, column=2, sticky=EW)

        for data in datalist:
            revDict.append([datetime.date(1900, data[0], 1).strftime('%B'),data[1],data[2]])

        monthcounter = 0
        month = ""
        for data in revDict:
            if month == data[0]:
                monthcounter += 1
                if monthcounter>2:
                    revDict.remove(data)
            else:
                monthcounter = 1
                month = data[0]

        for x in range(len(revDict)):
            if month == revDict[x][0]:
                revDict[x][0]=""
            else:
                month = revDict[x][0]

        rowCount = 2
        colCount = 0

        for lists in revDict:
            temp = Label(frame, text=lists[0])
            temp.grid(row=rowCount, column=colCount, sticky=EW)
            colCount = colCount + 1

            temp = Label(frame, text=lists[1])
            temp.grid(row=rowCount, column=colCount, sticky=EW)
            colCount = colCount + 1

            temp = Label(frame, text=lists[2])
            temp.grid(row=rowCount, column=colCount, sticky=EW)
            colCount = colCount + 1

            colCount = 0
            rowCount = rowCount + 1

        space = Label(frame)
        space.grid(row=rowCount + 1, column=0, sticky=W)

        backB = Button(frame, text="Back", command=self.funcBack)
        backB.grid(row=rowCount + 2, column=0, sticky=W)

        frame.pack()

    def logout(self):
        if self.userstate == 0:
            self.funcScreen.destroy()
        elif self.userstate == 1:
            self.funcScreenManager.destroy()
        self.win.deiconify()
        self.username.set("")
        self.password.set("")
        self.winList = []
        self.userstate = None

    def funcBack(self):
        for window in self.winList[1:]:
            window.destroy()
            self.winList.remove(window)
        self.winList[0].deiconify()

    def back(self):
        self.winList[-1].destroy()
        self.winList.remove(self.winList[-1])
        self.winList[-1].deiconify()

    def Connect(self):
        try:
            connection = pymysql.connect(host='academic-mysql.cc.gatech.edu', passwd="k7E1wfyD", user="cs4400_Team_73",
                                         db="cs4400_Team_73")
            cursor = connection.cursor()
            return connection
        except:
            print("Cannot connect to database")

window = Tk()
rankObj = GTTrains(window)
window.mainloop()
