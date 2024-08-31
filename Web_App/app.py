# Importing flask and the required modules
from flask import Flask , render_template , url_for , request , redirect
# Importing flask bcrypt to hashes the password 
from flask_bcrypt import Bcrypt
# Importing flask_mysql to connect to MySQL server 
from flask_mysqldb import MySQL
# Importing MySQLdb.cursor to execute SQL queries through python
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = "vishwa"



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


if __name__ == '__main__':
    app.run(debug=True)

