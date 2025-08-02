import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

st.set_page_config(page_title="Dự đoán điểm đánh giá", page_icon="🔍")
st.title("🔍 Dự đoán điểm đánh giá sản phẩm Amazon")

# Đọc dữ liệu
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("amazon_clean.csv")
        return df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return None

df = load_data()

if df is None or df.empty:
    st.error("❌ Không tìm thấy hoặc không thể đọc dữ liệu 'amazon_clean.csv'.")
    st.stop()

# Hiển thị dữ liệu
if st.checkbox("📊 Hiển thị dữ liệu"):
    st.dataframe(df.head())

# Kiểm tra cột bắt buộc
if 'reviews.text_length' not in df.columns or 'reviews.rating' not in df.columns:
    st.error("❌ Dữ liệu thiếu cột 'reviews.text_length' hoặc 'reviews.rating'.")
    st.stop()

# Lọc dữ liệu hợp lệ
df = df.dropna(subset=['reviews.text_length', 'reviews.rating'])

if len(df) < 5:
    st.warning("⚠️ Không đủ dữ liệu hợp lệ để huấn luyện mô hình.")
    st.stop()

# Huấn luyện mô hình
X = df[['reviews.text_length']]
y = df['reviews.rating']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

score = r2_score(y_test, model.predict(X_test))
st.success(f"✅ Mô hình huấn luyện xong (R²: {score:.2f})")

# Giao diện nhập dự đoán
length = st.number_input("Nhập độ dài đoạn review (số ký tự):", min_value=1, value=100)

if st.button("📈 Dự đoán điểm đánh giá"):
    predicted = model.predict([[length]])[0]
    st.write(f"⭐ Điểm đánh giá dự đoán: **{predicted:.2f}**")
