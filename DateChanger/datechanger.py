import os
import time
from datetime import datetime, timedelta

# Define the file name
file_name = "thefile.txt"

# Check if the file exists
if not os.path.isfile(file_name):
    raise FileNotFoundError(f"{file_name} does not exist in the current directory.")

# Calculate the timestamp for 3 years ago
three_years_ago = datetime.now() - timedelta(days=3*365)
timestamp = time.mktime(three_years_ago.timetuple())

# Set the file's access and modified times
os.utime(file_name, (timestamp, timestamp))

print(f"Successfully changed last modified time of '{file_name}' to {three_years_ago}.")
