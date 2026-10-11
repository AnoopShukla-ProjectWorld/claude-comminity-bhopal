"""
Visarjan Ghat Watch - Web Application
Bhopal Impact Lab 2026 · Track 2
Author: Anoop Shukla
Built for: Bhopal Municipal Corporation (BMC) Planning Officers
"""

import os
from flask import Flask, render_template, request, jsonify
from analysis.engine import GhatAnalysisEngine, GHAT_METADATA

app = Flask(__name__)
engine = GhatAnalysisEngine()

@app.route('/')
def dashboard():
    """Main executive risk dashboard for Durga Visarjan 2026."""
    summary = engine.get_ghat_summary()
    stats = engine.get_overall_stats()
    deltas = engine.get_immersion_impact_deltas()
    return render_template('dashboard.html', summary=summary, stats=stats, deltas=deltas)

@app.route('/brief')
def brief():
    """Forwardable executive brief in official Hindi and English format."""
    summary = engine.get_ghat_summary()
    stats = engine.get_overall_stats()
    return render_template('brief.html', summary=summary, stats=stats)

@app.route('/traceability')
def traceability():
    """Full 1,524 readings table with CPCB status and exact source PDF page citations."""
    selected_ghat = request.args.get('ghat', 'ALL')
    readings = engine.df.to_dict(orient='records')
    ghats_list = list(GHAT_METADATA.keys())
    return render_template('traceability.html', readings=readings, ghats_list=ghats_list, selected_ghat=selected_ghat)

@app.route('/api/summary')
def api_summary():
    """REST API endpoint returning ghat risk rankings and metrics."""
    return jsonify({
        'status': 'success',
        'stats': engine.get_overall_stats(),
        'rankings': engine.get_ghat_summary()
    })

@app.route('/api/readings')
def api_readings():
    """REST API endpoint returning raw readings."""
    ghat = request.args.get('ghat')
    if ghat:
        readings = engine.get_ghat_readings(ghat)
    else:
        readings = engine.df.to_dict(orient='records')
    return jsonify({
        'status': 'success',
        'count': len(readings),
        'data': readings
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"==================================================")
    print(f"🌊 Bhopal Visarjan Ghat Watch 2026 running!")
    print(f"👉 Local URL: http://localhost:{port}")
    print(f"==================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
