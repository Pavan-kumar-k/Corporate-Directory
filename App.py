from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEsBASE_URI'] = 'mysql://root:''@localhost/emp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
emp = SQLAlchemy(app)

#Creating model table for our database
class Data(emp.Model):
    id = emp.Column(emp.Integer, primary_key = True)
    name = emp.Column(emp.String(100))
    email = emp.Column(emp.String(100))
    phone = emp.Column(emp.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        data = Data(name, email, phone)
        emp.session.add(data)
        emp.session.commit()
        flash("Employee Inserted Successfully")
        return redirect(url_for('Index'))

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = Data.query.get(request.form.get('id'))
        data.name = request.form['name']
        data.email = request.form['email']
        data.phone = request.form['phone']
        emp.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('Index'))

#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    data = Data.query.get(id)
    emp.session.delete(data)
    emp.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)