from dotenv import load_dotenv
load_dotenv()

import os 
import pymongo

CONNECTION_STR = os.getenv("MONGODB_URI")

client = pymongo.MongoClient(CONNECTION_STR)

db = client.devdb
articles_collection = db.articles


articles = list(articles_collection.find({}))

print("Num of articles: ", len(articles))


sub_sections_set = set()


for article in articles:

	article = dict(article)
	sub_section = article.get("sub_section")
	if sub_section != None:
		sub_sections_set.add(sub_section)

		
print(sub_sections_set)
print("Num of sub_sections: " , len(sub_sections_set))

with open("sub_sections.txt", "w") as file:
	for sub_section in sub_sections_set:
		file.write(sub_section + "\n")
