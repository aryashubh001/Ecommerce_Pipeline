import sqlite3
import time
import random
import json
from datetime import datetime
from faker import Faker

# Initialize Faker to create fake names/IPs
fake = Faker()

def init_db():
    """Create the Raw Data table if it doesn't exist."""
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS raw_logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  timestamp TEXT, 
                  event_data TEXT)''')
    conn.commit()
    conn.close()

def generate_log():
    """Generate a single fake user event."""
    # 10% chance to generate "bad" data (to test your cleaning skills later)
    is_bad_data = random.random() < 0.1
    
    event_type = random.choice(['view', 'add_to_cart', 'purchase'])
    
    data = {
        # Simulate missing User ID (Null)
        'user_id': None if is_bad_data else fake.random_int(min=1, max=100),
        
        # Simulate product selection
        'product': random.choice(['Laptop', 'Mouse', 'Monitor', 'HDMI Cable', 'Headphones']),
        
        # Simulate invalid price (Negative) for bad data
        'price': random.choice([-50, 0]) if is_bad_data else random.randint(10, 2000),
        
        'event_type': event_type,
        'ip_address': fake.ipv4(),
        'city': fake.city()
    }
    return json.dumps(data)

if __name__ == "__main__":
    init_db()
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    
    print("🚀 Producer started! Generating logs... (Press Ctrl+C to stop)")
    try:
        while True:
            log_entry = generate_log()
            timestamp = datetime.now().isoformat()
            
            # Insert raw JSON string into database
            c.execute("INSERT INTO raw_logs (timestamp, event_data) VALUES (?, ?)", 
                      (timestamp, log_entry))
            conn.commit()
            
            print(f"Logged: {log_entry}")
            time.sleep(1) # Wait 1 second between logs
    except KeyboardInterrupt:
        print("\n🛑 Producer stopped.")
        conn.close()