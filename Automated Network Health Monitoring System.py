import nmap
import paramiko
from flask import Flask, render_template, jsonify
import threading
import time
import sqlite3

app = Flask(__name__)
DATABASE = 'network_devices.db'

# Function to scan the network and check device status
def scan_network():
    nm = nmap.PortScanner()
    while True:
        conn = get_db_connection()
        devices = conn.execute('SELECT * FROM devices').fetchall()

        for device in devices:
            ip = device['ip']
            status = 'Down'
            
            try:
                nm.scan(hosts=ip, arguments='-sn')
                if nm[ip].state() == 'up':
                    status = 'Up'
            except:
                pass

            conn.execute('UPDATE devices SET status = ? WHERE id = ?', (status, device['id']))
            conn.commit()
        
        conn.close()
        time.sleep(60)  # Re-scan every minute

# Function to establish SSH connection to a device (optional)
def ssh_to_device(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command('show ip interface brief')
    print(stdout.read().decode())
    ssh.close()

# Flask route for network dashboard
@app.route('/')
def index():
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices').fetchall()
    conn.close()
    return render_template('index.html', devices=devices)

# Route for AJAX calls to get live network status
@app.route('/get_status')
def get_status():
    conn = get_db_connection()
    devices = conn.execute('SELECT * FROM devices').fetchall()
    conn.close()
    return jsonify([dict(row) for row in devices])

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ip TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Unknown'
        )
    ''')
    conn.close()

# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    init_db()
    threading.Thread(target=scan_network).start()  # Start network scan in a separate thread
    app.run(debug=True)
