import mysql.connector

class MySQLClient:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(host = host,
             user = user,
             password = password,
             database = database,
             auth_plugin='mysql_native_password')

    def converByteStringToString(self,byteString):
        return byteString.decode("utf-8")

    # Queries for databases
    def showDatabases(self):
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("SHOW DATABASES")
        return cursor.fetchall()

    def useDatabase(self,dbName):
        # Enter to database
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("USE {}".format(dbName))
        print('Database entering is successful')

    def showTables(self,dbName):
        # Show tabales inside the database
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute('USE {}'.format(dbName))
        cursor.execute('SHOW TABLES')
        return cursor.fetchall()

    def readDataFromTable(self,dbName,tableName):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute('SELECT * FROM {}.{}'.format(dbName,tableName))
        return cursor.fetchall()

    # Entering data to the table
    def insert_data(self,tableName,idStudents,Password,StudentUsername,student_Index):
        cursor = self.connection.cursor()
        # Execute the query
        query = """INSERT INTO `{}` (idStudents,Password,StudentUsername,student_Index) VALUES (%s,%s,%s,%s);""".format(tableName)
        val = (idStudents,Password,StudentUsername,student_Index)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record is entered successfully")

    # Entering data to the application table
    def insert_applicationData(self,tableName,idapplications,request_status,Details,evidence,from_id,to_id,requestType):
        cursor = self.connection.cursor()
        # Execute the query
        query = """INSERT INTO `{}` (idapplications,request_status,Details,evidence,from_id,to_id,requestType) VALUES (%s,%s,%s,%s,%s,%s,%s);""".format(tableName)
        val = (idapplications,request_status,Details,evidence,from_id,to_id,requestType)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record is entered successfully")

    def update_Studentdata(self,tableName,StudentUsername,Password):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET Password=%s WHERE StudentUsername=%s;""".format(tableName)
        
        val = (Password,StudentUsername)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def update_Userdata(self,tableName,UserName,UserPassword):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET UserPassword=%s WHERE UserName=%s;""".format(tableName)
        val = (UserPassword,UserName)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def update_Staffdata(self,tableName,username,password):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET password=%s WHERE username=%s;""".format(tableName)
        
        val = (password,username)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def searchDataFromStudentTable(self,tableName,StudentUsername):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("SELECT * FROM {} WHERE StudentUsername='{}'".format(tableName,StudentUsername))
        return cursor.fetchall()

    def searchDataFromStaffTable(self,tableName,username):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("SELECT * FROM {} WHERE username='{}'".format(tableName,username))
        return cursor.fetchall()


# dbObj = MySQLClient('localhost','root','','student')
# print(dbObj.showTables('student'))
#print(dbObj.readDataFromTable('student','users'))

# dbObj.insert_data('students','23','pass23','Kamal','190045C')

# dbObj.update_data('students','DDD1', '10')

# print(dbObj.searchDataFromStudentTable('students','John'))
