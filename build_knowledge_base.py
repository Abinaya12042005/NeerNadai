"""
build_knowledge_base.py
-------------------------
RAG-oda "knowledge base" (the documents it searches through) idhu than.
Idhu run pannumbodhu, data-la irundhu real stats eduthu oru txt file
generate pannum + static water-conservation / SDG content vera files-a save pannum.

Run: python build_knowledge_base.py
Output: knowledge_base/*.txt
"""

import pandas as pd
import os

os.makedirs("knowledge_base", exist_ok=True)

# ---------- 1. Live dataset summary (auto-generated from real data) ----------
df = pd.read_csv("data/area_wise_consumption.csv")
summary_lines = ["CHENNAI AREA-WISE WATER CONSUMPTION - CURRENT DATASET SUMMARY", ""]

for area, group in df.groupby("Area"):
    avg_lpcd = group["Actual_LPCD"].mean()
    avg_wastage = group["Wastage_LPCD"].mean()
    pop = int(group["Population_Served"].iloc[0])
    summary_lines.append(
        f"Area: {area} | Population served: {pop:,} | "
        f"Average usage: {avg_lpcd:.1f} litres/person/day | "
        f"Average wastage above CPHEEO norm (135 LPCD): {avg_wastage:.1f} litres/person/day"
    )

worst_area = df.groupby("Area")["Wastage_LPCD"].mean().idxmax()
best_area = df.groupby("Area")["Wastage_LPCD"].mean().idxmin()
summary_lines.append("")
summary_lines.append(f"Highest wastage area currently: {worst_area}")
summary_lines.append(f"Lowest wastage (most efficient) area currently: {best_area}")

with open("knowledge_base/dataset_summary.txt", "w") as f:
    f.write("\n".join(summary_lines))

# ---------- 2. SDG 6 background (for the chatbot to explain SDG alignment) ----------
sdg_text = """SDG 6: CLEAN WATER AND SANITATION
SDG 6 aims to ensure availability and sustainable management of water and
sanitation for all by 2030. Key targets relevant to this project:
- Target 6.4: By 2030, substantially increase water-use efficiency across
  all sectors and ensure sustainable withdrawals to address water scarcity.
- Target 6.b: Support and strengthen participation of local communities in
  improving water and sanitation management.

Chennai context: Chennai depends heavily on four reservoirs (Poondi,
Cholavaram, Redhills, Chembarambakkam) and groundwater. The city faced a
severe "Day Zero" water crisis in 2019 when reservoirs ran nearly dry.
Chennai's water demand is projected to rise from about 1,200 MLD (million
litres per day) to over 2,100 MLD by 2031, while current supply is far
below projected demand - making water-use efficiency and wastage reduction
critical for the city's sustainability.
"""
with open("knowledge_base/sdg6_background.txt", "w") as f:
    f.write(sdg_text)

# ---------- 3. Water conservation tips (for chatbot Q&A) ----------
tips_text = """WATER CONSERVATION TIPS FOR CHENNAI HOUSEHOLDS
1. Fix leaking taps immediately - a single dripping tap can waste over
   15 litres of water per day.
2. Use bucket and mug for bathing instead of showers - showers use
   3-5x more water per minute.
3. Install aerators on taps to cut flow rate by up to 50% without
   reducing usability.
4. Collect and reuse RO reject water / washing machine rinse water for
   mopping, gardening or flushing.
5. Water plants early morning or late evening to reduce evaporation loss.
6. Set up rainwater harvesting (mandatory under Chennai building rules
   since 2003) to recharge groundwater during monsoon (Oct-Dec).
7. Report visible pipeline leaks to Chennai Metrowater immediately -
   distribution leakage is a major source of city-wide wastage.
8. Recommended usage benchmark: the CPHEEO (Govt of India) norm is
   135 litres per person per day (LPCD) for urban water supply. Usage
   consistently above this indicates wastage.
"""
with open("knowledge_base/water_conservation_tips.txt", "w") as f:
    f.write(tips_text)

# ---------- 4. Project / AI method explanation (for "how does this work" questions) ----------
project_text = """ABOUT THIS PROJECT - AI-POWERED SMART WATER ADVISOR
This project was built for the 1M1B AI for Sustainability Virtual
Internship (with IBM SkillsBuild and AICTE), addressing SDG 6: Clean
Water and Sanitation.

Problem: High water wastage across different areas/zones of Chennai,
a water-stressed city, due to lack of real-time visibility into
area-wise consumption patterns.

AI approach used:
1. Machine Learning (RandomForest classifier) predicts a wastage-risk
   category (Low/Medium/High) for each area based on consumption
   patterns, population served, and seasonality.
2. Retrieval-Augmented Generation (RAG) chatbot lets citizens and
   officials ask natural-language questions ("which area wastes the
   most water?", "how can I save water at home?") and get answers
   grounded in the real dataset and verified water-conservation
   knowledge, instead of the AI guessing from general training data.

Responsible AI considerations:
- Fairness: risk categories are based on per-person usage (LPCD), not
  raw totals, so densely populated areas aren't unfairly flagged.
- Transparency: the dashboard always shows the underlying data the
  prediction is based on, not just a black-box score.
- Privacy: only aggregated, publicly available area-level data is
  used - no individual household or personal data.
"""
with open("knowledge_base/project_info.txt", "w") as f:
    f.write(project_text)

print("Knowledge base created in knowledge_base/:")
for fname in os.listdir("knowledge_base"):
    print(" -", fname)
