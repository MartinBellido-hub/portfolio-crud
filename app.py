from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# The Model: one class = one table
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200))


# Create the database and table if they don't exist yet
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# READ
@app.route("/projects")
def projects():
    all_projects = db.session.execute(db.select(Project)).scalars().all()
    return render_template("projects.html", projects=all_projects)


# CREATE
@app.route("/projects/add", methods=["POST"])
def add_project():
    new_project = Project(
        title=request.form["title"],
        description=request.form["description"],
        link=request.form["link"],
    )
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for("projects"))


# UPDATE
@app.route("/projects/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):
    project = db.get_or_404(Project, id)
    if request.method == "POST":
        project.title = request.form["title"]
        project.description = request.form["description"]
        project.link = request.form["link"]
        db.session.commit()
        return redirect(url_for("projects"))
    return render_template("edit.html", project=project)


# DELETE
@app.route("/projects/delete/<int:id>", methods=["POST"])
def delete_project(id):
    project = db.get_or_404(Project, id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("projects"))


if __name__ == "__main__":
    app.run(debug=True)