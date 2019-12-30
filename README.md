## BookMyShow Clone using Flask

This is a simple BookMyShow Clone made with Flask. This Flask application framework is pre-configured with **Flask-SQLAlchemy**, **Flask-WTF**, and the **Bootstrap** frontend.

<hr>

### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/sARfY7/bookmyshow-clone.git
  $ cd bookmyshow-clone
  ```

2. Initialize and activate a virtualenv:
  ```
  $ python3 -m venv env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip3 install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python3 app.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)


# Instructions for Deploying to Production

I am assuming you are using Amazon EC2. In this project Elastic search have been disabled for production environmetns.

1.  Create an EC2 instance in AWS.
2. SSH into the instance
3. Git clone the project.
```
  $ git clone https://github.com/sARfY7/bookmyshow-clone.git
  $ cd bookmyshow-clone
```
5. Install `python3`  if not installed.
4. If you want to create a virtual environment then follow the steps ahead else you can skip ahead to step 6.
```
  $ python3 -m venv 'Your-Environment-Name-Here'
```
5. Activate your environment
```
  $ source Your-Environment-Name-Here/bin/activate
```
6. Install project dependencies
```
  $ pip3 install -r requirements.txt
```
7. Check if application works by running `flask run` or `python3 app.py`

## Integrating Gunicorn to your Flask Application

1. Install `gunicorn`
```
  $ pip3 install gunicorn
```
2. Run `gunicorn` by giving it your application
```
  $ gunicorn  app:app
```
3. Check if gunicorn is running correctly by going to `http://localhost:8000` (8000 is the default port for gunicorn).
4. `gunicorn` would not get environment variables by default. So, make sure you export them before running `gunicorn`.

---
### Creating `gunicorn` Service on Linux
---

If you want gunicorn to start automatically with your system then you'll have to create a service for that.

__gunicorn.service__
```
[Unit]
Description=Gunicorn Daemon
Requires=gunicorn.socket
After=network.target

[Service]
# Give the user you want to execute the service as
User=ubuntu
# Give the group you want to execute the service as
Group=ubuntu
RuntimeDirectory=gunicorn
# Path to Environment Variables containing file
EnvironmentFile=/home/ubuntu/bookmyshow-clone/.env
# Your Project Directory
WorkingDirectory=/home/ubuntu/bookmyshow-clone
# Execution Command
ExecStart=/home/ubuntu/.local/bin/gunicorn app:app --access-logfile /home/ubuntu/log/gunicorn/access/access.log --error-logfile /home/ubuntu/log/gunicorn/error/error.log
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Save the above file in `/etc/systemd/system/` directory with `.service` extension

__gunicorn.socket__
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
# Our service won't need permissions for the socket, since it
# inherits the file descriptor by socket activation
# only the nginx daemon will need access to the socket
User=www-data
# Optionally restrict the socket permissions even more.
# Mode=600

[Install]
WantedBy=sockets.target
```
Save the above file in `/etc/systemd/system/` directory with `.socket` extension

After creating both the files run these commands

```bash
# Enable your service for starting with the system
$ sudo systemctl enable gunicorn.service
# Start your service
$ sudo systemctl start gunicorn.service
```
---
### Configuring Nginx as a Reverse Proxy Server for Gunicorn
---
We'll be using nginx as a reverse proxy for conencting to our flask app. Make sure nginx is installed is on your system. If not then run `sudo apt install nginx`.

1. Go to `/etc/nginx/sites-available` directory.
2. Remove the default file.
3. Create a new file and give it any name you want. This file is your configuration file for your project.
4. Enter the configuration given below
```
server {
        listen 80;
        location / {
                # Url of the socket we created is passed here
                proxy_pass http://unix:/run/gunicorn.sock;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```
5. Save the file and run `sudo nginx -t`. This command tests the nginx configuration.
6. If configuration test return success then restart nginx service `sudo service nginx restart`.

Your Nginx reverse proxy server should now be working. To test goto [localhost](http://localhost)

---
### Creating Celery Service
---
This project uses Celery as a Task Queue to download user data. Instead of running Celery separately everytime we boot up oour application, we can make Celery a service that boots up with the machine.
> **Note**: In this project Celery uses Redis as a broker. So that is also a project dependency for this project. Please run `sudo apt install redis` if you don't have redis installed on your system.

__celery.service__
```
[Unit]
Description=Celery Service
After=network.target redis-server.service

[Service]
Type=forking
# Give the user you want to execute the service as
User=ubuntu
# Give the group you want to execute the service as
Group=ubuntu
EnvironmentFile=/home/ubuntu/bookmyshow-clone/celery
WorkingDirectory=/home/ubuntu/bookmyshow-clone
ExecStart=/home/ubuntu/.local/bin/celery multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}
ExecStop=/home/ubuntu/.local/bin/celery multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}
ExecReload=/home/ubuntu/.local/bin/celery multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}

[Install]
WantedBy=multi-user.target
```

> **Important**: Celery Worker requires its own environment variables. Assign the environment file in the service.

Enable the above created service and it'll start automatically with the system.