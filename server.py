from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb2')

@app.route('/', methods=['GET'])
def index():
    query = "SELECT * FROM friends"                         
    friends = mysql.query_db(query)                          
    return render_template('index.html', all_friends=friends)

#CREATE

@app.route('/friends', methods=['POST'])
def create():
    addressToVerify =request.form['email']
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    if match == None:
        print 'invalid email'
        return redirect('/')
    else:
        query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) \
            VALUES (:first_name, :last_name, :email, NOW(), NOW())"
        data = {
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'email': request.form['email']
            }
        mysql.query_db(query, data)
        return redirect('/')

#READ

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    addressToVerify = request.form['email']
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    if match == None:
        print 'invalid email'
        return redirect('/friends/' + str(id) + '/edit')
    else:
        query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
        data = {
                'id': id,
                'first_name': request.form['first_name'],
                'last_name':  request.form['last_name'],
                'email': request.form['email'],
            }
        mysql.query_db(query, data)
        return redirect('/friends/' + str(id) + '/edit')

#UPDATE

@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
    query = "SELECT * FROM friends WHERE id = {}".format(id)
    friends = mysql.query_db(query)[0]
    return render_template('show.html', friend=friends)

#DELETE

@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)