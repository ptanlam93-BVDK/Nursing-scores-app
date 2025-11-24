import streamlit as st

st.set_page_config(page_title="Nursing Scores App", layout="wide")

st.title("Bộ Công Cụ Tính thang Điểm dành cho Điều Dưỡng ")
st.write("AVPU • GCS • Braden • Morse Fall • qSOFA • CRT • Phlebitis (VIP) • NEWS • RASS • CAM-ICU")

# ---------------------------- AVPU ----------------------------
st.header("1. Thang điểm AVPU")
avpu = st.selectbox("Chọn mức AVPU:", ["A - Alert", "V - Voice", "P - Pain", "U - Unresponsive"])
avpu_score = {"A - Alert": 0, "V - Voice": 1, "P - Pain": 2, "U - Unresponsive": 3}[avpu]
st.info(f"Điểm AVPU: {avpu_score}")

# ---------------------------- GCS ----------------------------
st.header("2. Glasgow Coma Scale (GCS)")
E = st.slider("Mở mắt (E)", 1, 4, 4)
V = st.slider("Lời nói (V)", 1, 5, 5)
M = st.slider("Vận động (M)", 1, 6, 6)
gcs_total = E + V + M
if gcs_total <= 8:
    gcs_level = "Nguy kịch – Cân nhắc đặt nội khí quản"
elif gcs_total <= 12:
    gcs_level = "Trung bình – Theo dõi sát"
else:
    gcs_level = "Nhẹ"
st.success(f"GCS = {gcs_total} → {gcs_level}")

# ---------------------------- Braden ----------------------------
st.header("3. Thang điểm Braden (Loét tỳ đè)")
s = st.slider("Cảm giác đau (Sensory)", 1, 4, 4)
moi = st.slider("Độ ẩm da (Moisture)", 1, 4, 4)
act = st.slider("Hoạt động (Activity)", 1, 4, 3)
mob = st.slider("Vận động (Mobility)", 1, 4, 3)
nut = st.slider("Dinh dưỡng (Nutrition)", 1, 4, 4)
fric = st.slider("Ma sát & kéo (Friction)", 1, 3, 1)
braden_total = s + moi + act + mob + nut + fric
if braden_total <= 9:
    braden_risk = "Nguy cơ RẤT CAO"
elif braden_total <= 12:
    braden_risk = "Nguy cơ CAO"
elif braden_total <= 14:
    braden_risk = "Nguy cơ TRUNG BÌNH"
else:
    braden_risk = "Nguy cơ THẤP"
st.warning(f"Tổng điểm Braden = {braden_total} → {braden_risk}")

# ---------------------------- CRT ----------------------------
st.header("4. Capillary Refill Time (CRT)")
crt = st.number_input("Thời gian CRT (giây)", 0.0, 10.0, 2.0)
if crt > 3:
    st.error("CRT kéo dài → Tưới máu ngoại vi KÉM")
else:
    st.success("CRT bình thường")

# ---------------------------- Morse Fall ----------------------------
st.header("5. Morse Fall Scale (Nguy cơ té ngã)")
fall_prev = st.checkbox("Té ngã 3 tháng qua")
dx2 = st.checkbox("≥ 2 chẩn đoán bệnh")
aid = st.selectbox("Dụng cụ hỗ trợ đi lại", ["Không", "Bám đồ đạc", "Nạng/Gậy/Walker"])
iv = st.checkbox("Có truyền IV")
gait = st.selectbox("Dáng đi", ["Bình thường", "Yếu", "Rất kém"])
mental = st.selectbox("Nhận thức", ["Tỉnh táo", "Quên giới hạn"])
morse = 0
morse += 25 if fall_prev else 0
morse += 15 if dx2 else 0
morse += {"Không": 0, "Bám đồ đạc": 15, "Nạng/Gậy/Walker": 30}[aid]
morse += 20 if iv else 0
morse += {"Bình thường": 0, "Yếu": 10, "Rất kém": 20}[gait]
morse += {"Tỉnh táo": 0, "Quên giới hạn": 15}[mental]
if morse >= 45:
    morse_level = "Nguy cơ CAO"
elif morse >= 25:
    morse_level = "Nguy cơ TRUNG BÌNH"
else:
    morse_level = "Nguy cơ THẤP"
st.success(f"Morse = {morse} → {morse_level}")

# ---------------------------- qSOFA ----------------------------
st.header("6. qSOFA – Sàng lọc nhiễm khuẩn")
rr = st.number_input("Nhịp thở (lần/phút)", 5, 50, 18)
sbp = st.number_input("Huyết áp tâm thu (mmHg)", 50, 200, 120)
mental_change = 1 if avpu_score != 0 else 0
qsofa = (1 if rr >= 22 else 0) + (1 if sbp <= 100 else 0) + mental_change
if qsofa >= 2:
    qsofa_msg = "Nguy cơ cao → Báo bác sĩ ngay"
else:
    qsofa_msg = "Theo dõi thêm"
st.error(f"qSOFA = {qsofa} → {qsofa_msg}")

# ---------------------------- VIP ----------------------------
st.header("7. VIP – Viêm tĩnh mạch")
vip = st.slider("Điểm VIP", 0, 5, 0)
vip_desc = ["Không viêm", "Đỏ nhẹ", "Đỏ & đau", "Viêm vừa", "Viêm nặng", "Áp xe"][vip]
st.info(f"VIP = {vip}: {vip_desc}")

# ---------------------------- NEWS ----------------------------
st.header("8. NEWS – Thang cảnh báo sớm")
o2 = st.checkbox("Đang thở oxy?")
temp = st.number_input("Nhiệt độ (°C)", 30.0, 43.0, 37.0)
hr = st.number_input("Mạch (lần/phút)", 30, 200, 80)
news = 0
# RR
news += 3 if rr <= 8 else 1 if 9 <= rr <= 11 else 0 if 12 <= rr <= 20 else 2 if 21 <= rr <= 24 else 3
# SpO2
spo2 = st.number_input("SpO2 (%)", 60, 100, 97)
news += 3 if spo2 <= 91 else 2 if spo2 <= 93 else 1 if spo2 <= 95 else 0
# Temperature
news += 3 if temp <= 35 else 1 if temp <= 36 else 0 if temp <= 38 else 1 if temp <= 39 else 2
# SBP
news += 3 if sbp <= 90 else 2 if sbp <= 100 else 1 if sbp <= 110 else 0 if sbp <= 219 else 3
# Heart rate
news += 3 if hr <= 40 else 1 if hr <= 50 else 0 if hr <= 90 else 1 if hr <= 110 else 2 if hr <= 130 else 3
# AVPU
news += 3 if avpu_score != 0 else 0
# Oxygen support
news += 2 if o2 else 0
if news >= 7:
    news_level = "Nguy cơ RẤT CAO"
elif news >= 5:
    news_level = "Nguy cơ TRUNG BÌNH"
else:
    news_level = "Nguy cơ THẤP"
st.warning(f"Tổng điểm NEWS = {news} → {news_level}")

# ---------------------------- RASS (Richmond Agitation-Sedation Scale) ----------------------------
st.header("9. RASS – Đánh giá kích động / an thần (Richmond Scale)")
st.write("RASS từ -5 (completely unresponsive) đến +4 (combative). Chọn mức mô tả đúng.")
rass = st.selectbox("Chọn điểm RASS", [
    "-5: Unarousable",
    "-4: Deep sedation",
    "-3: Moderate sedation",
    "-2: Light sedation",
    "-1: Drowsy",
    "0: Alert and calm",
    "+1: Restless",
    "+2: Agitated",
    "+3: Very agitated",
    "+4: Combative"
])
# map to numeric value for logic
rass_map = {
    "-5: Unarousable": -5, "-4: Deep sedation": -4, "-3: Moderate sedation": -3,
    "-2: Light sedation": -2, "-1: Drowsy": -1, "0: Alert and calm": 0,
    "+1: Restless": 1, "+2: Agitated": 2, "+3: Very agitated": 3, "+4: Combative": 4
}
rass_value = rass_map[rass]
if rass_value <= -3:
    st.error(f"RASS = {rass_value} → An thần sâu, cân nhắc đánh giá thuốc/điều trị.")
elif rass_value < 0:
    st.warning(f"RASS = {rass_value} → An thần nhẹ, theo dõi.")
elif rass_value == 0:
    st.success("RASS = 0 → Bình thường")
else:
    st.error(f"RASS = +{rass_value} → Kích động, cần an toàn người bệnh & nhân viên. Báo kíp trực.")

# ---------------------------- CAM-ICU (Sàng lọc lú lẫn cho ICU) ----------------------------
st.header("10. CAM-ICU – Sàng lọc lú lẫn / thay đổi tri giác")
st.write("Điền các mục dưới để sàng lọc delirium (CAM-ICU đơn giản hóa)")

# Quy ước: A = Acute change or fluctuating course, B = Inattention, C = Altered level of consciousness, D = Disorganized thinking
a = st.checkbox("A. Có thay đổi cấp tính hoặc dao động về tri giác trong 24 giờ gần nhất?")
b = st.checkbox("B. Có giảm chú ý (ví dụ không thể nhắc lại 5 ký tự, bị phân tâm)?")
c = st.checkbox("C. Có thay đổi mức độ ý thức (không tỉnh táo hoàn toàn)? (ví dụ RASS != 0 hoặc AVPU != A)")
d = st.checkbox("D. Suy nghĩ rối loạn (ví dụ trả lời câu đơn giản không chính xác, nói lắp)")

# CAM-ICU dương nếu A + B và (C hoặc D)
cam_positive = False
if a and b and (c or d):
    cam_positive = True

if cam_positive:
    st.error("KẾT LUẬN: CAM-ICU DƯƠNG → Nghi ngờ delirium. Báo bác sĩ/điều tra nguyên nhân (nhiễm khuẩn, thuốc, rối loạn điện giải...).")
else:
    st.success("CAM-ICU âm hoặc chưa đủ tiêu chuẩn dương — tiếp tục theo dõi.")

# ---------------------------- Footer / Note ----------------------------
st.markdown("---")
st.info("Ghi chú: Đây là công cụ hỗ trợ nhanh cho điều dưỡng. Trước khi dùng lâm sàng, cần phê duyệt bởi hội đồng y tế. Nếu cần, có thể thêm lưu lịch sử (CSV/DB) hoặc xuất báo cáo.")
