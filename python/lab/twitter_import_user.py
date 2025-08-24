import csv
import os

from rss_send import db_handler

# Set the path to the directory containing the CSV file
directory = r'C:\Users\fueqq\Downloads\twitter'

# Find the first CSV file in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
third_column_values = []
print(len(csv_files))
for csv_file in csv_files:
    file_path = os.path.join(directory, csv_file)

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Skip the header row if it exists
        next(csv_reader, None)

        # Create a list to store all values from the third column

        # Read all values from the third column
        for row in csv_reader:
            if len(row) > 2:
                third_column_values.append(row[2])
db_handle2 = db_handler('twitter_user_name', 'media')

# Print all values from the third column
print("All values from the third column:")
for i, user in enumerate(third_column_values):
    if not db_handle2.thread_id_exists(user):
        if i < len(third_column_values) // 2:
            print("1", user)
            db_handle2.insert_url3(user, '', 1)
        else:
            print("2", user)
            db_handle2.insert_url3(user, '', 2)

# Print the total number of values
print(f"\nTotal number of values: {len(third_column_values)}")

