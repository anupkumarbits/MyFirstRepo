
from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'it_helpdesk'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, password, 'user'))
        mysql.connection.commit()
        flash('Registered successfully!')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        if user:
            session['id'] = user[0]
            session['role'] = user[4]
            return redirect('/dashboard')
        flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/login')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tickets")
    tickets = cur.fetchall()
    return render_template('dashboard.html', tickets=tickets)

@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    user_id = session['id']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tickets (title, description, priority, status, user_id) VALUES (%s, %s, %s, %s, %s)",
                (title, description, priority, 'open', user_id))
    mysql.connection.commit()
    flash('Ticket created!')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
