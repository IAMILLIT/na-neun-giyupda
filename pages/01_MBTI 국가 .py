import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI Country Explorer", layout="wide")

# ---------------------------
# 1. 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

st.title("🌍 국가별 MBTI 분포 대시보드")
st.write("Plotly 기반 인터랙티브 시각화 / 국가 선택 → MBTI 비율 막대그래프 표시")

# ---------------------------
# 2. 국가 선택 UI
# ---------------------------
countries = df["Country"].sort_values().unique()
selected_country = st.selectbox("국가를 선택하십시오:", countries)

# ---------------------------
# 3. 선택한 국가의 MBTI 추출
# ---------------------------
row = df[df["Country"] == selected_country].iloc[0]
mbti_df = row.drop(labels=["Country"]).reset_index()
mbti_df.columns = ["MBTI", "Value"]

# 1등 MBTI 찾기
top_type = mbti_df.loc[mbti_df["Value"].idxmax(), "MBTI"]

# ---------------------------
# 4. 색상 설정 : 1등 = 빨간색, 나머지 = 파란톤 그라데이션
# ---------------------------
colors = []
for mbti in mbti_df["MBTI"]:
    if mbti == top_type:
        colors.append("red")             # 1등 빨간색
    else:
        colors.append("rgba(0, 120, 255, 0.5)")  # 나머지 파란 계열(그라데이션 느낌)

# ---------------------------
# 5. Plotly 막대그래프
# ---------------------------
fig = px.bar(
    mbti_df,
    x="MBTI",
    y="Value",
    title=f"{selected_country} MBTI Distribution",
)

# 색상 적용
fig.update_traces(marker_color=colors)

fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    title_font_size=22,
)

# ---------------------------
# 6. 출력
# ---------------------------
st.plotly_chart(fig, use_container_width=True)

st.caption("Made with Streamlit + Plotly")
