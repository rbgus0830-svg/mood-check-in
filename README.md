# 🌤 우리 반 마음 날씨 체크인

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mood-check-in.streamlit.app/)

🔗 **바로가기**: https://mood-check-in.streamlit.app/

## 소개
이 프로젝트는 학생이 매일 자신의 기분을 5단계 날씨(맑음~천둥)로 선택해 기록하면,
이를 누적 저장하여 학급 전체의 감정 분포와 개별 학생의 정서 변화 추이를
시각적으로 보여주는 Streamlit 기반 웹 프로그램입니다.
특히 부정적 감정이 연속으로 나타나는 학생을 자동으로 감지해
담임교사에게 알려주는 기능을 핵심으로 합니다.

## 주요 기능
- 학생 개별/일괄 등록 (한 명씩 등록 또는 여러 명 한 번에 등록)
- 오늘의 마음 날씨 기록 (5단계 감정 선택 + 한줄 메모, "천둥" 선택 시 즉시 알림)
- 오늘 학급 전체 감정 분포 시각화 (막대그래프)
- 특정 학생 최근 기록 조회 (최근 5개, 최신순)
- 상담 필요 학생 자동 감지 (최근 3일간 부정 감정 2회 이상 학생 자동 필터링)

## 사용 방법

### 1) 웹에서 바로 사용하기 (설치 불필요)
아래 링크에 접속하면 바로 사용할 수 있습니다.
👉 https://mood-check-in.streamlit.app/

### 2) 로컬에서 직접 실행하기
1. 저장소를 다운로드(clone)합니다.

2. git clone https://github.com/rbgus0830-svg/mood-check-in.git
cd mood-check-in

3. 필요한 라이브러리를 설치합니다.
    pip install -r requirements.txt

4. 아래 명령어로 앱을 실행합니다.
    streamlit run app.py

## 라이선스
MIT License














