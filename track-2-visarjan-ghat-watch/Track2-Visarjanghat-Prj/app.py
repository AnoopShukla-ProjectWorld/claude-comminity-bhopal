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
