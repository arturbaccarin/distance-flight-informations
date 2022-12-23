from flask import Flask, render_template

app = Flask(__name__)


@app.route("/find_airport")
def success_airport():
    return render_template("find_airport.html")


@app.route("/not_find_airport")
def fail_airport():
    return render_template("not_find_airport.html")


@app.route("/correct_airports")
def correct_airports():
    return render_template("correct_airports.html")


if __name__ == "__main__":
    app.run()
