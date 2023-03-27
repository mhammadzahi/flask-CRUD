from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database

app = Flask(__name__)
app.secret_key = "mysecretkey"
db = Database()

@app.route('/')
def index():
    data = db.read(None)

    return render_template('index.html', data = data)
#################################################################################################################

@app.route('/add/')
def add():
    return render_template('add.html')


@app.route('/addphone', methods = ['POST', 'GET'])  #not be shown
def addphone():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("A new phone number has been added")
        else:
            flash("A new phone number can not be added")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
#################################################################################################################

@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id);

    if len(data) == 0:#go to index if id not exist
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('update.html', data = data)


@app.route('/updatephone', methods = ['POST'])  #not be shown
def updatephone():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('A phone number has been updated')

        else:
            flash('A phone number can not be updated')

        session.pop('update', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
#################################################################################################################

@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id);

    if len(data) == 0:#go to index if id not exist
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('delete.html', data = data)


@app.route('/deletephone', methods = ['POST'])  #not be shown
def deletephone():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('A phone number has been deleted')

        else:
            flash('A phone number can not be deleted')

        session.pop('delete', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
#################################################################################################################

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=8181, host="0.0.0.0")


"""
Another reason to use sessions for update and delete operations is to prevent unauthorized or accidental changes to data.
By storing the item ID or other identifying information in a session, it can be confirmed that the user is only modifying
the intended item.
"""