import psycopg2
import json
 
 
with open('test_result21.json', 'r') as json_file:
    data = json.load(json_file)
 
 
conn = psycopg2.connect(
    host="localhost",
    database="test",
    user="postgres",
    password="123456"
)
 
cur = conn.cursor()
 
# la table Suite
for test in data['tests']:
    suite_name = test['suite_name']
    start_time = test['start']
    end_time = test['finish']
 
    cur.execute("""
        INSERT INTO Suite (suite_name, start_time, end_time)
        VALUES (%s, %s, %s)
    """, (suite_name, start_time, end_time))
 
    #la table TestStatistics
    test_name = test['test_name']
    status = test['status']
    comment = test['comment']
    test_key = test.get('testKey', '')  
    testeur = test.get('testeur', '')
    environment= test.get('environment', '')
    cur.execute("""
        INSERT INTO TestStatistics (suite_id, test_name, status, start_time, end_time, comment, tags, testeur, environment)
        VALUES (currval(pg_get_serial_sequence('Suite', 'id')), %s, %s, %s, %s, %s, %s, %s, %s)
    """, (test_name, status, start_time, end_time, comment, test_key, testeur, environment))  
 
#  la table Total
total_tests = data['total_tests']
total_passed = data['total_passed']
total_failed = data['total_failed']
total_skipped = data['total_skipped']
 
cur.execute("""
    INSERT INTO Total (total_tests, total_passed, total_failed, total_skipped)
    VALUES (%s, %s, %s, %s)
""", (total_tests, total_passed, total_failed, total_skipped))
 
 
conn.commit()
cur.close()
conn.close()