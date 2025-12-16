import csv
from db import get_conn, init_db

def generate_task(task_id):
    """Generuje nową pracę do wykonania w formacie: id, status."""
    return [task_id, 'pending']

def add_task():
    conn = get_conn()
    conn.execute("INSERT INTO tasks(status) VALUES ('pending');")
    conn.close()

def add_many(n: int):
    conn = get_conn()
    conn.execute("BEGIN;")
    for _ in range(n):
        conn.execute("INSERT INTO tasks(status) VALUES ('pending');")
    conn.execute("COMMIT;")
    conn.close()

def producer():
    filename = 'tasks.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['task_id', 'status'])

        for task_id in range(1, 3):
            task = generate_task(task_id)
            writer.writerow(task)
            print(f"Zadanie {task_id} zapisane jako 'pending'.")

if __name__ == "__main__":
    init_db()
    producer()
    add_task()
    print("Added 1 task (pending).")
