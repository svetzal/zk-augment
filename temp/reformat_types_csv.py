import csv


def csv_to_plain_text(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            print(f'"{row[0]}": "{row[1]}"')


file_path = 'types.csv'  # Replace with your actual file path
csv_to_plain_text(file_path)
