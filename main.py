from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Uvt(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

@app.route('/filter', methods=['POST'])
def filter():
    try:
        uvt = Uvt.query.filter(date_from >= request.form['filter_date_from'])
        print(uvt)
        return render_template('create.html', uvt=uvt)
    except:
        return render_template('create.html')


@app.route('/')
def home():
    try:
        uvt = Uvt.query.all()
        return render_template('create.html', uvt=uvt)
    except:
        return render_template('create.html')

@app.route('/delete/<id>')
def delete(id):
    uvt = Uvt.query.filter_by(Id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<id>')
def update(id):
    uvt = Uvt.query.filter_by(Id=int(id)).first()
    uvt.value=uvt.value+3125
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/create', methods=['POST'])
def create():
    new_uvt = Uvt(value=request.form['value'], date_from=request.form['date_from'], date_to=request.form['date_to'])
    db.session.add(new_uvt)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=False)
