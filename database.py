import sqlite3
import json
import os

def init_db():
    """Initialize the database with crops table"""
    conn = sqlite3.connect("farming.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            division TEXT NOT NULL,
            district TEXT NOT NULL,
            soil TEXT NOT NULL,
            season TEXT NOT NULL,
            crop TEXT NOT NULL,
            plant_time TEXT,
            fertilizer TEXT,
            water TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def load_json_to_db(json_file):
    """Load data from JSON file to database"""
    try:
        # Check if JSON file exists
        if not os.path.exists(json_file):
            print(f"❌ JSON file {json_file} not found!")
            return False
            
        conn = sqlite3.connect("farming.db")
        cursor = conn.cursor()

        # Clear existing data first
        cursor.execute("DELETE FROM crops")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Insert data from JSON
        for item in data:
            cursor.execute("""
                INSERT INTO crops 
                (division, district, soil, season, crop, plant_time, fertilizer, water)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item['division'],
                item['district'], 
                item['soil'],
                item['season'],
                item['crop'],
                item['plant_time'],
                item['fertilizer'],
                item['water']
            ))

        conn.commit()
        conn.close()
        print(f"✅ Successfully loaded {len(data)} records from {json_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error loading JSON to database: {e}")
        return False


def check_database():
    """Check what's in the database"""
    try:
        conn = sqlite3.connect("farming.db")
        cursor = conn.cursor()
        
        # Count total records
        cursor.execute("SELECT COUNT(*) FROM crops")
        count = cursor.fetchone()[0]
        print(f"📊 Total records in database: {count}")
        
        # Show some sample data
        if count > 0:
            cursor.execute("SELECT division, district, soil, season, crop FROM crops LIMIT 5")
            samples = cursor.fetchall()
            print("📋 Sample data:")
            for sample in samples:
                print(f"  {sample}")
        else:
            print("❌ No data found in database!")
            
        conn.close()
        return count
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return 0


if __name__ == "__main__":
    init_db()
    if load_json_to_db("crop_data.json"):
        check_database()
    else:
        print("❌ Failed to load data into database")