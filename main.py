from flask import Flask, render_template, request, redirect, url_for, session, flash
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def age_check():
    if request.method == "POST":
        age = request.form.get("age")
        if not age or not age.isdigit() or int(age) < 18:
            flash("You must be over 18 to play. Goodbye!", "danger")
            return render_template("age_check.html", kicked=True)
        else:
            session["age_verified"] = True
            return redirect(url_for("enter_money"))
    return render_template("age_check.html", kicked=False)

@app.route("/enter_money", methods=["GET", "POST"])
def enter_money():
    if not session.get("age_verified"):
        return redirect(url_for("age_check"))
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount or not amount.isdigit() or int(amount) <= 0:
            flash("Enter a valid amount.", "danger")
            return render_template("enter_money.html")
        session["balance"] = int(amount)
        return redirect(url_for("home"))
    return render_template("enter_money.html")

@app.route("/home")
def home():
    if not session.get("age_verified") or "balance" not in session:
        return redirect(url_for("age_check"))
    return render_template("home.html", balance=session["balance"])

@app.route("/mines", methods=["GET", "POST"])
def mines():
    if not session.get("age_verified") or "balance" not in session:
        return redirect(url_for("age_check"))
    result = None
    if request.method == "POST":
        bet = int(request.form.get("bet", 0))
        if bet <= 0 or bet > session["balance"]:
            flash("Invalid bet.", "danger")
        else:
            mine = random.randint(1, 5)
            pick = int(request.form.get("pick", 0))
            if pick == mine:
                session["balance"] -= bet
                result = f"You hit a mine! Lost {bet} ZAR."
            else:
                win = bet * 2
                session["balance"] += bet
                result = f"You avoided the mine! Won {bet} ZAR."
    return render_template("mines.html", balance=session["balance"], result=result)

@app.route("/aviator", methods=["GET", "POST"])
def aviator():
    if not session.get("age_verified") or "balance" not in session:
        return redirect(url_for("age_check"))
    result = None
    if request.method == "POST":
        bet = int(request.form.get("bet", 0))
        if bet <= 0 or bet > session["balance"]:
            flash("Invalid bet.", "danger")
        else:
            multiplier = round(random.uniform(1.0, 10.0), 2)
            cashout = float(request.form.get("cashout", 1.0))
            if cashout <= multiplier:
                win = int(bet * cashout)
                session["balance"] += win - bet
                result = f"Plane reached {multiplier}x! You cashed out at {cashout}x and won {win} ZAR."
            else:
                session["balance"] -= bet
                result = f"Plane crashed at {multiplier}x! You lost {bet} ZAR."
    return render_template("aviator.html", balance=session["balance"], result=result)

@app.route("/dice", methods=["GET", "POST"])
def dice():
    if not session.get("age_verified") or "balance" not in session:
        return redirect(url_for("age_check"))
    result = None
    if request.method == "POST":
        bet = int(request.form.get("bet", 0))
        guess = int(request.form.get("guess", 0))
        if bet <= 0 or bet > session["balance"] or not (1 <= guess <= 6):
            flash("Invalid bet or guess.", "danger")
        else:
            roll = random.randint(1, 6)
            if guess == roll:
                win = bet * 6
                session["balance"] += win - bet
                result = f"Dice rolled {roll}. You guessed right! Won {win} ZAR."
            else:
                session["balance"] -= bet
                result = f"Dice rolled {roll}. You lost {bet} ZAR."
    return render_template("dice.html", balance=session["balance"], result=result)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("age_check"))

if __name__ == "__main__":
    app.run(debug=True)