# Importing flask and the required modules
from flask import Flask , render_template , url_for , request , redirect , flash 
# Importing flask bcrypt to hashes the password 
from flask_bcrypt import Bcrypt
# Importing flask_mysql to connect to MySQL server 
from flask_mysqldb import MySQL
# Importing MySQLdb.cursor to execute SQL queries through python
import MySQLdb.cursors
from MySQLdb import IntegrityError

# Importing  the queue python file 
from queue_module_ import *


app = Flask(__name__)
app.secret_key = 'vishwa'



# connecting to database
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sih_db'


# initialize the database & password_hash function
mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST','GET'])
def register():


    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'] 

        # hash the password
        password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            # Database operations here...

            # create cursor object 
            cursor= mysql.connection.cursor()

            # insert data to database
            cursor.execute("INSERT INTO users (username, email, password_hashed) VALUES (%s, %s, %s)", (username, email, password_hashed))

            # commit the transaction
            mysql.connection.commit()

            

            # close the connection
            cursor.close()


            return redirect (url_for('login') )
        

        except IntegrityError as e:
            if e.args[0] == 1062:  # Error code for duplicate entry
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect('/register')  # Redirect back to signup page
            else:
                flash('An error occurred. Please try again.', 'error')
                return redirect('/register')

        except Exception as e:
            flash(f'An unexpected error occurred: {str(e)}', 'error')
            return redirect('/register')

    return render_template('register.html')


@app.route('/login' , methods=['POST','GET'])
def login():
    if request.method == 'POST':
        # collect the info from the login form 
        username = request.form['username']
        password = request.form['password']

        # Create cursor object to retrieve the hashed_password in the database
        cursor= mysql.connection.cursor()

        # fetch the hashed password from the database
        cursor.execute("SELECT password_hashed FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

            # check if the query returned a password
        if result:
            password_hashed = result[0]

            # check if the provided password matches the hashed password
            if bcrypt.check_password_hash(password_hashed , password):
                return redirect(url_for('dashboard'))  # Redirect to a different page on successful login
            
            else:
                # Handle incorrect password
                return 'Invalid username or password'
        else:
            # Handle user not found
            return 'Invalid username or password'

    
    return render_template('login.html')    



@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/out_patient")
def out_patient():
    return render_template('out_patient.html')

# @app.route("/init", methods=["POST"])
# def init():
#     tot_doctors = request.form['tot_doctors']
#     patient_queuing_.num_doc(int(tot_doctors))
#     return ({"message": f"Initialized Doctors: {docs} " })




if __name__ == '__main__':
    app.run(debug=True)

