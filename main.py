import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(
    "최근 1년간 박스오피스 10위권에 든 영화 가운데, 해당 기간에 개봉한 216편의 데이터를 이용합니다."
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)

    # genre 열에 세로막대(|) 기호로 여러 장르가 적힌 경우, 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # 개봉일(openDt)을 여덟 자리 숫자(YYYYMMDD)에서 날짜형으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")

    return df


df = load_data()

with st.expander("원본 데이터 미리보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# 1. 장르별 영화 편수 (도넛 그래프)
# ------------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "genre", "genre": "count"})
)
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
    textinfo="percent+label",
)
fig_genre.update_layout(legend_title_text="장르")

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 적어 보세요.")

st.divider()

# ------------------------------------------------------------------
# (다음 그래프를 추가할 자리)
# ------------------------------------------------------------------
# st.header("2. ...")
# ...
# st.markdown("**이 그래프로 알 수 있는 것**")
# st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 적어 보세요.")
