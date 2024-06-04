import csv

def generate_csv(file_path, object_ids, lifecycle_state):
    data = [[obj_id, lifecycle_state] for obj_id in object_ids]
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "state__v"])
        writer.writerows(data)