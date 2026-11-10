import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Student Score Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
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

def line_icon(name, size=25):
    paths = {
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
        "trend": '<path d="m3 17 6-6 4 4 8-9"/><path d="M15 6h6v6"/>',
        "award": '<circle cx="12" cy="8" r="6"/><path d="m8.2 13-1 8 4.8-2.5 4.8 2.5-1-8"/>',
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths.get(name, paths["book"])}</svg>'

def metric_card(label, value, note, icon):
    st.markdown(
        f'<div class="metric-card"><div class="metric-top"><span>{label}</span>'
        f'<span class="metric-icon">{line_icon(icon, 25)}</span></div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

# ---------- Visual design ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');
:root { --ink:#174b3b; --muted:#648477; --green:#198754; --mint:#e5f7ed; --line:rgba(62,145,105,.16); }
html, body, [class*="css"] { font-family:'IBM Plex Sans Thai','Inter',sans-serif; }
.stApp { background:radial-gradient(ellipse at 12% 8%,#e4f8ec 0%,transparent 38%),linear-gradient(135deg,#f7fcf8 0%,#eef9f2 55%,#e4f5eb 100%); color:var(--ink); }
.block-container { max-width:1500px; padding:1.2rem 2.5rem 3rem; }
header[data-testid="stHeader"] { background:rgba(239,250,243,.72); backdrop-filter:blur(18px); }
div[data-testid="stPopover"] > button { border:1px solid rgba(39,139,88,.18); border-radius:14px; background:rgba(255,255,255,.58); color:#176b48; font-size:22px; min-height:48px; box-shadow:0 5px 20px rgba(28,111,70,.06); }
div[data-testid="stPopover"] > button:hover { border-color:#55b985; color:#11643f; }
div[data-testid="stPopoverBody"] { background:rgba(250,255,251,.94); backdrop-filter:blur(22px); border:1px solid rgba(54,145,96,.18); border-radius:16px; }
div[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] strong { color:#176b48; }
.top-brand { font-size:17px; font-weight:700; color:#145b40; padding:9px 2px; letter-spacing:-.2px; }
.top-mark { color:#269b68; text-align:right; font-size:25px; padding:5px; }
.page-heading { margin:1.6rem 0 1.5rem; padding:0 0 18px; border-bottom:1px solid var(--line); }
.eyebrow { color:#269b68; font-size:10px; font-weight:700; letter-spacing:1.7px; margin-bottom:8px; }
.page-heading h1 { color:#164b39; font-size:30px; font-weight:750; letter-spacing:-.8px; margin:0; }
.page-heading p { color:#668477; font-size:13px; margin:6px 0 0; }
.metric-card { background:rgba(255,255,255,.48); border:1px solid rgba(75,157,111,.20); border-radius:20px; padding:20px; min-height:142px; box-shadow:0 8px 28px rgba(39,117,75,.055),inset 0 1px 0 rgba(255,255,255,.85); backdrop-filter:blur(18px); }
.metric-top { display:flex; justify-content:space-between; align-items:center; color:#648477; font-size:13px; font-weight:500; }
.metric-icon { display:grid; place-items:center; width:43px; height:43px; border-radius:15px; background:rgba(206,242,220,.62); color:#198754; }
.metric-value { color:#174b3b; font-family:Inter,sans-serif; font-size:30px; font-weight:800; margin-top:10px; letter-spacing:-1px; }
.metric-note { color:#7b9b8c; font-size:11px; margin-top:3px; }
.panel { background:rgba(255,255,255,.48); border:1px solid rgba(75,157,111,.18); border-radius:18px; padding:20px 22px; box-shadow:0 8px 25px rgba(39,117,75,.045); backdrop-filter:blur(16px); margin-bottom:16px; }
.panel-title { font-size:16px; font-weight:700; color:#174b3b; margin-bottom:3px; }
.panel-subtitle,.small-muted { font-size:12px; color:#789789; margin-bottom:14px; }
div[data-testid="stForm"] { background:rgba(255,255,255,.48); border:1px solid rgba(75,157,111,.2); border-radius:18px; padding:22px; backdrop-filter:blur(16px); }
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"],.stTextArea textarea { background:rgba(255,255,255,.42); border:1px solid rgba(66,145,101,.22); border-radius:12px; }
.stButton > button,.stDownloadButton > button,div[data-testid="stFormSubmitButton"] > button { border-radius:12px; font-weight:600; min-height:42px; }
.stButton > button[kind="primary"],div[data-testid="stFormSubmitButton"] > button[kind="primary"] { background:#198754; border-color:#198754; color:white; }
.stButton > button[kind="primary"]:hover,div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover { background:#146c43; border-color:#146c43; }
[data-testid="stDataFrame"] { border:1px solid rgba(66,145,101,.18); border-radius:14px; overflow:hidden; }
div[data-testid="stAlert"] { border-radius:14px; background:rgba(220,247,230,.65); border:1px solid rgba(49,153,91,.2); }
[data-testid="stRadio"] label { color:#225d45; }
hr { border-color:var(--line); }
.footer-brand { text-align:center; color:#83a997; font-size:11px; padding:34px 0 0; letter-spacing:.3px; }
</style>
""", unsafe_allow_html=True)

# Compact top navigation with a persistent three-line menu.
# Keep the selected page in session_state so it survives Streamlit reruns
# after the popover closes.
PAGES = ["ภาพรวม", "เพิ่ม / แก้ไขคะแนน", "รายชื่อนักเรียน", "จัดการข้อมูล"]
if "active_page" not in st.session_state:
    st.session_state.active_page = "ภาพรวม"

top_left, top_search, top_right = st.columns([0.65, 3.2, 0.7], vertical_alignment="center")
with top_left:
    with st.popover("☰", use_container_width=True):
        st.markdown("**เมนูหลัก**")
        st.radio(
            "เลือกหน้าที่ต้องการ",
            PAGES,
            key="active_page",
            label_visibility="collapsed",
        )
page = st.session_state.active_page
with top_search:
    st.markdown('<div class="top-brand">Student Score Dashboard</div>', unsafe_allow_html=True)
with top_right:
    st.markdown('<div class="top-mark">✧</div>', unsafe_allow_html=True)

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
        ("นักเรียนทั้งหมด", f"{total_students:,}", "รายชื่อในระบบ", "users"),
        ("คะแนนที่บันทึก", f"{len(all_scores):,}", "คะแนนจากทุกวิชา", "book"),
        ("คะแนนเฉลี่ยรวม", average, "จากคะแนนที่มีการบันทึก", "trend"),
        ("อัตราการผ่าน", pass_rate, "เกณฑ์ผ่านตั้งแต่ 50 คะแนน", "award"),
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

st.markdown('<div class="footer-brand">Student Score Dashboard</div>', unsafe_allow_html=True)
