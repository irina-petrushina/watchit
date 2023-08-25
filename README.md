# WatchIt!

WatchIt! improve your health habits with wearable sensors.

<br />

With the vast amount of data produced by an Apple Watch daily, it is hard to identify which aspects of user’s health require their immediate attention, and what actions are necessary to improve their health. WatchIt! is designed to indicate the user’s health metrics that require improvement by comparing the user’s data to the medically established norms in their demographic group. Based on the outcome, the application also recommends local fitness classes that will help improve those metrics.

<br />
This application was built as a part of the Data Incubator Fellowship and serves as my Capstone Project. 

The web app is using an amazing template Swipe Bootstrap 5 by Themesberg.
<br />

> Links

- [LIVE Demo](https://watchit-934o.onrender.com/) - deployed website.

<br />

## Build from sources

```bash
$ # Clone the sources
$ git clone https://github.com/app-generator/watchit.git
$ cd watchit
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install requirements
$ pip3 install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Run the app
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the UI in browser: http://127.0.0.1:5000/
```

<br />

## Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The official website

<br />

---
[Jinja Template](https://appseed.us/jinja-template) Swipe - Provided by **AppSeed** [Web App Generator](https://appseed.us/app-generator).
