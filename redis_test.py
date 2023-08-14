import redis
import os

# Connect to Redis
redis_client = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), decode_responses=True)

# Check for connection errors
try:
    redis_client.ping()
except redis.ConnectionError:
    print("Error connecting to Redis")

# Set a string key-value pair
redis_client.set("string key", "string val")

# Set hash values
redis_client.hset("hash key", "hashtest 1", "some value")
redis_client.hset("hash key", "hashtest 2", "some other value")

# Get all keys from the hash
hash_keys = redis_client.hkeys("hash key")
print(f"{len(hash_keys)} replies:")
for i, key in enumerate(hash_keys):
    print(f"    {i}: {key}")

# Close the connection
redis_client.close()
