# **Automated Network Health Monitoring System**

**README.md:**

```markdown
# Automated Network Health Monitoring System

## Project Overview
The Automated Network Health Monitoring System continuously scans network devices (e.g., routers, switches, servers) and logs their statuses (up or down). The system provides a web-based dashboard that displays the current state of all network devices and their health metrics. It uses Flask for the web interface, Nmap for network scanning, and Paramiko for SSH connections to devices.

## Features
- Periodic network scanning to monitor the status of all devices.
- Web-based dashboard for viewing real-time network health.
- Ability to SSH into network devices for further diagnostics.
- Multithreading to handle network scanning concurrently for multiple devices.

## Technologies Used
- Python (Flask, Paramiko, Nmap)
- SQLite (for storing network device info)
- HTML, CSS, JavaScript (AJAX for real-time updates)
- Multithreading (to scan network devices concurrently)

## How to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/network-health-monitor.git
