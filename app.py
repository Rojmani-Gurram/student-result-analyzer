from flask import Flask, render_template, request, redirect
from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    avg = db.session.query(db.func.avg(Student.marks)).scalar()
    return render_template('index.html', students=students, average=round(avg, 2))

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    subject = request.form['subject']
    marks = int(request.form['marks'])
    student = Student(name=name, subject=subject, marks=marks)
    db.session.add(student)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
