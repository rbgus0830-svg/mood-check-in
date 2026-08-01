import streamlit as st
import json
import os
from datetime import date, timedelta
import pandas as pd

FILE_NAME = "mood_data.json"
STUDENT_FILE = "students.json"

WEATHER = {"맑음": "☀️", "구름": "☁️", "흐림": "🌥", "비": "🌧", "천둥": "⛈"}
NEGATIVE_WEATHER = ["비", "천둥"]

# ---------- 데이터 저장/불러오기 (콘솔 버전과 완전 동일) ----------

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_students():
    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_students(students):
    with open(STUDENT_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

# ---------- 페이지 기본 설정 ----------

st.set_page_config(page_title="우리 반 마음 날씨 체크인", page_icon="🌤", layout="centered")
st.title("🌤 우리 반 마음 날씨 체크인")

menu = st.sidebar.radio(
    "메뉴를 선택하세요",
    ["학생 등록", "학생 일괄 등록", "오늘의 마음 날씨 기록하기",
     "오늘 학급 전체 감정 보기", "특정 학생 최근 기록 보기", "🚨 상담 필요 학생 확인"]
)

# ---------- 1. 학생 등록 ----------

if menu == "학생 등록":
    st.subheader("👤 학생 등록")
    students = load_students()
    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("등록할 학생 이름")
        submitted = st.form_submit_button("등록하기")
    if submitted and name:
        if name in students:
            st.warning(f"'{name}' 학생은 이미 등록되어 있습니다.")
        else:
            students.append(name)
            save_students(students)
            st.success(f"'{name}' 학생이 등록되었습니다.")
    st.info(f"현재 등록된 학생 수: {len(students)}명")

# ---------- 2. 학생 일괄 등록 ----------

elif menu == "학생 일괄 등록":
    st.subheader("👥 학생 일괄 등록")
    students = load_students()
    count = st.number_input("등록할 학생 수", min_value=1, max_value=50, value=20)
    prefix = st.text_input("이름 접두사", value="학생")
    if st.button("일괄 등록하기"):
        added = 0
        for i in range(1, int(count) + 1):
            name = f"{prefix}{i}"
            if name not in students:
                students.append(name)
                added += 1
        save_students(students)
        st.success(f"'{prefix}1' ~ '{prefix}{int(count)}' 중 {added}명이 새로 등록되었습니다.")

# ---------- 3. 오늘의 마음 날씨 기록하기 ----------

elif menu == "오늘의 마음 날씨 기록하기":
    st.subheader("📝 오늘의 마음 날씨 기록")
    students = load_students()
    data = load_data()

    if not students:
        st.warning("등록된 학생이 없습니다. 먼저 학생을 등록해주세요.")
    else:
        with st.form("mood_form"):
            name = st.selectbox("이름을 선택하세요", students)
            weather = st.radio(
                "오늘의 기분",
                list(WEATHER.keys()),
                format_func=lambda w: f"{WEATHER[w]} {w}",
                horizontal=True
            )
            memo = st.text_input("한줄 메모 (선택)")
            submitted = st.form_submit_button("기록하기")

        if submitted:
            today = str(date.today())
            if today not in data:
                data[today] = {}
            data[today][name] = {"weather": weather, "memo": memo}
            save_data(data)
            st.success("✅ 기록 완료! 오늘도 솔직하게 말해줘서 고마워요 :)")

            if weather == "천둥":
                st.error(f"🚨 [실시간 알림] '{name}' 학생이 오늘 많이 힘든 상태예요. 관심이 필요할 수 있습니다.")

# ---------- 4. 오늘 학급 전체 감정 보기 ----------

elif menu == "오늘 학급 전체 감정 보기":
    st.subheader("📊 오늘 학급 전체 감정 분포")
    data = load_data()
    students = load_students()
    today = str(date.today())

    if today not in data or len(data[today]) == 0:
        st.info("아직 오늘 기록된 감정이 없습니다.")
    else:
        count = {w: 0 for w in WEATHER}
        for record in data[today].values():
            count[record["weather"]] += 1

        df = pd.DataFrame({"날씨": list(count.keys()), "인원": list(count.values())})
        st.bar_chart(df.set_index("날씨"))

        total = len(data[today])
        st.write(f"총 응답 인원: **{total}명 / {len(students)}명**")

# ---------- 5. 특정 학생 최근 기록 보기 ----------

elif menu == "특정 학생 최근 기록 보기":
    st.subheader("🔍 특정 학생 최근 기록")
    students = load_students()
    data = load_data()

    if students:
        name = st.selectbox("이름을 선택하세요", students)
        records = [(day, rec[name]) for day, rec in data.items() if name in rec]
        records.sort(key=lambda x: x[0], reverse=True)

        if not records:
            st.info(f"'{name}' 학생의 기록이 아직 없습니다.")
        else:
            for day, record in records[:5]:
                memo = record["memo"] if record["memo"] else "없음"
                st.write(f"**{day}** : {WEATHER[record['weather']]} {record['weather']} (메모: {memo})")

# ---------- 6. 상담 필요 학생 자동 감지 ----------

elif menu == "🚨 상담 필요 학생 확인":
    st.subheader("🚨 상담 필요 학생 자동 감지 (최근 3일 기준)")
    data = load_data()
    recent_days = [str(date.today() - timedelta(days=i)) for i in range(3)]

    at_risk = {}
    for day in recent_days:
        if day not in data:
            continue
        for name, record in data[day].items():
            if record["weather"] in NEGATIVE_WEATHER:
                at_risk[name] = at_risk.get(name, 0) + 1

    result = {name: cnt for name, cnt in at_risk.items() if cnt >= 2}

    st.caption(f"기준 기간: {recent_days[-1]} ~ {recent_days[0]}")

    if not result:
        st.success("최근 3일간 상담이 필요해 보이는 학생이 없습니다. 다행이네요 :)")
    else:
        for name, cnt in sorted(result.items(), key=lambda x: -x[1]):
            st.warning(f"⚠️ **{name}** : {cnt}회 (관심과 대화가 필요해 보입니다)")