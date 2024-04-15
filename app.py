import streamlit as st

def create_task(task_id, task, assigned_to, priority):
    st.write(f"Created task: {task_id}, {task}, {assigned_to}, {priority}")

def update_task(task_id, task, assigned_to, priority):
    st.write(f"Updated task: {task_id}, {task}, {assigned_to}, {priority}")

def delete_task(task_id):
    st.write(f"Deleted task: {task_id}")

def main():
    st.title("Task Manager")

    # Task input form
    task_id = st.text_input("Task ID")
    task = st.text_input("Task")
    assigned_to = st.text_input("Assigned To")
    priority = st.text_input("Priority")

    # CRUD operations
    if st.button("Create Task"):
        create_task(task_id, task, assigned_to, priority)
    if st.button("Update Task"):
        update_task(task_id, task, assigned_to, priority)
    if st.button("Delete Task"):
        delete_task(task_id)

if __name__ == "__main__":
    main()
