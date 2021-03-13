from flask import Flask, render_template, request, redirect, session, g, send_file
from flask.helpers import url_for
from flask_mysqldb import MySQL
from io import BytesIO

from mysqlConnector import MySQLClient

app = Flask(__name__)
app.secret_key = "hello"
# Configure db
# db = yaml.load(open('db.yaml'))
# app.config['MYSQL_HOST'] = db['mysql_host']
# app.config['MYSQL_USER'] = db['mysql_user']
# app.config['MYSQL_PASSWORD'] = db['mysql_password']
# app.config['MYSQL_DB'] = db['mysql_db']

#app.config['MYSQL_DATABASE_USER'] = 'check'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'check'
# app.config['MYSQL_DATABASE_DB'] = 'student'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#mysqll = MySQL(app)

# @app.route('/',methods=['GET','POST'])
# def send():
#     if request.method == "POST":
#         email = request.form['staticEmail']
#         password = request.form['inputPassword']
#         return render_template('show.html',email=email,password=password)
#     return render_template('LoginPage.html')

# @app.route('/show')
# def show():
#     conn = mysql.connect()
#     cursor =conn.cursor()

#     cursor.execute("SELECT * from users")
#     data = cursor.fetchone()
#     return data

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['test']
#     processed_text = text.upper()
#     return processed_text

# Login page


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('user', None)
        if 'user' not in session:
            username = request.form['username']
            password = request.form['password']
            session['user'] = username

            dbObj = MySQLClient('localhost', 'root', '', 'student')

            for rows in dbObj.readDataFromTable('student', 'users'):
                if rows[1] == username and rows[2] == password:

                    if rows[3] == 1:
                        return redirect(url_for("student", username=username))
                    else:
                        return redirect(url_for("staff", username=username))
        else:
            return redirect(url_for('login'))
        return render_template('Index.html', InvalidPassword="Invalid username or password")
    return render_template('Index.html', InvalidPassword="")

# check user before every request


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']
    if 'user' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))


@app.route('/student', methods=['GET', 'POST'])
def student():
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    username = request.args.get('username')
    userId = dbObj.searchDataFromUserTable('users', username)[0][0]
    if 'user' in session:

        if request.method == "POST":
            # for new submission button
            studentId = dbObj.searchDataFromStudentTable(
                'students', username)[0][3]
            if request.form.get("New Submission"):
                return redirect(url_for('newSubmission', username=username, studentId=studentId))
            if request.form.get("go"):
                return render_template("SApplicationSubView.html")
        # load leaderboard applications
        studentId = dbObj.searchDataFromStudentTable(
            'students', username)[0][0]
        listOfApplications = []
        for application in dbObj.searchRelatedDataStudentApplicationTable('applications', studentId):
            temp = []
            requestType = application[7]
            if requestType == '1':
                requestValue = "Late add/drop requests"
            elif requestType == '2':
                requestValue = "Repeat exams as first attempt with the next batch"
            elif requestType == '3':
                requestValue = "Extend assignment submission deadlines"
            elif requestType == '4':
                requestValue = "Rearrange of practical"
            else:
                requestValue = "Other"
            to_id = application[6]
            staffName = dbObj.searchDataFromIdUsingStaffTable('administrators', to_id)[
                0][2]
            #print(dbObj.searchDataFromIdUsingStudentTable('students', from_id))
            temp.append(application[0])
            temp.append(staffName)
            temp.append(requestValue)
            listOfApplications.append(temp)
        return render_template('SDashboard.html', username=username, errorMessage="", applications=listOfApplications[::-1], length=len(listOfApplications))
    else:
        redirect(url_for('logout'))

# for change password in students profiles


@app.route('/change', methods=['GET', 'POST'])
def change():
    username = session['user']
    dbObj = MySQLClient('localhost', 'root', '', 'student')

    studentDetails = dbObj.searchDataFromStudentTable('students', username)
    if request.form.get("changePassword"):
        oldPassword = request.form['OldPassword']
        newPassword = request.form['NewPassword']
        confirmPassword = request.form['ConfirmPassword']

        if studentDetails != []:
            previousPassword = dbObj.searchDataFromStudentTable('students', username)[
                0][1]
            print("student")
            if request.form.get("close"):
                return redirect(url_for('student', username=username))
            if oldPassword == previousPassword and newPassword == confirmPassword and newPassword != "":
                dbObj.update_Studentdata('students', username, newPassword)
                dbObj.update_Userdata('users', username, newPassword)
                return redirect(url_for('student', username=username))
            else:
                return render_template('settigns.html', username=username, errorMessage="Invalid password")

        else:
            previousPassword = dbObj.searchDataFromStaffTable('administrators', username)[
                0][1]
            print(previousPassword)
            if request.form.get("close"):
                return redirect(url_for('staff', username=username))
            if oldPassword == previousPassword and newPassword == confirmPassword and newPassword != "":
                dbObj.update_Staffdata('administrators', username, newPassword)
                dbObj.update_Userdata('users', username, newPassword)
                return redirect(url_for('staff', username=username))
            else:
                return render_template('settigns.html', username=username, errorMessage="Invalid password")

    if request.form.get("close"):
        if studentDetails != []:
            return redirect(url_for('student', username=username))
        else:
            return redirect(url_for('staff', username=username))
    return render_template('settigns.html', username=username, errorMessage="")


@app.route('/staff', methods=['GET', 'POST'])
def staff():
    username = request.args.get('username')
    userId = request.args.get('userId')
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    if 'user' in session:
        if request.method == "POST":

            # for change password in staff profiles
            if request.form.get("changePassword"):
                oldPassword = request.form['OldPassword']
                newPassword = request.form['NewPassword']
                confirmPassword = request.form['ConfirmPassword']

                previousPassword = dbObj.searchDataFromStaffTable(
                    'administrators', username)[0][1]
                if oldPassword == previousPassword and newPassword == confirmPassword and newPassword != "":
                    dbObj.update_Staffdata(
                        'administrators', username, newPassword)
                    dbObj.update_Userdata('users', username, newPassword)
                else:
                    return render_template('LDashboard.html', username=username, errorMessage="Invalid password")

        # filtering process
            if request.form.get("filter"):

                filterDetails = request.form
                FfromIndex = filterDetails['fromId']
                FtoIndex = filterDetails['toId']
                FrequestType = filterDetails['RequestType']
                FstatusType = filterDetails['StatusType']
                Fname = filterDetails['name']
                staffId = dbObj.searchDataFromStaffTable(
                    'administrators', username)[0][0]
                listOfApplications = []
                for application in dbObj.searchRelatedDataStaffApplicationTable('applications', staffId):

                    temp = []
                    requestType = application[7]
                    if requestType != FrequestType:
                        continue
                    from_id = application[5]
                    studentDetails = dbObj.searchDataFromIdUsingStudentTable(
                        'students', from_id)
                    studentName = studentDetails[0][2]
                    studentIndex = studentDetails[0][3]
                    print(studentName,)
                    if Fname != studentName:
                        continue
                    if studentIndex < FfromIndex and studentIndex > FtoIndex:
                        continue
                    if FstatusType != application[1]:
                        continue
                    if requestType == '1':
                        requestValue = "Late add/drop requests"
                    elif requestType == '2':
                        requestValue = "Repeat exams as first attempt with the next batch"
                    elif requestType == '3':
                        requestValue = "Extend assignment submission deadlines"
                    elif requestType == '4':
                        requestValue = "Rearrange of practical"
                    else:
                        requestValue = "Other"
                    temp.append(application[0])
                    temp.append(studentName)
                    temp.append(requestValue)
                    listOfApplications.append(temp)
                    return render_template('LDashboard.html', username=username, applications=listOfApplications[::-1], length=len(listOfApplications))

        # load leaderboard applications
        staffId = dbObj.searchDataFromStaffTable(
            'administrators', username)[0][0]
        listOfApplications = []
        for application in dbObj.searchRelatedDataStaffApplicationTable('applications', staffId):
            temp = []
            requestType = application[7]
            if requestType == '1':
                requestValue = "Late add/drop requests"
            elif requestType == '2':
                requestValue = "Repeat exams as first attempt with the next batch"
            elif requestType == '3':
                requestValue = "Extend assignment submission deadlines"
            elif requestType == '4':
                requestValue = "Rearrange of practical"
            else:
                requestValue = "Other"
            from_id = application[5]
            studentName = dbObj.searchDataFromIdUsingStudentTable('students', from_id)[
                0][2]
            #print(dbObj.searchDataFromIdUsingStudentTable('students', from_id))
            temp.append(application[0])
            temp.append(studentName)
            temp.append(requestValue)
            listOfApplications.append(temp)
        return render_template('LDashboard.html', username=username, applications=listOfApplications[::-1], length=len(listOfApplications))
    else:
        redirect(url_for('logout'))


# for new submissions
@app.route('/application', methods=['GET', 'POST'])
def newSubmission():
    username = request.args.get('username')
    studentAdmissionNum = request.args.get('studentId')
    if request.form.get("discard"):
        return redirect(url_for('student', username=username))
    return render_template('NewSubmissionForm.html', studentAdmissionNum=studentAdmissionNum)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/download')
def download_files():
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    filename, file_data = dbObj.dowloadfile('applications', '')
    print(filename)
    print(file_data)
    filecontent = BytesIO(file_data)
    return send_file(filecontent, attachment_filename=filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload():
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    # try except is added to control discard button function and othrer errors(i.e: Invalid administrater name)
    try:
        username = session['user']
        userDetails = request.form
        name = userDetails['studentName']
        lecturer = userDetails['staffName']
        requestType = userDetails['RequestType']
        details = userDetails['subject']
        staffId = dbObj.searchDataFromStaffTable(
            'administrators', lecturer)[0][0]
        studentId = dbObj.searchDataFromStudentTable(
            'students', username)[0][0]
        file = request.files['filename']

        length = dbObj.readDataFromTable('student', 'applications')[-1][0]

        dbObj.insert_applicationData('applications', str(
            length+1), '1', details, file.read(), file.filename, studentId, staffId, requestType)
        return redirect(url_for('student', username=session['user']))
    except:
        return redirect(url_for('student', username=session['user']))


if __name__ == "__main__":
    app.run(debug=True)


# LDashboard.html jinja for loop is moved error occured fix the loop
