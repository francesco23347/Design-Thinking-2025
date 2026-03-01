import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Study Planner", page_icon="📚")

st.title("📚 ระบบช่วยจัดตารางการอ่านหนังสือของนักศึกษา")

# ใช้ session state เก็บข้อมูล
if "schedules" not in st.session_state:
    st.session_state.schedules = []

# ฟอร์มเพิ่มข้อมูล
with st.form("schedule_form"):
    subject = st.text_input("ชื่อวิชา")
    day = st.selectbox("เลือกวัน", 
        ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
    )
    hours = st.number_input("จำนวนชั่วโมงอ่าน", min_value=1, step=1)

    submitted = st.form_submit_button("เพิ่มตาราง")

    if submitted:
        if subject != "":
            st.session_state.schedules.append({
                "วิชา": subject,
                "วัน": day,
                "ชั่วโมง": hours
            })
            st.success("เพิ่มตารางเรียบร้อยแล้ว ✅")
        else:
            st.warning("กรุณากรอกชื่อวิชา")

# แสดงตาราง
if st.session_state.schedules:
    df = pd.DataFrame(st.session_state.schedules)
    st.subheader("📋 ตารางการอ่าน")
    st.dataframe(df, use_container_width=True)

    # คำนวณชั่วโมงรวม
    total_hours = df["ชั่วโมง"].sum()
    st.markdown(f"### 📊 ชั่วโมงอ่านรวมทั้งหมด: {total_hours} ชั่วโมง")

    # ปุ่มลบข้อมูล
    st.subheader("🗑 ลบข้อมูล")
    index_to_delete = st.number_input(
        "ใส่ลำดับแถวที่ต้องการลบ (เริ่มจาก 0)", 
        min_value=0, 
        max_value=len(df)-1,
        step=1
    )

    if st.button("ลบข้อมูล"):
        st.session_state.schedules.pop(index_to_delete)
        st.success("ลบข้อมูลเรียบร้อยแล้ว")
        st.rerun()
else:
    st.info("ยังไม่มีข้อมูลตาราง")
