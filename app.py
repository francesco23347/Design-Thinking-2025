import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

st.set_page_config(page_title="Study Planner", page_icon="📚", layout="wide")

st.title("📚 ระบบช่วยจัดตารางการอ่านหนังสือของนักศึกษา")

days = ["จันทร์","อังคาร","พุธ","พฤหัสบดี","ศุกร์","เสาร์","อาทิตย์"]
time_slots = [
    f"{h:02d}:00-{(h+1)%24:02d}:00"
    for h in range(0, 24)
]

if "schedules" not in st.session_state:
    st.session_state.schedules = []

with st.form("schedule_form"):
    subject = st.text_input("ชื่อวิชา")
    day = st.selectbox("เลือกวัน", days)

    hours_display = [f"{h:02d}:00" for h in range(24)]
    start_display = st.selectbox("เวลาเริ่ม", hours_display)
    start_hour = int(start_display.split(":")[0])

    duration = st.number_input(
     "ระยะเวลา (ชั่วโมง)",
        min_value=1,
        max_value=24,
        step=1
)

    submitted = st.form_submit_button("เพิ่มตาราง")  

    if submitted:
        if subject:
            st.session_state.schedules.append({
                "วิชา": subject,
                "วัน": day,
                "เริ่ม": start_hour,
                "ชั่วโมง": duration
            })
            st.success("เพิ่มเรียบร้อย ✅")
        else:
            st.warning("กรอกชื่อวิชา")

# สร้าง DataFrame เปล่า
grid = pd.DataFrame("", index=days, columns=time_slots)

# เติมข้อมูลลง grid
from datetime import datetime, timedelta, time

for item in st.session_state.schedules:

    start_dt = datetime.combine(
    datetime.today(),
    time(item["เริ่ม"], 0)
)
    end_dt = start_dt + timedelta(hours=item["ชั่วโมง"])

    for h in range(24):
        slot_start = datetime.combine(datetime.today(), time(h,0))
        slot_end = slot_start + timedelta(hours=1)

        if start_dt < slot_end and end_dt > slot_start:
            slot_name = f"{h:02d}:00-{(h+1)%24:02d}:00"
            grid.loc[item["วัน"], slot_name] = item["วิชา"]

st.subheader("📅 ตารางรายสัปดาห์")

def highlight(val):
    if val != "":
        return "background-color: #FFA500; color: black;"
    return ""

styled = grid.style.applymap(highlight)

st.dataframe(styled, use_container_width=True)           

st.subheader("🛠 จัดการตาราง")

if st.session_state.schedules:

    # แสดงข้อมูลทั้งหมด
    df_manage = pd.DataFrame(st.session_state.schedules)
    df_manage.index.name = "ลำดับ"
    st.dataframe(df_manage, use_container_width=True)

    selected_index = st.number_input(
        "เลือกลำดับที่ต้องการแก้ไข / ลบ",
        min_value=0,
        max_value=len(st.session_state.schedules)-1,
        step=1
    )

    col1, col2 = st.columns(2)

    # 🔴 ปุ่มลบ
    with col1:
        if st.button("🗑 ลบรายการ"):
            st.session_state.schedules.pop(selected_index)
            st.success("ลบข้อมูลเรียบร้อย ✅")
            st.rerun()

    # 🟢 ปุ่มแก้ไข
    with col2:
        if st.button("✏ แก้ไขรายการ"):
            edit_item = st.session_state.schedules[selected_index]

            st.session_state.edit_mode = True
            st.session_state.edit_index = selected_index
            st.session_state.edit_data = edit_item
            st.rerun()

# ===============================
# โหมดแก้ไข
# ===============================
if "edit_mode" in st.session_state and st.session_state.edit_mode:

    st.subheader("✏ แก้ไขข้อมูล")

    edit_item = st.session_state.edit_data

    new_subject = st.text_input("ชื่อวิชา", value=edit_item["วิชา"])
    new_day = st.selectbox("วัน", days, index=days.index(edit_item["วัน"]))

    hours_display = [f"{h:02d}:00" for h in range(24)]
    current_hour = edit_item["เริ่ม"]
    new_start_display = st.selectbox(
        "เวลาเริ่ม",
        hours_display,
        index=current_hour
    )
    new_start_hour = int(new_start_display.split(":")[0])

    new_duration = st.number_input(
        "ระยะเวลา (ชั่วโมง)",
        min_value=1,
        max_value=24,
        value=edit_item["ชั่วโมง"]
    )

    if st.button("💾 บันทึกการแก้ไข"):
        st.session_state.schedules[st.session_state.edit_index] = {
            "วิชา": new_subject,
            "วัน": new_day,
            "เริ่ม": new_start_hour,
            "ชั่วโมง": new_duration
        }

        st.session_state.edit_mode = False
        st.success("แก้ไขเรียบร้อย ✅")
        st.rerun()
