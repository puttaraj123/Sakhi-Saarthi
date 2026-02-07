from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import date

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("role.html")

@app.route("/role.html")
def role():
    return render_template("role.html")

@app.route("/women.html")
def women():
    return render_template("women.html")

@app.route("/womenschemes.html")
def womenschemes():
    return render_template("womenschemes.html")

@app.route("/eligibility.html")
def eligibility():
    return render_template("eligibility.html")

@app.route("/helplines.html")
def helplines():
    return render_template("helplines.html")

@app.route("/legal_rights.html")
def legal_rights():
    return render_template("legal_rights.html")

@app.route("/child.html")
def child():
    return render_template("child.html")

@app.route("/nutrition.html")
def nutrition():
    return render_template("nutrition.html")

@app.route("/education.html")
def education():
    return render_template("education.html")

@app.route("/child_abuse.html")
def child_abuse():
    return render_template("child_abuse.html")

@app.route("/admin.html")
def admin():
    return render_template("admin.html")

@app.route("/admin-dashboard.html")
def admindashboard():
    return render_template("admin-dashboard.html")

@app.route("/anganawadi.html")
def anganawadi():
    return render_template("anganawadi.html")

@app.route("/A1image.html")
def A1image():
    return render_template("A1image.html")

@app.route("/A2image.html")
def A2image():
    return render_template("A2image.html")

@app.route("/test-scheme")
def test_scheme():
    return render_template("test-scheme.html")
@app.route("/edit_scheme/<int:id>", methods=["GET", "POST"])
def edit_scheme(id):
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        beneficiary = request.form.get("beneficiary")

        cursor.execute(
            "UPDATE schemes SET name=%s, category=%s, beneficiary=%s WHERE id=%s",
            (name, category, beneficiary, id)
        )
        db.commit()
        return redirect("/schemes")

    cursor.execute("SELECT * FROM schemes WHERE id=%s", (id,))
    scheme = cursor.fetchone()
    return render_template("edit-scheme.html", scheme=scheme)


app.secret_key = "secret123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sakhi_saarthi",
    autocommit=True   # 🔴 THIS LINE IS IMPORTANT
)

cursor = db.cursor(dictionary=True)


# ---------------- ADMIN LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin":
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")



# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT COUNT(*) AS total FROM schemes")
    schemes_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM complaints")
    complaints_count = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM anganwadi")
    anganwadi_count = cursor.fetchone()["total"]

    return render_template(
        "admin-dashboard.html",
        schemes=schemes_count,
        complaints=complaints_count,
        anganwadi=anganwadi_count
    )
cursor = db.cursor(dictionary=True)


# ---------------- COMPLAINTS ----------------
# IMPORTANT: cursor must be defined BEFORE routes
cursor = db.cursor(dictionary=True)


@app.route("/complaints", methods=["GET", "POST"])
def complaints():
    if request.method == "POST":
        name = request.form.get("name")
        ctype = request.form.get("type")
        description = request.form.get("description")

        cursor.execute(
            "INSERT INTO complaints (name, type, description, date) VALUES (%s, %s, %s, CURDATE())",
            (name, ctype, description)
        )
        db.commit()
        return redirect("/complaints")

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    return render_template("admin-complaints.html", complaints=complaints)


@app.route("/edit_complaint/<int:id>", methods=["GET", "POST"])
def edit_complaint(id):
    if request.method == "POST":
        status = request.form.get("status")

        cursor.execute(
            "UPDATE complaints SET status=%s WHERE id=%s",
            (status, id)
        )
        db.commit()
        return redirect("/complaints")

    cursor.execute("SELECT * FROM complaints WHERE id=%s", (id,))
    complaint = cursor.fetchone()
    return render_template("edit-complaint.html", complaint=complaint)


@app.route("/delete_complaint/<int:id>")
def delete_complaint(id):
    cursor.execute("DELETE FROM complaints WHERE id=%s", (id,))
    db.commit()
    return redirect("/complaints")

# ---------------- SCHEMES ----------------
@app.route("/schemes", methods=["GET", "POST"])
def schemes():
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        beneficiary = request.form.get("beneficiary")

        print("POST DATA:", name, category, beneficiary)

        cursor.execute(
            "INSERT INTO schemes (name, category, beneficiary) VALUES (%s, %s, %s)",
            (name, category, beneficiary)
        )
        db.commit()

        return "INSERT OK"

    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()
    return render_template("admin-schemes.html", schemes=schemes)


@app.route("/delete_scheme/<int:id>")
def delete_scheme(id):
    cursor.execute("DELETE FROM schemes WHERE id = %s", (id,))
    db.commit()
    return redirect("/schemes")


# ---------------- ANGANWADI ----------------
@app.route("/anganwadi", methods=["GET", "POST"])
def anganwadi():
    if request.method == "POST":
        center_name = request.form.get("center_name")
        location = request.form.get("location")
        worker_name = request.form.get("worker_name")
        contact = request.form.get("contact")

        print("ADD ANGANWADI:", center_name, location, worker_name, contact)

        cursor.execute(
            "INSERT INTO anganwadi (center_name, location, worker_name, contact) VALUES (%s, %s, %s, %s)",
            (center_name, location, worker_name, contact)
        )
        db.commit()

        return redirect("/anganwadi")

    cursor.execute("SELECT * FROM anganwadi")
    centers = cursor.fetchall()
    return render_template("admin-anganwadi.html", centers=centers)
cursor = db.cursor(dictionary=True)

@app.route("/edit_anganwadi/<int:id>", methods=["GET", "POST"])
def edit_anganwadi(id):
    if request.method == "POST":
        cursor.execute(
            "UPDATE anganwadi SET center_name=%s, location=%s, worker_name=%s, contact=%s WHERE id=%s",
            (
                request.form["center_name"],
                request.form["location"],
                request.form["worker_name"],
                request.form["contact"],
                id
            )
        )
        db.commit()
        return redirect("/anganwadi")

    cursor.execute("SELECT * FROM anganwadi WHERE id=%s", (id,))
    center = cursor.fetchone()

    return render_template("edit-anganwadi.html", center=center)

@app.route("/delete_anganwadi/<int:id>")
def delete_anganwadi(id):
    print("DELETE HIT:", id)   # debug line
    cursor.execute("DELETE FROM anganwadi WHERE id=%s", (id,))
    db.commit()
    return redirect("/anganwadi")




# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



@app.route("/test-scheme")
def test_scheme():
    return render_template("test-scheme.html")



@app.route("/edit_scheme/<int:id>", methods=["GET", "POST"])
def edit_scheme(id):
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        beneficiary = request.form["beneficiary"]

        cursor.execute(
            "UPDATE schemes SET name=%s, category=%s, beneficiary=%s WHERE id=%s",
            (name, category, beneficiary, id)
        )
        db.commit()
        return redirect("/schemes")

    cursor.execute("SELECT * FROM schemes WHERE id=%s", (id,))
    scheme = cursor.fetchone()
    return render_template("edit-scheme.html", scheme=scheme)


@app.route("/edit_scheme/<int:id>", methods=["GET", "POST"])
def edit_scheme(id):
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        beneficiary = request.form.get("beneficiary")

        cursor.execute(
            "UPDATE schemes SET name=%s, category=%s, beneficiary=%s WHERE id=%s",
            (name, category, beneficiary, id)
        )
        db.commit()
        return redirect("/schemes")

    # GET request
    cursor.execute("SELECT * FROM schemes WHERE id=%s", (id,))
    scheme = cursor.fetchone()

    if scheme is None:
        return "Scheme not found", 404

    return render_template("edit-scheme.html", scheme=scheme)


@app.route("/add-test", methods=["GET", "POST"])
def add_test():
    if request.method == "POST":
        print("FORM DATA RECEIVED:", request.form)
        return "FORM RECEIVED"

    return """
    <form method="POST">
        <input name="x">
        <button type="submit">Send</button>
    </form>
    """



