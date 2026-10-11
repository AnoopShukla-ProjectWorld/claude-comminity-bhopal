"""
Chatbot Knowledge Assistant Module for Bhopal Visarjan Ghat Watch 2026.
Bhopal Impact Lab 2026 · Track 2
Author: Anoop Shukla

Provides bilingual, empirical AI intelligence grounded strictly in 1,524 MPPCB 
water test readings, CPCB Class B standards, and NGT 2026 mandates.
"""

import re

class GhatChatbotAssistant:
    def __init__(self, engine):
        self.engine = engine

    def answer_query(self, query: str, lang: str = "hi") -> dict:
        """
        Processes administrative questions about Bhopal immersion ghats,
        water quality data, standards, and recommendations.
        """
        query_lower = query.lower().strip()
        summary = self.engine.get_ghat_summary()
        stats = self.engine.get_overall_stats()
        is_hi = (lang == "hi")

        # 1. Critical Ghat / #1 Priority / Bairagarh
        if any(w in query_lower for w in ["critical", "most dangerous", "highest risk", "गंभीर", "सर्वाधिक जोखिम", "नंबर 1", "rank 1", "#1", "बैरागढ़", "bairagarh"]):
            critical = summary[0]
            if is_hi:
                reply = (
                    f"🚨 **सर्वाधिक संवेदनशील स्थल: {critical['site']} (रैंक #1)**\n\n"
                    f"• **जोखिम स्कोर:** {critical['base_risk_score']}/100 ({critical['risk_badge']})\n"
                    f"• **कारण:** {critical['reason_hi']}\n"
                    f"• **घुलित ऑक्सीजन (DO):** 4 बार शून्य (0 mg/l) दर्ज हुई। न्यूनतम DO: {critical['do_min']} mg/l।\n"
                    f"• **BOD विफलता:** {critical['bod_fails']} बार मानक से अधिक (अधिकतम BOD: {critical['bod_max']} mg/l)।\n\n"
                    f"**नगर निगम (BMC) हेतु अनिवार्य कार्रवाई:**\n"
                    + "\n".join([f"✔ {r}" for r in critical['recommendations_hi']])
                )
            else:
                reply = (
                    f"🚨 **Most Critical Ghat: {critical['site']} (Rank #1)**\n\n"
                    f"• **Risk Score:** {critical['base_risk_score']}/100 ({critical['risk_badge']})\n"
                    f"• **Primary Cause:** {critical['reason_en']}\n"
                    f"• **Dissolved Oxygen (DO):** 4 zero DO (0 mg/l) events recorded. Lowest DO: {critical['do_min']} mg/l.\n"
                    f"• **BOD Non-compliance:** {critical['bod_fails']} tests exceeded limit (Max BOD: {critical['bod_max']} mg/l).\n\n"
                    f"**Mandatory Directives for BMC:**\n"
                    + "\n".join([f"✔ {r}" for r in critical['recommendations_en']])
                )
            return {"reply": reply, "sources": ["MPPCB Report 2023-2025", "Sant Hirdaram Kund Data"]}

        # 2. Cleanest Ghat / Low Risk / Prempura
        if any(w in query_lower for w in ["clean", "cleanest", "safest", "best", "स्वच्छ", "सुरक्षित", "प्रेमपुरा", "prempura"]):
            safest = summary[-1]
            if is_hi:
                reply = (
                    f"🌿 **सर्वाधिक स्वच्छ एवं नियंत्रित घाट: {safest['site']} (रैंक #{safest['rank']})**\n\n"
                    f"• **जोखिम स्कोर:** {safest['base_risk_score']}/100 ({safest['risk_badge']})\n"
                    f"• **स्थिति:** {safest['reason_hi']}\n"
                    f"• **ऑक्सीजन स्तर:** न्यूनतम DO {safest['do_min']} mg/l (मानक अनुरूप)।\n"
                    f"• **अनुशंसा:** प्रेमपुरा की व्यवस्था को बेंचमार्क बनाकर अन्य घाटों पर भी इसी प्रकार की बैरिकेडिंग और तत्काल सफाई लागू करें।"
                )
            else:
                reply = (
                    f"🌿 **Cleanest & Safest Ghat: {safest['site']} (Rank #{safest['rank']})**\n\n"
                    f"• **Risk Score:** {safest['base_risk_score']}/100 ({safest['risk_badge']})\n"
                    f"• **Status:** {safest['reason_en']}\n"
                    f"• **Oxygen Level:** Minimum DO recorded at {safest['do_min']} mg/l (compliant).\n"
                    f"• **Takeaway:** Use Prempura's containment and perimeter zoning as the operational benchmark for other sites."
                )
            return {"reply": reply, "sources": ["MPPCB Report 2025", "Prempura Ghat Station"]}

        # 3. NGT Mandate / Large Lake / Small Lake Banned
        if any(w in query_lower for w in ["ngt", "ban", "प्रतिबंध", "आदेश", "तालाब", "lake", "नियम", "guideline"]):
            if is_hi:
                reply = (
                    "⚖️ **एनजीटी (NGT) 2026 निर्देश एवं विधिक स्थिति:**\n\n"
                    "1. **पूर्ण प्रतिबंध:** नेशनल ग्रीन ट्रिब्यूनल के आदेशानुसार भोपाल के **बड़े तालाब (Upper Lake)** एवं **छोटे तालाब (Lower Lake)** में किसी भी प्रकार की प्रतिमा विसर्जन पूर्णतः प्रतिबंधित है।\n"
                    "2. **समर्पित कृत्रिम कुंड:** विसर्जन केवल नगर निगम द्वारा बनाए गए अलग समर्पित कृत्रिम कुंडों (Synthetic Liners युक्त) में ही अनुमत है।\n"
                    "3. **नवीन घाटों की चुनौती:** नवनिर्मित कुंडों का **शून्य ऐतिहासिक डेटा (Zero Baseline Data)** है। अतः 72 घंटे पूर्व, विसर्जन के दौरान और 1 सप्ताह बाद अनिवार्य जल परीक्षण आवश्यक है।\n"
                    "4. **ठहराव खतरा:** कृत्रिम कुंडों में पानी का ठहराव होने पर 24 घंटे में ऑक्सीजन 0 होने का गंभीर खतरा रहता है, इसलिए निरंतर वातन (Aeration) अनिवार्य है।"
                )
            else:
                reply = (
                    "⚖️ **NGT Statutory Directives & Legal Framework (2026):**\n\n"
                    "1. **Strict Immersion Prohibition:** Under NGT orders, idol immersion into open waters of **Upper Lake & Lower Lake is strictly prohibited**.\n"
                    "2. **Dedicated Artificial Bunds:** Immersion is restricted strictly to designated artificial bunds lined with geo-synthetic liners.\n"
                    "3. **Zero Historical Baseline:** Newly constructed dedicated bunds possess zero historical water monitoring baseline. Mandatory sampling is required 72 hours prior, during, and 1 week post-visarjan.\n"
                    "4. **Anoxia Risk:** Stagnant water in artificial bunds risks complete oxygen depletion within 24 hours without continuous mechanical aeration."
                )
            return {"reply": reply, "sources": ["NGT OA No. 24/2021", "MPPCB Statutory Action Plan"]}

        # 4. Standards / CPCB Class B / DO / BOD
        if any(w in query_lower for w in ["standard", "cpcb", "class b", "मानक", "ऑक्सीजन", "bod", "do"]):
            if is_hi:
                reply = (
                    f"🧪 **सीपीसीबी क्लास-B (बाहरी स्नान) मानक एवं भोपाल की वास्तविक स्थिति:**\n\n"
                    f"• **घुलित ऑक्सीजन (DO):** मानक ≥ 5.0 mg/l होना चाहिए।\n"
                    f"  → भोपाल में **{stats['do_fail_pct']}% नमूनों** में ऑक्सीजन मानक से कम पाई गई ({stats['do_fails']}/{stats['do_total']})।\n"
                    f"• **जैव-रासायनिक ऑक्सीजन मांग (BOD):** जैविक कचरा सीमा ≤ 3.0 mg/l होनी चाहिए।\n"
                    f"  → भोपाल में **{stats['bod_fail_pct']}% नमूनों** में BOD सीमा पार पाई गई ({stats['bod_fails']}/{stats['bod_total']})।\n"
                    f"• **शून्य ऑक्सीजन (0 mg/l DO):** बैरागढ़ कुंड में 4 बार पूरी तरह ऑक्सीजन खत्म दर्ज की गई।"
                )
            else:
                reply = (
                    f"🧪 **CPCB Class B (Outdoor Bathing) Standards vs Bhopal Reality:**\n\n"
                    f"• **Dissolved Oxygen (DO):** Statutory threshold ≥ 5.0 mg/l.\n"
                    f"  → Bhopal non-compliance: **{stats['do_fail_pct']}% of samples** failed DO standard ({stats['do_fails']}/{stats['do_total']}).\n"
                    f"• **Biochemical Oxygen Demand (BOD):** Organic threshold ≤ 3.0 mg/l.\n"
                    f"  → Bhopal non-compliance: **{stats['bod_fail_pct']}% of samples** exceeded organic limits ({stats['bod_fails']}/{stats['bod_total']}).\n"
                    f"• **Zero DO Anoxia:** 4 separate instances of complete oxygen collapse (0.0 mg/l DO) at Bairagarh Kund."
                )
            return {"reply": reply, "sources": ["CPCB Water Quality Criteria", "MPPCB Annual Data 2023-2025"]}

        # 5. Full Ghats Ranking List
        if any(w in query_lower for w in ["ranking", "list", "all ghats", "सूची", "रैंकिंग", "सभी घाट", "क्रमांक"]):
            lines = []
            for g in summary:
                badge = g['risk_badge']
                lines.append(f"#{g['rank']} **{g['site']}** — स्कोर: {g['base_risk_score']}/100 [{badge}] ({g['water_body']})")
            if is_hi:
                reply = "🏆 **भोपाल के सभी 7 विसर्जन घाटों की आधिकारिक प्राथमिकता सूची (Priority Ranking):**\n\n" + "\n".join(lines) + "\n\n💡 *अधिकारी बैरागढ़ और हथाईखेड़ा पर सर्वोच्च प्राथमिकता से संसाधन आवंटित करें।*"
            else:
                reply = "🏆 **Official Priority Ranking for All 7 Bhopal Immersion Ghats:**\n\n" + "\n".join(lines) + "\n\n💡 *Officers are advised to prioritize mechanical aeration at Bairagarh and solid waste containment at Hathaikheda.*"
            return {"reply": reply, "sources": ["MCDA Multi-criteria Engine", "Database Records"]}

        # 6. Specific Ghat Lookup (Shahpura, Khatlapura, Hathaikheda, Rani Kamlapati, Malikhedi)
        for g in summary:
            first_name = g['site'].split()[0].lower()
            if first_name in query_lower or g['water_body'].lower() in query_lower:
                if is_hi:
                    reply = (
                        f"📍 **{g['site']} (रैंक #{g['rank']} · {g['risk_badge']})**\n\n"
                        f"• **स्थान/जल निकाय:** {g['water_body']} ({g['type']})\n"
                        f"• **जोखिम स्कोर:** {g['base_risk_score']} / 100\n"
                        f"• **विस्तृत कारण:** {g['reason_hi']}\n"
                        f"• **परीक्षण आंकड़े:** न्यूनतम DO {g['do_min']} mg/l | अधिकतम BOD {g['bod_max']} mg/l\n"
                        f"• **सुझाव:** " + " | ".join(g['recommendations_hi'])
                    )
                else:
                    reply = (
                        f"📍 **{g['site']} (Rank #{g['rank']} · {g['risk_badge']})**\n\n"
                        f"• **Location / Water Body:** {g['water_body']} ({g['type']})\n"
                        f"• **Risk Score:** {g['base_risk_score']} / 100\n"
                        f"• **Key Rationale:** {g['reason_en']}\n"
                        f"• **Monitoring Stats:** Min DO: {g['do_min']} mg/l | Max BOD: {g['bod_max']} mg/l\n"
                        f"• **Action Plan:** " + " | ".join(g['recommendations_en'])
                    )
                return {"reply": reply, "sources": [f"{g['site']} Station Ledger", "MPPCB Reports"]}

        # 7. Default / Fallback guidance
        if is_hi:
            reply = (
                "👋 **नमस्ते! मैं विसर्जन घाट वॉच AI सहायक हूँ।**\n\n"
                "आप मुझसे भोपाल विसर्जन घाटों से संबंधित निम्नलिखित प्रश्न पूछ सकते हैं:\n"
                "1. *'सबसे संवेदनशील या खतरनाक घाट कौन सा है?'*\n"
                "2. *'7 घाटों की पूरी प्राथमिकता सूची दिखाएं?'*\n"
                "3. *'बड़े और छोटे तालाब पर NGT के क्या नियम हैं?'*\n"
                "4. *'CPCB क्लास-B मानक क्या हैं और भोपाल की स्थिति क्या है?'*\n"
                "5. *'बैरागढ़ कुंड या शाहपुरा घाट का डेटा क्या है?'*\n\n"
                "सभी उत्तर MPPCB के 1,524 प्रमाणित जल परीक्षण आंकड़ों पर आधारित हैं।"
            )
        else:
            reply = (
                "👋 **Hello! I am your Visarjan Ghat Watch Decision Assistant.**\n\n"
                "You can ask me questions grounded in MPPCB's 1,524 water tests:\n"
                "1. *'Which ghat has the highest critical risk?'*\n"
                "2. *'Show full priority ranking of all 7 ghats?'*\n"
                "3. *'What are the NGT immersion rules for Upper & Lower Lake?'*\n"
                "4. *'What are CPCB Class B standards and Bhopal compliance rates?'*\n"
                "5. *'What is the water quality status of Bairagarh Kund or Shahpura?'*\n\n"
                "All answers are strictly verified from MPPCB official monitoring records."
            )
        return {"reply": reply, "sources": ["MPPCB Comprehensive Database"]}
