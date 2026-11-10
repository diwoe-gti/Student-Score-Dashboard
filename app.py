import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Score Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

SUBJECTS = ["Python", "คณิตศาสตร์", "ฟิสิกส์"]
PASS_SCORE = 50

if "students" not in st.session_state:
    st.session_state.students = []

def grade(score):
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 50:
        return "D"
    return "F"

def dataframe():
    rows = []
    for student in st.session_state.students:
        row = {"รหัสนักเรียน": student["id"], "ชื่อ": student["name"]}
        valid = []
        for subject in SUBJECTS:
            score = student["scores"].get(subject)
            row[subject] = score
            row[f"เกรด {subject}"] = grade(score) if score is not None else "-"
            if score is not None:
                valid.append(score)
        row["คะแนนเฉลี่ย"] = round(sum(valid) / len(valid), 2) if valid else None
        rows.append(row)
    return pd.DataFrame(rows)

def page_header(eyebrow, title, subtitle):
    st.markdown(
        f'<div class="page-heading"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def metric_card(label, value, note, icon):
    st.markdown(
        f'<div class="metric-card"><div class="metric-top"><span>{label}</span>'
        f'<span class="metric-icon">{icon}</span></div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

# ---------- Visual design ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #111827;
    --muted: #64748b;
    --blue: #2563eb;
    --line: #e5e7eb;
    --surface: #ffffff;
    --canvas: #f8fafc;
}
html, body, [class*="css"] { font-family: 'IBM Plex Sans Thai', 'Inter', sans-serif; }
.stApp { background: #f8fafc; color: var(--ink); }
.block-container { padding: 2rem 2.6rem 3rem; max-width: 1540px; }
[data-testid="stSidebar"] { background: #111827; border-right: 1px solid #263244; }
[data-testid="stSidebar"] * { color: #eef2ff !important; }
[data-testid="stSidebar"] .stRadio label { padding: 9px 12px; border-radius: 10px; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #aeb9d3 !important; }
[data-testid="stSidebar"] hr { border-color: #34415e; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { font-size: 12px; color: #aeb9d3 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 5px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent; border: 1px solid transparent; border-radius: 9px;
    padding: 10px 12px; transition: .18s;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: #1f2b3d; border-color: #334155;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
    background: #1d4ed8; border-color: #3b82f6;
}
.page-heading { margin: 0 0 1.5rem; }
.eyebrow { color: #2563eb; font-size: 10px; font-weight: 700; letter-spacing: 1.7px; text-transform: uppercase; margin-bottom: 8px; }
.page-heading { padding-bottom: 18px; border-bottom: 1px solid #e5e7eb; }
.page-heading h1 { color: #111827; font-size: 30px; font-weight: 750; letter-spacing: -.8px; margin: 0; }
.page-heading p { color: #64748b; font-size: 13px; margin: 6px 0 0; }
.metric-card {
    background: #ffffff; border: 1px solid #e5e7eb; border-radius: 13px;
    padding: 19px 20px; min-height: 132px; box-shadow: 0 2px 8px rgba(15,23,42,.035);
}
.metric-top { display:flex; justify-content:space-between; align-items:center; color:var(--muted); font-size:13px; font-weight:500; }
.metric-icon { display:grid; place-items:center; width:34px; height:34px; border-radius:9px; background:#eff6ff; color:#1d4ed8; font-size:17px; }
.metric-value { color:var(--ink); font-family:Inter,sans-serif; font-size:29px; font-weight:800; margin-top:9px; letter-spacing:-1px; }
.metric-note { color:#8b96aa; font-size:11px; margin-top:2px; }
.panel {
    background:#fff; border:1px solid #e5e7eb; border-radius:13px;
    padding:20px 22px; box-shadow:0 2px 8px rgba(15,23,42,.025); margin-bottom:16px;
}
.panel-title { font-size:16px; font-weight:700; color:var(--ink); margin-bottom:3px; }
.panel-subtitle { font-size:12px; color:var(--muted); margin-bottom:14px; }
div[data-testid="stForm"] { background:#fff; border:1px solid var(--line); border-radius:16px; padding:22px; }
.stButton > button, .stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
    border-radius:8px; font-weight:600; min-height:42px;
}
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    border-radius:8px;
}
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
div[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:var(--line); }
.small-muted { color:var(--muted); font-size:12px; }
.brand { color:#fff; font-size:20px; font-weight:800; letter-spacing:-.5px; }
.brand-sub { color:#94a3b8; font-size:10px; letter-spacing:1px; margin-top:4px; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#94a3b8 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong { color:#cbd5e1 !important; font-size:10px; letter-spacing:1.2px; }
.stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background:#2563eb; border-color:#2563eb; color:#fff;
}
.stButton > button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    background:#1d4ed8; border-color:#1d4ed8;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="brand">✦ STUDENT<span style="color:#91a0ff">HUB</span></div><div class="brand-sub">ACADEMIC MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**WORKSPACE**")
    page = st.radio(
        "เมนูหลัก",
        ["ภาพรวม", "เพิ่ม / แก้ไขคะแนน", "รายชื่อนักเรียน", "จัดการข้อมูล"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Student Score Dashboard**")
    st.markdown('<p class="small-muted">ระบบจัดการและวิเคราะห์ผลการเรียน</p>', unsafe_allow_html=True)
    st.caption("เวอร์ชันทดลอง • ข้อมูลยังเก็บในเซสชัน")

df = dataframe()

if page == "ภาพรวม":
    page_header("ACADEMIC OVERVIEW", "ภาพรวมผลการเรียน", "ติดตามคะแนนและสถานะการเรียนของนักเรียนในภาพรวม")
    total_students = len(st.session_state.students)
    all_scores = [
        s["scores"][sub]
        for s in st.session_state.students
        for sub in SUBJECTS
        if s["scores"].get(sub) is not None
    ]
    passed = sum(score >= PASS_SCORE for score in all_scores)
    average = f"{sum(all_scores) / len(all_scores):.1f}" if all_scores else "—"
    pass_rate = f"{passed / len(all_scores) * 100:.0f}%" if all_scores else "—"

    cols = st.columns(4, gap="medium")
    metrics = [
        ("นักเรียนทั้งหมด", f"{total_students:,}", "รายชื่อในระบบ", "👥"),
        ("คะแนนที่บันทึก", f"{len(all_scores):,}", "คะแนนจากทุกวิชา", "📝"),
        ("คะแนนเฉลี่ยรวม", average, "จากคะแนนที่มีการบันทึก", "📈"),
        ("อัตราการผ่าน", pass_rate, "เกณฑ์ผ่านตั้งแต่ 50 คะแนน", "🏅"),
    ]
    for col, item in zip(cols, metrics):
        with col:
            metric_card(*item)

    st.write("")
    if not df.empty:
        left, right = st.columns([1.15, 0.85], gap="large")
        with left:
            st.markdown('<div class="panel-title">คะแนนเฉลี่ยรายวิชา</div><div class="panel-subtitle">เปรียบเทียบผลคะแนนเฉลี่ยของแต่ละวิชา</div>', unsafe_allow_html=True)
            means = pd.Series({sub: df[sub].dropna().mean() for sub in SUBJECTS}, name="คะแนนเฉลี่ย")
            st.bar_chart(means, height=260, color="#6577ed")
        with right:
            st.markdown('<div class="panel-title">สัดส่วนเกรด</div><div class="panel-subtitle">จำนวนผลการเรียนในแต่ละระดับ</div>', unsafe_allow_html=True)
            grade_counts = {g: 0 for g in ["A", "B", "C", "D", "F"]}
            for sub in SUBJECTS:
                for value in df[f"เกรด {sub}"]:
                    if value in grade_counts:
                        grade_counts[value] += 1
            st.bar_chart(pd.Series(grade_counts, name="จำนวน"), height=260, color="#9a8cf0")
        st.markdown('<div class="panel-title">รายชื่อนักเรียน</div><div class="panel-subtitle">ข้อมูลคะแนนล่าสุดที่บันทึกในระบบ</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("ยังไม่มีข้อมูลนักเรียน เริ่มต้นได้ที่เมนู “เพิ่ม / แก้ไขคะแนน”")

elif page == "เพิ่ม / แก้ไขคะแนน":
    page_header("STUDENT ENTRY", "เพิ่มข้อมูลนักเรียน", "กรอกข้อมูลพื้นฐานและคะแนนเพื่อบันทึกเข้าสู่ระบบ")
    with st.form("student_form", clear_on_submit=True):
        st.markdown("**ข้อมูลทั่วไป**")
        name = st.text_input("ชื่อ - นามสกุล", placeholder="เช่น ธนพร พุทธา")
        st.write("")
        st.markdown("**ผลคะแนนรายวิชา**")
        cols = st.columns(3)
        scores = {}
        for col, subject in zip(cols, SUBJECTS):
            with col:
                scores[subject] = st.number_input(f"{subject} (0–100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        st.write("")
        submitted = st.form_submit_button("บันทึกข้อมูลนักเรียน", type="primary", use_container_width=True)
    if submitted:
        clean_name = " ".join(name.split())
        if not clean_name:
            st.error("กรุณากรอกชื่อนักเรียนก่อนบันทึก")
        else:
            existing = next((s for s in st.session_state.students if s["name"].casefold() == clean_name.casefold()), None)
            if existing:
                existing["scores"] = scores
                st.success(f"อัปเดตคะแนนของ {clean_name} เรียบร้อยแล้ว")
            else:
                sid = f"S{len(st.session_state.students)+1:03d}"
                st.session_state.students.append({"id": sid, "name": clean_name, "scores": scores})
                st.success(f"เพิ่ม {clean_name} สำเร็จ • รหัส {sid}")
    st.caption("หมายเหตุ: หากกรอกชื่อที่มีอยู่แล้ว ระบบจะอัปเดตคะแนนของนักเรียนคนนั้น")

elif page == "รายชื่อนักเรียน":
    page_header("STUDENT DIRECTORY", "รายชื่อนักเรียน", "ค้นหา ตรวจสอบผลคะแนน และส่งออกข้อมูล")
    if df.empty:
        st.info("ยังไม่มีข้อมูลนักเรียน")
    else:
        query = st.text_input("ค้นหานักเรียน", placeholder="พิมพ์ชื่อหรือรหัสนักเรียน...")
        view = df.copy()
        if query:
            view = view[
                view["ชื่อ"].str.contains(query, case=False, na=False)
                | view["รหัสนักเรียน"].str.contains(query, case=False, na=False)
            ]
        st.markdown(f'<div class="small-muted">พบข้อมูล {len(view)} รายการ</div>', unsafe_allow_html=True)
        st.dataframe(view, use_container_width=True, hide_index=True)
        csv = view.to_csv(index=False).encode("utf-8-sig")
        st.download_button("ดาวน์โหลดรายงาน CSV", csv, "student_scores.csv", "text/csv")

elif page == "จัดการข้อมูล":
    page_header("DATA MANAGEMENT", "จัดการข้อมูลนักเรียน", "แก้ไขคะแนนหรือเอารายชื่อนักเรียนออกจากระบบ")
    if not st.session_state.students:
        st.info("ยังไม่มีข้อมูลนักเรียน")
    else:
        labels = {f'{s["id"]} — {s["name"]}': s["id"] for s in st.session_state.students}
        selected = st.selectbox("เลือกนักเรียนที่ต้องการจัดการ", list(labels))
        student = next(s for s in st.session_state.students if s["id"] == labels[selected])
        with st.form("edit_form"):
            new_name = st.text_input("ชื่อ - นามสกุล", value=student["name"])
            st.markdown("**แก้ไขคะแนนรายวิชา**")
            edited = {}
            cols = st.columns(3)
            for col, subject in zip(cols, SUBJECTS):
                with col:
                    current = student["scores"].get(subject, 0)
                    edited[subject] = st.number_input(
                        subject, min_value=0.0, max_value=100.0,
                        value=float(current or 0), step=1.0,
                        key=f"edit_{student['id']}_{subject}",
                    )
            save = st.form_submit_button("บันทึกการแก้ไข", type="primary", use_container_width=True)
        if save:
            student["name"] = " ".join(new_name.split()) or student["name"]
            student["scores"] = edited
            st.success("บันทึกการแก้ไขเรียบร้อยแล้ว")
        st.divider()
        confirm_delete = st.checkbox("ฉันยืนยันว่าต้องการลบนักเรียนคนนี้")
        if st.button("ลบนักเรียน", type="secondary", disabled=not confirm_delete):
            st.session_state.students = [s for s in st.session_state.students if s["id"] != student["id"]]
            st.rerun()

st.markdown('<div style="text-align:center;color:#9aa4b8;font-size:11px;padding:28px 0 0">STUDENTHUB • STUDENT SCORE MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
