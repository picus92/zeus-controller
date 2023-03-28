import os
from flask import Flask, request
import psycopg2
import sys

app = Flask(__name__)

try:
    dbConn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
except psycopg2.OperationalError as e:
    print("Error connecting to the database: ", e)
    sys.exit(1)

@app.route('/register-node', methods=['POST'])
def register_node():
    data = request.get_json()
    node_id = data.get('node_id')
    node_name = data.get('node_name')
    node_ip = data.get('node_ip')
    node_az = data.get('node_az')
    node_az_id = data.get('node_az_id')

    if not node_id or not node_name or not node_ip or not node_az:
        return "Error registering node: Missing required parameters", 400

    try:
        cursor = dbConn.cursor()
        cursor.execute("INSERT INTO nodes (node_id, node_name, node_ip, node_az) VALUES (%s, %s, %s)", (node_id, node_name, node_ip, node_az))
        dbConn.commit()
    except psycopg2.Error as e:
        print("Error inserting data into the database: ", e)
        return "Error registering node: " + str(e), 500

    return "Node registered successfully!"

if __name__ == '__main__':
    app.run()
