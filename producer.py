import redis
import json
import time
import random
from datetime import datetime
from faker import Faker

fake = Faker()

# Paste your Upstash Redis connection details here
import redis

r = redis.Redis.from_url("rediss://default:gQAAAAAAAfllAAIgcDIwZGY2MWZjMjk5MTM0OGZiYjBjYTc3OTJkZjMwMjllNg@tight-sculpin-129381.upstash.io:6379")

r.set('foo', 'bar')
value = r.get('foo')

STREAM_NAME = 'fraud_transactions'

print("Starting Real-Time Transaction Generator... Press Ctrl+C to stop.")

try:
    while True:
        card_id = f"card_{random.randint(1000, 1050)}"
        amount = round(random.uniform(5.0, 150.0), 2)
        location = fake.city()
        
        # Inject a simulated fraudulent transaction ~5% of the time
        if random.random() < 0.05:
            amount = round(random.uniform(5000.0, 10000.0), 2)  # High amount anomaly
        
        # Create payload
        payload = {
            "transaction_id": fake.uuid4(),
            "card_id": card_id,
            "amount": str(amount),  # Redis streams store field-value pairs as strings
            "location": location,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # XADD appends the data to the Redis Stream
        # '*' tells Redis to automatically generate a unique time-based ID for the message
        message_id = r.xadd(STREAM_NAME, payload, id='*')
        
        print(f"Sent Transaction {payload['transaction_id']} to Stream. Message ID: {message_id}")
        
        # Throttle the loop to simulate realistic human transaction pacing
        time.sleep(random.uniform(0.5, 2.0))

except KeyboardInterrupt:
    print("\nGenerator stopped by user.")