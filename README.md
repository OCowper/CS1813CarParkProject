
# Car Park System - Group 8

This is a software representation of the 'Holborn Car Park System' described in the specification provided to us.

## Installation

### Clone the project

```bash
  git clone https://github.com/OCowper/CS1813CarParkProject.git
```

### Go to the project directory

```bash
  cd CS1813CarParkProject
```

**NB: The way this next command is ran varies depending on installation of python,
you may have to write python3.9 or instead of python3**

### Create a virtual environment
```bash
python3 -m venv env
```

### Activate virtual environment
#### Windows
##### CMD
```bash
env\Scripts\activate.bat
```

##### Powershell
```bash
env\Scripts\Activate.ps1
```

#### Linux / MacOS / NoMachine
```bash
  source env/bin/activate
```


### Install dependencies
**NB: This time actually just write python since you're in a virtual environment so the 
python version remains consistent, if you want to double check just run: python --version**

```bash
  python -m pip install -r requirements.txt
```

---
## Run Locally

**Make sure the virtual environment is activated, see 'Activate virtual environment' in Installation section**


Start the web server

```bash
  flask run
```

If you don't already have an app/database.db file, 
the software will automatically create one for you with pre-set dummy values, default usernames and passwords are (user1, pass1), (user2, pass2), (user3, pass3)


Visit the website at: 

* localhost:5000 
**or** 
* 127.0.0.1:5000

----
## Exiting

When you've finished running the website, press Ctrl+C on your terminal to end the flask process, 
then to leave the virtual environment type:

```bash
deactivate
```

## Usage/Examples
#### This shows how a customer would enter the car park:

![Entering and exiting car park animation](screenshots/enterexit.gif?raw=true)


#### This shows how a manager would login:

![Manager login](screenshots/managerlogin.gif?raw=true "Manager login")


#### This shows how a manager would start/end happy hour manually or schedule it:

![Manager start/end happy hour](screenshots/happyhour.gif?raw=true)


#### This shows how a manager would view reports with a table and graphs:

![Manger viewing reports](screenshots/reportview.gif?raw=true)

## FAQ

#### I tried to open the website and got an 'Access to 127.0.0.1 was denied' error

![Access denied screenshot](screenshots/accessdenied.png?raw=true)

Chances are you've not started the web server

However if this issue persists, clear your browser cookies and visit the website again


## Authors

- @Charles Kasina
- [@Oscar Cowper](mailto:oscar.cowper.2021@live.rhul.ac.uk)
- @Zuhayr Mohsen
- @Yazan Al-Arab
