"""
Visarjan Ghat Watch - Dynamic Web Application (SQLite Backed)
Bhopal Impact Lab 2026 · Track 2
Author: Anoop Shukla
Built for: Bhopal Municipal Corporation (BMC) Planning Officers
"""

import os
import urllib.parse
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
from analysis.engine import GhatAnalysisEngine
from chatbot_assistant import GhatChatbotAssistant

app = Flask(__name__)
db = Database()
engine = GhatAnalysisEngine(db=db)
assistant = GhatChatbotAssistant(engine=engine)

@app.route('/')
def dashboard():
    """Main executive risk dashboard for Durga Visarjan 2026."""
    w_do = float(request.args.get('w_do', 50))
    w_bod = float(request.args.get('w_bod', 40))
    w_ph = float(request.args.get('w_ph', 10))

    summary = engine.get_ghat_summary(w_do, w_bod, w_ph)
    stats = engine.get_overall_stats()
    deltas = engine.get_immersion_impact_deltas()
    statewide = engine.get_statewide_comparison()

    return render_template(
        'dashboard.html',
        summary=summary,
        stats=stats,
        deltas=deltas,
        statewide=statewide,
        w_do=w_do,
        w_bod=w_bod,
        w_ph=w_ph
    )

@app.route('/ghat/<path:site_name>')
def ghat_detail(site_name):
    """Deep-dive individual page for a specific ghat with YoY trends and phase spikes."""
    decoded_site = urllib.parse.unquote(site_name)
    deep_dive = engine.get_ghat_deep_dive(decoded_site)
    if not deep_dive:
        return f"Ghat '{decoded_site}' not found in database", 404

    summary_list = engine.get_ghat_summary()
    ghat_summary = next((g for g in summary_list if g['site'] == decoded_site), summary_list[0])

    return render_template(
        'ghat_detail.html',
        ghat=deep_dive['meta'],
        ghat_summary=ghat_summary,
        deep_dive=deep_dive
    )

@app.route('/brief')
def brief():
    """Forwardable executive brief in official Hindi and English format."""
    summary = engine.get_ghat_summary()
    stats = engine.get_overall_stats()
    return render_template('brief.html', summary=summary, stats=stats)

@app.route('/traceability')
def traceability():
    """Full readings table with CPCB status and exact source PDF page citations."""
    selected_ghat = request.args.get('ghat', 'ALL')
    engine.refresh_data()
    readings = engine.df.to_dict(orient='records')
    ghats_list = [g['site'] for g in db.get_ghats()]
    return render_template(
        'traceability.html',
        readings=readings,
        ghats_list=ghats_list,
        selected_ghat=selected_ghat
    )

@app.route('/api/summary')
def api_summary():
    """REST API endpoint returning ghat risk rankings with dynamic weights."""
    w_do = float(request.args.get('w_do', 50))
    w_bod = float(request.args.get('w_bod', 40))
    w_ph = float(request.args.get('w_ph', 10))

    return jsonify({
        'status': 'success',
        'stats': engine.get_overall_stats(),
        'rankings': engine.get_ghat_summary(w_do, w_bod, w_ph)
    })

@app.route('/api/add-reading', methods=['POST'])
def api_add_reading():
    """Dynamic endpoint to record a new 2026 water testing sample into SQLite."""
    data = request.get_json() if request.is_json else request.form.to_dict()
    if not data or not data.get('site') or not data.get('parameter'):
        return jsonify({'status': 'error', 'message': 'Site and Parameter are required fields'}), 400

    # If it's a new ghat, register it first
    if data.get('site') and not any(g['site'] == data['site'] for g in db.get_ghats()):
        db.add_ghat({
            'site': data['site'],
            'water_body': data.get('water_body', 'Dedicated Kund'),
            'type': 'New Dedicated Kund (2026)',
            'ngt_status': 'Permitted dedicated artificial site'
        })

    new_id = db.add_reading(data)
    engine.refresh_data()

    return jsonify({
        'status': 'success',
        'message': 'Reading successfully saved to database',
        'reading_id': new_id
    })

@app.route('/api/add-ghat', methods=['POST'])
def api_add_ghat():
    """Dynamically register a new ghat / immersion site."""
    data = request.get_json() if request.is_json else request.form.to_dict()
    site = (data.get('site') or '').strip()
    if not site:
        return jsonify({'status': 'error', 'message': 'Ghat site name is required'}), 400

    db.add_ghat({
        'site': site,
        'water_body': data.get('water_body', 'Dedicated Kund'),
        'type': data.get('type', 'Dedicated Immersion Kund'),
        'ngt_status': data.get('ngt_status', 'Permitted dedicated artificial site'),
        'lat': float(data.get('lat', 23.2500)),
        'lon': float(data.get('lon', 77.4000)),
        'missing_notes': data.get('missing_notes', 'Newly registered immersion site for 2026.')
    })
    engine.refresh_data()
    return jsonify({
        'status': 'success',
        'message': f"Ghat '{site}' successfully registered",
        'site': site
    })

@app.route('/api/bulk-import', methods=['POST'])
def api_bulk_import():
    """Bulk import water readings from uploaded CSV or Excel file."""
    import io
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    filename = file.filename.lower()
    try:
        if filename.endswith('.csv'):
            stream = io.StringIO(file.stream.read().decode('utf-8', errors='replace'))
            df_in = pd.read_csv(stream)
        elif filename.endswith(('.xls', '.xlsx')):
            df_in = pd.read_excel(file)
        else:
            return jsonify({'status': 'error', 'message': 'Please upload a CSV or Excel (.xlsx) file'}), 400

        # Normalize column names (lowercase, stripped, underscore)
        df_in.columns = [str(c).strip().lower().replace(' ', '_') for c in df_in.columns]

        # Check required columns
        required_cols = ['site', 'parameter', 'value']
        missing_cols = [c for c in required_cols if c not in df_in.columns]
        if missing_cols:
            return jsonify({
                'status': 'error',
                'message': f"Missing mandatory columns: {', '.join(missing_cols)}. Required: site, parameter, value."
            }), 400

        # Register any new ghats discovered in the file
        existing_ghats = {g['site'] for g in db.get_ghats()}
        unique_sites = df_in['site'].dropna().unique()
        for s in unique_sites:
            s_clean = str(s).strip()
            if s_clean and s_clean not in existing_ghats:
                wb = 'Dedicated Kund'
                if 'water_body' in df_in.columns:
                    wb_vals = df_in[df_in['site'] == s]['water_body'].dropna()
                    if not wb_vals.empty:
                        wb = str(wb_vals.iloc[0])
                db.add_ghat({
                    'site': s_clean,
                    'water_body': wb,
                    'type': 'Imported Immersion Site',
                    'ngt_status': 'Permitted dedicated artificial site'
                })
                existing_ghats.add(s_clean)

        records_to_insert = []
        for _, row in df_in.iterrows():
            site_val = str(row['site']).strip()
            param_val = str(row['parameter']).strip()
            if not site_val or not param_val or pd.isna(row['value']):
                continue

            records_to_insert.append({
                'year': int(row['year']) if 'year' in row and pd.notna(row['year']) else 2026,
                'festival': str(row['festival']).strip() if 'festival' in row and pd.notna(row['festival']) else 'Durga',
                'site': site_val,
                'water_body': str(row.get('water_body', '')).strip() if pd.notna(row.get('water_body')) else '',
                'phase': str(row.get('phase', 'pre')).strip().lower() if pd.notna(row.get('phase')) else 'pre',
                'parameter': param_val,
                'value': row['value'],
                'unit_assumed': str(row.get('unit_assumed', 'mg/l')).strip() if pd.notna(row.get('unit_assumed')) else 'mg/l',
                'flag': str(row.get('flag', '')).strip() if pd.notna(row.get('flag')) else '',
                'source_page': int(row.get('source_page', 1)) if pd.notna(row.get('source_page')) else 1
            })

        if not records_to_insert:
            return jsonify({'status': 'error', 'message': 'No valid water readings found in the file'}), 400

        inserted_count = db.bulk_add_readings(records_to_insert)
        engine.refresh_data()

        return jsonify({
            'status': 'success',
            'message': f"Successfully imported {inserted_count} certified water readings!",
            'inserted_count': inserted_count,
            'total_in_db': len(engine.df)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Import failed: {str(e)}"}), 500

@app.route('/api/recalculate', methods=['POST'])
def api_recalculate():
    """Forces recalculation of all metrics and MCDA scores across the entire dataset."""
    w_do = float(request.args.get('w_do', 50))
    w_bod = float(request.args.get('w_bod', 40))
    w_ph = float(request.args.get('w_ph', 10))

    engine.refresh_data()
    summary = engine.get_ghat_summary(w_do, w_bod, w_ph)
    stats = engine.get_overall_stats()

    return jsonify({
        'status': 'success',
        'message': 'Engine successfully recalculated all metrics and priority rankings',
        'total_readings': stats['total_rows'],
        'total_ghats': len(summary),
        'rankings': summary
    })

@app.route('/download-template')
def download_template():
    """Generates standard CSV template for easy data collection and bulk upload."""
    from flask import Response
    sample_df = pd.DataFrame([
        {
            'year': 2026,
            'festival': 'Durga',
            'site': 'Bairagarh (Sant Hirdaram) kund',
            'water_body': 'Upper Lake',
            'phase': 'pre',
            'parameter': 'Dissolved oxygen',
            'value': 5.4,
            'unit_assumed': 'mg/l',
            'flag': '',
            'source_page': 1
        },
        {
            'year': 2026,
            'festival': 'Durga',
            'site': 'Bairagarh (Sant Hirdaram) kund',
            'water_body': 'Upper Lake',
            'phase': 'during',
            'parameter': 'Dissolved oxygen',
            'value': 3.1,
            'unit_assumed': 'mg/l',
            'flag': '',
            'source_page': 1
        },
        {
            'year': 2026,
            'festival': 'Durga',
            'site': 'Bairagarh (Sant Hirdaram) kund',
            'water_body': 'Upper Lake',
            'phase': 'during',
            'parameter': 'BOD',
            'value': 8.5,
            'unit_assumed': 'mg/l',
            'flag': '',
            'source_page': 1
        },
        {
            'year': 2026,
            'festival': 'Durga',
            'site': 'Shahpura lake ghat',
            'water_body': 'Shahpura Lake',
            'phase': 'pre',
            'parameter': 'pH',
            'value': 7.6,
            'unit_assumed': '',
            'flag': '',
            'source_page': 1
        }
    ])
    csv_str = sample_df.to_csv(index=False, encoding='utf-8')
    return Response(
        csv_str,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=mppcb_visarjan_readings_template_2026.csv"}
    )

@app.route('/api/readings')
def api_readings():
    """REST API endpoint returning raw readings."""
    ghat = request.args.get('ghat')
    engine.refresh_data()
    if ghat:
        readings = engine.df[engine.df['site'] == ghat].to_dict(orient='records')
    else:
        readings = engine.df.to_dict(orient='records')
    return jsonify({
        'status': 'success',
        'count': len(readings),
        'data': readings
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """REST API endpoint for the bilingual Visarjan Ghat AI assistant."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    lang = data.get('lang', 'hi')
    if not message:
        return jsonify({'status': 'error', 'message': 'Message cannot be empty'}), 400

    result = assistant.answer_query(message, lang=lang)
    return jsonify({
        'status': 'success',
        'reply': result['reply'],
        'sources': result['sources']
    })

@app.route('/pdf/<path:filename>')
def serve_pdf(filename):
    """Serves official MPPCB report PDFs for direct browser inspection and page jumps."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    res_candidates = [
        os.path.abspath(os.path.join(current_dir, '..', 'resources')),
        os.path.abspath(os.path.join(current_dir, 'resources'))
    ]
    for r_dir in res_candidates:
        if os.path.exists(os.path.join(r_dir, filename)):
            from flask import send_from_directory
            return send_from_directory(r_dir, filename)
    return f"PDF '{filename}' not found", 404

@app.route('/export-csv')
def export_csv():
    """Generates downloadable CSV report of current ghat risk rankings."""
    from flask import Response
    summary = engine.get_ghat_summary()
    export_df = pd.DataFrame([{
        'Rank': g['rank'],
        'Site': g['site'],
        'Water_Body': g['water_body'],
        'Risk_Score': g['base_risk_score'],
        'Risk_Level': g['risk_level'],
        'DO_Failures': g['do_fails'],
        'BOD_Failures': g['bod_fails'],
        'DO_Min_mg_l': g['do_min'],
        'BOD_Max_mg_l': g['bod_max'],
        'NGT_Status': g['ngt_status'],
        'Plain_Reason': g['reason_en'],
        'Actions_Required': ' | '.join(g['recommendations_en'])
    } for g in summary])
    
    csv_data = export_df.to_csv(index=False, encoding='utf-8')
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=bhopal_visarjan_ghat_risk_ranking_2026.csv"}
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("==================================================")
    print("Bhopal Visarjan Ghat Watch 2026 - Server Ready")
    print(f"Local URL: http://localhost:{port}")
    print("==================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
