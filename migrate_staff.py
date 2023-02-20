from dotenv import load_dotenv
load_dotenv()

import pymongo
import os 
import json
from tqdm import tqdm

from datetime import datetime

CONNECTION_STR = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(CONNECTION_STR)

db = client.devdb
staff_collection = db.staffs

error_indexes = []
staffs = []
with open("staff.json", "r") as staff_file:
	staffs = json.load(staff_file)

print("Initial array length: ", len(staffs))

upload_array = []
for i in tqdm(range(len(staffs))):
	staff = staffs[i]
	try:
		name = str(staff["first_name"] + " "  + staff["last_name"]).strip()
		
		email = str(staff["email"])

		description =  staff["description"]
		description = "" if not description else description

		slug = staff["slug"]
		created_at = datetime.fromisoformat(staff["created_at"])

		# print(name, email + "|" +  str(description) + "|",  slug)
		

		attempted_found_staff = staff_collection.find_one({"email" : email})

		if attempted_found_staff: # If the staff member already exists in the db, move to next
			continue

		# print(name, email,  slug)

		
		upload_array.append(
			{
				"name" : name,
				"email" : email,
				"description" : description,
				"slug" : slug,
				"created_at" : created_at
			} 
		)
	except Exception as error:
		error_indexes.append(i)

error_json = []
for error_index in error_indexes:
	error_json.append(staffs[error_index])

with open("error.json", "w") as error_file:
	json.dump(error_json, error_file)

print("Upload array length: ", len(upload_array))
staff_collection.insert_many(upload_array)