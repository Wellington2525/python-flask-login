from flask import Flask, render_template, request, redirect, url_for,session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import jsonify,json
from flask_table import Table, Col, LinkCol
import bcrypt 
import jwt
from werkzeug.security import generate_password_hash, check_password_hash 
import pyfiglet






app = Flask(__name__)
app.secret_key ='DRTIO34598'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

result = pyfiglet.figlet_format("Mired.py", font="banner3-D")
print(result)





@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #print('normal pass',password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            password_rs = account['password']
            #print('hast',password_rs) 
            
            if check_password_hash(password_rs, password):
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                
                
                print('pase')
                return redirect(url_for('home'))
                
            else:
                print('error password')
        else:
            print('error users')
        
    return render_template('index.html', msg='')


@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    id=2
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
    # account = cursor.fetchone()
        
    # if account:
    #     password_rs = account['password']
    
    #     cursor.execute('INSERT INTO logon (id_user) VALUES (%s)', (password_rs,))
    # mysql.connection.commit()
    
 
    
    return redirect(url_for('login'))


@app.route('/login/aplicativo', methods=['GET','POST'])
def aplicativo():
    
    msg=''
    if request.method == 'POST' and 'nombre' in request.form and 'descripcion' in request.form:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM aplicativo WHERE nombre =%s', (descripcion,))
        rows =cursor.fetchone()
        print('rows')
        if rows:
            msg='Este aplicativo ya esta ingresado a la BD'
        else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO aplicativo (nombre,descripcion) VALUES (%s, %s)', (nombre,descripcion))
            mysql.connection.commit()
            msg = 'Registro ingresado'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('registeraplicativo.html', msg=msg)
        
        
    

    

@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        _hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Este registro ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Por favor introducir bien el email'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username'
        elif not username or not password or not email:
            msg = 'Por favor introducir password'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)', (username, _hashed_password, email))
            mysql.connection.commit()
            msg = 'Registro ingresado'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)



@app.route('/login/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/login/profile')
def profile():
    # Check if user is loggedin
  
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/login/delete/<string:id>', methods=['GET'])
def delete(id):
    
    # We need all the account info for the user so we can display it on the profile page
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE  FROM accounts WHERE id = %s', (id,))
    mysql.connection.commit()
    print(id)
    return redirect(url_for('crud'))


# class Results(Table):
#     id = Col('id', show=False)
#     unsername = Col('username')
#     email = Col('email')
#     password = Col('password', show=False)
#     edit = LinkCol('Edit', 'edit_view', url_kwargs=dict(id='user_id'))
#     delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='user_id'))

@app.route('/login/crud')
def crud():
    #usuarios =[]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id,username, password,email,fecha  FROM accounts')
    row = cursor.fetchall()
   
    return render_template('crud.html', accounts=row)


@app.route('/login/datatable')
def datatable():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id,nombre,descripcion,fecha FROM aplicativo')
    row = cursor.fetchall()
   
    return render_template('aplicativo_data.html', aplicativo=row)
    



@app.route('/update/<id>', methods=['POST'])
def edit(id):
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    #if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
    if request.method == 'POST':    
        #id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        _hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
        cursor.execute("""UPDATE accounts SET username=%s, password=%s, email=%s WHERE id=%s""",(username, _hashed_password, email,id))
        mysql.connection.commit()
        msg = 'Registro actualizado'

    return redirect(url_for('crud'))


# @app.route('/login/select2',methods=['GET','POST'])
# def selectw():
#     cursor = mysql.connection.cursor()
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     if request.method == 'POST': 
#         user_id = request.form['user_id']
#         print(user_id)      
#         result = cur.execute("SELECT * FROM accounts WHERE id = %s", [user_id])
#         rsusers = cur.fetchall()
#         userearray = []
#         for rs in rsusers:
#             user_dict = {
#                     'Id': rs['id'],
#                     'username': rs['username'],
#                     'password': rs['password'],
#                     'email': rs['email']
#                     }
#             userearray.append(user_dict)
#         return json.dumps(userearray) 
    
@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    cur = cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print("pase la conex")
    sql ="SELECT * FROM accounts WHERE id = %s;"
    args =[id,]
    cur.execute(sql, args)
    #cur.execute("SELECT * FROM accounts WHERE id = %s", (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', usuario=data[0])
          
        
        
   
    
    

   




if __name__ == '__main__':
    app.debug = True
    app.run(host = 'localhost', port = 5000)
    





