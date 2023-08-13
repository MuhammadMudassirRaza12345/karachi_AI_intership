 
from flask import Flask, request, jsonify 
import mysql.connector
import random
import string
from faker import Faker
import bcrypt

app = Flask(__name__)

# MySQL database configuration. Replace 'username', 'password', 'database_name', and 'host' with your actual database credentials.
db_conn = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL host
    user="my_user",  # Replace with your MySQL username
    database='tmc_hr_prod',  # Replace with your MySQL database name
    password="my_password"  # Replace with your MySQL password
)
 

# Check if the 'user' table exists and create if it doesn't
with db_conn.cursor() as cursor:
    cursor.execute('SHOW TABLES LIKE "user"')
    if not cursor.fetchone():
        cursor.execute('''
            CREATE TABLE user (
              id INT AUTO_INCREMENT PRIMARY KEY,
              created_by VARCHAR(255),
              enabled BIT,
              password VARCHAR(255),
              useremail VARCHAR(255),
              employee_id INT
            )
        ''')
        db_conn.commit()
  
@app.route('/signup', methods=['POST'])
def signup():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 400

    data = request.get_json()
    fake = Faker()

    # Generate random password for the user
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    

    # Insert the new user data into the 'users' table with the fetched 'employee_id'
    with db_conn.cursor() as cursor:
        sql = 'INSERT INTO user (created_by, enabled, password, useremail, employee_id) VALUES (%s, %s, %s, %s, %s)'
        values = (data['created_by'], data.get('enabled', False), hashed_password, data['useremail'], data['employee_id'])
        cursor.execute(sql, values)
        db_conn.commit()

    # Construct the user data (excluding the password and last_modified_by)
    user_data = {
        'created_by': data['created_by'],
        'enabled': data.get('enabled', False),
        'useremail': data['useremail'],
        'employee_id': data['employee_id']
    }

    return jsonify({'message': 'User created successfully!', 'user_data': user_data}), 201



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)