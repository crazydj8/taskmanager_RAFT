# CC_Project_Batch1
PES University - Semester 6 Cloud Computing Mini Project

To run this project:

1. Clone this repository

2. create a virtual environment with python version 3.6.8 using the following command(assuming you have conda installed):
```
conda create -n myenv python=3.6.8
```

4. Activate the virtual environment using the following command:
```
conda activate myenv
```

4. Install the required packages using the following command:
```
cd pythonapp
pip install -r requirements.txt
```

3. Come back to root directory and build the docker image using the following command:
```
docker compose build
```

4. Run the docker containers using the following command:
```
docker compose up
```

5. go back to pythonapp directory and run the following command to run the python application:
```
cd pythonapp
streamlit run app.py
```
* It will open a browser window with the application running.

6. now run the route.py file using the following command:
```
export FLASK_APP=route.py
flask run
```
* It will start the flask server.

7. now start the raft application using the following command:
```
python3 node.py --node 1
python3 node.py --node 2
python3 node.py --node 3
```