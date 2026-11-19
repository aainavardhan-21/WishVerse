from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.utils import secure_filename
from database import init_db

app = Flask(__name__)
app.secret_key = "wishverse_secret_key"

# -------------------------
# Upload Folder
# -------------------------
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------
# Initialize Database
# -------------------------
init_db()


# -------------------------
# Database Connection
# -------------------------
def get_db_connection():
    conn = sqlite3.connect("wishverse.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# REGISTER
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(?,?,?)
            """,
            (username, email, password),
        )

        conn.commit()
        conn.close()

        flash("Registration Successful! Please Login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password),
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")
# -------------------------
# DASHBOARD
# -------------------------
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    cards = conn.execute(
        """
        SELECT * FROM cards
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (session["user_id"],),
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        cards=cards,
        username=session["username"]
    )


# -------------------------
# CREATE CARD
# -------------------------
@app.route("/create-card", methods=["GET", "POST"])
def create_card():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        receiver = request.form["receiver"]
        sender = request.form["sender"]
        occasion = request.form["occasion"]
        theme = request.form["theme"]
        message = request.form["message"]
        secret_letter = request.form["secret_letter"]

        cover_image = ""

        file = request.files.get("cover_image")

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )
            cover_image = filename

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO cards
            (
            user_id,
            title,
            receiver,
            sender,
            occasion,
            theme,
            message,
            secret_letter,
            cover_image,
            music
            )

            VALUES
            (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                session["user_id"],
                title,
                receiver,
                sender,
                occasion,
                theme,
                message,
                secret_letter,
                cover_image,
                ""
            ),
        )

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("create_card.html")

# Edit Section 

@app.route("/edit-card/<int:card_id>", methods=["GET", "POST"])
def edit_card(card_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    card = conn.execute(
        """
        SELECT * FROM cards
        WHERE id=? AND user_id=?
        """,
        (card_id, session["user_id"]),
    ).fetchone()

    if card is None:
        conn.close()
        flash("Card not found.")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        title = request.form["title"]
        receiver = request.form["receiver"]
        sender = request.form["sender"]
        occasion = request.form["occasion"]
        theme = request.form["theme"]
        message = request.form["message"]
        secret_letter = request.form["secret_letter"]

        cover_image = card["cover_image"]

        file = request.files.get("cover_image")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            cover_image = filename

        conn.execute(
            """
            UPDATE cards
            SET title=?,
                receiver=?,
                sender=?,
                occasion=?,
                theme=?,
                message=?,
                secret_letter=?,
                cover_image=?
            WHERE id=? AND user_id=?
            """,
            (
                title,
                receiver,
                sender,
                occasion,
                theme,
                message,
                secret_letter,
                cover_image,
                card_id,
                session["user_id"],
            ),
        )

        conn.commit()
        conn.close()

        flash("Card updated successfully!")
        return redirect(url_for("dashboard"))

    conn.close()

    return render_template("edit_card.html", card=card)

# -------------------------
# VIEW CARD
# -------------------------
@app.route("/card/<int:card_id>")
def view_card(card_id):

    conn = get_db_connection()

    card = conn.execute(
        """
        SELECT * FROM cards
        WHERE id=?
        """,
        (card_id,),
    ).fetchone()

    conn.close()

    if card is None:
        return "Card Not Found"

    return render_template(
        "view_card.html",
        card=card
    )
# # -------------------------
# # PREVIEW CARD
# # -------------------------
# @app.route("/preview/<int:card_id>")
# def preview(card_id):

#     if "user_id" not in session:
#         return redirect(url_for("login"))

#     conn = get_db_connection()

#     card = conn.execute(
#         """
#         SELECT * FROM cards
#         WHERE id=? AND user_id=?
#         """,
#         (card_id, session["user_id"]),
#     ).fetchone()

#     conn.close()

#     if card is None:
#         flash("Card not found.")
#         return redirect(url_for("dashboard"))

#     return render_template(
#         "preview.html",
#         card=card
#     )


# -------------------------
# DELETE CARD
# -------------------------
@app.route("/delete-card/<int:card_id>")
def delete_card(card_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM cards
        WHERE id=? AND user_id=?
        """,
        (card_id, session["user_id"]),
    )

    conn.commit()
    conn.close()

    flash("Card Deleted Successfully!")

    return redirect(url_for("dashboard"))


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.")

    return redirect(url_for("home"))


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)