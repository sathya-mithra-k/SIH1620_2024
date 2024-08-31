from flask import Flask , render_template , url_for , request , redirect


app = Flask(__name__)
app.secret_key = "vishwa"


@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/home')
# def home():
#     return render_template('home.html')



@app.route('/register', methods=['POST','GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'] 


        # Database operations here...

        return redirect (url_for('login') )

    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')    






if __name__ == '__main__':
    app.run(debug=True)

