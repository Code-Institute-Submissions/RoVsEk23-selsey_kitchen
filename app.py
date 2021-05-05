import os
import boto3
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, send_from_directory)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
if os.path.exists("env.py"):
    import env

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_LOCATION = os.environ.get("S3_LOCATION")

app = Flask(__name__)

# ---------CONFIGURATION--------  #

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

s3 = boto3.client("s3", aws_access_key_id=S3_KEY,
                  aws_secret_access_key=S3_SECRET)

mongo = PyMongo(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# ---------HOMEPAGE--------  #

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find().sort(
        "_id", -1))
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


# ---------USERS--------  #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        # sign up
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("dashboard", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "dashboard", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password!")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out!")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    # Only users can access profile
    if not session.get("user"):
        return render_template("404.html")

    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    recipes = list(mongo.db.recipes.find())
    return render_template("dashboard.html", username=username, recipes=recipes)


# ---------ADD RECIPES--------  #

@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    # Only users can add recipes
    if not session.get("user"):
        return render_template("404.html")

    if request.method == "POST":
        image_path = upload_file()
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("recipe_title"),
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_description": request.form.get("recipe_description"),
            "file": image_path,
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("dashboard", username=session['user']))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipe.html", categories=categories)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------IMAGES--------  #

def upload_file():
    path = url_for('static', filename='images/placeholder.png')
    # Placeholder used if user does not upload a file
    if 'file' not in request.files:
        return path
    file = request.files['file']
    if file.filename == '':
        return path
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        path = upload_file_to_s3(file)
    return path


def upload_file_to_s3(file):
    """
    Amazon S3 Photo Bucket Configuration:
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename, ExtraArgs={
                          "ACL": "public-read", "ContentType":
                          file.content_type})
    except Exception as e:
        print("Something Happened: ", e)
        return e

    # return "{}{}".format(S3_LOCATION, file.filename)
    return "https://{}.s3.amazonaws.com/{}".format(S3_BUCKET_NAME, file.filename)


# ---------UPDATE RECIPES--------  #

@app.route("/update_recipe/<recipe_id>", methods=["GET", "POST"])
def update_recipe(recipe_id):
    # Only users can update recipes
    if not session.get("user"):
        return render_template("404.html")

    if request.method == "POST":
        update_path = upload_file()
        submit = {
            "category_name": request.form.get("category_name"),
            "recipe_title": request.form.get("recipe_title"),
            "recipe_ingredients": request.form.get("recipe_ingredients"),
            "recipe_description": request.form.get("recipe_description"),
            "file": update_path,
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe Successfully Updated!")
        return redirect(url_for("dashboard", username=session['user']))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("update_recipe.html",
                           recipe=recipe, categories=categories)


# ---------DELETE RECIPES--------  #

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted!")
    return redirect(url_for("dashboard", username=session['user']))


# ---------CATEGORIES--------  #

@app.route("/get_categories")
def get_categories():
    # Only admin can access categories
    if not session.get("user") == "admin":
        return render_template("404.html")
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added!")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Only admin can access categories
    if not session.get("user") == "admin":
        return render_template("404.html")

    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Successfully Updated!")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted!")
    return redirect(url_for("get_categories"))


# ---------ERROR HANDLER--------  #

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# ---------RUN--------  #

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
