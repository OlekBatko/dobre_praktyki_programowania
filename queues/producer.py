import csv

def generate_task(task_id):
    """Generuje nową pracę do wykonania w formacie: id, status."""
    return [task_id, 'pending']

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
    producer()
