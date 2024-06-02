from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#My app

app= Flask(__name__)
Scss(app)

# /Users/saurabhverma/Data-Engineering-Course/my_crud_app

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users/saurabhverma/Data-Engineering-Course/my_crud_app.database.db"
# Construct the path for the database file relative to the my_crud_app directory
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(basedir, 'database.db')

# Set the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db= SQLAlchemy(app)
app.app_context().push()

class MyTask(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    content= db.Column(db.String(100), nullable= False)
    complete= db.Column(db.Integer, default=0)
    created= db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

#routes to homepage
@app.route('/', methods= ["POST", "GET"])
def index():
    #Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task= MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR {e}")
            return(f"ERROR {e}")
    
    else:
        tasks= MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks= tasks)



#delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task= MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return  f"ERROR: {e}"
    
#edit an item

# @app.route("/edit/<int:id>", methods= ["GET", "POST"] )
# def edit(id:int):
#     edit_item= MyTask.query.get_or_404(id)
#     if request.method == "POST":
#         edit_item.content = request.form['content']
#     try:
#         db.session.commit()
#         return redirect("/")
#     except Exception as e:
#         return f"Error:{e}"
    
#     else:
#         return "HOME"
    

@app.route("/edit/<int:id>", methods= ["GET", "POST"] )
def edit(id:int):
    edit_item= MyTask.query.get_or_404(id)
    if request.method == "POST":
        edit_item.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
     
    else:
        return "HOME"


if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

