"""Flask Application for Paws Rescue Center."""

from sys import stderr
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from forms import LoginForm, SignUpForm, PetForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "dfewfew123213rwdsgert34tgfd1234trgf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paws.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    pets = db.relationship("Pet", backref="user")


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String, nullable=True)
    posted_by = db.Column(db.String, db.ForeignKey("user.id"))


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)


@app.route("/")
def home():
    """Information regarding the Pets in the System."""
    return render_template("home.html", pets=Pet.query.all())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        query = User.query.filter_by(email=form.email.data, password=form.password.data)
        user = query.first()
        if user:
            session["user"] = user.id
            message = "Logged in successfully"
        else:
            message = "Invalid credentials"
        return render_template("login.html", form=form, message=message)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    print("here")
    if "user" in session:
        session.pop("user")
    return redirect(url_for("home", _external=True))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(new_user)

        try:
            db.session.commit()
            message = "Successfully Created User"
        except IntegrityError as e:
            db.session.rollback()
            message = "This email already exists in the system! Please log in instead"
            eprint(e)
        except SQLAlchemyError as e:
            db.session.rollback()
            message = "Error when creating user - please try again"
            eprint(e)
        finally:
            db.session.close()

        return render_template("signup.html", form=form, message=message)
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)


@app.route("/details/<int:id>", methods=["GET", "POST"])
def details(id):
    pet = Pet.query.get_or_404(id, "No Pet was found with the given ID")
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()

    # if "user" in session and session["user"] == pet.posted_by:
    if "user" in session:
        return render_template("details.html", pet=pet, form=form)
    return render_template("details.html", pet=pet)


@app.route("/delete/<int:id>")
def delete_pet(id):
    pet = Pet.query.get_or_404(id, "No Pet was found with the given ID")
    db.session.delete(pet)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)

    return redirect(url_for("home", _external=True))


def populate_db():
    # Create "team" user and add it to session
    team = User(
        full_name="Pet Rescue Team", email="team@petrescue.co", password="adminpass"
    )
    db.session.merge(team)

    # Create all pets
    nelly = Pet(
        id=1,
        name="Nelly",
        age="5 weeks",
        bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.",
    )
    yuki = Pet(
        id=2,
        name="Yuki",
        age="8 months",
        bio="I am a handsome gentle-cat. I like to dress up in bow ties.",
    )
    basker = Pet(
        id=3,
        name="Basker",
        age="1 year",
        bio="I love barking. But, I love my friends more.",
    )
    mrfurrkins = Pet(id=4, name="Mr. Furrkins", age="5 years", bio="Probably napping.")

    # Add all pets to the session
    db.session.merge(nelly)
    db.session.merge(yuki)
    db.session.merge(basker)
    db.session.merge(mrfurrkins)

    # Commit changes in the session
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


@app.route("/reset")
def reset():
    populate_db()
    return redirect(url_for("home", _external=True))


if __name__ == "__main__":
    """ """
    # Creation of the database tables within the application context.
    with app.app_context():
        db.create_all()
        populate_db()

    app.run(debug=True, host="0.0.0.0", port=3001)
