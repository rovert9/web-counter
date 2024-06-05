# Web Counter

# Deploying on Ubuntu (EC2)
First, clone the repository in the `/home/ubuntu/app` folder:
```
git clone https://github.com/jonatasbaldin/web-counter.git /home/ubuntu/app
cd /home/ubuntu/app
```

## Update APT cache
```
sudo apt-cache update
```

## PostgreSQL
Install PostgreSQL:
```
sudo apt install postgresql postgresql-contrib -y
```

Create a user and database on PostgreSQL:
```
# logs into the psql shell
sudo -u postgres psql

# creates the databse
CREATE DATABASE countdb;

# creates the user/password
CREATE USER mary WITH PASSWORD '123456A!';

# allows the user access to the databse
GRANT ALL PRIVILEGES ON DATABASE countdb TO mary;

# grants all privileges in the schema and table for the created used
# required for PostgreSQL 15+
\c countdb
GRANT ALL PRIVILEGES ON SCHEMA public TO mary;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mary;

# exits the psql shell
exit
```

## Python
Install the Python virtual environment package:
```
sudo apt install python3-venv -y
```

Install the dependencies necessary to use the `psycopg2`, the package used to connect the Python application to the PostgreSQL database:
```
sudo apt install build-essential libssl-dev python3-dev libpq-dev -y
```

Create a Python virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install the Python dependencies:
```
pip install -r requirements.txt
```

## Python Service
Run the Python application as a service (using `systemd`).

Create the `/etc/systemd/system/app.service` file with the following content:
```
[Unit]
Description=Python App
After=network.target

[Service]
Environment="DB_NAME=countdb"
Environment="DB_USER=mary"
Environment="DB_PASSWORD=123456A!"
Environment="DB_HOST=localhost"

User=root
WorkingDirectory=/home/ubuntu/app
ExecStart=/home/ubuntu/app/venv/bin/python /home/ubuntu/app/app.py

[Install]
WantedBy=multi-user.target
```

Reload the service daemon:
```
sudo systemctl daemon-reload
```

Enable and start the Python app:
```
sudo systemctl enable app
sudo systemctl start app
sudo systemctl status app
```

## Nginx
Install Nginx:
```
sudo apt install nginx -y
```

Add the following block in the `/etc/nginx/sites-enabled/default` file, at the end of the `server` block:
```
location /api {
    proxy_pass http://127.0.0.1:5000;
    add_header Access-Control-Allow-Origin "*";
}
```

Copy the `index.html` file to the `/var/www/html` folder:
```
sudo cp index.html /var/www/html/
```

Restart and check the Nginx service:
```
sudo systemctl restart nginx
sudo systemctl status nginx
```

## Testing the Application
Grab the external IP address by running:
```
curl ifconfig.me
```

On your web browser, access the IP given from the last command. You should see the application up and running!