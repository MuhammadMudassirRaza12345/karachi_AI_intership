from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
current_dateTime = datetime.now()
app = Flask(__name__)

# MySQL database configuration. Replace 'username', 'password', 'database_name', and 'host' with your actual database credentials.
db_conn =mysql.connector.connect(
    host="localhost",
    username="root",
    database='tmc_hr_prod',
    password=""
) 
with db_conn.cursor() as cursor:
    cursor.execute('SHOW TABLES LIKE "employee"')
    if not cursor.fetchone():
        cursor.execute('''
            CREATE TABLE employee (
              id INT AUTO_INCREMENT PRIMARY KEY,
              created_by VARCHAR(255),
              personal_email VARCHAR(255),
              cnic VARCHAR(255),
              contact_no VARCHAR(255),
              email VARCHAR(255),
              enabled BIT,
              father_name VARCHAR(255),
              first_name VARCHAR(255),
              last_name VARCHAR(255),
              qualification VARCHAR(255),
              total_leaves INT,
              manager_id BIGINT,
              employee_type VARCHAR(100),
              personal_no VARCHAR(45)
            )
        ''')
        db_conn.commit()





@app.route('/user', methods=['POST','GET'])
def user():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Invalid Content-Type. Expected application/json.'}), 400

    data = request.get_json()
    
    created_by = data.get('created_by')
    personal_email = data.get('personal_email')
    cnic = data.get('cnic')
    contact_no = data.get('contact_no')
    email = data.get('email')
    enabled = data.get('enabled')
    father_name = data.get('father_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    qualification = data.get('qualification')
    total_leaves = data.get('total_leaves')
    manager_id = data.get('manager_id')
    employee_type = data.get('employee_type')
    personal_no = data.get('personal_no')

    if not ( created_by and personal_email and cnic and contact_no and email and enabled
            and father_name and first_name and last_name and qualification and total_leaves
            and manager_id and employee_type and personal_no):
        return jsonify({'error': 'All fields are required!'}), 400

    # Check if the email or CNIC is already registered
    with db_conn.cursor() as cursor:
        cursor.execute('SELECT id FROM employee WHERE personal_email = %s OR cnic = %s', (personal_email, cnic))
        result = cursor.fetchone()
        if result:
            return jsonify({'error': 'Personal email or CNIC already registered!'}), 409

    # Insert the new user data into the 'users' table
    with db_conn.cursor() as cursor:
        sql = 'INSERT INTO employee ( created_by, personal_email, cnic, contact_no, email, enabled, father_name, first_name, last_name, qualification, total_leaves, manager_id, employee_type, personal_no) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = ( created_by, personal_email, cnic, contact_no, email, enabled, father_name, first_name, last_name, qualification, total_leaves, manager_id, employee_type, personal_no)
        cursor.execute(sql, values)
        db_conn.commit()

    return jsonify({'message': 'User created successfully!', 'user': {
        'created_by': created_by,
        'personal_email': personal_email,
        'cnic': cnic,
        'contact_no': contact_no,
        'email': email,
        'enabled': enabled,
        'father_name': father_name,
        'first_name': first_name,
        'last_name': last_name,
        'qualification': qualification,
        'total_leaves': total_leaves,
        'manager_id': manager_id,
        'employee_type': employee_type,
        'personal_no': personal_no
    }}), 201

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8000)
 