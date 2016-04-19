def Connect():
    try:
        connection = pymysql.connect(host = 'academic-mysql.cc.gatech.edu', passwd = "k7E1wfyD", user = "cs4400_Team_73", db = "cs4400_Team_73")
        cursor = connection.cursor()
        return connection
    except:
        print("Cannot connect to database")

data = self.Connect()
cursor = data.cursor()
#add for loops and what not here to iteratively add data
query = 'INSERT INTO Travelers(Username,Password,LastName)VALUES("{0}","{1}","{2}")'.format(self.user.get(),self.pass1.get(),self.name.get())
cursor.execute(query)
#easy
data.commit()
cursor.close()
data.close()
