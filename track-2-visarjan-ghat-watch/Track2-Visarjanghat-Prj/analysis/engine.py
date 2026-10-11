"""
Visarjan Ghat Watch - Analysis Engine
Author: Anoop Shukla (Bhopal Impact Lab 2026)
Processes MPPCB water quality data (2023-2025) for 7 Bhopal idol immersion ghats
and computes traceable risk scores against CPCB Class B outdoor bathing criteria.
"""

import os
import pandas as pd
import numpy as np

# CPCB Class B (Outdoor Bathing) Criteria
CPCB_CLASS_B = {
    'Dissolved oxygen': {'limit': 5.0, 'type': 'min', 'unit': 'mg/l'},
    'BOD': {'limit': 3.0, 'type': 'max', 'unit': 'mg/l'},
    'pH': {'min': 6.5, 'max': 8.5, 'type': 'range', 'unit': ''}
}

# Source PDF mapping for page traceability
REPORT_PDF_MAP = {
    2023: 'Idol_immer._Report_23_CPCB.pdf',
    2024: 'Ganesh_and_Durga_visarjan_report-2024.pdf',
    2025: 'Ganesh_and_Durga_visarjan_report-2025.pdf'
}

# Ghat metadata
GHAT_METADATA = {
    'Bairagarh (Sant Hirdaram) kund': {
        'water_body': 'Upper Lake',
        'confidence': 'high',
        'type': 'Temporary Kund (Upper Lake basin)',
        'ngt_status': 'Banned (Upper Lake Basin - NGT Order Feb 2026)',
        'missing_notes': 'No Durga 2025 sampling in MPPCB report. Only "during" phase sampled in Ganesh 2025.'
    },
    'Khatlapura ghat': {
        'water_body': 'Lower Lake',
        'confidence': 'high',
        'type': 'Natural Lake Ghat',
        'ngt_status': 'Banned (Lower Lake - NGT Order Feb 2026)',
        'missing_notes': 'BOD missing during Durga 2023; 4 metals missing during Ganesh 2023.'
    },
    'Prempura ghat': {
        'water_body': 'Upper Lake',
        'confidence': 'high',
        'type': 'Natural Lake Ghat',
        'ngt_status': 'Banned (Upper Lake - NGT Order Feb 2026)',
        'missing_notes': 'BOD missing in all 3 phases & pH missing during Durga 2023.'
    },
    'Rani Kamlapati ghat / Kamla Park kund': {
        'water_body': 'Lower Lake',
        'confidence': 'medium',
        'type': 'Ghat / Kund (Dual naming in MPPCB)',
        'ngt_status': 'Banned (Lower Lake - NGT Order Feb 2026)',
        'missing_notes': 'Report prints "Kamla Park kund" for Ganesh and "Lower Lake ghat" for Durga. Medium site match confidence.'
    },
    'Hathaikheda dam / kund': {
        'water_body': 'Hathaikheda dam',
        'confidence': 'high',
        'type': 'Dam Reservoir / Visarjan Kund',
        'ngt_status': 'Permitted dedicated site',
        'missing_notes': 'Complete sampling across all years.'
    },
    'Malikhedi kund': {
        'water_body': 'Kund',
        'confidence': 'high',
        'type': 'Dedicated Immersion Kund',
        'ngt_status': 'Permitted dedicated site',
        'missing_notes': 'No Durga 2025 sampling in MPPCB report. Only "during" phase sampled in Ganesh 2025.'
    },
    'Shahpura lake ghat': {
        'water_body': 'Shahpura Lake',
        'confidence': 'high',
        'type': 'Urban Lake Ghat',
        'ngt_status': 'Permitted (outside Upper/Lower Lake ban)',
        'missing_notes': 'Complete sampling across all years.'
    }
}

class GhatAnalysisEngine:
    def __init__(self, data_path=None):
        if data_path is None:
            # Check parent track data directory (preserves clean original data)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            candidate1 = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'bhopal_ghats_2023_2025.csv'))
            candidate2 = os.path.abspath(os.path.join(current_dir, '..', 'data', 'bhopal_ghats_2023_2025.csv'))
            if os.path.exists(candidate1):
                data_path = candidate1
            elif os.path.exists(candidate2):
                data_path = candidate2
            else:
                data_path = 'bhopal_ghats_2023_2025.csv'
        self.data_path = data_path
        self.df = None
        self.load_data()

    def load_data(self):
        """Loads and standardizes the Bhopal ghats dataset with traceability metadata."""
        self.df = pd.read_csv(self.data_path, encoding='utf-8')
        
        # Clean flags & values
        self.df['is_bdl'] = self.df['flag'].isin(['BDL', 'ND'])
        self.df['is_missing'] = self.df['flag'].isin(['not sampled', '*', '**']) | (self.df['value'].isna() & ~self.df['is_bdl'])
        
        # Link source report filename
        self.df['report_pdf'] = self.df['year'].map(REPORT_PDF_MAP)
        
        # Determine CPCB Class B compliance
        def check_compliance(row):
            param = row['parameter']
            val = row['value']
            
            if row['is_missing']:
                return 'NOT_SAMPLED'
            if row['is_bdl']:
                return 'SAFE_BDL' # Heavy metals BDL is safe
            if pd.isna(val):
                return 'UNKNOWN'
                
            if param == 'Dissolved oxygen':
                if val == 0:
                    return 'CRITICAL_ZERO'
                elif val < 4.0:
                    return 'FAIL_CLASS_D' # Fails even wildlife/fishery
                elif val < 5.0:
                    return 'FAIL_CLASS_B' # Fails outdoor bathing
                else:
                    return 'PASS'
            elif param == 'BOD':
                if val > 10.0:
                    return 'CRITICAL_BOD'
                elif val > 3.0:
                    return 'FAIL_CLASS_B'
                else:
                    return 'PASS'
            elif param == 'pH':
                if val < 6.5 or val > 8.5:
                    return 'FAIL_CLASS_B'
                else:
                    return 'PASS'
            return 'NO_CRITERIA'

        self.df['cpcb_status'] = self.df.apply(check_compliance, axis=1)

    def get_ghat_summary(self):
        """Generates comprehensive aggregated metrics for each of the 7 ghats."""
        ghats = list(GHAT_METADATA.keys())
        summary = []

        for ghat in ghats:
            gdf = self.df[self.df['site'] == ghat]
            meta = GHAT_METADATA[ghat]

            # DO analysis
            do_vals = gdf[(gdf['parameter'] == 'Dissolved oxygen') & gdf['value'].notna()]['value']
            do_total = len(do_vals)
            do_fails = len(do_vals[do_vals < 5.0])
            do_zeros = len(do_vals[do_vals == 0.0])
            do_min = do_vals.min() if do_total > 0 else None
            do_median = do_vals.median() if do_total > 0 else None

            # BOD analysis
            bod_vals = gdf[(gdf['parameter'] == 'BOD') & gdf['value'].notna()]['value']
            bod_total = len(bod_vals)
            bod_fails = len(bod_vals[bod_vals > 3.0])
            bod_max = bod_vals.max() if bod_total > 0 else None
            bod_median = bod_vals.median() if bod_total > 0 else None

            # pH analysis
            ph_vals = gdf[(gdf['parameter'] == 'pH') & gdf['value'].notna()]['value']
            ph_total = len(ph_vals)
            ph_fails = len(ph_vals[(ph_vals < 6.5) | (ph_vals > 8.5)])
            ph_max = ph_vals.max() if ph_total > 0 else None
            ph_min = ph_vals.min() if ph_total > 0 else None

            # Usable cells count (numeric + BDL) out of 234 total expected
            usable_cells = len(gdf[gdf['value'].notna() | gdf['is_bdl']])
            completeness_pct = round((usable_cells / 234.0) * 100, 1)

            # Recent 2025 Durga condition check
            durga_2025 = gdf[(gdf['year'] == 2025) & (gdf['festival'] == 'Durga')]
            has_durga_2025 = len(durga_2025) > 0
            recent_do = durga_2025[durga_2025['parameter'] == 'Dissolved oxygen']['value'].tolist()
            recent_bod = durga_2025[durga_2025['parameter'] == 'BOD']['value'].tolist()

            # Pre-to-After immersion spike (Ganesh + Durga)
            # Calculate average during/after BOD elevation
            bod_phases = gdf[gdf['parameter'] == 'BOD'].pivot_table(index=['year', 'festival'], columns='phase', values='value')
            bod_spike = None
            if 'during' in bod_phases.columns and 'pre' in bod_phases.columns:
                delta = bod_phases['during'] - bod_phases['pre']
                bod_spike = delta.mean()

            # -----------------
            # RISK SCORE FORMULA
            # Transparent and defensible:
            # 1. DO severity (50% weight): DO < 5 shortfall, zero DO heavily penalized
            # 2. BOD severity (40% weight): BOD > 3 excess
            # 3. pH severity (10% weight): pH outside 6.5-8.5
            # + Recency multiplier for Durga 2025 conditions
            # -----------------
            do_severity = 0.0
            if do_total > 0:
                shortfalls = [max(0.0, (5.0 - v) / 5.0) for v in do_vals]
                do_severity = (sum(shortfalls) / do_total) * 100
                # Extra penalty for anoxic water (DO = 0)
                do_severity += (do_zeros * 12.5)

            bod_severity = 0.0
            if bod_total > 0:
                excesses = [min(3.0, max(0.0, (v - 3.0) / 3.0)) / 3.0 for v in bod_vals]
                bod_severity = (sum(excesses) / bod_total) * 100

            ph_severity = 0.0
            if ph_total > 0:
                ph_severity = (ph_fails / ph_total) * 100

            # Composite base score (0 to 100 scale)
            base_risk = (0.50 * do_severity) + (0.40 * bod_severity) + (0.10 * ph_severity)

            # Recency & festival weight
            durga_score = base_risk
            durga_df = gdf[gdf['festival'] == 'Durga']
            if len(durga_df) > 0:
                d_do = durga_df[(durga_df['parameter'] == 'Dissolved oxygen') & durga_df['value'].notna()]['value']
                d_bod = durga_df[(durga_df['parameter'] == 'BOD') & durga_df['value'].notna()]['value']
                d_do_zeros = len(d_do[d_do == 0.0])
                d_do_sev = (sum([max(0.0, (5.0 - v)/5.0) for v in d_do]) / len(d_do) * 100) + (d_do_zeros * 15) if len(d_do) > 0 else 0
                d_bod_sev = (sum([min(3.0, max(0.0, (v - 3.0)/3.0))/3.0 for v in d_bod]) / len(d_bod) * 100) if len(d_bod) > 0 else 0
                durga_score = (0.55 * d_do_sev) + (0.45 * d_bod_sev)

            # Plain language reasons (English & Hindi)
            reason_en, reason_hi = self._generate_reasons(
                ghat, do_zeros, do_fails, do_total, bod_fails, bod_total, 
                do_min, bod_max, has_durga_2025, recent_do, recent_bod
            )

            # Actionable engineering recommendations
            recommendations_en, recommendations_hi = self._generate_recommendations(
                ghat, base_risk, do_zeros, do_min, bod_max, has_durga_2025, meta['ngt_status']
            )

            # Classification
            if base_risk >= 35.0 or do_zeros > 0:
                risk_level = 'CRITICAL'
                risk_badge = '🔴 अति संवेदनशील (Critical)'
                badge_color = 'rose'
            elif base_risk >= 22.0 or (do_min and do_min < 3.0):
                risk_level = 'HIGH'
                risk_badge = '🟠 उच्च जोखिम (High)'
                badge_color = 'orange'
            elif base_risk >= 14.0:
                risk_level = 'MODERATE'
                risk_badge = '🟡 मध्यम जोखिम (Moderate)'
                badge_color = 'amber'
            else:
                risk_level = 'LOW'
                risk_badge = '🟢 नियंत्रित (Low / Cleanest)'
                badge_color = 'emerald'

            summary.append({
                'site': ghat,
                'water_body': meta['water_body'],
                'type': meta['type'],
                'confidence': meta['confidence'],
                'ngt_status': meta['ngt_status'],
                'missing_notes': meta['missing_notes'],
                'has_durga_2025': has_durga_2025,
                'completeness_pct': completeness_pct,
                'usable_cells': usable_cells,
                'do_fails': f"{do_fails}/{do_total}",
                'do_fail_pct': round((do_fails/do_total)*100, 1) if do_total else 0,
                'do_zeros': do_zeros,
                'do_min': do_min,
                'do_median': do_median,
                'bod_fails': f"{bod_fails}/{bod_total}",
                'bod_fail_pct': round((bod_fails/bod_total)*100, 1) if bod_total else 0,
                'bod_max': bod_max,
                'bod_median': bod_median,
                'ph_fails': f"{ph_fails}/{ph_total}",
                'ph_range': f"{ph_min:.2f} - {ph_max:.2f}" if ph_min else "N/A",
                'base_risk_score': round(base_risk, 1),
                'durga_risk_score': round(durga_score, 1),
                'risk_level': risk_level,
                'risk_badge': risk_badge,
                'badge_color': badge_color,
                'reason_en': reason_en,
                'reason_hi': reason_hi,
                'recommendations_en': recommendations_en,
                'recommendations_hi': recommendations_hi
            })

        # Rank ghats by composite risk score descending
        summary.sort(key=lambda x: x['base_risk_score'], reverse=True)
        for i, item in enumerate(summary, 1):
            item['rank'] = i

        return summary

    def _generate_reasons(self, ghat, do_zeros, do_fails, do_total, bod_fails, bod_total, do_min, bod_max, has_durga_2025, recent_do, recent_bod):
        if 'Bairagarh' in ghat:
            en = "Dissolved Oxygen dropped to 0.0 mg/l four times (anoxic dead water). 100% of BOD tests exceed bathing limit. Highly mineralized stagnant kund with zero Durga 2025 data."
            hi = "घुलित ऑक्सीजन (DO) 4 बार शून्य (0.0 mg/l) दर्ज हुई (जलीय जीवन असंभव)। 100% नमूनों में BOD सीमा पार। दुर्गा 2025 का कोई परीक्षण उपलब्ध नहीं।"
        elif 'Shahpura' in ghat:
            en = f"BOD exceeded bathing limit in 100% ({bod_fails}/{bod_total}) of readings. In Durga 2025, DO fell to a critical 2.5 mg/l with during-immersion BOD jumping to 11.4 mg/l."
            hi = f"सभी 18 नमूनों (100%) में BOD मानक से अधिक। दुर्गा 2025 में ऑक्सीजन गिरकर 2.5 mg/l रह गई तथा विसर्जन दौरान BOD 11.4 mg/l तक पहुँच गई।"
        elif 'Malikhedi' in ghat:
            en = "Critical post-immersion surge (Ganesh 2023: BOD jumped from 1.6 to 16.8 mg/l; COD 10 to 127.4 mg/l). DO read 0.6 mg/l in 2025. Missing Durga 2025 test."
            hi = "विसर्जन के बाद सर्वाधिक जल प्रदूषण वृद्धि (BOD 1.6 से 16.8 mg/l, COD 10 से 127.4 mg/l तक उछला)। 2025 में DO मात्र 0.6 mg/l दर्ज। दुर्गा 2025 डेटा अनुपलब्ध।"
        elif 'Rani Kamlapati' in ghat:
            en = f"100% of BOD tests violate limit (median 5.9 mg/l). In Durga 2025, DO remained severely depressed at ~2.5 mg/l across all 3 phases (pre/during/after)."
            hi = "सभी नमूनों में BOD सीमा से अधिक (औसत 5.9 mg/l)। दुर्गा 2025 में तीनों चरणों में ऑक्सीजन ~2.5 mg/l के खतरनाक स्तर पर रही। निचली झील पूरे साल प्रदूषित।"
        elif 'Hathaikheda' in ghat:
            en = f"Never failed DO (super-saturated by algae), but recorded the highest BOD (22.0 mg/l), COD (177.8 mg/l) and turbidity (193.5 NTU) in the entire dataset after Ganesh 2024. Alkaline pH up to 8.92."
            hi = "ऑक्सीजन सामान्य रही किंतु पूरे भोपाल में सर्वाधिक BOD (22.0 mg/l), COD (177.8 mg/l) व मैलापन (193.5 NTU) दर्ज हुआ। क्षारीय pH 8.92 तक पहुँचा।"
        elif 'Khatlapura' in ghat:
            en = f"Failed DO in {do_fails}/{do_total} readings. Lower Lake baseline is chronically polluted. Ganesh 2024 showed an acute heavy-metal and conductivity spike during immersion."
            hi = f"कुल {do_total} में से {do_fails} नमूनों में ऑक्सीजन 5 से कम। निचली झील का बेसलाइन पानी पहले से दूषित। गणेश 2024 विसर्जन दौरान धातुओं व लवणता का भारी उछाल।"
        elif 'Prempura' in ghat:
            en = "Consistently the cleanest among all 7 ghats. Lowest conductivity (200-400 µS/cm) and lowest median BOD (3.2 mg/l), though still occasionally exceeds bathing limit."
            hi = "सभी 7 घाटों में सबसे स्वच्छ स्थिति। सबसे कम लवणता (200-400 µS/cm) तथा न्यूनतम औसत BOD (3.2 mg/l)। फिर भी विसर्जन दौरान सतर्कता आवश्यक।"
        else:
            en = f"DO failed in {do_fails}/{do_total} readings. BOD failed in {bod_fails}/{bod_total} readings."
            hi = f"DO {do_fails}/{do_total} में विफल, BOD {bod_fails}/{bod_total} में विफल।"
        return en, hi

    def _generate_recommendations(self, ghat, score, zeros, do_min, bod_max, has_durga_2025, ngt_status):
        rec_en = []
        rec_hi = []

        if 'Banned' in ngt_status:
            rec_en.append("NGT BAN COMPLIANCE: Direct lake immersion strictly prohibited. Ensure barricading and redirect public to artificial containment kunds.")
            rec_hi.append("एनजीटी प्रतिबंध: प्राकृतिक झील में विसर्जन पूरी तरह वर्जित। बैरिकेडिंग करें व जनता को कृत्रिम कुंडों की ओर निर्देशित करें।")

        if zeros > 0 or (do_min and do_min < 3.0):
            rec_en.append("EMERGENCY AERATION: Install mechanical splash aerators / fountains 48 hours before visarjan to prevent water asphyxiation.")
            rec_hi.append("आपातकालीन वातन (Aeration): विसर्जन से 48 घंटे पूर्व स्प्लैश एरेटर/फव्वारे लगाएं ताकि ऑक्सीजन शून्य न हो।")

        if not has_durga_2025:
            rec_en.append("MANDATORY TEST PROTOCOL: Historical Durga 2025 data was absent. MPPCB must deploy pre-visarjan sampling 72h prior to Oct 20.")
            rec_hi.append("अनिवार्य नमूना जांच: 2025 का दुर्गा डेटा गायब था। 20 अक्टूबर से 72 घंटे पूर्व अनिवार्य पूर्व-परीक्षण करें।")

        if bod_max and bod_max > 10.0:
            rec_en.append("RAPID CLEANING: High organic sludge risk. Mandate idol frame retrieval & silt scooping within 24 hours post-visarjan.")
            rec_hi.append("त्वरित सफाई: अत्यधिक जैविक कचरा जोखिम। विसर्जन के 24 घंटे के भीतर मूर्तियों के ढांचे व सिल्ट बाहर निकालना अनिवार्य करें।")

        if not rec_en:
            rec_en.append("Standard monitoring: Maintain regular nirmalya collection nets and routine testing.")
            rec_hi.append("मानक निगरानी: नियमित निर्माल्य संग्रहण जाल और सामान्य परीक्षण बनाए रखें।")

        return rec_en, rec_hi

    def get_ghat_readings(self, ghat_name):
        """Returns all 234 expected cells and readings for a given ghat with full traceability."""
        gdf = self.df[self.df['site'] == ghat_name].copy()
        gdf = gdf.sort_values(by=['year', 'festival', 'phase', 'parameter'])
        return gdf.to_dict(orient='records')

    def get_immersion_impact_deltas(self):
        """Calculates paired pre vs during vs after median changes across all Bhopal ghats."""
        params = ['Dissolved oxygen', 'BOD', 'COD', 'Turbidity', 'Conductivity', 'Suspended solids', 'Total solids']
        deltas = []

        for p in params:
            sub = self.df[(self.df['parameter'] == p) & self.df['value'].notna()]
            piv = sub.pivot_table(index=['year', 'festival', 'site'], columns='phase', values='value')
            
            d_during_pre = None
            d_after_pre = None
            pct_after_higher = None

            if 'during' in piv.columns and 'pre' in piv.columns:
                diff_during = piv['during'] - piv['pre']
                d_during_pre = diff_during.median()

            if 'after' in piv.columns and 'pre' in piv.columns:
                diff_after = piv['after'] - piv['pre']
                d_after_pre = diff_after.median()
                valid_diff = diff_after.dropna()
                if len(valid_diff) > 0:
                    pct_after_higher = round((len(valid_diff[valid_diff > 0]) / len(valid_diff)) * 100, 1)

            unit = sub['unit_assumed'].iloc[0] if len(sub) > 0 else ''
            deltas.append({
                'parameter': p,
                'unit': unit,
                'median_change_during': round(d_during_pre, 2) if d_during_pre is not None else 'N/A',
                'median_change_after': round(d_after_pre, 2) if d_after_pre is not None else 'N/A',
                'pct_after_higher': f"{pct_after_higher}%" if pct_after_higher is not None else 'N/A'
            })

        return deltas

    def get_overall_stats(self):
        """Returns headline stats matching problem statement verification."""
        do_sub = self.df[self.df['parameter'] == 'Dissolved oxygen'].dropna(subset=['value'])
        bod_sub = self.df[self.df['parameter'] == 'BOD'].dropna(subset=['value'])
        ph_sub = self.df[self.df['parameter'] == 'pH'].dropna(subset=['value'])

        do_total = len(do_sub)
        do_fails = len(do_sub[do_sub['value'] < 5.0])
        do_zeros = len(do_sub[do_sub['value'] == 0.0])

        bod_total = len(bod_sub)
        bod_fails = len(bod_sub[bod_sub['value'] > 3.0])

        ph_total = len(ph_sub)
        ph_fails = len(ph_sub[(ph_sub['value'] < 6.5) | (ph_sub['value'] > 8.5)])

        return {
            'total_rows': len(self.df),
            'ghats_count': 7,
            'years': '2023 - 2025',
            'do_total': do_total,
            'do_fails': do_fails,
            'do_fail_pct': round((do_fails / do_total) * 100, 1),
            'do_zeros': do_zeros,
            'bod_total': bod_total,
            'bod_fails': bod_fails,
            'bod_fail_pct': round((bod_fails / bod_total) * 100, 1),
            'ph_total': ph_total,
            'ph_fails': ph_fails,
            'target_event': 'Durga Visarjan · 20 October 2026',
            'days_remaining': 9
        }
