# Backend service


### 1. Install virtual environment

we’ll create our virtual environment and install our packages (Python3.6+).

For Linux (Bash)
```` Bash
$ cd server
$ python3.9 -m venv venv
$ source venv/bin/activate
$ pip install fastapi
$ pip install uvicorn[standard]
$ pip install motor
````

For Windows (Scripts)
````
cd server
python3.9 -m venv venv
venv\Scripts\activate.bat
pip install fastapi
pip install uvicorn[standard]
pip install motor
````

For more about virtual environment you can refer [here](https://docs.python.org/3/tutorial/venv.html)

### 2. Packages

[uvicorn](https://www.uvicorn.org/) is used to run the server and [motor](https://pypi.org/project/motor/) is our async driver for mongoDB.

### 3. Run

````
uvicorn main:app
````

Then access at `localhost:2110` or `localhost:2110/docs` to see the interactive api documentation.
