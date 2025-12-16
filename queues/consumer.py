import csv
import time
import os
from db import get_conn, init_db

POLL_SECONDS = 5
WORK_SECONDS = 30

def claim_one_task(conn, consumer_id: str):
    conn.execute("BEGIN IMMEDIATE;")

    row = conn.execute("""
        SELECT id
        FROM tasks
        WHERE status = 'pending'
        ORDER BY id
        LIMIT 1;
    """).fetchone()

    if row is None:
        conn.execute("COMMIT;")
        return None

    task_id = row["id"]
    updated = conn.execute("""
        UPDATE tasks
        SET status = 'in_progress',
            started_at = datetime('now'),
            consumer_id = ?
        WHERE id = ?
          AND status = 'pending';
    """, (consumer_id, task_id)).rowcount

    conn.execute("COMMIT;")

    if updated == 0:
        return None

    return task_id

def mark_done(conn, task_id: int):
    conn.execute("""
        UPDATE tasks
        SET status = 'done',
            finished_at = datetime('now')
        WHERE id = ?;
    """, (task_id,))

def consumer_loop(consumer_id: str):
    conn = get_conn()
    print(f"[{consumer_id}] started")

    while True:
        try:
            task_id = claim_one_task(conn, consumer_id)
            if task_id is None:
                time.sleep(POLL_SECONDS)
                continue

            print(f"[{consumer_id}] claimed task {task_id} -> working {WORK_SECONDS}s")
            time.sleep(WORK_SECONDS)
            mark_done(conn, task_id)
            print(f"[{consumer_id}] done task {task_id}")

        except Exception as e:
            print(f"[{consumer_id}] ERROR:", e)
            time.sleep(POLL_SECONDS)

def update_task_status(task_id, new_status):
    tasks = []
    with open('tasks.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        tasks = list(reader)

    for row in tasks:
        if row[0] == str(task_id):
            row[1] = new_status

    with open('tasks.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(tasks)


def consume_task():
    print("Zadanie w trakcie wykonywania... 30 sekund...")
    time.sleep(30)


def consumer():
    while True:
        with open('tasks.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            tasks = list(reader)

        # Szukaj zadania z statusem 'pending'
        for row in tasks:
            if row[1] == 'pending':
                task_id = row[0]
                print(f"Zadanie {task_id} znalezione. Zmieniam status na 'in_progress'.")
                update_task_status(task_id, 'in_progress')
                consume_task()
                print(f"Zadanie {task_id} wykonane. Zmieniam status na 'done'.")
                update_task_status(task_id, 'done')
                break
        time.sleep(5)


if __name__ == "__main__":
    init_db()
    consumer_id = os.environ.get("CONSUMER_ID", f"consumer-{os.getpid()}")
    consumer_loop(consumer_id)
