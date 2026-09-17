const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5 in

const NAVY = "0C4A6E";
const BLUE = "2563EB";
const DARK = "0F172A";
const GRAY = "64748B";
const LIGHTBG = "F8FAFC";
const GREEN = "16A34A";
const AMBER = "D97706";
const RED = "DC2626";
const WHITE = "FFFFFF";

function baseSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  return s;
}

function title(s, text, opts = {}) {
  s.addText(text, {
    x: 0.6, y: 0.45, w: 12.1, h: 0.8,
    fontSize: 28, bold: true, color: DARK, fontFace: "Arial",
    isTextBox: true,
    ...opts,
  });
}

function footer(s, n) {
  s.addText("Chennai Smart Water Watch  |  1M1B AI for Sustainability Internship", {
    x: 0.6, y: 7.15, w: 10, h: 0.3, fontSize: 9, color: GRAY, isTextBox: true,
  });
  s.addText(String(n), {
    x: 12.4, y: 7.15, w: 0.4, h: 0.3, fontSize: 9, color: GRAY, isTextBox: true, align: "right",
  });
}

// ---------------- Slide 1: Title ----------------
{
  const s = baseSlide();
  s.background = { color: NAVY };
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.33, h: 7.5, fill: { color: NAVY } });
  s.addText("💧", { x: 5.9, y: 1.1, w: 1.5, h: 1.2, fontSize: 60, isTextBox: true, align: "center" });
  s.addText("Chennai Smart Water Watch", {
    x: 1, y: 2.5, w: 11.33, h: 1, fontSize: 40, bold: true, color: WHITE,
    align: "center", isTextBox: true, fontFace: "Arial",
  });
  s.addText("AI-Powered Area-Wise Water Wastage Monitor & RAG Chatbot", {
    x: 1, y: 3.5, w: 11.33, h: 0.6, fontSize: 18, color: "BFDBFE",
    align: "center", isTextBox: true,
  });
  s.addText("SDG 6: Clean Water and Sanitation", {
    x: 1, y: 4.15, w: 11.33, h: 0.5, fontSize: 16, color: "93C5FD",
    align: "center", isTextBox: true, italic: true,
  });
  s.addText([
    { text: "Abi", options: { bold: true, breakLine: true } },
    { text: "B.Tech, Artificial Intelligence & Data Science", options: { breakLine: true } },
    { text: "Saranathan College of Engineering, Trichy" },
  ], {
    x: 1, y: 5.6, w: 11.33, h: 1, fontSize: 14, color: WHITE, align: "center", isTextBox: true,
  });
  s.addText("1M1B AI for Sustainability Virtual Internship  |  IBM SkillsBuild & AICTE", {
    x: 1, y: 6.8, w: 11.33, h: 0.4, fontSize: 11, color: "94A3B8", align: "center", isTextBox: true,
  });
}

// ---------------- Slide 2: Problem Statement ----------------
{
  const s = baseSlide();
  title(s, "Problem Statement");
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 1.4, w: 6.0, h: 5.3, fill: { color: LIGHTBG }, line: { type: "none" } });
  s.addText([
    { text: "Chennai is a water-stressed city.", options: { bold: true, breakLine: true, color: NAVY } },
    { text: " ", options: { breakLine: true } },
    { text: "It depends almost entirely on 4 reservoirs and groundwater, and faced a severe \"Day Zero\" crisis in 2019 when reservoirs nearly ran dry.", options: { breakLine: true, color: DARK } },
    { text: " ", options: { breakLine: true } },
    { text: "Water demand is projected to rise from ~1,200 MLD to over 2,100 MLD by 2031 — but there is no easy way for citizens or officials to see which areas are wasting the most water, in real time.", options: { color: DARK } },
  ], { x: 0.9, y: 1.7, w: 5.4, h: 4.7, fontSize: 14, isTextBox: true, valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 7.0, y: 2.3, w: 5.7, h: 3.2, fill: { color: "EFF6FF" }, rectRadius: 0.12, line: { type: "none" } });
  s.addText("How might we use AI to give real-time, area-wise visibility into water wastage — so Chennai can use its limited water more sustainably?", {
    x: 7.35, y: 2.3, w: 5.0, h: 3.2, fontSize: 15, italic: true, bold: true, color: BLUE,
    align: "left", isTextBox: true, valign: "middle",
  });
  footer(s, 2);
}

// ---------------- Slide 3: SDG Alignment ----------------
{
  const s = baseSlide();
  title(s, "SDG Alignment");
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 1.5, w: 2.6, h: 2.6, fill: { color: "0891B2" }, rectRadius: 0.15, line: { type: "none" } });
  s.addText("SDG 6", { x: 0.6, y: 1.9, w: 2.6, h: 0.6, fontSize: 26, bold: true, color: WHITE, align: "center", isTextBox: true });
  s.addText("Clean Water\n& Sanitation", { x: 0.6, y: 2.6, w: 2.6, h: 1.2, fontSize: 15, color: WHITE, align: "center", isTextBox: true });

  const targets = [
    { t: "Target 6.4", d: "Substantially increase water-use efficiency and ensure sustainable withdrawals to address water scarcity." },
    { t: "Target 6.b", d: "Support and strengthen participation of local communities in improving water and sanitation management." },
  ];
  let y = 1.5;
  targets.forEach((tg) => {
    s.addText([
      { text: tg.t + "  ", options: { bold: true, color: NAVY } },
      { text: tg.d, options: { color: DARK } },
    ], { x: 3.6, y, w: 9.1, h: 1.1, fontSize: 14, isTextBox: true, valign: "top" });
    y += 1.3;
  });

  s.addText("This project turns SDG 6 targets into a concrete, usable tool: it makes water-use efficiency visible (6.4) and gives citizens a way to engage with their own consumption data (6.b).", {
    x: 3.6, y: 4.3, w: 9.1, h: 1.5, fontSize: 13, italic: true, color: GRAY, isTextBox: true,
  });
  footer(s, 3);
}

// ---------------- Slide 4: AI Solution Overview ----------------
{
  const s = baseSlide();
  title(s, "AI Solution Overview");

  const boxes = [
    { x: 0.6, label: "1. Data Layer", desc: "Area-wise water consumption & reservoir data (Kaggle: Chennai Water Management)", color: "0891B2" },
    { x: 4.6, label: "2. ML Prediction", desc: "RandomForest classifier predicts wastage-risk (Low/Medium/High) per area", color: BLUE },
    { x: 8.6, label: "3. RAG Chatbot", desc: "FAISS retrieval + IBM Granite (Hugging Face) answers citizen questions using real data", color: "7C3AED" },
  ];
  boxes.forEach((b) => {
    s.addShape(pres.ShapeType.roundRect, { x: b.x, y: 1.7, w: 3.9, h: 2.3, fill: { color: LIGHTBG }, rectRadius: 0.1, line: { color: b.color, width: 1.5 } });
    s.addShape(pres.ShapeType.rect, { x: b.x, y: 1.7, w: 3.9, h: 0.55, fill: { color: b.color }, line: { type: "none" } });
    s.addText(b.label, { x: b.x, y: 1.7, w: 3.9, h: 0.55, fontSize: 15, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true });
    s.addText(b.desc, { x: b.x + 0.2, y: 2.4, w: 3.5, h: 1.5, fontSize: 12.5, color: DARK, isTextBox: true, valign: "top" });
  });

  s.addText("→", { x: 4.3, y: 2.5, w: 0.5, h: 1, fontSize: 26, color: GRAY, isTextBox: true, align: "center" });
  s.addText("→", { x: 8.3, y: 2.5, w: 0.5, h: 1, fontSize: 26, color: GRAY, isTextBox: true, align: "center" });

  s.addText("Output: a live web dashboard (Flask) showing area-wise wastage risk + an embedded chatbot for natural-language Q&A.", {
    x: 0.6, y: 4.4, w: 11.9, h: 0.6, fontSize: 14, bold: true, color: NAVY, isTextBox: true,
  });

  s.addText("Technologies used: Python, Flask, scikit-learn (RandomForest), sentence-transformers, FAISS, IBM Granite (via Hugging Face free inference API), Chart.js", {
    x: 0.6, y: 5.3, w: 11.9, h: 1.3, fontSize: 13, color: GRAY, isTextBox: true, italic: true,
  });
  footer(s, 4);
}

// ---------------- Slide 5: Target Users ----------------
{
  const s = baseSlide();
  title(s, "Target Users");
  const users = [
    { icon: "🏛️", h: "Chennai Metrowater officials", d: "Identify high-wastage zones quickly to prioritize leak repair and awareness drives" },
    { icon: "🏠", h: "Residents & housing societies", d: "Check their zone's usage vs. the recommended norm and get personalized conservation tips" },
    { icon: "🎓", h: "Students & researchers", d: "Use the open dataset and dashboard for further sustainability research" },
  ];
  let x = 0.6;
  users.forEach((u) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.7, w: 3.9, h: 3.6, fill: { color: LIGHTBG }, rectRadius: 0.12, line: { type: "none" } });
    s.addText(u.icon, { x, y: 2.0, w: 3.9, h: 1, fontSize: 40, align: "center", isTextBox: true });
    s.addText(u.h, { x: x + 0.2, y: 3.0, w: 3.5, h: 0.7, fontSize: 15, bold: true, color: NAVY, align: "center", isTextBox: true });
    s.addText(u.d, { x: x + 0.3, y: 3.7, w: 3.3, h: 1.4, fontSize: 12.5, color: DARK, align: "center", isTextBox: true, valign: "top" });
    x += 4.2;
  });
  footer(s, 5);
}

// ---------------- Slide 6: Responsible AI Considerations ----------------
{
  const s = baseSlide();
  title(s, "Responsible AI Considerations");
  const items = [
    { h: "Fairness", d: "Risk scores are based on per-person usage (LPCD), not raw totals — so densely populated areas aren't unfairly flagged as \"wasteful\".", color: GREEN },
    { h: "Transparency", d: "The dashboard always shows the underlying data behind each prediction — never just a black-box score — and clearly labels simulated vs. real-time data.", color: BLUE },
    { h: "Privacy", d: "Only aggregated, publicly available area-level data is used. No individual household or personal data is collected or stored.", color: AMBER },
  ];
  let y = 1.6;
  items.forEach((it) => {
    s.addShape(pres.ShapeType.roundRect, { x: 0.6, y, w: 11.9, h: 1.5, fill: { color: LIGHTBG }, rectRadius: 0.1, line: { type: "none" } });
    s.addText(it.h, { x: 0.9, y, w: 3, h: 1.5, fontSize: 16, bold: true, color: it.color, isTextBox: true, valign: "middle" });
    s.addText(it.d, { x: 4.0, y, w: 8.3, h: 1.5, fontSize: 13.5, color: DARK, isTextBox: true, valign: "middle" });
    y += 1.75;
  });
  footer(s, 6);
}

// ---------------- Slide 7: Expected Impact ----------------
{
  const s = baseSlide();
  title(s, "Expected Impact");
  const stats = [
    { big: "135 LPCD", small: "CPHEEO recommended norm used as the wastage benchmark" },
    { big: "4 zones", small: "Monitored area-wise, extensible to all 15 Chennai zones" },
    { big: "24x7", small: "Dashboard auto-refreshes as new data arrives" },
  ];
  let x = 0.6;
  stats.forEach((st) => {
    s.addText(st.big, { x, y: 1.7, w: 3.9, h: 1, fontSize: 32, bold: true, color: BLUE, align: "center", isTextBox: true });
    s.addText(st.small, { x: x + 0.2, y: 2.7, w: 3.5, h: 1, fontSize: 12.5, color: GRAY, align: "center", isTextBox: true });
    x += 4.2;
  });
  s.addShape(pres.ShapeType.rect, { x: 0.6, y: 4.0, w: 12.1, h: 2.4, fill: { color: LIGHTBG }, line: { type: "none" } });
  s.addText([
    { text: "If adopted at city scale:  ", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "Officials can target leak-repair and awareness campaigns where they matter most, instead of city-wide blanket efforts.", options: { bullet: true, breakLine: true } },
    { text: "Residents get instant, personalized feedback instead of a once-a-year water bill.", options: { bullet: true, breakLine: true } },
    { text: "Even a 10% cut in the average 14 LPCD wastage seen in this pilot data could save millions of litres per day city-wide.", options: { bullet: true } },
  ], { x: 0.9, y: 4.2, w: 11.5, h: 2.1, fontSize: 13.5, color: DARK, isTextBox: true, valign: "top" });
  footer(s, 7);
}

// ---------------- Slide 8: Prototype / Demo ----------------
{
  const s = baseSlide();
  title(s, "Prototype & Demo");
  s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 1.5, w: 7.0, h: 5.2, fill: { color: NAVY }, rectRadius: 0.1, line: { type: "none" } });
  s.addText("💧 Chennai Smart Water Watch", { x: 0.9, y: 1.75, w: 6.4, h: 0.5, fontSize: 15, bold: true, color: WHITE, isTextBox: true });
  s.addText("Area-wise water wastage monitor", { x: 0.9, y: 2.2, w: 6.4, h: 0.35, fontSize: 10, color: "93C5FD", isTextBox: true });

  const zones = [
    { name: "REDHILLS", risk: "Low", color: GREEN },
    { name: "CHOLAVARAM", risk: "Medium", color: AMBER },
    { name: "POONDI", risk: "High", color: RED },
    { name: "CHEMBARAMBAKKAM", risk: "High", color: RED },
  ];
  let zx = 0.9;
  zones.forEach((z) => {
    s.addShape(pres.ShapeType.roundRect, { x: zx, y: 2.8, w: 1.5, h: 1.5, fill: { color: WHITE }, rectRadius: 0.08, line: { type: "none" } });
    s.addText(z.name, { x: zx + 0.05, y: 2.9, w: 1.4, h: 0.5, fontSize: 8, bold: true, color: DARK, align: "center", isTextBox: true });
    s.addShape(pres.ShapeType.roundRect, { x: zx + 0.25, y: 3.55, w: 1.0, h: 0.3, fill: { color: z.color }, rectRadius: 0.15, line: { type: "none" } });
    s.addText(z.risk, { x: zx + 0.25, y: 3.55, w: 1.0, h: 0.3, fontSize: 8, bold: true, color: WHITE, align: "center", valign: "middle", isTextBox: true });
    zx += 1.6;
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.9, y: 4.6, w: 6.1, h: 1.8, fill: { color: "1E3A5F" }, rectRadius: 0.08, line: { type: "none" } });
  s.addText("🤖  Water Advisor Chatbot", { x: 1.1, y: 4.75, w: 5.7, h: 0.4, fontSize: 12, bold: true, color: WHITE, isTextBox: true });
  s.addText("\"Which area wastes the most water?\"", { x: 1.1, y: 5.2, w: 5.7, h: 0.4, fontSize: 10.5, italic: true, color: "BFDBFE", isTextBox: true });
  s.addText("→ Poondi currently shows the highest wastage (15.6 L/person above the 135 LPCD norm)...", { x: 1.1, y: 5.65, w: 5.7, h: 0.6, fontSize: 10, color: "E2E8F0", isTextBox: true });

  s.addText([
    { text: "Live dashboard + chatbot", options: { bold: true, color: NAVY, breakLine: true } },
    { text: "🔗 GitHub: github.com/[your-username]/chennai-smart-water-watch", options: { breakLine: true, color: DARK } },
    { text: " ", options: { breakLine: true } },
    { text: "🎥 Demo video: [add your video link]", options: { breakLine: true, color: DARK } },
    { text: " ", options: { breakLine: true } },
    { text: "Run locally: python app.py → localhost:5000", options: { color: GRAY, italic: true } },
  ], { x: 8.0, y: 2.2, w: 4.7, h: 3.5, fontSize: 13, isTextBox: true, valign: "top" });
  footer(s, 8);
}

pres.writeFile({ fileName: "Chennai_Smart_Water_Watch.pptx" }).then(() => {
  console.log("PPT created.");
});
