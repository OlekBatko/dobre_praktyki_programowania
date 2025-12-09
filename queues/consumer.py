import csv
import time


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
    consumer()
