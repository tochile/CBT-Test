

from __future__ import division, print_function

from flask import Flask,render_template,url_for,request

from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
import os
import random
import string
import time
import pyttsx3
import speech_recognition as sr



app = Flask(__name__)

Bootstrap(app)
with open('db.yaml') as f:
    
    db = yaml.load(f, Loader=yaml.FullLoader)
   
    app.config['MYSQL_HOST'] = db['mysql_host']
    app.config['MYSQL_USER'] = db['mysql_user']
    app.config['MYSQL_PASSWORD'] = db['mysql_password']
    app.config['MYSQL_DB'] = db['mysql_db']
    mysql = MySQL(app)

@app.route('/', methods=['GET'])

def index():
    return render_template('index.html')




# define route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    engine = pyttsx3.init()
    if request.method == 'POST':
        # get user's voice command for username
        engine.say('Please say your username.')
        engine.runAndWait()
        username = request.form['username']

        # get user's voice command for password
        engine.say('Please say your password.')
        engine.runAndWait()
        password = request.form['password']
        
        c = mysql.connection.cursor()

        # check if username and password are valid
        result = c.execute("SELECT * FROM users WHERE username=%s AND password=%s", [username, password])

        if result:
            # if username and password are valid, show success message
            engine.say('Login successful.')
            engine.runAndWait()
            
            
                
            result1 = c.execute("SELECT questions, A, B, C, answer FROM questions")
            if(result1>0):
                questions = c.fetchall()
            return render_template('questions.html', questions=questions)
        else:
            # if username and password are invalid, show error message
            engine.say('Invalid username or password.')
            engine.runAndWait()
            return 'Invalid username or password.'
    else:
        # if request method is GET, show login form
        return '''
            <form method="post">
                <p>Username: <input type="text" name="username"></p>
                <p>Password: <input type="password" name="password"></p>
                <p><input type="submit" value="Login"></p>
            </form>
        '''

@app.route('/question', methods=['POST','GET'])

def question():
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        answer = request.form['answer']

        cur = mysql.connection.cursor()
        query = "INSERT INTO questions (questions,A,B,C,D, answer) VALUES (%s,%s,%s,%s,%s,%s)"
        cur.execute(query, (question,option1,option2,option3,option4,answer))
        mysql.connection.commit()
        cur.close()
        marked = 'sucessful'
        
        
        
        return render_template('dashboard.html', marked=marked)
    
    
@app.route('/teacher_login')

def teacher_login():
    
    return render_template('teacher_login.html')

@app.route('/ad_login', methods=['POST'])

def ad_login():
    
    if request.method=='POST':
    
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * from teachers where binary username=%s and binary password=%s",[username,password])
        if(result>0):
            return render_template("dashboard2.html", username=username)
        else:
            
            error = 'failed'
            return render_template("teacher_login.html", error=error)
        

@app.route('/admin_login')

def admin_login():
    
    return render_template('admin_login.html')

@app.route('/add_questions')

def add_questions():
    
    return render_template('dashboard.html')

@app.route('/adm_login', methods=['POST'])

def adm_login():
    
    if request.method=='POST':
    
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * from admin where binary username=%s and binary password=%s",[username,password])
        if(result>0):
            return render_template("dashboard1.html", username=username)
        else:
            
            error = 'failed'
            return render_template("admin_login.html", error=error)
        
        
@app.route('/register_teachers')

def register_teachers():
    
    return render_template("register_teachers.html")

@app.route('/Register_t', methods=['POST','GET'])

def Register_t():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        
        cur = mysql.connection.cursor()
        query = "INSERT INTO teachers (username,password,email,gender) VALUES (%s,%s,%s,%s)"
        cur.execute(query, (username,password,email,gender))
        mysql.connection.commit()
        cur.close()
        marked = 'Registration sucessful'
        
        
        
        return render_template('register_teachers.html', marked=marked)
    
    
@app.route('/view_teachers')

def view_teachers():
    
    c = mysql.connection.cursor()
    result1 = c.execute("SELECT * FROM teachers")
    if(result1>0):
        view = c.fetchall()
   
        return render_template("view_teachers.html", view=view)


@app.route('/delete_t', methods=['POST'])

def delete_t():
    if request.method == 'POST':
        username = request.form['name']
        c = mysql.connection.cursor()
        c.execute("DELETE FROM teachers WHERE username=%s",[username])
        mysql.connection.commit()
        c.close()
           
        marked= "Profile deleted Sucessfully"
        return render_template("view_teachers.html", marked=marked)
        
        
 
        
@app.route('/register_students')

def register_students():


    return render_template("register_students.html")

@app.route('/Register_s', methods=['POST','GET'])

def Register_s():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        
        cur = mysql.connection.cursor()
        query = "INSERT INTO users (username,password,email,gender) VALUES (%s,%s,%s,%s)"
        cur.execute(query, (username,password,email,gender))
        mysql.connection.commit()
        cur.close()
        marked = 'Registration sucessful'
        
        
        
        return render_template('register_students.html', marked=marked)
    
@app.route('/view_students2')

def view_students2():
    c = mysql.connection.cursor()
    result1 = c.execute("SELECT * FROM users")
    if(result1>0):
        view = c.fetchall()
   
        return render_template("view_students2.html", view=view)


@app.route('/delete_s', methods=['POST','GET'])

def delete_s():
    if request.method == 'POST':
        username = request.form['name']
        print(username)
        c = mysql.connection.cursor()
        result7 = "DELETE FROM users WHERE username=%s"
        c.execute(result7, [username])
        mysql.connection.commit()
        c.close()
        msg = 'deleted successfully'
        
       
        return render_template("view_students2.html", msg=msg)
        
@app.route('/view_students')

def view_students():
    c = mysql.connection.cursor()
    result1 = c.execute("SELECT * FROM users")
    if(result1>0):
        view = c.fetchall()
   
        return render_template("view_students.html", view=view)
     
        
@app.route('/fetch_questions')

def fetch_questions():
    cur1 = mysql.connection.cursor()
        
    result1 = cur1.execute("SELECT questions, A, B, C, D, answer FROM questions")
    if(result1>0):
        questions = cur1.fetchall()
        # Create a cursor object to execute SQL queries
        
        
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        
        # Initialize the speech recognition engine
        r = sr.Recognizer()
        
        # Set the voice rate (higher value means faster speaking)
        
        print(questions)
        engine.setProperty('rate', 150)


        engine.setProperty('volume', 1)
        
        # Set the voice (change to a voice installed on your system)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        
        # Define a function to speak out the text
        def speak(text):
            engine.say(text)
            engine.runAndWait()
        
        # Define a function to recognize speech
        def recognize_speech():
            with sr.Microphone(device_index=1) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Speak now...")
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio)
                    print("You said:", text)
                    return text
                except:
                    print("Sorry, I didn't catch that.")
                    return ""
        
        # Loop through the questions and ask them
        score = 0
        for q in questions:
            # Speak the question
            speak(q[0])
            print(q[0])
        
            # Speak the options
            speak("A")
            speak(q[1])
            print("A:", q[1])
            speak("B")
            speak(q[2])
            print("B:", q[2])
            speak("C")
            speak(q[3])
            print("C:", q[3])
            speak(q[4])
            print("C:", q[4])
           
        
            # Recognize the answer
            answer = recognize_speech()
        
            # Check if the answer is correct and speak the result
            if answer.lower() == q[5].lower():
                speak("Correct!")
                print("Correct!")
                score += 1
            else:
                speak("Wrong!")
                print("Wrong!")
            
            # Speak the current score
            speak("Your score is " + str(score))
            print("Your score is", score)


    return render_template('questions.html')
  
@app.route('/view_questions')

def view_questions():
    cur1 = mysql.connection.cursor()
        
    result1 = cur1.execute("SELECT questions, A, B, C, D, answer FROM questions")
    if(result1>0):
        questions = cur1.fetchall()
       

    return render_template('view_questions.html', questions=questions)

if __name__=='__main__':



	app.run(debug=True)

