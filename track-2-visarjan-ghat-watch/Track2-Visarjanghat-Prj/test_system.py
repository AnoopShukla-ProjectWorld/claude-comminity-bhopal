import urllib.parse
from app import app, db

client = app.test_client()

print("============================================================")
print("[1] DATABASE CONNECTION & DATA INTEGRITY VERIFICATION")
print("============================================================")
readings_df = db.get_readings_dataframe()
ghats = db.get_ghats()
print(f" SQLite Database Path: {db.db_path}")
print(f" Total Readings stored in SQLite: {len(readings_df)}")
print(f" Total Registered Ghats in SQLite: {len(ghats)}")
assert len(readings_df) >= 1524, "Missing historical data"
assert len(ghats) == 7, "Missing ghats"

print("\n" + "============================================================")
print("[2] CORE ROUTES & PAGE CLICKS VERIFICATION")
print("============================================================")
pages = [
    ('/', 'Main Executive Dashboard'),
    ('/brief', 'Forwardable Bilingual Brief (Memo)'),
    ('/traceability', '1,524 Verified Readings Table'),
    ('/api/summary', 'JSON Summary API'),
    ('/api/readings', 'JSON Raw Readings API')
]
for path, desc in pages:
    res = client.get(path)
    assert res.status_code == 200, f"Route {path} failed!"
    print(f" [PASS] {path:<15} ({desc:<35}) -> HTTP 200 ({len(res.data):,} bytes)")

print("\n" + "============================================================")
print("[3] EVERY INDIVIDUAL GHAT DEEP-DIVE PAGE (7/7)")
print("============================================================")
for g in ghats:
    encoded_name = urllib.parse.quote(g['site'])
    url = f"/ghat/{encoded_name}"
    res = client.get(url)
    assert res.status_code == 200, f"Ghat page {url} failed!"
    print(f" [PASS] {g['site']:<38} -> HTTP 200 ({len(res.data):,} bytes)")

print("\n" + "============================================================")
print("[4] DYNAMIC SENSITIVITY SLIDERS (REAL-TIME RE-RANKING)")
print("============================================================")
res = client.get('/api/summary?w_do=70&w_bod=20&w_ph=10')
assert res.status_code == 200
rankings = res.json['rankings']
assert len(rankings) == 7
print(f" [PASS] Dynamic weights (70/20/10) re-ranked {len(rankings)} ghats successfully:")
for r in rankings[:3]:
    print(f"        Rank #{r['rank']}: {r['site']} (Score: {r['base_risk_score']})")

print("\n" + "============================================================")
print("[5] DYNAMIC WRITE & FETCH (INSERT NEW 2026 TEST SAMPLE)")
print("============================================================")
new_sample = {
    'year': 2026,
    'festival': 'Durga',
    'site': 'Shahpura lake ghat',
    'phase': 'pre',
    'parameter': 'Dissolved oxygen',
    'value': '4.85',
    'unit_assumed': 'mg/l'
}
add_res = client.post('/api/add-reading', json=new_sample)
assert add_res.status_code == 200
new_id = add_res.json['reading_id']
print(f" [PASS] Inserted new reading into SQLite database! Generated ID: {new_id}")

# Fetch back directly using fresh SQL query
conn = db.get_connection()
cursor = conn.cursor()
cursor.execute('SELECT * FROM readings WHERE id = ?', (new_id,))
row = dict(cursor.fetchone())
conn.close()

assert float(row['value']) == 4.85
assert row['site'] == 'Shahpura lake ghat'
assert row['year'] == 2026
print(f" [PASS] Fetched back directly from SQLite: ID={row['id']} | Site={row['site']} | Year={row['year']} | Value={row['value']} {row['unit_assumed']}")

print("\n" + "============================================================")
print("[6] BULK DATA IMPORT (MULTI-PARAMETER CSV & SCOPE OVERRIDES)")
print("============================================================")
import io
# Test 1: Long format with scope override from popup
csv_content_long = """phase,parameter,value
pre,Dissolved oxygen,5.8
during,Dissolved oxygen,2.4
during,BOD,14.6
"""
data1 = {
    'file': (io.BytesIO(csv_content_long.encode('utf-8')), 'test_long_2026.csv'),
    'override_site': 'Bairagarh (Sant Hirdaram) kund',
    'override_year': '2026',
    'override_festival': 'Durga'
}
bulk_res1 = client.post('/api/bulk-import', data=data1, content_type='multipart/form-data')
assert bulk_res1.status_code == 200, f"Bulk import long failed: {bulk_res1.data}"
assert bulk_res1.json['inserted_count'] == 3
print(f" [PASS] Long format with popup overrides imported {bulk_res1.json['inserted_count']} readings.")

# Test 2: Wide format (All parameters in single row)
csv_content_wide = """phase,dissolved_oxygen,bod,ph
pre,6.2,2.8,7.4
during,3.1,12.0,8.2
"""
data2 = {
    'file': (io.BytesIO(csv_content_wide.encode('utf-8')), 'test_wide_matrix.csv'),
    'override_site': 'Prempura ghat',
    'override_year': '2026',
    'override_festival': 'Durga'
}
bulk_res2 = client.post('/api/bulk-import', data=data2, content_type='multipart/form-data')
assert bulk_res2.status_code == 200, f"Bulk import wide failed: {bulk_res2.data}"
assert bulk_res2.json['inserted_count'] == 6 # 3 parameters * 2 rows = 6 readings
print(f" [PASS] Wide matrix format (all parameters in one file) imported {bulk_res2.json['inserted_count']} readings and auto-recalculated!")

print("\n" + "============================================================")
print("[7] NEW GHAT / KUND REGISTRATION & INSTANT ONBOARDING")
print("============================================================")
new_ghat_payload = {
    'site': 'Kolar Dam Dedicated Kund (Test)',
    'water_body': 'Kolar Reservoir',
    'type': 'Dedicated Artificial Kund',
    'lat': 23.2100,
    'lon': 77.4100
}
ghat_res = client.post('/api/add-ghat', json=new_ghat_payload)
assert ghat_res.status_code == 200
print(f" [PASS] Registered new ghat: '{ghat_res.json['site']}'")

# Recalculate
recalc_res = client.post('/api/recalculate')
assert recalc_res.status_code == 200
assert recalc_res.json['total_ghats'] == 8
print(f" [PASS] Instant Recalculate updated total ghats from 7 to 8!")

# Cleanup test records and test ghat
conn = db.get_connection()
c = conn.cursor()
c.execute("DELETE FROM readings WHERE site = 'Kolar Dam Dedicated Kund (Test)' OR id >= ?", (new_id,))
c.execute("DELETE FROM ghats WHERE site = 'Kolar Dam Dedicated Kund (Test)'")
conn.commit()
conn.close()
print(" [PASS] Cleaned up temporary test records cleanly.")

print("\n" + "============================================================")
print("[SUCCESS] ALL AUDIT CHECKS PASSED: 100% OPERATIONAL AND CONNECTED!")
print("============================================================")
