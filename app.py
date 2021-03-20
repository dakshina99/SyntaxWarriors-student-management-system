from flask import Flask, render_template, request, redirect, session, g, send_file
from flask.helpers import url_for
from flask_mysqldb import MySQL
from io import BytesIO
from datetime import datetime

from mysqlConnector import MySQLClient

app = Flask(__name__)
app.secret_key = "hello"

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
        return render_template('Index.html', InvalidPassword="*Invalid username or password")
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
    global tempComments
    global previousComments
    previousComments = []
    tempComments = []
    userId = dbObj.searchDataFromUserTable('users', username)[0][0]
    if 'user' in session:

        if request.method == "POST":
            # for new submission button
            studentId = dbObj.searchDataFromStudentTable(
                'students', username)[0][3]
            if request.form.get("New Submission"):
                return redirect(url_for('newSubmission', username=username, studentId=studentId))
            if request.form.get("discardSview"):
                return redirect(url_for('student', username=username))
            # fill read only values in student revisit form
            # changed
            for index in dbObj.searchStudentRelatedApplicationIds(
                    'applications', userId):
                if request.form.get(str(index[0])):
                    previousComments = dbObj.searchDataFromIdThreadsUsingCommentTable(
                        'comments', str(index[0]))
                    dbObj.updateApplicationStudentRead(
                        'applications', str(index[0]), '1')
                    required = dbObj.searchDataFromApplicationTable(
                        'applications', index[0])[0][11]
                    return redirect(url_for('studentRevisit', applicationId=str(index[0]), studentId=studentId, required=required, userId=userId))
        # load leaderboard applications
        studentId = dbObj.searchDataFromStudentTable(
            'students', username)[0][0]
        listOfApplications = []
        unreadCount = 0
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
            sentDate = application[8]
            studentReaded = application[9]
            if studentReaded == "0":
                unreadCount += 1
            staffName = dbObj.searchDataFromIdUsingStaffTable('administrators', to_id)[
                0][2]
            # print(dbObj.searchDataFromIdUsingStudentTable('students', from_id))
            temp.append(application[0])
            temp.append(staffName)
            temp.append(requestValue)
            temp.append(sentDate)
            temp.append(studentReaded)
            listOfApplications.append(temp)

        return render_template('SDashboard.html', username=username, errorMessage="", applications=listOfApplications[::-1], length=unreadCount)
    else:
        redirect(url_for('logout'))

# load staff leaderboad


@app.route('/staff', methods=['GET', 'POST'])
def staff():
    global tempComments
    tempComments = []
    global previousComments
    previousComments = []
    username = request.args.get('username')
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    userId = dbObj.searchDataFromUserTable('users', username)[0][0]
    if 'user' in session:
        if request.method == "POST":
            # fill read only values in student revisit form
            # changed
            for index in dbObj.searchStaffRelatedApplicationIds('applications', userId):
                if request.form.get(str(index[0])):
                    previousComments = dbObj.searchDataFromIdThreadsUsingCommentTable(
                        'comments', str(index[0]))
                    dbObj.updateApplicationStaffRead(
                        'applications', str(index[0]), '1')
                    return redirect(url_for('staffRevisit', applicationId=str(index[0])))

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
                    return render_template('LDashboard.html', username=username, errorMessage="⚠ Invalid password")

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
                if FrequestType != '0' and requestType != FrequestType:
                    continue
                from_id = application[5]
                studentDetails = dbObj.searchDataFromIdUsingStudentTable(
                    'students', from_id)
                studentName = studentDetails[0][2]
                studentIndex = studentDetails[0][3]
                if Fname != "" and str(Fname) != str(studentName):
                    continue
                if FfromIndex != "" and str(studentIndex) < str(FfromIndex):
                    continue
                if FtoIndex != "" and str(studentIndex) > str(FtoIndex):
                    continue
                if FstatusType != "0" and str(FstatusType) != str(application[1]):
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
                sentDate = application[8]
                staffReaded = application[10]
                temp.append(application[0])
                temp.append(studentName)
                temp.append(requestValue)
                temp.append(sentDate)
                temp.append(staffReaded)
                listOfApplications.append(temp)
            return render_template('LDashboard.html', username=username, applications=listOfApplications[::-1], length=len(listOfApplications))

        # load leaderboard applications
        staffId = dbObj.searchDataFromStaffTable(
            'administrators', username)[0][0]
        listOfApplications = []
        unreadCount = 0
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
            sentDate = application[8]
            staffReaded = application[10]
            if staffReaded == "0":
                unreadCount += 1
            studentName = dbObj.searchDataFromIdUsingStudentTable('students', from_id)[
                0][2]
            # print(dbObj.searchDataFromIdUsingStudentTable('students', from_id))
            temp.append(application[0])
            temp.append(studentName)
            temp.append(requestValue)
            temp.append(sentDate)
            temp.append(staffReaded)
            listOfApplications.append(temp)
        return render_template('LDashboard.html', username=username, applications=listOfApplications[::-1], length=unreadCount)
    else:
        redirect(url_for('logout'))


# student revisit view


@app.route('/studentRevisit', methods=["GET", "POST"])
def studentRevisit():
    global tempComments
    global previousComments
    global required
    global studentId
    global userId
    global studentId
    applicationId = request.args.get("applicationId")
    required = request.args.get("required")
    userId = request.args.get("userId")
    global globaCurrentlId
    globaCurrentlId = applicationId
    studentId = request.args.get("studentId")
    username = session['user']
    isnull = False
    if request.form.get("discardSview"):
        return redirect(url_for('student', username=username))
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    if request.form.get('submitSview'):
        dbObj.updateApplicationStaffRead('applications', applicationId, '0')
        if tempComments != []:
            ##########################################################
            #####################updated date in application when comment ######################
            ##################get application details and insert data with updated today#####################
            # create new application and delete previous
            today = datetime.today().strftime('%b %d')
            applicatonDetails = dbObj.searchDataFromApplicationTable(
                'applications', globaCurrentlId)[0]
            newIndex = dbObj.readDataFromTable(
                'student', 'applications')[-1][0] + 1
            dbObj.insert_applicationData('applications', newIndex, applicatonDetails[1], applicatonDetails[2], applicatonDetails[3], applicatonDetails[4], applicatonDetails[
                5], applicatonDetails[6], applicatonDetails[7], today, applicatonDetails[9], applicatonDetails[10], applicatonDetails[11])
            dbObj.updateCommentsThreadId('comments', globaCurrentlId, newIndex)
            dbObj.deleteApplication('applications', globaCurrentlId)
            globaCurrentlId = newIndex
            ##########################################################
            indexComment = len(dbObj.readDataFromTable('student', 'comments'))
            for comment in tempComments:
                indexComment += 1
                dbObj.insert_commentData(
                    'comments', indexComment, "1", comment[0], globaCurrentlId, comment[1])
        return redirect(url_for('student', username=username))

    # download icon cn
    if request.form.get("downloadFile"):
        return redirect(url_for("download_files", applicationId=applicationId))

    applicationData = dbObj.searchRelatedDataApplicationApplicationTable(
        'applications', applicationId)[0]
    to_id = applicationData[6]
    evidence = applicationData[4]
    if evidence == "":
        isnull = True
    staffName = dbObj.searchDataFromIdUsingStaffTable('administrators', to_id)[
        0][2]
    requestType = applicationData[7]
    filename = applicationData[4]
    if len(filename) > 15:
        filename = filename[:5]+"....."+filename[-5:]
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

    details = applicationData[2]
    requestStatus = applicationData[1]
    if requestStatus == 1:
        status = "Pending"
    elif requestStatus == 2:
        status = "Accepted"
    else:
        status = "Declined"
    if request.form.get('RsubmitSview'):
        dbObj.updateApplicationStaffRead('applications', applicationId, '0')
        if tempComments != []:
            ##########################################################
            #####################updated date in application when comment ######################
            ##################get application details and insert data with updated today#####################
            # create new application and delete previous
            today = datetime.today().strftime('%b %d')
            applicatonDetails = dbObj.searchDataFromApplicationTable(
                'applications', globaCurrentlId)[0]
            newIndex = dbObj.readDataFromTable(
                'student', 'applications')[-1][0] + 1
            dbObj.insert_applicationData('applications', newIndex, applicatonDetails[1], applicatonDetails[2], applicatonDetails[3], applicatonDetails[4], applicatonDetails[
                5], applicatonDetails[6], applicatonDetails[7], today, applicatonDetails[9], applicatonDetails[10], applicatonDetails[11])
            dbObj.updateCommentsThreadId('comments', globaCurrentlId, newIndex)
            dbObj.deleteApplication('applications', globaCurrentlId)
            globaCurrentlId = newIndex
            ##########################################################
            indexComment = len(dbObj.readDataFromTable('student', 'comments'))
            for comment in tempComments:
                indexComment += 1
                dbObj.insert_commentData(
                    'comments', indexComment, "1", comment[0], globaCurrentlId, comment[1])
        return render_template("SApplicationSubView.html", studentAdmissionNum=studentId, username=username, staffName=staffName, requestValue=requestValue, details=details, status=status, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)

    if request.form.get('add'):
        newComment = request.form['newComment']
        today = datetime.today().strftime('%b %d at %H:%M')
        tempComments.append([newComment, today, '1'])
        if required == '1':
            return render_template("Resubmission.html", studentAdmissionNum=studentId, username=username, staffName=staffName, requestValue=requestValue, details=details, status=status, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)
        else:
            return render_template("SApplicationSubView.html", studentAdmissionNum=studentId, username=username, staffName=staffName, requestValue=requestValue, details=details, status=status, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)
    if required == '1':
        return render_template("Resubmission.html", studentAdmissionNum=studentId, username=username, staffName=staffName, requestValue=requestValue, details=details, status=status, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)
    else:
        return render_template("SApplicationSubView.html", studentAdmissionNum=studentId, username=username, staffName=staffName, requestValue=requestValue, details=details, status=status, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)


# student revisit view


@app.route('/staffRevisit', methods=["GET", "POST"])
def staffRevisit():
    global previousComments
    global tempComments
    applicationId = request.args.get("applicationId")
    global globaCurrentlId
    globaCurrentlId = applicationId
    isnull = False
    username = session['user']
    if request.form.get("discardLview"):
        return redirect(url_for('staff', username=username))
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    if request.form.get('submitLview'):
        requestStatuss = request.form['RequestStatuss']
        dbObj.updateApplicationStatus(
            'applications', applicationId, requestStatuss)
        dbObj.updateApplicationStudentRead('applications', applicationId, '0')
        if tempComments != []:
            ##########################################################
            #####################updated date in application when comment ######################
            ##################get application details and insert data with updated today#####################
            # create new application and delete previous
            today = datetime.today().strftime('%b %d')
            applicatonDetails = dbObj.searchDataFromApplicationTable(
                'applications', globaCurrentlId)[0]
            newIndex = dbObj.readDataFromTable(
                'student', 'applications')[-1][0] + 1
            dbObj.insert_applicationData('applications', newIndex, applicatonDetails[1], applicatonDetails[2], applicatonDetails[3], applicatonDetails[4], applicatonDetails[
                5], applicatonDetails[6], applicatonDetails[7], today, applicatonDetails[9], applicatonDetails[10], applicatonDetails[11])
            dbObj.updateCommentsThreadId('comments', globaCurrentlId, newIndex)
            dbObj.deleteApplication('applications', globaCurrentlId)
            globaCurrentlId = newIndex
            ##########################################################
            indexComment = len(dbObj.readDataFromTable('student', 'comments'))
            for comment in tempComments:
                indexComment += 1
                dbObj.insert_commentData(
                    'comments', indexComment, "0", comment[0], globaCurrentlId, comment[1])
        if request.form.get("more"):
            dbObj.updateApplicationMore('applications', applicationId, '1')
            dbObj.removeEvidence('applications', applicationId)
        elif not(request.form.get("more")):
            dbObj.updateApplicationMore('applications', applicationId, '0')
        return redirect(url_for('staff', username=username))
    if request.form.get("downloadFile"):
        return redirect(url_for("download_files", applicationId=applicationId))
    applicationData = dbObj.searchRelatedDataApplicationApplicationTable(
        'applications', applicationId)[0]

    from_id = applicationData[5]
    evidence = applicationData[4]
    if evidence == "":
        isnull = True
    studentName = dbObj.searchDataFromIdUsingStudentTable('students', from_id)[
        0][2]
    studentId = dbObj.searchDataFromStudentTable(
        'students', studentName)[0][3]
    requestType = applicationData[7]
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
    requestStatus = applicationData[1]
    filename = applicationData[4]
    if len(filename) > 15:
        filename = filename[:5]+"....."+filename[-5:]
    details = applicationData[2]
    required = dbObj.searchDataFromApplicationTable(
        'applications', applicationId)[0][11]
    if request.form.get('add'):
        newComment = request.form['newComment']
        today = datetime.today().strftime('%b %d at %H:%M')
        tempComments.append([newComment, today, '0'])
        print(previousComments)
        print(tempComments)
        return render_template("LSubmissionForm.html", studentAdmissionNum=studentId, username=username, studentName=studentName, requestValue=requestValue, details=details, requestStatus=requestStatus, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)
    return render_template("LSubmissionForm.html", studentAdmissionNum=studentId, username=username, studentName=studentName, requestValue=requestValue, details=details, requestStatus=requestStatus, isnull=isnull, filename=filename, required=required, tempComments=tempComments, previousComments=previousComments)


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
            if request.form.get("close"):
                return redirect(url_for('student', username=username))
            if oldPassword == previousPassword and newPassword == confirmPassword and newPassword != "":
                dbObj.update_Studentdata('students', username, newPassword)
                dbObj.update_Userdata('users', username, newPassword)
                return redirect(url_for('student', username=username))
            else:
                return render_template('settigns.html', username=username, errorMessage="⚠ Invalid password")

        else:
            previousPassword = dbObj.searchDataFromStaffTable('administrators', username)[
                0][1]
            if request.form.get("close"):
                return redirect(url_for('staff', username=username))
            if oldPassword == previousPassword and newPassword == confirmPassword and newPassword != "":
                dbObj.update_Staffdata('administrators', username, newPassword)
                dbObj.update_Userdata('users', username, newPassword)
                return redirect(url_for('staff', username=username))
            else:
                return render_template('settigns.html', username=username, errorMessage="⚠ Invalid password")

    if request.form.get("close"):
        if studentDetails != []:
            return redirect(url_for('student', username=username))
        else:
            return redirect(url_for('staff', username=username))
    return render_template('settigns.html', username=username, errorMessage="")


# for new submissions
@ app.route('/application', methods=['GET', 'POST'])
def newSubmission():
    username = request.args.get('username')
    studentAdmissionNum = request.args.get('studentId')
    if request.form.get("discard"):
        return redirect(url_for('student', username=username))
    return render_template('NewSubmissionForm.html', studentAdmissionNum=studentAdmissionNum)


@ app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@ app.route('/download', methods=['GET', 'POST'])
def download_files():
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    global globaCurrentlId
    applicationId = globaCurrentlId
    file_data, filename = dbObj.dowloadfile('applications', applicationId)

    filecontent = BytesIO(file_data)
    return send_file(filecontent, attachment_filename=filename, as_attachment=True, cache_timeout=0)


@ app.route('/upload', methods=['POST'])
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
        today = datetime.today().strftime('%b %d')
        length = dbObj.readDataFromTable('student', 'applications')[-1][0]
        dbObj.insert_applicationData('applications', length+1, '1', details, file.read(
        ), file.filename, studentId, staffId, requestType, today, '1', '0', '0')
        return redirect(url_for('student', username=session['user']))
    except:
        return redirect(url_for('student', username=session['user']))

# reupload evidence func


@ app.route('/upload2', methods=['POST'])
def upload2():
    print("run")
    global globaCurrentlId
    global required
    global userId
    global studentId
    global globaCurrentlId
    dbObj = MySQLClient('localhost', 'root', '', 'student')
    file = request.files['filename']
    dbObj.updateEvidence('applications', globaCurrentlId,
                         file.read(), file.filename)
    if file.filename != '':
        dbObj.updateApplicationMore('applications', globaCurrentlId, '0')
    # create new application and delete previous
    today = datetime.today().strftime('%b %d')
    applicatonDetails = dbObj.searchDataFromApplicationTable(
        'applications', globaCurrentlId)[0]
    newIndex = dbObj.readDataFromTable('student', 'applications')[-1][0] + 1
    dbObj.insert_applicationData('applications', newIndex, applicatonDetails[1], applicatonDetails[2], applicatonDetails[3], applicatonDetails[4], applicatonDetails[
                                 5], applicatonDetails[6], applicatonDetails[7], today, applicatonDetails[9], applicatonDetails[10], applicatonDetails[11])
    dbObj.updateCommentsThreadId('comments', globaCurrentlId, newIndex)
    dbObj.deleteApplication('applications', globaCurrentlId)
    globaCurrentlId = newIndex

    return redirect(url_for('studentRevisit', applicationId=globaCurrentlId, required=required, userId=userId, studentId=studentId))


if __name__ == "__main__":
    app.run(debug=True)

# test
