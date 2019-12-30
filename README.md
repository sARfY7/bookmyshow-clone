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

### Creating `gunicorn` Service on Linux

If you want gunicorn to start automatically with your system then you'll have to create a service for that.
