#!/usr/bin/env python3
# ============================================================
# DevMatch AI - Database Diagnostic Tool
# ============================================================

import sqlite3
import os
from datetime import datetime

def diagnose_database():
    """Comprehensive database diagnostic"""
    
    db_path = 'devmatch.db'
    
    print("🔍 === DATABASE DIAGNOSTIC REPORT === 🔍\n")
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print("❌ Database file 'devmatch.db' not found!")
        return
    
    file_size = os.path.getsize(db_path)
    print(f"📁 Database file: {db_path}")
    print(f"📏 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"🕒 Last modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
    
    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        print(f"\n📊 === TABLE ANALYSIS === 📊")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📋 {table_name}: {count} records")
            
            # Show sample data for key tables
            if table_name in ['projects', 'developers', 'match_results']:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                samples = cursor.fetchall()
                if samples:
                    print(f"    🔸 Sample records:")
                    for i, sample in enumerate(samples, 1):
                        print(f"      {i}: {sample}")
        
        # Specific match_results analysis
        print(f"\n🎯 === MATCH RESULTS ANALYSIS === 🎯")
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_matches,
                AVG(technical_match) as avg_technical,
                MAX(technical_match) as max_technical,
                MIN(technical_match) as min_technical
            FROM match_results
        """)
        
        stats = cursor.fetchone()
        if stats and stats[0] > 0:
            print(f"  📈 Total matches: {stats[0]}")
            print(f"  🎯 Average technical score: {stats[1]:.1f}%")
            print(f"  🏆 Best technical score: {stats[2]:.1f}%")
            print(f"  📉 Lowest technical score: {stats[3]:.1f}%")
            
            # Recent matches
            cursor.execute("""
                SELECT project_id, developer_id, technical_match, created_at 
                FROM match_results 
                ORDER BY created_at DESC 
                LIMIT 3
            """)
            recent = cursor.fetchall()
            print(f"  🕒 Recent matches:")
            for match in recent:
                print(f"    Project {match[0]} - Developer {match[1]}: {match[2]:.1f}% ({match[3]})")
        else:
            print("  ⚠️  No match results found!")
        
        # Check for relationships
        print(f"\n🔗 === RELATIONSHIP CHECK === 🔗")
        
        cursor.execute("""
            SELECT 
                mr.project_id,
                p.name as project_name,
                mr.developer_id, 
                d.name as developer_name,
                mr.technical_match
            FROM match_results mr
            LEFT JOIN projects p ON mr.project_id = p.id
            LEFT JOIN developers d ON mr.developer_id = d.id
            LIMIT 3
        """)
        
        relationships = cursor.fetchall()
        for rel in relationships:
            print(f"  🔸 {rel[3]} → {rel[1]}: {rel[4]:.1f}%")
        
        conn.close()
        
        print(f"\n✅ Database appears to be healthy and contains data!")
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

if __name__ == "__main__":
    diagnose_database()