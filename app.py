from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from bus_scheduling_module import *
import mysql.connector
import json
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Ensure this is complex and unique for security

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="bus_scheduling"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Route to display the home (index) page
@app.route("/")
def index():
    return render_template("index.html")

# Route to display the sign-up page from index
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/aboutus")
def about_us():
    return render_template("aboutus.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/terms_n_condition")
def terms_n_condition():
    return render_template("terms_n_condition.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/forget_password")
def forget_password():
    return render_template("forget_password.html")

# Route to handle Admin Sign-Up
@app.route("/admin-signup", methods=["POST"])
def admin_signup():
    data = request.form
    connection = get_db_connection()
    try:
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO admin (first_name, mid_name, last_name, email, admin_id, phone_number, age, gender, security_question, security_answer, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data["first_name"],
                data.get("mid_name", ""),
                data.get("last_name", ""),
                data["email"],
                data["admin_id"],
                data["Phone_number"],
                data["age"],
                data["gender"],
                data.get("security_question", ""),
                data.get("security_answer", ""),
                data["password"]
            )
            cursor.execute(query, values)
            connection.commit()
            flash("Admin registered successfully! Login Now", "success")
        else:
            flash("Database connection error!", "danger")
    except Error as e:
        flash(f"Error: {e}", "danger")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return redirect(url_for("signup"))

# Route to handle Traveler Sign-Up
@app.route("/traveler-signup", methods=["POST"])
def traveler_signup():
    data = request.form
    connection = get_db_connection()
    try:
        if connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO traveler (first_name, mid_name, last_name, email, traveler_id, phone_number, age, gender, security_question, security_answer, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                data["first_name"],
                data.get("mid_name", ""),
                data.get("last_name", ""),
                data["email"],
                data["traveler_id"],
                data["Phone_number"],
                data["age"],
                data["gender"],
                data.get("security_question", ""),
                data.get("security_answer", ""),
                data["password"]
            )
            cursor.execute(query, values)
            connection.commit()
            flash("Traveler registered successfully! Login Now", "success")
        else:
            flash("Database connection error!", "danger")
    except Error as e:
        flash(f"Error: {e}", "danger")
    finally:
        if connection:
            cursor.close()
            connection.close()
    return redirect(url_for("signup"))

# Route to handle Login
@app.route("/dashboard_login", methods=["POST"])
def login_post():
    user_id = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")  # Captures 'admin' or 'traveler'
    
    connection = get_db_connection()

    if connection:
        cursor = connection.cursor(dictionary=True)
        if user_type == "admin":
            query = "SELECT * FROM admin WHERE (admin_id = %s OR email = %s) AND password = %s"
        else:
            query = "SELECT * FROM traveler WHERE (traveler_id = %s OR email = %s) AND password = %s"
        
        cursor.execute(query, (user_id, user_id, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["admin_id"] if user_type == "admin" else user["traveler_id"]
            session["user_type"] = user_type
            
            # Redirect based on the user type
            if user_type == "admin":
                return jsonify({"success": True, "redirect_url": "/admin_dashboard"})
            else:
                return jsonify({"success": True, "redirect_url": "/traveler_dashboard"})
        else:
            return jsonify({"success": False, "error": "Invalid ID/email or password!"})  # Return error message
        cursor.close()
        connection.close()
    else:
        return jsonify({"success": False, "error": "Database connection error!"})



# Admin Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("user_type") == "admin":
        admin_id = session.get("user_id")  # Get admin ID from session
        connection = get_db_connection()

        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT first_name FROM admin WHERE admin_id = %s"
            cursor.execute(query, (admin_id,))
            admin = cursor.fetchone()  # Fetch the admin data

            if admin:
                admin_name = admin["first_name"]  # Get the admin's first name
                cursor.close()
                connection.close()
                return render_template("admin_dashboard.html", admin_name=admin_name)
            else:
                flash("Admin not found!", "danger")
                cursor.close()
                connection.close()
        else:
            flash("Database connection error!", "danger")
        return redirect(url_for("login"))
    flash("Access Denied!", "danger")
    return redirect(url_for("login"))

# Traveler Dashboard
@app.route("/traveler_dashboard")
def traveler_dashboard():
    if session.get("user_type") == "traveler":
        traveler_id = session.get("user_id")  # Get traveler ID from session
        connection = get_db_connection()

        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT first_name FROM traveler WHERE traveler_id = %s"
            cursor.execute(query, (traveler_id,))
            traveler = cursor.fetchone()  # Fetch the traveler data

            if traveler:
                traveler_name = traveler["first_name"]  # Get the traveler's first name
                cursor.close()
                connection.close()
                return render_template("traveler_dashboard.html", traveler_name=traveler_name)
            else:
                flash("Traveler not found!", "danger")
                cursor.close()
                connection.close()
        else:
            flash("Database connection error!", "danger")
        return redirect(url_for("login"))
    flash("Access Denied!", "danger")
    return redirect(url_for("login"))

@app.route('/crew_management')
def crew_management():
    crew_data = get_all_crew_data()  
    return render_template('crew_management.html', crew_data=crew_data)

@app.route('/bus_management')
def bus_management():
    bus_data = get_all_bus_data()  
    return render_template('bus_management.html', bus_data=bus_data)


@app.route('/validate_schedule', methods=['POST'])
def validate_schedule():
    data = request.get_json()
    crew_id = data['crew_id']
    bus_id = data['bus_id']
    departure_time = data['departure_time']
    scheduling_type = data['scheduling_type']
    emergency = data['emergency']
    route = data['route']

    # Convert departure time to datetime
    try:
        departure_time = datetime.strptime(departure_time, '%H:%M')
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format."})

    # Check if crew and bus IDs exist and are not already assigned
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Check if crew exists
    cursor.execute("SELECT * FROM crews WHERE crew_id = %s", (crew_id,))
    crew = cursor.fetchone()
    if not crew:
        return jsonify({"status": "error", "message": "Crew ID does not exist."})

    # Check if bus exists
    cursor.execute("SELECT * FROM buses WHERE bus_id = %s", (bus_id,))
    bus = cursor.fetchone()
    if not bus:
        return jsonify({"status": "error", "message": "Bus ID does not exist."})

    # Check if crew has 30 minutes rest time
    if crew['last_assignment_time']:
        last_assignment_time = crew['last_assignment_time']
        current_time = datetime.now()
        if current_time - last_assignment_time < timedelta(minutes=30):
            return jsonify({"status": "error", "message": "Crew must have at least 30 minutes rest."})

    # Check if crew and bus are already assigned
    cursor.execute("SELECT * FROM crews WHERE crew_id = %s AND on_duty=1", (crew_id,))
    crew_assign = cursor.fetchone()
    cursor.execute("SELECT * FROM buses WHERE bus_id = %s AND on_road=1", (bus_id,))
    bus_assign = cursor.fetchone()
    if crew_assign or bus_assign:
        return jsonify({"status": "error", "message": "Bus or Crew is already assigned."})

    # Check if crew's daily assignment limit is less than 5
    if crew['daily_assignment_limit'] <=0:
        return jsonify({"status": "error", "message": "Crew has reached daily assignment limit."})

    # Insert into assignments table
    cursor.execute("INSERT INTO assignments (crew_id, bus_id, assignment_time, accepted, is_emergency, scheduling_type) VALUES (%s, %s, %s, %s, %s, %s)",
                   (crew_id, bus_id, departure_time, 1, emergency, scheduling_type))

    # Update the crews table
    update_values = {
        'assigned_bus': bus_id,
        'on_duty': 1,
        'accept_count': crew['accept_count'] + 1,
        'reject_count': crew['reject_count'],
        'emergency_count': crew['emergency_count'] + 1 if emergency==1 else crew['emergency_count'],
        'total_proposals': crew['total_proposals'] + 1,
        'daily_assignment_limit': crew['daily_assignment_limit'] - 1
    }
    cursor.execute("""
        UPDATE crews SET assigned_bus = %s, on_duty = %s, accept_count = %s, reject_count = %s,
        emergency_count = %s, total_proposals = %s, daily_assignment_limit = %s
        WHERE crew_id = %s
    """, (update_values['assigned_bus'], update_values['on_duty'], update_values['accept_count'],
          update_values['reject_count'], update_values['emergency_count'], update_values['total_proposals'],
          update_values['daily_assignment_limit'], crew_id))

    # Update the buses table
    # If bus already has a schedule, append to it, otherwise create a new list
    bus_schedule = json.loads(bus['schedule']) if bus['schedule'] else []
    bus_schedule.append(departure_time.strftime('%H:%M'))
    cursor.execute("""
        UPDATE buses SET route = %s, assigned_crew = %s, on_road = %s, schedule = %s
        WHERE bus_id = %s
    """, (route, crew_id, 1, json.dumps(bus_schedule), bus_id))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"status": "success", "message": "Schedule added successfully!"})


if __name__ == "__main__":
    app.run(debug=True, port=3000)
