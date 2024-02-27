from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to the Homepage!\n"


@app.route("/educative")
def learn():
    return "Happy Learning at Educative!\n"


@app.route("/<my_name>")
def greatings(my_name):
    """View function to greet the user by name."""
    return "Welcome " + my_name + "!\n"


@app.route("/square/<int:number>")
def show_square(number):
    """View that shows the square of the number passed by URL"""
    return "Square of " + str(number) + " is: " + str(number * number) + "\n"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3001)
