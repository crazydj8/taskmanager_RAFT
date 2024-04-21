import streamlit as st
import requests
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

def forward_to_flask(url, data):
    response = requests.post(url, json=data)
    st.write(f"Response from Flask: {response.text}")

def read_from_database(id):
    port = f'3306{id}'
    engine = create_engine(f'mysql://root:mysql@127.0.0.1:{port}/taskmanager')
    df = pd.read_sql('SELECT * FROM tasks', engine)
    st.dataframe(df)

def main():
    st.title("Task Manager")

    operation = st.radio('Select operation:', ['Read', 'Insert', 'Update', 'Delete'])

    if operation == 'Read':
        server = st.radio('Select MySQL Server:', [1, 2, 3])
        if st.button("Show Tasks"):
            read_from_database(server)

    elif operation == 'Insert':
        task = st.text_input("Task")
        assigned_to = st.text_input("Assigned To")
        priority = st.text_input("Priority")
        status = st.text_input("Status")
        if st.button("Create Task"):
            forward_to_flask(f'http://localhost:5000/create_task', {'task': task, 'assigned_to': assigned_to, 'priority': priority, 'status': status})

    elif operation == 'Update':
        task_id = st.text_input("Task ID")
        field = st.selectbox("Select field to update", ['task', 'assigned_to', 'status', 'priority'])
        new_value = st.text_input(f"New value for {field}")
        if st.button("Update Task"):
            forward_to_flask(f'http://localhost:5000/update_task', {'task_id': task_id, 'field': field, 'new_value': new_value})

    elif operation == 'Delete':
        task_id = st.text_input("Task ID")
        if st.button("Delete Task"):
            forward_to_flask(f'http://localhost:5000/delete_task', {'task_id': task_id})

if __name__ == "__main__":
    main()