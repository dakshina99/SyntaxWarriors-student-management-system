from flask import Flask,render_template,request,redirect,session,g
from flask.helpers import url_for
from flask_mysqldb import MySQL

from mysqlConnector import MySQLClient

app = Flask(__name__)
app.secret_key="hello"
#Configure db
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

#Login page
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        session.pop('user',None)
        if 'user' not in session:
            username = request.form['username']
            password = request.form['password']
            session['user']=username

            dbObj = MySQLClient('localhost','root','','student')

            for rows in dbObj.readDataFromTable('student','users'):
                if rows[1]==username and rows[2]==password:
                    if rows[3]==1:
                        return redirect(url_for("student",username=username))
                    else:
                        return redirect(url_for("staff",username=username))
        else:
            return redirect(url_for('login'))
        return render_template('Index.html',InvalidPassword="Invalid username or password")
    return render_template('Index.html',InvalidPassword="")

#check user before every request
@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']
    if 'user' not in session and request.endpoint != 'login':
        return redirect(url_for('login'))
    
    


@app.route('/student',methods=['GET','POST'])
def student():
    username=request.args.get('username')

    if 'user' in session:
        if request.method == "POST":
            dbObj = MySQLClient('localhost','root','','student')
            #for new submission button
            studentId=dbObj.searchDataFromStudentTable('students',username)[0][3]
            if request.form.get("New Submission"):
                return redirect(url_for('newSubmission',username=username,studentId=studentId))
            #for change password in students profiles
            if request.form.get("changePassword"):
                oldPassword = request.form['OldPassword']
                newPassword = request.form['NewPassword']
                confirmPassword = request.form['ConfirmPassword']
                
                previousPassword=dbObj.searchDataFromStudentTable('students',username)[0][1]
                if oldPassword==previousPassword and newPassword==confirmPassword and newPassword!="":
                    dbObj.update_Studentdata('students',username,newPassword)
                    dbObj.update_Userdata('users',username,newPassword)
                else:
                    return render_template('SDashboard.html',username=username,errorMessage="Invalid password")
                
        return render_template('SDashboard.html',username=username,errorMessage="")
    else:
        redirect(url_for('logout'))

@app.route('/staff',methods=['GET','POST'])
def staff():
    # global loggedIn
    username=request.args.get('username')
    if 'user' in session:
        if request.method == "POST":
            dbObj = MySQLClient('localhost','root','','student')

             #for change password in staff profiles
            if request.form.get("changePassword"):
                oldPassword = request.form['OldPassword']
                newPassword = request.form['NewPassword']
                confirmPassword = request.form['ConfirmPassword']
                
                previousPassword=dbObj.searchDataFromStaffTable('administrators',username)[0][1]
                if oldPassword==previousPassword and newPassword==confirmPassword and newPassword!="":
                    dbObj.update_Staffdata('administrators',username,newPassword)
                    dbObj.update_Userdata('users',username,newPassword)
                else:
                    return render_template('LDashboard.html',username=username,errorMessage="Invalid password")


        return render_template('LDashboard.html',username=request.args.get('username'))
    else:
        redirect(url_for('logout'))


#for new submissions 
@app.route('/application',methods = ['GET','POST'])
def newSubmission():
    username=request.args.get('username')
    studentAdmissionNum=request.args.get('studentId')
    if request.method == 'POST':        
        userDetails = request.form
        name =userDetails['studentName']
        lecturer = userDetails['staffName']
        requestType = userDetails['RequestType']
        details = userDetails['subject']
        #evidence = file

        if userDetails.get('apply'):
            dbObj = MySQLClient('localhost','root','','moodle')
            staffId=dbObj.searchDataFromStaffTable('administrators',username)[0][0]
            studentId=dbObj.searchDataFromStaffTable('administrators',username)[0][0]
            #dbObj.insert_applicationData('applications','1','1',details,'evidence',studentId,staffId,requestType)
            return redirect(url_for('student',username=username))
        elif userDetails.get('discard'):
            return redirect(url_for('student',username=username))
    return render_template('NewSubmissionForm.html',studentAdmissionNum=studentAdmissionNum)


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)