import sqlite3

# Connect to the source database (love_lihkg_media.db)
source_conn = sqlite3.connect('work_lihkg_media.db')
source_cursor = source_conn.cursor()

# Connect to the target database (news_lihkg_media.db)
target_conn = sqlite3.connect('news_lihkg_media.db')
target_cursor = target_conn.cursor()

# Query the data from the source database
source_cursor.execute("SELECT thread_id, url FROM media")  # Replace media with the actual table name in love_lihkg_media.db
rows = source_cursor.fetchall()

# Prepare the insert query for the target database
insert_query = "INSERT INTO media (thread_id, url) VALUES (?, ?)"  # Adjust the table name if needed

# Insert each row into the target database
for row in rows:
    target_cursor.execute(insert_query, row)

# Commit the changes to the target database
target_conn.commit()

# Close the connections
source_conn.close()
target_conn.close()

print("Data transferred successfully!")
