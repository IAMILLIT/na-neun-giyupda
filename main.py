import streamlit as st

# Baskin-Robbins 스타일 키오스크 - Streamlit 단일 파일 앱
# 외부 라이브러리 없이 Streamlit만 사용합니다.
# 한국어(하십시오체) 친절한 안내와 이모지를 포함합니다.

st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", layout="centered")

st.title("🍨 베스킨라빈스 키오스크")
st.markdown("안녕하세요! 주문을 도와드리겠습니다. 아래에서 선택해주십시오. 😊")

# 1) 매장 식사 여부
dine_choice = st.radio("1) 매장에서 드시겠습니까, 아니면 포장해가시겠습니까?", ("매장 식사 (포크/스푼 제공)", "포장 (테이크아웃)"))

# 2) 용기 선택 (용기별 최대 스쿱 수 정의)
containers = {
    "싱글 컵 (1스쿱)": 1,
    "더블 컵 (2스쿱)": 2,
    "파인트 (4스쿱) - 테이크아웃 적합": 4,
    "쿼터 (8스쿱) - 가족용": 8,
    "와플콘 (1~2스쿱)": 2,
}

st.subheader("2) 용기를 선택하십시오 🧁")
container = st.selectbox("용기 선택", list(containers.keys()))
max_scoops = containers[container]

# 3) 맛 선택: 전체 맛 목록 제공, 용기에 맞춰 선택 수 제한 검사
all_flavors = [
    "바닐라", "초콜릿", "스트로베리", "쿠키앤크림", "민트초코칩",
    "그린티", "피스타치오", "카라멜", "녹차", "아몬드",
    "망고", "요거트", "라즈베리 소르베", "레몬 소르베"
]

st.subheader(f"3) 아이스크림 맛을 선택하십시오 (최대 {max_scoops}개) 🍦")
selected = st.multiselect("맛 선택 (스쿱 수에 맞춰 선택) — 선택한 맛이 곧 각 스쿱이 됩니다.", all_flavors, default=None)

# 만약 사용자가 용기보다 많은 맛을 선택하면 경고를 보여주고 주문 버튼을 비활성화
if len(selected) > max_scoops:
    st.warning(f"선택하신 맛이 용기 허용 스쿱 수 ({max_scoops})를 초과했습니다. {max_scoops}개 이하로 선택해주십시오.")

# 4) 가격 계산
# 가격 정책 (간단하게 설계): 1스쿱 당 2,500원
PRICE_PER_SCOOP = 2500
# 포장 용기 추가 요금(포장일 때만 적용)
TAKEOUT_FEE = 500

scoops = len(selected)
if scoops == 0:
    st.info("아직 맛을 선택하지 않으셨습니다. 최소 1개를 선택하십시오. 🧐")

subtotal = scoops * PRICE_PER_SCOOP
pack_fee = TAKEOUT_FEE if "포장" in dine_choice else 0
total = subtotal + pack_fee

st.subheader("4) 주문 요약 및 결제 💳")
col1, col2 = st.columns([2,1])
with col1:
    st.write(f"- 매장 여부: **{dine_choice}**")
    st.write(f"- 용기: **{container}** (허용 스쿱: {max_scoops})")
    st.write(f"- 선택한 맛 ({scoops}개): {', '.join(selected) if selected else '없음'}")
with col2:
    st.write(f"소계: {subtotal:,}원")
    st.write(f"포장비: {pack_fee:,}원")
    st.markdown(f"### 총합: {total:,}원 💸")

# 5) 결제 방식 선택
payment = st.radio("결제 방식 선택", ("현금", "카드", "결제 취소"))

# 결제 버튼 활성화 조건: 최소 1스쿱 선택 및 선택 수가 용기 허용 범위 내여야 함
can_pay = (scoops > 0) and (scoops <= max_scoops) and (payment != "결제 취소")

if st.button("결제 진행하기 ✅"):
    if payment == "결제 취소":
        st.error("결제를 취소하셨습니다. 처음부터 다시 선택해주십시오. 🚫")
    elif scoops == 0:
        st.error("맛을 최소 1개 선택해야 합니다. 🍨")
    elif scoops > max_scoops:
        st.error(f"선택한 맛이 용기 허용 스쿱 수 ({max_scoops})를 초과합니다. 용기를 바꾸거나 맛 수를 줄여주십시오.")
    else:
        # 결제 성공 시 영수증 출력
        st.success("결제가 완료되었습니다. 감사합니다! 🎉")
        st.markdown("---")
        st.subheader("🧾 영수증")
        st.write(f"매장 여부: {dine_choice}")
        st.write(f"용기: {container}")
        st.write(f"맛: {', '.join(selected)}")
        st.write(f"스쿱 수: {scoops}")
        st.write(f"결제 방식: {payment}")
        st.write(f"총 결제 금액: **{total:,}원**")
        st.markdown("---")
        st.info("카운터에서 상품을 받아가시기 바랍니다. 행복한 하루 되십시오! 😊")

# 보조 기능: 주문 초기화
if st.button("주문 초기화 🔁"):
    st.experimental_rerun()

# 하단 안내
st.caption("제작: Streamlit 키오스크 데모 — 외부 라이브러리 미사용 | 이 데모는 교육/시연용입니다.")
