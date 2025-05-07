import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Database connection configuration
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "justrentmalta")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "KmCji@5BxmiWK")
DB_NAME = os.environ.get("DB_NAME", "jrm_db")

# Determine which database to use based on environment
# If running locally or in development without MySQL access, use SQLite
try:
    if os.environ.get("VERCEL_ENV") or os.environ.get("USE_MYSQL", "0") == "1":
        # In production (on Vercel or when explicitly requesting MySQL)
        encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
        mysql_uri = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
        app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
        print(f"Configured MySQL connection to {DB_HOST}/{DB_NAME} with user {DB_USER}")
    else:
        # For local development in Replit, use SQLite
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///property_database.db"
        print("Using SQLite database for local development")
except Exception as e:
    print(f"Error configuring database connection: {str(e)}")
    # Fallback to SQLite in case of configuration error
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///property_database.db"
    print("Falling back to SQLite due to configuration error")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Property model - Matches the structure of properties_old table
class Property(db.Model):
    __tablename__ = 'properties_old'  # Real table name from the database
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Property {self.id}>'
        
# For the demo, let's create a function to add sample data
def create_sample_data():
    # Only create sample data if the table is empty
    if not Property.query.first():
        for i in range(1, 6):
            sample_property = Property(
                id=i,
                address=f"123 Main St, Apartment {i}, Saint Paul's Bay, Malta"
            )
            db.session.add(sample_property)
        db.session.commit()
        print("Added sample properties to the database")

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = ""
    success_message = ""
    properties = []
    
    if request.method == 'POST':
        property_id = request.form.get('id')
        address = request.form.get('address')
        
        # Validate inputs
        if not property_id or not address:
            error_message = "Both ID and address fields are required."
        else:
            try:
                property_id = int(property_id)
                
                # Find the property
                property_to_update = Property.query.get(property_id)
                
                if property_to_update:
                    # Update the address
                    property_to_update.address = address
                    db.session.commit()
                    success_message = "Address updated successfully!"
                else:
                    error_message = "No property found with the provided ID."
                    
            except ValueError:
                error_message = "ID must be a valid integer."
            except Exception as e:
                error_message = f"Database error: {str(e)}"
                print(f"Error in POST handler: {str(e)}")
    
    # Fetch all properties to display in a table with error handling
    try:
        properties = Property.query.all()
        print(f"Retrieved {len(properties)} properties from the database")
    except Exception as e:
        error_message = f"Failed to load properties: {str(e)}"
        print(f"Error fetching properties: {str(e)}")
    
    return render_template('index.html', 
                         error_message=error_message, 
                         success_message=success_message,
                         properties=properties)

# Create tables and sample data if they don't exist (in development)
with app.app_context():
    try:
        db.create_all()
        # Call function to create sample data
        create_sample_data()
    except Exception as e:
        print(f"Could not create database tables: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)