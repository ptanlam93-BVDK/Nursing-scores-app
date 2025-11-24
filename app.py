# app.py
# Nursing Scores App — Full combined file
# - Includes: dark hero header, sky-blue background, logo processing (convert uploaded JPG -> PNG with transparency),
#   teal-styled sections & badges, scoring modules (AVPU, GCS, Braden, Morse, qSOFA, CRT, VIP, NEWS, RASS, CAM-ICU),
#   save to CSV + download, quick alert actions.
#
# BEFORE DEPLOYING: ensure requirements.txt contains:
#   streamlit>=1.22.0
#   pandas>=2.0
#   Pillow>=9.0

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid

# For image processing (make white -> transparent)
from PIL import Image

# ---------------- Config ----------------
st.set_page_config(page_title="Công cụ đánh giá dành cho điều dưỡng", layout="bule")

# ---------------- Paths ----------------
# Path to the logo image you uploaded in the chat (use this exact path)
UPLOADED_LOGO = "/mnt/data/AB03982D-A2B3-4221-BE1A-FBD4C29A7492.jpeg"
# Output processed (transparent) logo filename
PROCESSED_LOGO = "logo_trans.png"

# CSV save path
CSV_PATH = "evaluations.csv"

# ---------------- Process logo (convert white bg -> transparent if needed) ----------------
def ensure_transparent_logo(src_path: str, out_path: str, white_threshold=240):
    """
    Convert near-white background pixels to transparent and save as PNG.
    Only runs if src exists and out_path doesn't exist yet (so it doesn't repeat every run).
    """
    try:
        if os.path.exists(src_path) and not os.path.exists(out_path):
            img = Image.open(src_path).convert("RGBA")
            datas = img.getdata()
            newData = []
            for item in datas:
                # item is (R,G,B,A)
                if item[0] >= white_threshold and item[1] >= white_threshold and item[2] >= white_threshold:
                    # make transparent
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img.putdata(newData)
            img.save(out_path, "PNG")
            return True
    except Exception as e:
        # If conversion fails, just ignore and use original
        print("Logo processing error:", e)
    return False

# Try to create processed logo if possible
ensure_transparent_logo(UPLOADED_LOGO, PROCESSED_LOGO)

# Choose which logo to show (prefer processed PNG)
if os.path.exists(PROCESSED_LOGO):
    LOGO_PATH_TO_USE = PROCESSED_LOGO
elif os.path.exists(UPLOADED_LOGO):
    LOGO_PATH_TO_USE = UPLOADED_LOGO
else:
    LOGO_PATH_TO_USE = None  # no logo available

# ---------------- CSS (sky-blue background + hero + teal theme) ----------------
PAGE_CSS = """
<style>
/* HERO (dark) */
.hero {
  background: #0f1724;
  color: #ffffff;
  padding: 36px 24px;
  border-radius: 8px;
  margin-bottom: 18px;
}
.hero .title {
  font-size: 44px;
  font-weight: 800;
  line-height: 1.02;
  margin: 0 0 8px 0;
}
.hero .lead {
  font-size: 16px;
  color: #cbd5d9;
  max-width: 980px;
  margin: 0;
  opacity: 0.95;
}

/* Page background: light sky blue */
[data-testid="stAppViewContainer"] {
  background: #E6F4FF !important;
}

/* Header row (logo + title) */
.header-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}
.logo-img {
  width: 84px;
  height: 84px;
  border-radius: 6px;
  object-fit: contain;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  background: transparent;
}
.header-title {
  font-size: 26px;
  font-weight: 800;
  color: #0b7f6b;
  margin: 0;
}
.header-sub {
  margin: 2px 0 0 0;
  color: #2b6f63;
  font-size: 13px;
}

/* Section cards */
.section {
  background: rgba(255,255,255,0.85);
  border-left: 5px solid #0b7f6b;
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

/* badges */
.badge {
  display:inline-block;
  padding:6px 12px;
  border-radius:14px;
  color:white;
  font-weight:700;
  font-size:13px;
}
.badge-green { background:#059669; }   /* low */
.badge-yellow { background:#f59e0b; }  /* medium */
.badge-red { background:#dc2626; }     /* high */

/* Button style */
.stButton>button {
  background: linear-gradient(180deg,#10b981,#059669);
  border: none;
  color: white;
  padding: .45rem .9rem;
  border-radius: 8px;
}

/* Small note */
.small-note {
  background: #ffffff;
  border: 1px solid #dff5ef;
  padding: 10px;
  border-radius: 8px;
  color: #234d48;
}

/* Responsive */
@media (max-width: 600px) {
  .hero .title { font-size: 30px; }
  .logo-img { width:64px; height:64px;}
  .header-title { font-size:18px; }
}
</style>
"""
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# ---------------- Header (logo + title) ----------------
header_html = ""
if LOGO_PATH_TO_USE:
    # Use the logo file from repo/workspace
    header_html = f"""
    <div class="header-row">
      <img src="{LOGO_PATH_TO_USE}" class="logo-img" />
      <div>
        <div class="header-title">Công cụ đánh giá cho điều dưỡng</div>
        <div class="header-sub">AVPU · GCS · Braden · Morse · qSOFA · CRT · VIP · NEWS · RASS · CAM-ICU</div>
      </div>
    </div>
    """
else:
    header_html = """
    <div class="header-row">
      <div>
        <div class="header-title">Công cụ đánh giá cho điều dưỡng</div>
        <div class="header-sub">AVPU · GCS · Braden · Morse · qSOFA · CRT · VIP · NEWS · RASS · CAM-ICU</div>
      </div>
    </div>
    """

st.markdown(header_html, unsafe_allow_html=True)

# ---------------- HERO (dark) ----------------
HERO_HTML = """
<div class="hero">
  <div class="title">Công cụ đánh giá dành cho điều dưỡng </div>
  <p class="lead">
    Công cụ này <strong>tính toán và hiển thị kết quả</strong>, không lưu dữ liệu (trừ khi bạn bấm lưu CSV). 
    Sử dụng nhanh tại giường được xây dựng, viết bởi <strong>CN.ĐD Phan Tấn Lãm</strong>, Khoa Hồi sức Tích cực - Chống độc (ICU), Bệnh viện Đa khoa Đồng Tháp.
  </p>
</div>
"""
st.markdown(HERO_HTML, unsafe_allow_html=True)

# ---------------- helper ----------------
def badge_html(level):
    if level == 'low':
        cls = 'badge-green'
        text = 'Thấp'
    elif level == 'medium':
        cls = 'badge-yellow'
        text = 'Trung bình'
    else:
        cls = 'badge-red'
        text = 'Cao'
    return f'<span class="badge {cls}">{text}</span>'

# ---------------- AVPU & GCS ----------------
st.markdown('<div class="section"><b>1. AVPU & GCS</b></div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    avpu = st.selectbox("AVPU", ["A - Alert", "V - Voice", "P - Pain", "U - Unresponsive"])
    avpu_score = {"A - Alert": 0, "V - Voice": 1, "P - Pain": 2, "U - Unresponsive": 3}[avpu]
    st.markdown(f'**AVPU:** {avpu} — Mã: {avpu_score}')
with col2:
    st.markdown("**Glasgow Coma Scale (GCS)**")
    E = st.slider("Mở mắt (E)", 1, 4, 4)
    V = st.slider("Lời nói (V)", 1, 5, 5)
    M = st.slider("Vận động (M)", 1, 6, 6)
    gcs_total = E + V + M
    if gcs_total <= 8:
        gcs_level = 'high'
    elif gcs_total <= 12:
        gcs_level = 'medium'
    else:
        gcs_level = 'low'
    st.markdown(f'**GCS = {gcs_total}** &nbsp; {badge_html(gcs_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- Braden ----------------
st.markdown('<div class="section"><b>2. Braden (Nguy cơ loét tỳ đè)</b></div>', unsafe_allow_html=True)
s = st.slider("Sensory (1–4)", 1, 4, 4)
moi = st.slider("Moisture (1–4)", 1, 4, 4)
act = st.slider("Activity (1–4)", 1, 4, 3)
mob = st.slider("Mobility (1–4)", 1, 4, 3)
nut = st.slider("Nutrition (1–4)", 1, 4, 4)
fric = st.slider("Friction & Shear (1–3)", 1, 3, 1)
braden_total = s + moi + act + mob + nut + fric
if braden_total <= 9:
    braden_level = 'high'
elif braden_total <= 14:
    braden_level = 'medium'
else:
    braden_level = 'low'
st.markdown(f'**Braden = {braden_total}** &nbsp; {badge_html(braden_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- CRT ----------------
st.markdown('<div class="section"><b>3. Capillary Refill Time (CRT)</b></div>', unsafe_allow_html=True)
crt = st.number_input("CRT (giây)", 0.0, 10.0, 2.0, step=0.1)
crt_level = 'low' if crt <= 3.0 else 'high'
st.markdown(f'**CRT = {crt:.1f}s** &nbsp; {badge_html(crt_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- Morse ----------------
st.markdown('<div class="section"><b>4. Morse Fall Scale</b></div>', unsafe_allow_html=True)
fall_prev = st.checkbox("Té ngã trong 3 tháng")
dx2 = st.checkbox("≥2 chẩn đoán")
aid = st.selectbox("Dụng cụ trợ đi", ["Không", "Bám đồ đạc", "Nạng/Gậy/Walker"])
iv = st.checkbox("Có IV")
gait = st.selectbox("Dáng đi", ["Bình thường", "Yếu", "Rất kém"])
mental = st.selectbox("Nhận thức", ["Tỉnh táo", "Quên giới hạn"])
morse = 0
morse += 25 if fall_prev else 0
morse += 15 if dx2 else 0
morse += {"Không":0,"Bám đồ đạc":15,"Nạng/Gậy/Walker":30}[aid]
morse += 20 if iv else 0
morse += {"Bình thường":0,"Yếu":10,"Rất kém":20}[gait]
morse += {"Tỉnh táo":0,"Quên giới hạn":15}[mental]
if morse >= 45:
    morse_level = 'high'
elif morse >= 25:
    morse_level = 'medium'
else:
    morse_level = 'low'
st.markdown(f'**Morse = {morse}** &nbsp; {badge_html(morse_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- qSOFA ----------------
st.markdown('<div class="section"><b>5. qSOFA</b></div>', unsafe_allow_html=True)
rr = st.number_input("Nhịp thở (l/p)", 5, 60, 18)
sbp = st.number_input("Huyết áp tâm thu (mmHg)", 50, 220, 120)
mental_change = 1 if avpu_score != 0 else 0
qsofa = (1 if rr >= 22 else 0) + (1 if sbp <= 100 else 0) + mental_change
qsofa_level = 'high' if qsofa >= 2 else 'low'
st.markdown(f'**qSOFA = {qsofa}** &nbsp; {badge_html(qsofa_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- VIP ----------------
st.markdown('<div class="section"><b>6. VIP (Viêm tĩnh mạch)</b></div>', unsafe_allow_html=True)
vip = st.slider("VIP (0–5)", 0, 5, 0)
vip_desc = ["Không","Đỏ nhẹ","Đỏ & đau","Viêm vừa","Viêm nặng","Áp xe"][vip]
vip_level = 'low' if vip <= 1 else 'medium' if vip <= 3 else 'high'
st.markdown(f'**VIP = {vip}** — {vip_desc} &nbsp; {badge_html(vip_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- NEWS ----------------
st.markdown('<div class="section"><b>7. NEWS</b></div>', unsafe_allow_html=True)
o2 = st.checkbox("Đang thở oxy?")
temp = st.number_input("Nhiệt độ (°C)", 30.0, 43.0, 37.0)
hr = st.number_input("Nhịp tim (l/p)", 30, 200, 80)
spo2 = st.number_input("SpO2 (%)", 50, 100, 97)
news = 0
news += 3 if rr <= 8 else 1 if 9 <= rr <= 11 else 0 if 12 <= rr <= 20 else 2 if 21 <= rr <= 24 else 3
news += 3 if spo2 <= 91 else 2 if spo2 <= 93 else 1 if spo2 <= 95 else 0
news += 3 if temp <= 35 else 1 if temp <= 36 else 0 if temp <= 38 else 1 if temp <= 39 else 2
news += 3 if sbp <= 90 else 2 if sbp <= 100 else 1 if sbp <= 110 else 0
news += 3 if hr <= 40 else 1 if hr <= 50 else 0 if hr <= 90 else 1 if hr <= 110 else 2 if hr <= 130 else 3
news += 3 if avpu_score != 0 else 0
news += 2 if o2 else 0
news_level = 'high' if news >= 7 else 'medium' if news >= 5 else 'low'
st.markdown(f'**NEWS = {news}** &nbsp; {badge_html(news_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- RASS ----------------
st.markdown('<div class="section"><b>8. RASS</b></div>', unsafe_allow_html=True)
rass = st.selectbox("Chọn RASS", [
    "-5 Unarousable","-4 Deep sedation","-3 Moderate sedation","-2 Light sedation","-1 Drowsy",
    "0 Alert and calm","+1 Restless","+2 Agitated","+3 Very agitated","+4 Combative"
])
try:
    rass_val = int(rass.split()[0])
except:
    rass_val = 0
if rass_val <= -3:
    rass_level = 'high'
elif rass_val < 0:
    rass_level = 'medium'
elif rass_val == 0:
    rass_level = 'low'
else:
    rass_level = 'high'
st.markdown(f'**RASS = {rass_val}** &nbsp; {badge_html(rass_level)}', unsafe_allow_html=True)

st.markdown('---')

# ---------------- CAM-ICU ----------------
st.markdown('<div class="section"><b>9. CAM-ICU (sàng lọc delirium)</b></div>', unsafe_allow_html=True)
a = st.checkbox("A: Thay đổi cấp tính/dao động?")
b = st.checkbox("B: Giảm chú ý?")
c = st.checkbox("C: Thay đổi mức độ ý thức (AVPU != A hoặc RASS != 0)?")
d = st.checkbox("D: Suy nghĩ rối loạn?")
cam_pos = a and b and (c or d)
st.markdown(f'**CAM-ICU = {"Dương" if cam_pos else "Âm"}**', unsafe_allow_html=True)

st.markdown('---')

# ---------------- Collect results ----------------
result = {
    "id": str(uuid.uuid4()),
    "timestamp": datetime.now().isoformat(timespec='seconds'),
    "avpu": avpu, "avpu_score": avpu_score,
    "gcs": gcs_total,
    "braden": braden_total, "braden_level": braden_level,
    "crt": crt, "crt_level": crt_level,
    "morse": morse, "morse_level": morse_level,
    "qsofa": qsofa, "qsofa_level": qsofa_level,
    "vip": vip, "vip_desc": vip_desc, "vip_level": vip_level,
    "news": news, "news_level": news_level,
    "rass": rass_val, "rass_level": rass_level,
    "cam_pos": cam_pos
}

# ---------------- Save & Actions ----------------
st.markdown("### Lưu / Hành động")
col_save, col_actions = st.columns([1,2])
with col_save:
    if st.button("💾 Lưu kết quả (Save to CSV)"):
        df_row = pd.DataFrame([result])
        if os.path.exists(CSV_PATH):
            try:
                df_exist = pd.read_csv(CSV_PATH)
                df_all = pd.concat([df_exist, df_row], ignore_index=True)
            except Exception:
                df_all = df_row
        else:
            df_all = df_row
        df_all.to_csv(CSV_PATH, index=False)
        st.success(f"Đã lưu vào `{CSV_PATH}` — tổng {len(df_all)} bản ghi.")
        csv_bytes = df_all.to_csv(index=False).encode('utf-8')
        st.download_button("Tải CSV", data=csv_bytes, file_name="evaluations.csv", mime="text/csv")
with col_actions:
    any_high = any([braden_level=='high', crt_level=='high', morse_level=='high', qsofa_level=='high', vip_level=='high', news_level=='high', rass_level=='high', cam_pos])
    if any_high:
        st.markdown("<h3 style='color:#dc2626'>⚠️ Cảnh báo: Có ít nhất 1 chỉ số MỨC CAO</h3>", unsafe_allow_html=True)
        st.markdown("**Hành động nhanh:**", unsafe_allow_html=True)
        # EDIT these to real contact info before use:
        phone_number = "0123456789"   # <-- chỉnh ở đây
        doctor_email = "doctor@example.com"  # <-- chỉnh ở đây
        st.markdown(f"- 📞 Gọi ngay: [Gọi bác sĩ]({'tel:'+phone_number})", unsafe_allow_html=True)
        mailto_msg = f"subject=Alert%20from%20Nursing%20Scores%20App&body=Patient%20alert%20-%20please%20review%20record%20ID%20{result['id']}"
        st.markdown(f"- ✉️ Gửi email nhanh: [Email bác sĩ](mailto:{doctor_email}?{mailto_msg})", unsafe_allow_html=True)
        if st.button("🆘 Gửi thông báo nhanh (hiển thị alert)"):
            st.error("Đã gửi cảnh báo nội bộ (ví dụ: thông báo trên màn hình). Vui lòng gọi/ thông báo đội trực.")
    else:
        st.info("Không có chỉ số mức CAO. Theo dõi và lưu nếu cần.")

st.markdown('---')
st.markdown('<div class="small-note">Ghi chú: Màu & badge chỉ để tham khảo trực quan. Trước khi dùng lâm sàng, cần phê duyệt bởi hội đồng y tế. CSV lưu tạm trên server; để lưu lâu dài hãy tích hợp DB/Google Drive/S3.</div>', unsafe_allow_html=True)