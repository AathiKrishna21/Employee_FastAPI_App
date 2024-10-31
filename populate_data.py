import pymongo
import json

# Connecting to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["employees"]
collection = db["employees"]

# Read employees from sample.json
with open("sample.json", "r") as f:
    employees = json.load(f)

# Create index for efficient retrieval
collection.create_index("id")

# # add rating field to each employee
# for employee in employees:
#     employee['rating'] = {'total': 0, 'count': 0}

# # add rating field to each chapter
# for employee in employees:
#     for chapter in employee['chapters']:
#         chapter['rating'] = {'total': 0, 'count': 0}

# Add employees to collection
for employee in employees:
    collection.insert_one(employee)

# Close MongoDB connection
client.close()