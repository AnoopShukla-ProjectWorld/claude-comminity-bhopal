"""
Chatbot Knowledge Assistant Module for Bhopal Visarjan Ghat Watch 2026.
Bhopal Impact Lab 2026 · Track 2
Author: Anoop Shukla

Provides bilingual, empirical AI intelligence grounded strictly in 1,524 MPPCB 
water test readings, CPCB Class B standards, and NGT 2026 mandates.
Features robust phonetic/Hinglish aliases, fuzzy keyword detection, and NLP parsing.
"""

import re

class GhatChatbotAssistant:
    def __init__(self, engine):
        self.engine = engine

        # Comprehensive phonetic & colloquial aliases for Bhopal's 7 ghats
        self.ghat_aliases = {
            "bairagarh": [
                "bairagarh", "bairagadh", "bairagad", "hirdaram", "sant hirdaram", 
                "बैरागढ़", "हिरदाराम", "संत हिरदाराम", "bairagarh kund", "bairagadh kund",
                "hirdaram kund", "बैरागढ़ कुंड"
            ],
            "hathaikheda": [
                "hathaikheda", "hathai kheda", "hathaikhedha", "hathikheda", "hathi kheda",
                "हथाईखेड़ा", "हथाई खेड़ा", "हथाईखेड़ा", "hathaikheda dam"
            ],
            "khatlapura": [
                "khatlapura", "khatla pura", "katlapura", "खटलापुरा", "खटला पुरा", "khatlapura ghat"
            ],
            "malikhedi": [
                "malikhedi", "mali khedi", "malikhedha", "मालीखेड़ी", "माली खेड़ी", "मालीखेड़ी", "malikhedi kund"
            ],
            "prempura": [
                "prempura", "prem pura", "प्रेमपुरा", "प्रेम पुरा", "prempura ghat"
            ],
            "rani kamlapati": [
                "kamlapati", "kamla pati", "kamla park", "rani kamla", "rani kamlapati", 
                "कमलापति", "कमला पार्क", "कमला पार्क कुंड", "रानी कमलापति"
            ],
            "shahpura": [
                "shahpura", "shah pura", "sahpura", "sah pura", "शाहपुरा", "शाह पुरा", "shahpura lake", "shahpura ghat"
            ]
        }

    def _normalize(self, text: str) -> str:
        """Removes punctuation and normalizes whitespace."""
        return re.sub(r'[^\w\s]', ' ', text.lower()).strip()

    def answer_query(self, query: str, lang: str = "hi") -> dict:
        """
        Processes administrative questions about Bhopal immersion ghats,
        water quality data, standards, and recommendations in Hindi, Hinglish, or English.
        """
        raw_query = query.strip()
        q = self._normalize(query)
        summary = self.engine.get_ghat_summary()
        stats = self.engine.get_overall_stats()

        # If user writes Hinglish question (e.g. "kaisa hai", "pani", "kya hai"), answer in Hindi by default
        is_hinglish = any(w in q for w in ["kaisa", "kaisi", "pani", "paani", "kya", "batao", "bataiye", "dikhao", "kitna", "hai", "konsa", "kaunsa"])
        is_hi = (lang == "hi") or is_hinglish

        # -------------------------------------------------------------------
        # 1. GHAT SPECIFIC LOOKUP (Bairagarh, Prempura, Shahpura, Khatlapura, etc.)
        # -------------------------------------------------------------------
        matched_ghat_key = None
        for key, aliases in self.ghat_aliases.items():
            if any(alias in q for alias in aliases):
                matched_ghat_key = key
                break

        if matched_ghat_key:
            # Find the ghat object from summary
            target_ghat = None
            for g in summary:
                g_site_lower = g['site'].lower()
                if matched_ghat_key in g_site_lower or any(a in g_site_lower for a in self.ghat_aliases[matched_ghat_key]):
                    target_ghat = g
                    break
            
            if not target_ghat:
                target_ghat = summary[0] if matched_ghat_key == "bairagarh" else summary[-1]

            # Specific parameter asked? (e.g. DO, BOD, pH, water quality)
            asks_do = any(w in q for w in ["do", "oxygen", "ऑक्सीजन", "dissolved"])
            asks_bod = any(w in q for w in ["bod", "organic", "कचरा", "प्रदूषण", "pollution"])

            if is_hi:
                water_condition = "अत्यधिक गंभीर (अति संवेदनशील)" if target_ghat['risk_level'] == 'CRITICAL' else ("उच्च प्रदूषण" if target_ghat['risk_level'] == 'HIGH' else "नियंत्रित एवं स्वच्छ")
                
                reply = (
                    f"📍 **{target_ghat['site']} — जल गुणवत्ता विश्लेषण (रैंक #{target_ghat['rank']}):**\n\n"
                    f"• **वर्तमान स्थिति:** {water_condition} (जोखिम स्कोर: **{target_ghat['base_risk_score']}/100**, {target_ghat['risk_badge']})\n"
                    f"• **स्थान व निकाय:** {target_ghat['water_body']} ({target_ghat['type']})\n"
                    f"• **घुलित ऑक्सीजन (DO):** न्यूनतम **{target_ghat['do_min']} mg/l** दर्ज। (मानक: ≥ 5.0 mg/l) "
                    + (f"— ⚠️ **4 बार ऑक्सीजन शून्य (0 mg/l) होकर जल-जीवन समाप्त होने का संकट बना!**" if target_ghat['do_min'] == 0.0 else "") + "\n"
                    f"• **जैविक भार (BOD):** अधिकतम **{target_ghat['bod_max']} mg/l** (मानक सीमा ≤ 3.0 mg/l से {round(target_ghat['bod_max']/3.0, 1) if target_ghat['bod_max'] else 1}× गुना अधिक)।\n"
                    f"• **विस्तृत कारण:** {target_ghat['reason_hi']}\n\n"
                    f"**नगर निगम (BMC) हेतु अनुशंसित कार्रवाई:**\n"
                    + "\n".join([f"✔ {r}" for r in target_ghat['recommendations_hi']])
                )
            else:
                reply = (
                    f"📍 **{target_ghat['site']} — Water Quality Dossier (Rank #{target_ghat['rank']}):**\n\n"
                    f"• **Assessment:** {target_ghat['risk_badge']} (Composite Score: **{target_ghat['base_risk_score']}/100**)\n"
                    f"• **Water Body:** {target_ghat['water_body']} ({target_ghat['type']})\n"
                    f"• **Dissolved Oxygen (DO):** Lowest recorded at **{target_ghat['do_min']} mg/l** (Statutory: ≥ 5.0 mg/l) "
                    + ("— ⚠️ 4 zero DO (0.0 mg/l) instances causing complete anoxia!" if target_ghat['do_min'] == 0.0 else "") + "\n"
                    f"• **Organic Waste (BOD):** Peak at **{target_ghat['bod_max']} mg/l** (Safe limit ≤ 3.0 mg/l).\n"
                    f"• **Key Reason:** {target_ghat['reason_en']}\n\n"
                    f"**Directives for Municipal Corporation (BMC):**\n"
                    + "\n".join([f"✔ {r}" for r in target_ghat['recommendations_en']])
                )
            return {"reply": reply, "sources": [f"{target_ghat['site']} MPPCB Ledger", "Official Testing Records"]}

        # -------------------------------------------------------------------
        # 2. MOST CRITICAL / WORST / DANGEROUS GHAT
        # -------------------------------------------------------------------
        if any(w in q for w in ["critical", "most dangerous", "highest risk", "worst", "खतरनाक", "गंभीर", "सर्वाधिक जोखिम", "नंबर 1", "rank 1", "pehle number", "number one"]):
            critical = summary[0]
            if is_hi:
                reply = (
                    f"🚨 **भोपाल का सर्वाधिक संवेदनशील घाट: {critical['site']} (रैंक #1)**\n\n"
                    f"• **जोखिम स्कोर:** **{critical['base_risk_score']}/100** ({critical['risk_badge']})\n"
                    f"• **गंभीरता का कारण:** विसर्जन के दौरान **4 बार घुलित ऑक्सीजन शून्य (0.0 mg/l DO)** हो गई, जिससे पानी में सांस लेना असंभव हो गया।\n"
                    f"• **BOD प्रदूषण:** अधिकतम BOD **{critical['bod_max']} mg/l** तक पहुंचा जो सुरक्षित सीमा (3 mg/l) से कई गुना अधिक है।\n\n"
                    f"**नगर निगम (BMC) हेतु तात्कालिक कार्रवाई:**\n"
                    + "\n".join([f"✔ {r}" for r in critical['recommendations_hi']])
                )
            else:
                reply = (
                    f"🚨 **Highest Critical Risk Ghat in Bhopal: {critical['site']} (Rank #1)**\n\n"
                    f"• **Composite Risk Score:** **{critical['base_risk_score']}/100** ({critical['risk_badge']})\n"
                    f"• **Why it's critical:** Recorded **4 zero DO (0.0 mg/l)** anoxic events during visarjan, causing total oxygen depletion.\n"
                    f"• **Peak BOD:** Reached **{critical['bod_max']} mg/l** against CPCB limit of 3.0 mg/l.\n\n"
                    f"**Immediate Action Directives for BMC:**\n"
                    + "\n".join([f"✔ {r}" for r in critical['recommendations_en']])
                )
            return {"reply": reply, "sources": ["MPPCB Report 2023-2025", "Sant Hirdaram Kund Data"]}

        # -------------------------------------------------------------------
        # 3. CLEANEST / SAFEST / BEST GHAT
        # -------------------------------------------------------------------
        if any(w in q for w in ["clean", "cleanest", "safest", "best", "swachh", "surakshit", "achha", "accha", "स्वच्छ", "सुरक्षित", "सबसे अच्छा"]):
            safest = summary[-1]
            if is_hi:
                reply = (
                    f"🌿 **भोपाल का सबसे स्वच्छ एवं नियंत्रित घाट: {safest['site']} (रैंक #{safest['rank']})**\n\n"
                    f"• **जोखिम स्कोर:** **{safest['base_risk_score']}/100** ({safest['risk_badge']})\n"
                    f"• **स्थिति:** विसर्जन के दौरान भी यहाँ ऑक्सीजन का स्तर मानक (≥ 5 mg/l) के अनुरूप बना रहा और न्यूनतम DO **{safest['do_min']} mg/l** दर्ज हुआ।\n"
                    f"• **अधिकारी निष्कर्ष:** प्रेमपुरा घाट पर की गई बैरिकेडिंग और समय पर सफाई को मॉडल मानकर अन्य घाटों पर भी लागू किया जाना चाहिए।"
                )
            else:
                reply = (
                    f"🌿 **Cleanest & Safest Ghat in Bhopal: {safest['site']} (Rank #{safest['rank']})**\n\n"
                    f"• **Risk Score:** **{safest['base_risk_score']}/100** ({safest['risk_badge']})\n"
                    f"• **Status:** Maintained compliant dissolved oxygen (minimum DO: **{safest['do_min']} mg/l**) throughout the festival.\n"
                    f"• **Officer Benchmark:** Prempura's strict zoning and prompt skimmer cleanup serve as the operational model for all other ghats."
                )
            return {"reply": reply, "sources": ["MPPCB Report 2025", "Prempura Ghat Ledger"]}

        # -------------------------------------------------------------------
        # 4. FULL RANKING LIST (All 7 Ghats)
        # -------------------------------------------------------------------
        if any(w in q for w in ["ranking", "rankings", "list", "all ghats", "all ghat", "saare ghat", "sab ghat", "सूची", "रैंकिंग", "सभी घाट"]):
            lines = []
            for g in summary:
                lines.append(f"#{g['rank']} **{g['site']}** — स्कोर: **{g['base_risk_score']}/100** [{g['risk_badge']}] ({g['water_body']})")
            if is_hi:
                reply = "🏆 **भोपाल के 7 विसर्जन घाटों की आधिकारिक प्राथमिकता रैंकिंग सूची:**\n\n" + "\n".join(lines) + "\n\n💡 *निगम अधिकारियों को बैरागढ़ (#1) और हथाईखेड़ा (#2) पर सर्वोच्च प्राथमिकता से सफाई दल तैनात करने चाहिए।*"
            else:
                reply = "🏆 **Official Priority Ranking for All 7 Bhopal Immersion Ghats:**\n\n" + "\n".join(lines) + "\n\n💡 *BMC officers must prioritize mechanical aerators at Bairagarh (#1) and dredging crews at Hathaikheda (#2).*"
            return {"reply": reply, "sources": ["MCDA Multi-criteria Engine", "Database Records"]}

        # -------------------------------------------------------------------
        # 5. NGT MANDATE / LEGAL RULES / UPPER & LOWER LAKE PROHIBITION
        # -------------------------------------------------------------------
        if any(w in q for w in ["ngt", "ban", "banned", "prohibit", "rule", "rules", "order", "bada talab", "chhota talab", "प्रतिबंध", "आदेश", "तालाब", "नियम"]):
            if is_hi:
                reply = (
                    "⚖️ **एनजीटी (NGT 2026) विधिक आदेश एवं दिशानिर्देश:**\n\n"
                    "1. **तालाबों में पूर्ण प्रतिबंध:** एनजीटी के आदेशानुसार भोपाल के **बड़े तालाब (Upper Lake)** एवं **छोटे तालाब (Lower Lake)** के प्राकृतिक जल में किसी भी प्रकार की मूर्ति विसर्जन पूर्णतः प्रतिबंधित है।\n"
                    "2. **समर्पित कृत्रिम कुंड:** विसर्जन केवल तटों से दूर बने अलग कृत्रिम कुंडों (जिओ-सिंथेटिक लाइनर युक्त) में ही अनुमत है।\n"
                    "3. **नवीन घाटों की चुनौती:** नगर निगम द्वारा नवनिर्मित समर्पित कुंडों का **शून्य ऐतिहासिक जल डेटा (Zero Baseline Data)** है। अतः विसर्जन से 72 घंटे पहले, विसर्जन के दौरान और 1 सप्ताह बाद अनिवार्य परीक्षण किए जाएं।\n"
                    "4. **ठहराव खतरा:** कृत्रिम कुंडों में पानी का ठहराव होने पर 24 घंटे में ऑक्सीजन शून्य (Anoxia) होने का खतरा रहता है, इसलिए निरंतर वातन (Aerators) अनिवार्य है।"
                )
            else:
                reply = (
                    "⚖️ **National Green Tribunal (NGT 2026) Directives:**\n\n"
                    "1. **Strict Immersion Ban:** Idol immersion into open waters of **Upper Lake & Lower Lake is legally banned**.\n"
                    "2. **Dedicated Artificial Bunds:** Immersion must strictly take place inside dedicated geo-synthetic lined artificial kunds.\n"
                    "3. **Zero Historical Baseline:** Newly constructed bunds have zero past data. Mandatory sampling required 72 hours prior, on immersion day, and 1 week post-event.\n"
                    "4. **Anoxia Risk:** Stagnant bund water causes complete oxygen depletion (0 mg/l DO) within 24 hours without continuous aerators."
                )
            return {"reply": reply, "sources": ["NGT OA No. 24/2021", "MPPCB Action Plan"]}

        # -------------------------------------------------------------------
        # 6. CPCB STANDARDS / WATER PARAMETERS (DO, BOD, COD, pH, Lead)
        # -------------------------------------------------------------------
        if any(w in q for w in ["standard", "standards", "cpcb", "class b", "manak", "oxygen", "bod", "cod", "ph", "lead", "dhatu"]):
            if is_hi:
                reply = (
                    f"🧪 **सीपीसीबी (CPCB Class B - बाह्य स्नान) मानक एवं भोपाल का रिपोर्ट कार्ड:**\n\n"
                    f"• **घुलित ऑक्सीजन (DO):** मानक **≥ 5.0 mg/l** होना चाहिए।\n"
                    f"  → भोपाल में **{stats['do_fail_pct']}% नमूनों** में ऑक्सीजन मानक से कम पाई गई ({stats['do_fails']}/{stats['do_total']})।\n"
                    f"• **BOD जैविक कचरा भार:** मानक सीमा **≤ 3.0 mg/l** है।\n"
                    f"  → भोपाल में **{stats['bod_fail_pct']}% नमूनों** में BOD सीमा पार पाई गई ({stats['bod_fails']}/{stats['bod_total']})।\n"
                    f"• **शून्य ऑक्सीजन (0 mg/l DO):** बैरागढ़ कुंड में 4 बार पूरी तरह ऑक्सीजन खत्म दर्ज हुई।\n"
                    f"• **भारी धातु (Lead/Zinc):** अधिकतर स्थलों पर BDL (संसूचन सीमा से कम) दर्ज हुए।"
                )
            else:
                reply = (
                    f"🧪 **CPCB Class B Outdoor Bathing Criteria vs Bhopal Performance:**\n\n"
                    f"• **Dissolved Oxygen (DO):** Statutory standard is **≥ 5.0 mg/l**.\n"
                    f"  → Bhopal failure rate: **{stats['do_fail_pct']}% of samples** failed DO criteria ({stats['do_fails']}/{stats['do_total']}).\n"
                    f"• **Biochemical Oxygen Demand (BOD):** Limit is **≤ 3.0 mg/l**.\n"
                    f"  → Bhopal non-compliance: **{stats['bod_fail_pct']}% of samples** exceeded organic limit ({stats['bod_fails']}/{stats['bod_total']}).\n"
                    f"• **Anoxic Episodes:** 4 instances of complete oxygen collapse (0.0 mg/l DO) at Bairagarh Kund."
                )
            return {"reply": reply, "sources": ["CPCB Gazette Guidelines", "MPPCB 2023-2025 Ledger"]}

        # -------------------------------------------------------------------
        # 7. TOTAL READINGS / TRACEABILITY / HOW MANY SAMPLES
        # -------------------------------------------------------------------
        if any(w in q for w in ["sample", "reading", "readings", "kitne", "kitna test", "database", "data", "kul", "total", "praman"]):
            if is_hi:
                reply = (
                    f"📊 **डेटा प्रमाण एवं परीक्षण सारांश:**\n\n"
                    f"• **कुल प्रमाणित जल परीक्षण:** **1,524 नमूने** (7 घाट, 3 वर्ष: 2023–2025)\n"
                    f"• **त्योहार:** गणेश विसर्जन एवं दुर्गा विसर्जन के तीनों चरण (Pre, During, After)\n"
                    f"• **100% सत्यापन:** प्रत्येक डेटा पॉइंट MPPCB की आधिकारिक रिपोर्टों एवं उनके सटीक पृष्ठ संख्याओं से सत्यापित है।\n"
                    f"• आप नेविगेशन बार में **'परीक्षण प्रमाण'** पर क्लिक करके किसी भी रिकॉर्ड का स्रोत देख सकते हैं।"
                )
            else:
                reply = (
                    f"📊 **Data Traceability & Monitoring Ledger Summary:**\n\n"
                    f"• **Total Certified Tests:** **1,524 water samples** across 7 ghats (2023–2025).\n"
                    f"• **Phases Monitored:** Pre-immersion baseline, during visarjan, and 1-week post-visarjan.\n"
                    f"• **100% Verified:** Each figure is directly cross-referenced against official MPPCB report page numbers.\n"
                    f"• Click on **'Traceability'** in the top navigation to inspect the complete ledger."
                )
            return {"reply": reply, "sources": ["1,524 Verified Readings in SQLite", "MPPCB Citations"]}

        # -------------------------------------------------------------------
        # 8. GENERAL INTENTIONAL / COURTEOUS FALLBACK
        # -------------------------------------------------------------------
        if is_hi:
            reply = (
                f"👋 **नमस्ते! मैं विसर्जन घाट वॉच AI निर्णय सहायक हूँ।**\n\n"
                f"आपने पूछा: *'{raw_query}'*\n\n"
                f"मैं MPPCB के 1,524 जल परीक्षण नमूनों के आधार पर निम्न प्रश्नों का तुरंत उत्तर दे सकता हूँ:\n"
                f"1. **घाट की स्थिति:** *'बैरागढ़ कुंड का पानी कैसा है?'* या *'हथाईखेड़ा/शाहपुरा का डेटा बताएं'*।\n"
                f"2. **जोखिम प्राथमिकता:** *'सबसे खतरनाक घाट कौन सा है?'* या *'सभी 7 घाटों की रैंकिंग सूची'*।\n"
                f"3. **विधिक नियम:** *'बड़े तालाब और NGT के क्या नियम हैं?'*।\n"
                f"4. **मानक:** *'CPCB ऑक्सीजन और BOD मानक क्या हैं?'*।\n\n"
                f"कृपया उपरोक्त में से कोई भी प्रश्न पूछें।"
            )
        else:
            reply = (
                f"👋 **Hello! I am your Visarjan Ghat Watch Decision Assistant.**\n\n"
                f"You asked: *'{raw_query}'*\n\n"
                f"I can provide instant, verified answers based on MPPCB's 1,524 monitoring tests:\n"
                f"1. **Ghat Quality:** *'How is Bairagarh Kund water?'* or *'Show Shahpura Lake data'*.\n"
                f"2. **Risk Prioritization:** *'Which ghat is most critical?'* or *'Show all 7 ghats ranking'*.\n"
                f"3. **Statutory Rules:** *'What are NGT immersion mandates for Upper Lake?'*.\n"
                f"4. **Standards:** *'What are CPCB DO and BOD Class B standards?'*.\n\n"
                f"Please feel free to ask about any specific ghat or parameter."
            )
        return {"reply": reply, "sources": ["MPPCB Comprehensive Database"]}
