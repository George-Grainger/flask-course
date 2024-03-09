"""Flask Application for Paws Rescue Center."""

from flask import Flask, render_template, abort, session, redirect, url_for
from forms import LoginForm, SignUpForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "dfewfew123213rwdsgert34tgfd1234trgf"

"""Information regarding the Users in the System."""
users = [
    {
        "id": 1,
        "full_name": "Pet Rescue Team",
        "email": "team@pawsrescue.co",
        "password": "adminpass",
    },
]

PETS = [
    {
        "id": 1,
        "name": "Nelly",
        "age": "5 weeks",
        "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.",
    },
    {
        "id": 2,
        "name": "Yuki",
        "age": "8 months",
        "bio": "I am a handsome gentle-cat. I like to dress up in bow ties.",
    },
    {
        "id": 3,
        "name": "Basker",
        "age": "1 year",
        "bio": "I love barking. But, I love my friends more.",
    },
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
]


@app.route("/")
def home():
    """Information regarding the Pets in the System."""

    return render_template("home.html", pets=PETS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        # Get the first user
        user = next(user for user in users if user["email"] == form.email.data)
        if user and user["password"] == password:
            message = "Successfully Logged In"
            session["user"] = user
        else:
            message = "Wrong credentials. Please try again."
        print(session)
        return render_template("login.html", form=form, message=message)
    print(session)
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
        if any(user["email"] == form.email.data for user in users):
            message = "User already exists"
        else:
            message = "Successfully Created User"
            users.append(
                {
                    "id": len(users) + 1,
                    "full_name": form.full_name.data,
                    "email": form.email.data,
                    "password": form.password.data,
                }
            )
        return render_template("signup.html", form=form, message=message)
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)


@app.route("/details/<int:id>")
def details(id):
    pet = next((p for p in PETS if p.get("id") == id), None)

    if pet:
        return render_template("details.html", pet=pet)
    else:
        abort(404, description="No Pet was found with the given ID")


if __name__ == "__main__":
    """ """
    app.run(debug=True, host="0.0.0.0", port=3001)
