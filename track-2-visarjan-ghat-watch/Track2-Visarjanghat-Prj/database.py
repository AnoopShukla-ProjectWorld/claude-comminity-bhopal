"""
Visarjan Ghat Watch - SQLite Database Layer
Author: Anoop Shukla (Bhopal Impact Lab 2026)
Persistent zero-config database managing water quality readings, custom ghats, and dynamic additions.
"""

import os
import sqlite3
import pandas as pd

DB_FILE = 'visarjan_data.db'

# 7 Bhopal Ghats with official metadata and real-world geographic coordinates
DEFAULT_GHATS = [
    {
        'site': 'Bairagarh (Sant Hirdaram) kund',
        'water_body': 'Upper Lake',
        'type': 'Temporary Kund (Upper Lake basin)',
        'ngt_status': 'Banned (Upper Lake Basin - NGT Order Feb 2026)',
        'lat': 23.2842,
        'lon': 77.3385,
        'missing_notes': 'No Durga 2025 sampling in MPPCB report. Only "during" phase sampled in Ganesh 2025.'
    },
    {
        'site': 'Shahpura lake ghat',
        'water_body': 'Shahpura Lake',
        'type': 'Urban Lake Ghat',
        'ngt_status': 'Permitted (outside Upper/Lower Lake ban)',
        'lat': 23.2085,
        'lon': 77.4265,
        'missing_notes': 'Complete sampling across all years.'
    },
    {
        'site': 'Malikhedi kund',
        'water_body': 'Kund',
        'type': 'Dedicated Immersion Kund',
        'ngt_status': 'Permitted dedicated site',
        'lat': 23.2810,
        'lon': 77.4520,
        'missing_notes': 'No Durga 2025 sampling in MPPCB report. Only "during" phase sampled in Ganesh 2025.'
    },
    {
        'site': 'Rani Kamlapati ghat / Kamla Park kund',
        'water_body': 'Lower Lake',
        'type': 'Ghat / Kund (Dual naming in MPPCB)',
        'ngt_status': 'Banned (Lower Lake - NGT Order Feb 2026)',
        'lat': 23.2505,
        'lon': 77.3995,
        'missing_notes': 'Report prints "Kamla Park kund" for Ganesh and "Lower Lake ghat" for Durga. Medium site match confidence.'
    },
    {
        'site': 'Hathaikheda dam / kund',
        'water_body': 'Hathaikheda dam',
        'type': 'Dam Reservoir / Visarjan Kund',
        'ngt_status': 'Permitted dedicated site',
        'lat': 23.2642,
        'lon': 77.4815,
        'missing_notes': 'Complete sampling across all years.'
    },
    {
        'site': 'Khatlapura ghat',
        'water_body': 'Lower Lake',
        'type': 'Natural Lake Ghat',
        'ngt_status': 'Banned (Lower Lake - NGT Order Feb 2026)',
        'lat': 23.2486,
        'lon': 77.4082,
        'missing_notes': 'BOD missing during Durga 2023; 4 metals missing during Ganesh 2023.'
    },
    {
        'site': 'Prempura ghat',
        'water_body': 'Upper Lake',
        'type': 'Natural Lake Ghat',
        'ngt_status': 'Banned (Upper Lake - NGT Order Feb 2026)',
        'lat': 23.2389,
        'lon': 77.3621,
        'missing_notes': 'BOD missing in all 3 phases & pH missing during Durga 2023.'
    }
]

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, DB_FILE)
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes tables and seeds initial 1,524 readings if empty."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Ghats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ghats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT UNIQUE NOT NULL,
                water_body TEXT NOT NULL,
                type TEXT,
                ngt_status TEXT,
                lat REAL,
                lon REAL,
                missing_notes TEXT
            )
        ''')

        # Water readings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                festival TEXT NOT NULL,
                site TEXT NOT NULL,
                water_body TEXT,
                phase TEXT NOT NULL,
                parameter TEXT NOT NULL,
                value REAL,
                unit_assumed TEXT,
                flag TEXT,
                value_as_printed TEXT,
                parameter_as_printed TEXT,
                site_as_printed TEXT,
                site_match_confidence TEXT,
                source_page INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

        # Seed ghats if empty
        cursor.execute('SELECT COUNT(*) FROM ghats')
        if cursor.fetchone()[0] == 0:
            for g in DEFAULT_GHATS:
                cursor.execute('''
                    INSERT INTO ghats (site, water_body, type, ngt_status, lat, lon, missing_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (g['site'], g['water_body'], g['type'], g['ngt_status'], g['lat'], g['lon'], g['missing_notes']))
            conn.commit()

        # Seed readings from CSV if empty
        cursor.execute('SELECT COUNT(*) FROM readings')
        if cursor.fetchone()[0] == 0:
            self._seed_from_csv(conn)

        conn.close()

    def _seed_from_csv(self, conn):
        """Seeds historical 1,524 readings from bhopal_ghats_2023_2025.csv."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_candidates = [
            os.path.abspath(os.path.join(current_dir, '..', 'data', 'bhopal_ghats_2023_2025.csv')),
            os.path.abspath(os.path.join(current_dir, 'data', 'bhopal_ghats_2023_2025.csv')),
            'bhopal_ghats_2023_2025.csv'
        ]
        
        csv_file = None
        for c in csv_candidates:
            if os.path.exists(c):
                csv_file = c
                break

        if csv_file:
            df = pd.read_csv(csv_file, encoding='utf-8')
            records = []
            for _, r in df.iterrows():
                val = float(r['value']) if pd.notna(r['value']) else None
                pg = int(r['source_page']) if pd.notna(r['source_page']) else None
                records.append((
                    int(r['year']),
                    str(r['festival']),
                    str(r['site']),
                    str(r['water_body']) if pd.notna(r['water_body']) else '',
                    str(r['phase']),
                    str(r['parameter']),
                    val,
                    str(r['unit_assumed']) if pd.notna(r['unit_assumed']) else '',
                    str(r['flag']) if pd.notna(r['flag']) else '',
                    str(r['value_as_printed']) if pd.notna(r['value_as_printed']) else '',
                    str(r['parameter_as_printed']) if pd.notna(r['parameter_as_printed']) else '',
                    str(r['site_as_printed']) if pd.notna(r['site_as_printed']) else '',
                    str(r['site_match_confidence']) if pd.notna(r['site_match_confidence']) else 'high',
                    pg
                ))
            
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO readings (
                    year, festival, site, water_body, phase, parameter, value,
                    unit_assumed, flag, value_as_printed, parameter_as_printed,
                    site_as_printed, site_match_confidence, source_page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', records)
            conn.commit()

    def get_readings_dataframe(self):
        """Returns all readings as a pandas DataFrame."""
        conn = self.get_connection()
        df = pd.read_sql_query('SELECT * FROM readings ORDER BY year DESC, festival, site, phase, parameter', conn)
        conn.close()
        return df

    def get_ghats(self):
        """Returns list of all registered ghats."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ghats ORDER BY site')
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def add_reading(self, data):
        """Adds a single reading dynamically."""
        conn = self.get_connection()
        cursor = conn.cursor()

        val = float(data['value']) if data.get('value') not in [None, '', 'BDL', 'ND'] else None
        flag = data.get('flag', '')
        if data.get('value') in ['BDL', 'ND']:
            flag = data.get('value')

        cursor.execute('''
            INSERT INTO readings (
                year, festival, site, water_body, phase, parameter, value,
                unit_assumed, flag, value_as_printed, parameter_as_printed,
                site_as_printed, site_match_confidence, source_page
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(data.get('year', 2026)),
            data.get('festival', 'Durga'),
            data.get('site'),
            data.get('water_body', ''),
            data.get('phase', 'pre'),
            data.get('parameter'),
            val,
            data.get('unit_assumed', 'mg/l'),
            flag,
            str(data.get('value', '')),
            data.get('parameter', ''),
            data.get('site', ''),
            'high',
            int(data.get('source_page', 1))
        ))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    def bulk_add_readings(self, records_list):
        """Adds multiple readings in a single atomic transaction.
        Each item in records_list should be a dictionary with reading fields.
        Returns the number of rows successfully inserted.
        """
        if not records_list:
            return 0
            
        conn = self.get_connection()
        cursor = conn.cursor()
        inserted_count = 0
        try:
            tuples_to_insert = []
            for data in records_list:
                val = float(data['value']) if data.get('value') not in [None, '', 'BDL', 'ND'] else None
                flag = data.get('flag', '')
                if data.get('value') in ['BDL', 'ND']:
                    flag = data.get('value')

                tuples_to_insert.append((
                    int(data.get('year', 2026)),
                    str(data.get('festival', 'Durga')),
                    str(data.get('site')),
                    str(data.get('water_body', '')),
                    str(data.get('phase', 'pre')),
                    str(data.get('parameter')),
                    val,
                    str(data.get('unit_assumed', 'mg/l')),
                    flag,
                    str(data.get('value', '')),
                    str(data.get('parameter', '')),
                    str(data.get('site', '')),
                    'high',
                    int(data.get('source_page', 1))
                ))

            cursor.executemany('''
                INSERT INTO readings (
                    year, festival, site, water_body, phase, parameter, value,
                    unit_assumed, flag, value_as_printed, parameter_as_printed,
                    site_as_printed, site_match_confidence, source_page
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuples_to_insert)
            conn.commit()
            inserted_count = len(tuples_to_insert)
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
            
        conn.close()
        return inserted_count

    def add_ghat(self, data):
        """Registers a new dedicated ghat."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO ghats (site, water_body, type, ngt_status, lat, lon, missing_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['site'],
            data.get('water_body', 'Dedicated Kund'),
            data.get('type', 'New Dedicated Kund (2026)'),
            data.get('ngt_status', 'Permitted dedicated artificial site'),
            float(data.get('lat', 23.25)),
            float(data.get('lon', 77.40)),
            data.get('missing_notes', 'Newly constructed site - mandatory pre/during/after testing protocol.')
        ))
        conn.commit()
        conn.close()
