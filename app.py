import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Student Score Dashboard", page_icon="📚", layout="wide")

SUBJECTS = ["Python", "คณิตศาสตร์", "ฟิสิกส์"]
PASS_SCORE = 50

if "students" not in st.session_state:
    st.session_state.students = []

def grade(score):
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"

def status(score):
    return "ผ่าน" if score >= PASS_SCORE else "ไม่ผ่าน"

def dataframe():
    rows = []
    for student in st.session_state.students:
        row = {"รหัสนักเรียน": student["id"], "ชื่อ": student["name"]}
        for subject in SUBJECTS:
            score = student["scores"].get(subject)
            row[subject] = score
            row[f"เกรด {subject}"] = grade(score) if score is not None else "-"
        valid = [v for v in student["scores"].values() if v is not None]
        row["คะแนนเฉลี่ย"] = round(sum(valid) / len(valid), 2) if valid else None
        rows.append(row)
    return pd.DataFrame(rows)

st.title("📚 Student Score Dashboard")
st.caption("ระบบจัดการคะแนนนักเรียน • บันทึก แก้ไข วิเคราะห์ และส่งออกข้อมูล")

with st.sidebar:
    st.header("เมนู")
    page = st.radio("เลือกหน้าที่ต้องการ", ["ภาพรวม", "เพิ่ม / แก้ไขคะแนน", "รายชื่อนักเรียน", "จัดการข้อมูล"])
    st.divider()
    st.info("ข้อมูลในเวอร์ชันนี้เก็บในเซสชันของผู้ใช้ และจะไม่ถาวรเมื่อเซสชันสิ้นสุด")

df = dataframe()

if page == "ภาพรวม":
    st.subheader("ภาพรวมผลการเรียน")
    total_students = len(st.session_state.students)
    all_scores = [s["scores"][sub] for s in st.session_state.students for sub in SUBJECTS if s["scores"][sub] is not None]
    passed = sum(score >= PASS_SCORE for score in all_scores)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("นักเรียนทั้งหมด", f"{total_students:,} คน")
    c2.metric("คะแนนที่บันทึก", f"{len(all_scores):,}")
    c3.metric("คะแนนเฉลี่ยรวม", f"{sum(all_scores)/len(all_scores):.2f}" if all_scores else "—")
    c4.metric("อัตราผ่าน", f"{passed/len(all_scores)*100:.1f}%" if all_scores else "—")
    st.divider()
    if not df.empty:
        left, right = st.columns(2)
        with left:
            st.markdown("**คะแนนเฉลี่ยรายวิชา**")
            means = {sub: df[sub].dropna().mean() for sub in SUBJECTS}
            st.bar_chart(pd.Series(means, name="คะแนนเฉลี่ย"))
        with right:
            st.markdown("**การกระจายเกรดรวม**")
            grade_counts = {}
            for sub in SUBJECTS:
                for value in df[f"เกรด {sub}"]:
                    if value != "-":
                        grade_counts[value] = grade_counts.get(value, 0) + 1
            st.bar_chart(pd.Series(grade_counts, name="จำนวน"))
        st.markdown("**ข้อมูลนักเรียนล่าสุด**")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("ยังไม่มีข้อมูล เริ่มต้นโดยไปที่เมนู “เพิ่ม / แก้ไขคะแนน”")

elif page == "เพิ่ม / แก้ไขคะแนน":
    st.subheader("เพิ่มนักเรียนและบันทึกคะแนน")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("ชื่อนักเรียน", placeholder="กรอกชื่อ-นามสกุล")
        cols = st.columns(3)
        scores = {}
        for col, subject in zip(cols, SUBJECTS):
            with col:
                scores[subject] = st.number_input(f"{subject} (0–100)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        submitted = st.form_submit_button("บันทึกข้อมูล", type="primary", use_container_width=True)
    if submitted:
        clean_name = " ".join(name.split())
        if not clean_name:
            st.error("กรุณากรอกชื่อนักเรียน")
        else:
            existing = next((s for s in st.session_state.students if s["name"].casefold() == clean_name.casefold()), None)
            if existing:
                existing["scores"] = scores
                st.success(f"อัปเดตคะแนนของ {clean_name} แล้ว")
            else:
                sid = f"S{len(st.session_state.students)+1:03d}"
                st.session_state.students.append({"id": sid, "name": clean_name, "scores": scores})
                st.success(f"เพิ่ม {clean_name} สำเร็จ (รหัส {sid})")
    st.caption("การบันทึกชื่อเดิมอีกครั้งจะเป็นการอัปเดตคะแนนของนักเรียนคนนั้น")

elif page == "รายชื่อนักเรียน":
    st.subheader("รายชื่อนักเรียนและผลคะแนน")
    if df.empty:
        st.info("ยังไม่มีข้อมูลนักเรียน")
    else:
        query = st.text_input("ค้นหาด้วยชื่อหรือรหัส")
        view = df.copy()
        if query:
            view = view[view["ชื่อ"].str.contains(query, case=False, na=False) | view["รหัสนักเรียน"].str.contains(query, case=False, na=False)]
        st.dataframe(view, use_container_width=True, hide_index=True)
        csv = view.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ ดาวน์โหลด CSV", csv, "student_scores.csv", "text/csv")

elif page == "จัดการข้อมูล":
    st.subheader("แก้ไขและลบข้อมูล")
    if not st.session_state.students:
        st.info("ยังไม่มีข้อมูลนักเรียน")
    else:
        labels = {f'{s["id"]} — {s["name"]}': s["id"] for s in st.session_state.students}
        selected = st.selectbox("เลือกนักเรียน", list(labels))
        student = next(s for s in st.session_state.students if s["id"] == labels[selected])
        with st.form("edit_form"):
            new_name = st.text_input("ชื่อ", value=student["name"])
            edited = {}
            cols = st.columns(3)
            for col, subject in zip(cols, SUBJECTS):
                current = student["scores"][subject]
                with col:
                    edited[subject] = st.number_input(subject, min_value=0.0, max_value=100.0, value=float(current or 0), step=1.0, key=f"edit_{student['id']}_{subject}")
            save = st.form_submit_button("บันทึกการแก้ไข", type="primary")
        if save:
            student["name"] = " ".join(new_name.split()) or student["name"]
            student["scores"] = edited
            st.success("บันทึกการแก้ไขแล้ว")
        st.divider()
        if st.button("ลบนักเรียนคนนี้", type="secondary"):
            st.session_state.students = [s for s in st.session_state.students if s["id"] != student["id"]]
            st.rerun()

st.divider()
st.caption("Student Score Dashboard • พัฒนาด้วย Python และ Streamlit")
