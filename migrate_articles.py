from dotenv import load_dotenv
load_dotenv()

import pymongo
import os 
import json
import requests 
from datetime import datetime
from tqdm import tqdm

# New big section order via the old section names
big_section_order = ["news","features","opinions","science","humor","sports","ae","media", "spec-plus"]

CONNECTION_STR = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(CONNECTION_STR)

db = client.devdb
staff_collection = db.staffs

all_staff = list(staff_collection.find({}))
all_staff_slugs = list(map(lambda i : i["slug"], all_staff))

def find_staff_by_slug(slug: str):
	index = all_staff_slugs.index(slug)
	return all_staff[index]

articles_collection = db.articles

error_indexes = []
articles = []
with open("articles.json", "r") as articles_file:
	articles = json.load(articles_file)

print("Initial array length: ", len(articles))

upload_array = []
for i in tqdm(range(len(articles)) ):
	article = articles[i]
	
	try:
		title = article["title"]
		slug = article["slug"]
		text = article["content"]
		volume = article["volume"]
		issue = article["issue"]
		is_published = article["is_published"]	
		section_id = article["section_id"]

		created_at = datetime.fromisoformat(article["created_at"])

		summary = article["summary"]
		
		# jsonstr = '{"operationName":"ArticleQuery","variables":{"slug":"to-all-the-objects-we-ve-loved-before"},"query":"query ArticleQuery($slug: String!) {\n  articleBySlug(slug: $slug) {\n       slug\n       media {\n      id\n      attachment_url\n      medium_attachment_url\n      thumb_attachment_url\n      media_type\n      caption\n      title\n      is_featured\n      user {\n        first_name\n        last_name\n        slug\n        __typename\n      }\n      __typename\n    }\n    created_at\n    contributors {\n      first_name\n      last_name\n      slug\n      __typename\n    }\n    section {\n      id\n      name\n      permalink\n      description\n      parent_section {\n        id\n        name\n        permalink\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}'
		jsonstr = {
		"operationName": "ArticleQuery",
		"variables": {"slug": slug},
		"query": """query ArticleQuery($slug: String!) {
			articleBySlug(slug: $slug) {
				slug
				media {
				id
				attachment_url
				medium_attachment_url
				thumb_attachment_url
				media_type
				caption
				title
				is_featured
				user {
					first_name
					last_name
					slug
					__typename
				}
				__typename
				}
				created_at
				contributors {
				first_name
				last_name
				slug
				__typename
				}
				section {
				id
				name
				permalink
				description
				parent_section {
					id
					name
					permalink
					__typename
				}
				__typename
				}
				__typename
			}
		}
		"""
		}
		r = requests.post("https://api.stuyspec.com/graphql", headers= {"Content-Type": "application/json"}, json=jsonstr)
		j = r.json()["data"]["articleBySlug"]

		contributor_slugs = list(map(lambda j : j['slug'], j['contributors']))
		contributor_ids = list(map(lambda slug : find_staff_by_slug(slug)["_id"], contributor_slugs))
		
		raw_section = str(j["section"]['permalink']).split("/")[1].lower()
		corresponding_section_id = big_section_order.index(raw_section)
		
		to_append = {
				"title" : title,
				"slug" : slug,
				"text" : text,
				"volume" : volume,
				"issue" : issue,
				"is_published" : is_published,
				"section_id" : section_id,
				"created_at" : created_at,
				"summary" : summary,
				"section_id" : corresponding_section_id,
				"contributors" : contributor_ids,
				"created_at" : created_at
		} 

		raw_media = j['media']
		cover_image_url = None
		cover_image_contributor_id = None
		if len(raw_media) > 0:
			cover_image_url = j['media'][0]["attachment_url"]
			cover_image_contributor_id = find_staff_by_slug(j['media'][0]['user']['slug'])['_id'] # Already in mongodb BSON ObjectId format
			to_append["cover_image"] = cover_image_url
			to_append["cover_image_contributor"] = cover_image_contributor_id


		upload_array.append(to_append)

		
	except Exception as error:
		print(error)
		error_indexes.append(i)

print("Error indexes: ", len(error_indexes))

error_json = []
for error_index in error_indexes:
	error_json.append(articles[error_index])

with open("error_articles.json", "w") as error_file:
	json.dump(error_json, error_file)

print("Upload array length: ", len(upload_array))


# with open("successful_articles.json", "w") as s_articles:
# 	json.dump(upload_array, s_articles)
articles_collection.insert_many(upload_array)