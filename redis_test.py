import os
import time
import redis
from dotenv import load_dotenv

if os.environ.get("GITHUB_ACTIONS") is None:
    load_dotenv()

# Connect to Redis
print("\033[32mOpening a redis client...\033[0m")
redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST"),
    port=int(os.environ.get("REDIS_PORT")),
    decode_responses=True,
)

# Check for connection errors
try:
    redis_client.ping()
except redis.ConnectionError:
    print("Error connecting to Redis")

# Set a string key-value pair
print("Generating the data...")
redis_client.set("string key", "string val")

# Set hash values
redis_client.hset("hash key", "hashtest 1", "some value")
redis_client.hset("hash key", "hashtest 2", "some other value")
time.sleep(1)
print("Data generated...")

time.sleep(1)

print("Printing the data...")

# Get the value of the string key
string_value = redis_client.get("string key")
print(f"\033[94mValue of 'string key': {string_value}\033[0m")

time.sleep(1)

# Get all keys from the hash
hash_keys = redis_client.hkeys("hash key")
print(f"\033[94m{len(hash_keys)} replies for hash keys:\033[0m")
for i, key in enumerate(hash_keys):
    print(f"\033[94m    {i}: {key}\033[0m")

time.sleep(1)

# Delete the data
print("Deleting the data...")
redis_client.delete("string key")
redis_client.delete("hash key")
print("Data deleted...")

# Close the connection
print("\033[31mClosing the client...\033[0m")
redis_client.close()
