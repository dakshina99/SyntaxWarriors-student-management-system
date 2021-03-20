import mysql.connector


class MySQLClient:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = mysql.connector.connect(host=host,
                                                  user=user,
                                                  password=password,
                                                  database=database,
                                                  auth_plugin='mysql_native_password')

    def converByteStringToString(self, byteString):
        return byteString.decode("utf-8")

    # Queries for databases
    def showDatabases(self):
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("SHOW DATABASES")
        return cursor.fetchall()

    def useDatabase(self, dbName):
        # Enter to database
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute("USE {}".format(dbName))
        print('Database entering is successful')

    def showTables(self, dbName):
        # Show tabales inside the database
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute('USE {}'.format(dbName))
        cursor.execute('SHOW TABLES')
        return cursor.fetchall()

    def readDataFromTable(self, dbName, tableName):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute('SELECT * FROM {}.{}'.format(dbName, tableName))
        return cursor.fetchall()

    # Entering data to the table
    def insert_data(self, tableName, idStudents, Password, StudentUsername, student_Index):
        cursor = self.connection.cursor()
        # Execute the query
        query = """INSERT INTO `{}` (idStudents,Password,StudentUsername,student_Index) VALUES (%s,%s,%s,%s);""".format(
            tableName)
        val = (idStudents, Password, StudentUsername, student_Index)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record is entered successfully")

    # Entering data to the application table
    def insert_applicationData(self, tableName, idapplications, request_status, Details, evidence, filename, from_id, to_id, requestType, today, studentReaded, staffReaded, required):
        cursor = self.connection.cursor()
        # Execute the query
        query = """INSERT INTO `{}` (idapplications,request_status,Details,evidence,filename,from_id,to_id,requestType,date,studentReaded, staffReaded,required) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""".format(
            tableName)
        val = (idapplications, request_status, Details,
               evidence, filename, from_id, to_id, requestType, today, studentReaded, staffReaded, required)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record is entered successfully")

    # Entering data to the comments table
    def insert_commentData(self, tableName, idComments, commentUserType, content, idThreads, dateTime):
        cursor = self.connection.cursor()
        # Execute the query
        query = """INSERT INTO `{}` (idComments, commentUserType, content, idThreads, dateTime) VALUES (%s,%s,%s,%s,%s);""".format(
            tableName)
        val = (idComments, commentUserType, content, idThreads, dateTime)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record is entered successfully")

    def update_Studentdata(self, tableName, StudentUsername, Password):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET Password=%s WHERE StudentUsername=%s;""".format(
            tableName)

        val = (Password, StudentUsername)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def removeEvidence(self, tableName, idapplications):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET evidence = '', filename = '' WHERE idapplications=%s;""".format(
            tableName)
        val = (idapplications,)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateEvidence(self, tableName, idapplications, evidence, filename):
        cursor = self.connection.cursor()
        # Execute the query
        #strId = str(idapplications)
        query = """UPDATE `{}` SET evidence = %s, filename = %s WHERE idapplications=%s;""".format(
            tableName)
        val = (evidence, filename, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def update_Userdata(self, tableName, UserName, UserPassword):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET UserPassword=%s WHERE UserName=%s;""".format(
            tableName)
        val = (UserPassword, UserName)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateApplicationStatus(self, tableName, idapplications, request_status):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET request_status=%s WHERE idapplications=%s;""".format(
            tableName)
        val = (request_status, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateApplicationStudentRead(self, tableName, idapplications, studentReaded):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET studentReaded=%s WHERE idapplications=%s;""".format(
            tableName)
        val = (studentReaded, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateApplicationStaffRead(self, tableName, idapplications, staffReaded):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET staffReaded=%s WHERE idapplications=%s;""".format(
            tableName)
        val = (staffReaded, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateCommentsThreadId(self, tableName, previousId, newId):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET idThreads=%s WHERE idThreads=%s;""".format(
            tableName)
        val = (newId, previousId)
        cursor.execute(query, val)
        self.connection.commit()

    def updateApplicationMore(self, tableName, idapplications, required):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET required=%s WHERE idapplications=%s;""".format(
            tableName)
        val = (required, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateApplicationDetails(self, tableName, idapplications, Details):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET Details=%s WHERE idapplications=%s;""".format(
            tableName)
        val = (Details, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def updateApplicationRead(self, tableName, idapplications, readed):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET readed=%s WHERE idapplications=%s;""".format(
            tableName)
        val = (readed, idapplications)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def update_Staffdata(self, tableName, username, password):
        cursor = self.connection.cursor()
        # Execute the query
        query = """UPDATE `{}` SET password=%s WHERE username=%s;""".format(
            tableName)

        val = (password, username)
        cursor.execute(query, val)
        self.connection.commit()

        print("Record updated successfully")

    def deleteApplication(self, tableName, idapplications):
        cursor = self.connection.cursor()
        query = """DELETE FROM `{}` WHERE idapplications=%s;""".format(
            tableName)
        val = (idapplications,)
        cursor.execute(query, val)
        self.connection.commit()

    def searchDataFromStudentTable(self, tableName, StudentUsername):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE StudentUsername='{}'".format(tableName, StudentUsername))
        return cursor.fetchall()

    def searchDataFromIdUsingStudentTable(self, tableName, idStudents):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE idStudents='{}'".format(tableName, idStudents))
        return cursor.fetchall()

    def searchDataFromIdUsingStaffTable(self, tableName, idadministrators):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE idadministrators='{}'".format(tableName, idadministrators))
        return cursor.fetchall()

    def searchDataFromIdThreadsUsingCommentTable(self, tableName, idThreads):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE idThreads='{}'".format(tableName, idThreads))
        return cursor.fetchall()

    def searchDataFromStaffTable(self, tableName, username):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE username='{}'".format(tableName, username))
        return cursor.fetchall()

    def searchDataFromUserTable(self, tableName, UserName):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE UserName='{}'".format(tableName, UserName))
        return cursor.fetchall()

    def searchDataFromApplicationTable(self, tableName, idapplications):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE idapplications='{}'".format(tableName, idapplications))
        return cursor.fetchall()

    def searchRelatedDataStaffApplicationTable(self, tableName, to_id):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE to_id='{}'".format(tableName, to_id))
        return cursor.fetchall()

    def searchRelatedDataStudentApplicationTable(self, tableName, from_id):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE from_id='{}'".format(tableName, from_id))
        return cursor.fetchall()

    def searchStudentRelatedApplicationIds(self, tableName, from_id):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT idapplications FROM {} WHERE from_id='{}'".format(tableName, from_id))
        return cursor.fetchall()

    def searchStaffRelatedApplicationIds(self, tableName, to_id):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT idapplications FROM {} WHERE to_id='{}'".format(tableName, to_id))
        return cursor.fetchall()

    def searchRelatedDataApplicationApplicationTable(self, tableName, idapplications):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            "SELECT * FROM {} WHERE idapplications='{}'".format(tableName, idapplications))
        return cursor.fetchall()

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        print(filename)
        return (binaryData, filename)

    def insert_filetest(self, tableName, id, name, filecontent, filename):
        cursor = self.connection.cursor()
        # Execute the query
        query = """INSERT INTO `{}` (`idapplications`, `name`, `filetab`,`filename`) VALUES (%s,%s,%s,%s);""".format(
            tableName)
        val = (id, name, filecontent, filename)
        cursor.execute(query, val)
        self.connection.commit()

    def dowloadfile(self, tableName, idapplications):
        # Read data from a table
        cursor = self.connection.cursor()
        # Execute the query
        cursor.execute(
            'SELECT * FROM {} WHERE idapplications = {}'.format(tableName, idapplications))
        current_row = cursor.fetchall()[0]
        return current_row[3], current_row[4]


# dbObj = MySQLClient('localhost','root','','student')
# print(dbObj.showTables('student'))
# print(dbObj.readDataFromTable('student','users'))

# dbObj.insert_data('students','23','pass23','Kamal','190045C')

# dbObj.update_data('students','DDD1', '10')

# print(dbObj.searchDataFromStudentTable('students','John'))
