from flask import Flask, render_template, request, redirect, flash
import subprocess

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if not name:
            flash("Error: Name cannot be empty.", "error")
            return redirect("/")

        try:
            # I sure hope no one tries to run any commands by injecting here...
            output = subprocess.check_output(f"echo {name}", shell=True, text=True, stderr=subprocess.STDOUT)
            flash(f"Hello, {output.strip()}! Good luck!", "success")
            # ...alright, the challenges won't be this obvious on game day, but I hope it gives you a good idea of how the game is played!
        except subprocess.CalledProcessError as e:
            flash(f"Error: {e.output.strip()}", "error")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
