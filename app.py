from flask import Flask, render_template, request, redirect, url_for, flash
from crm_db import init_db, list_customers, search_customers, create_customer

# Flask application object
app = Flask(__name__)

# Secret key: used by Flask for secure session + flash messages
app.secret_key = "dev-secret"

# Initialize database (create table if needed)
init_db()


@app.route("/")
def index():
    """
    Redirect root URL '/' to '/customers'.
    """
    return redirect(url_for("customers_list"))


@app.route("/customers")
def customers_list():
    """
    List customers or search if 'q' query parameter is given.
    """
    q = request.args.get("q", "").strip()

    if q:
        customers = search_customers(q)
    else:
        customers = list_customers()

    return render_template("customers.html", customers=customers, q=q)


@app.route("/customers/add", methods=["GET", "POST"])
def customers_add():
    """
    Show add form (GET) or handle form submission (POST).
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip() or None

        if not name or not email:
            flash("Name and email are required.")
            return redirect(url_for("customers_add"))

        try:
            create_customer(name=name, email=email, phone=phone)
            flash("Customer added.")
            return redirect(url_for("customers_list"))
        except Exception as e:
            # Exception = Python error object
            flash(f"Error adding customer: {e}")
            return redirect(url_for("customers_add"))

    # GET: render the form
    return render_template("customer_add.html")


if __name__ == "__main__":
    print("Starting Flask server…")
    app.run(debug=True)
