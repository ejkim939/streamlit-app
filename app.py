import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configure matplotlib for Korean fonts
plt.rcParams['font.family'] = 'NanumGothic' # Ensure this font is installed in the environment where streamlit runs
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(layout="wide")
st.title('서울 지하철 이용객 분석 대시보드')

# Data loading and preprocessing
@st.cache_data
def load_data():
    df = pd.read_csv('서울지하철.csv', encoding='cp949')
    df['승차총승객수'] = pd.to_numeric(df['승차총승객수'], errors='coerce').fillna(0)
    df['하차총승객수'] = pd.to_numeric(df['하차총승객수'], errors='coerce').fillna(0)
    df['총승객수'] = df['승차총승객수'] + df['하차총승객수']
    df['사용일자'] = pd.to_datetime(df['사용일자'], format='%Y%m%d')
    return df

df = load_data()

# Filter for the latest date
latest_date = df['사용일자'].max()
df_latest = df[df['사용일자'] == latest_date].copy()

st.markdown(f"### 데이터 분석일: {latest_date.strftime('%Y-%m-%d')}")

# 1. Histogram of total passengers
st.subheader('총승객수 분포 히스토그램')
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.hist(df_latest['총승객수'], bins=50, color='skyblue', edgecolor='black')
ax1.set_title(f'총승객수 분포 히스토그램 ({latest_date.strftime("%Y-%m-%d")})', fontsize=15)
ax1.set_xlabel('총승객수', fontsize=12)
ax1.set_ylabel('빈도수', fontsize=12)
ax1.grid(axis='y', alpha=0.75)
st.pyplot(fig1)
plt.close(fig1) # Close the figure to prevent display issues outside streamlit

# 2. Bar chart of high-passenger stations
st.subheader('총승객수 상위 역 분석 (총승객수 >= 80,000)')
df_high_passenger = df_latest[df_latest['총승객수'] >= 80000].sort_values(by='총승객수', ascending=False)

if not df_high_passenger.empty:
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    cmap = plt.colormaps.get_cmap('tab10')

    unique_lines = df_high_passenger['호선명'].unique()
    for i, line in enumerate(unique_lines):
        data = df_high_passenger[df_high_passenger['호선명'] == line]
        ax2.bar(data['역명'], data['총승객수'], color=cmap(i % cmap.N), label=line)

    ax2.set_title('총승객수 상위 역 (총승객수 >= 80,000)', fontsize=15)
    ax2.set_xlabel('역명', fontsize=12)
    ax2.set_ylabel('총승객수', fontsize=12)
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(title='호선명')
    ax2.grid(axis='y', alpha=0.75)
    st.pyplot(fig2)
    plt.close(fig2)
else:
    st.write("총승객수 8만 명 이상인 역이 없습니다.")

# 3. Pie chart of line distribution for high-passenger stations
st.subheader('총승객수 8만 명 이상 역의 호선별 분포')
if not df_high_passenger.empty:
    line_counts = df_high_passenger['호선명'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(10, 10))
    ax3.pie(line_counts, labels=line_counts.index, autopct='%1.1f%%', startangle=140, colors=cmap(range(len(line_counts))))
    ax3.set_title('총승객수 8만 명 이상 역의 호선별 분포', fontsize=15)
    ax3.axis('equal')
    st.pyplot(fig3)
    plt.close(fig3)
else:
    st.write("총승객수 8만 명 이상인 역이 없어 호선별 분포를 표시할 수 없습니다.")

st.markdown("""
## Streamlit 앱 실행 방법
1. 이 코드를 `app.py` 라는 파일로 저장합니다.
2. 터미널을 열고 `app.py` 파일이 있는 디렉토리로 이동합니다.
3. 다음 명령어를 실행합니다: `streamlit run app.py`
""")
