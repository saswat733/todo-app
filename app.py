from flask import Flask, render_template , request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db=SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = User(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = User.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)



@app.route('/update/<int:sno>')
def update(sno):
    todo=User.query.filter_by(sno=sno).first()
    
    db.session.commit()
    return redirect('/')
    
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=User.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True)
