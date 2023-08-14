import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv

if os.environ.get("GITHUB_ACTIONS") is None:
    load_dotenv()

PORT = os.environ.get("MONGODB_PORT")
HOST = os.environ.get("MONGODB_HOST")
MONGO_URI = None

print("GITHUB_ACTIONS VALUE: ")
print(os.environ.get("GITHUB_ACTIONS"))

if os.environ.get("GITHUB_ACTIONS") is None:
    MONGO_URI = f"mongodb://{HOST}:{PORT}/ghActionsTest"
else:
    MONGO_URI = f"mongodb://root:example@{HOST}:{PORT}/admin"

# Generating the client
print("\033[32m# Generating the client...\033[0m")  # Cyan comment
time.sleep(1)
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["ghActionsTest"]
collection = db.exampleCollection
document = {"someKey": "someVal"}

insert_result = None

try:
    # Insert the document
    print("\033[36m# Inserting the document...\033[0m")  # Cyan comment
    time.sleep(1)
    insert_result = collection.insert_one(document)

    # Find and print the inserted document
    print(
        "\033[36m# Finding and printing the inserted document...\033[0m"
    )  # Cyan comment
    time.sleep(1)
    result = collection.find_one({"_id": insert_result.inserted_id})
    print(result)
    time.sleep(1)
except Exception as e:
    print(f"Error: {e}")
finally:
    # Delete the inserted document
    print("\033[36m# Deleting the inserted document...\033[0m")  # Cyan comment
    time.sleep(1)
    collection.delete_one({"_id": insert_result.inserted_id})
    print("Item deleted successfully.")
    time.sleep(1)

    # Closing the client
    print("\033[31m# Closing the client...\033[0m")  # Red comment
    time.sleep(1)
    client.close()
