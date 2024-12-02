from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__, static_folder='assets')
app.secret_key = '#Key0123456789#'  

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssw0rd'
app.config['MYSQL_DB'] = 'rentdb'

mysql = MySQL(app)

# Route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info('Running the index.html page...')
    return render_template('index.html')

# Route for authentication page
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    app.logger.info('Running the auth.html page...')
    return render_template('auth.html')

# Route for login
@app.route('/login', methods=['POST'])
def login():
    app.logger.info('Inside the login block')
    email = request.form['email']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
    user = cur.fetchone()
    
    if user:
        # Ensure password is correct by checking hash
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]  
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to home page after login
        else:
            flash('Invalid password, please try again.', 'danger')
    else:
        flash('No user found with that email.', 'danger')

    app.logger.info('End of login module')
    return redirect(url_for('auth'))  # Redirect back to the authentication page if login fails

# Route for registration
@app.route('/register', methods=['POST'])
def register():
    app.logger.info('Start the register block')
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        flash('Email already registered. Please log in.', 'danger')
        return redirect(url_for('auth'))
    
    # Insert new user into the database
    cur.execute("INSERT INTO Users (Name, Email, Password) VALUES (%s, %s, %s)", (full_name, email, hashed_password))
    mysql.connection.commit()

    # Fetch the newly created user
    cur.execute("SELECT * FROM Users WHERE Email = %s", (email,))
    new_user = cur.fetchone()

    if new_user:  # Ensure the new user was added successfully
        session['user_id'] = new_user[0]  # Set the user session
        flash('Registration successful! Redirecting to the home page...', 'success')
        app.logger.info('End of register module')
        return redirect(url_for('index'))  # Redirect to home page after successful registration
    else:
        flash('Registration failed. Please try again later.', 'danger')
        app.logger.error('Failed to fetch newly registered user')
        return redirect(url_for('auth'))  # Redirect back to auth page if registration fails

# Route to display all cars when the "View More" button is clicked
@app.route('/view-more', methods=['GET'])
def view_more_cars():
    app.logger.info('Accessing the all cars page from the "View More" button...')

    # Ensure the user is logged in before showing cars
    if 'user_id' not in session:
        app.logger.warning("User not logged in, redirecting to /auth")
        flash('Please log in to view all cars.', 'warning')
        return redirect(url_for('auth'))

    try:
        # Fetch all cars that are available
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Cars WHERE AvailabilityStatus = TRUE")
        cars = cur.fetchall()

        if cars:  # Check if we have any cars to display
            app.logger.info(f"Fetched Cars: {cars}")
        else:
            flash('No cars available at the moment.', 'info')
            app.logger.info('No cars available')

        return render_template('cars.html', cars=cars)  # Display cars page with all cars

    except Exception as e:
        app.logger.error(f"Error fetching cars: {str(e)}")
        flash("An error occurred. Please try again later.", "danger")
        return redirect(url_for('index'))

@app.route('/cars', methods=['GET'])
def cars():
    search_query = request.args.get('search', '').strip()  # Get search query (if any)

    try:
        cur = mysql.connection.cursor()
        
        if search_query:
            # Fetch cars that match the search query
            cur.execute("""
                SELECT * FROM Cars
                WHERE (Name LIKE %s OR Fuel_Type LIKE %s) AND OwnerID IS NOT NULL
            """, (f"%{search_query}%", f"%{search_query}%"))
        else:
            # Fetch all cars
            cur.execute("SELECT * FROM Cars WHERE OwnerID IS NOT NULL")

        cars = cur.fetchall()
        return render_template('cars.html', cars=cars, search_query=search_query)

    except Exception as e:
        app.logger.error(f"Error fetching cars: {str(e)}")
        flash("An error occurred while fetching car data.", "danger")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
