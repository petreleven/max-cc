from flask import Flask,redirect,url_for
from database import db
from flask  import render_template
from flask import request
from database import user
from database import initaitive
from database import Photo
from werkzeug.utils import secure_filename
import os


app = Flask('MAX ECO SYSTEM STEAM PROJECT')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db.init_app(app)

with app.app_context():#trying to create the tabels
    db.create_all()

@app.route("/")
def home():
    all_initaitive = db.session.execute(db.select(initaitive)).scalars()
    return render_template("home.html" , all_initaitive = all_initaitive)

@app.route("/detail/<int:id>")
def detail(id):
    # Retrieve only the one initiative that matches the ID
    single_initiative = db.session.get(initaitive, id)
    if single_initiative is None:
        return "Initiative not found", 404
        
    return render_template("detail.html", initiative=single_initiative)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # 1. Get Text Data
        title = request.form.get("Title")
        tag = request.form.get("Tag")
        overview = request.form.get("Overview")
        notes = request.form.get("additional_notes")

        # 2. Create Initiative Object
        new_initaitive = initaitive(
            Title=title, Tag=tag, Latitude=0, Logitude=0, 
            Date="8/3/2026", OverView=overview, 
            additional_notes=notes, owner_ID=1
        )
        db.session.add(new_initaitive)
        db.session.flush() # This gets us the ID before committing

        # 3. Handle Multiple File Uploads
        files = request.files.getlist("photos")
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Ensure directory exists
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                
                new_photo = Photo(image_filename=filename, initiative_id=new_initaitive.id)
                db.session.add(new_photo)

        db.session.commit()
        return redirect(url_for('home')) 

    return render_template("initaitive.html")


@app.route("/signup" , methods=["Get" , "POST"])
def signup():
    if request.method =="POST":
        print("someone has pressed the button")
       
        username = request.form.get("username")
        print(username)
        FirstName = request.form.get("FirstName")
        print(FirstName)
        LastName = request.form.get("LastName")
        print(LastName)

        new_user = user(username = username , FirstName = FirstName , LastName = LastName) 
        db.session.add(new_user)
        db.session.commit()

    return render_template("signup.html")



app.run()



