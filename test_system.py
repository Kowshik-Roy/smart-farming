import sqlite3
from database import init_db, load_json_to_db, check_database

def test_specific_query():
    """Test a specific query to see if data exists"""
    try:
        conn = sqlite3.connect("farming.db")
        cursor = conn.cursor()
        
        # Test with Dhaka division
        cursor.execute("""
            SELECT division, district, soil, season, crop, plant_time 
            FROM crops 
            WHERE division='ঢাকা' 
            LIMIT 10
        """)
        results = cursor.fetchall()
        
        print("🔍 Testing query for Dhaka division:")
        if results:
            for row in results:
                print(f"  {row}")
        else:
            print("  ❌ No results found for Dhaka division")
            
        # Test count by division
        print("\n📈 Data count by division:")
        cursor.execute("SELECT division, COUNT(*) FROM crops GROUP BY division")
        division_counts = cursor.fetchall()
        for div, count in division_counts:
            print(f"  {div}: {count} records")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    print("🚀 Testing the farming system...")
    
    # Initialize database
    init_db()
    
    # Load data
    if load_json_to_db("crop_data.json"):
        # Check database
        check_database()
        
        # Test specific queries
        test_specific_query()
    else:
        print("❌ Could not load data into database")