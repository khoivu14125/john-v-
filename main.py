import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Tiêu đề
st.title("🔍 Dự đoán điểm đánh giá sản phẩm Amazon")

# Tải dữ liệu
@st.cache_data
def load_data():
    return pd.read_csv("amazon_clean.csv")

df = load_data()

# Kiểm tra đủ dữ liệu không
if len(df) < 5:
    st.error("❌ Không đủ dữ liệu hợp lệ để huấn luyện mô hình.")
    st.stop()

# Hiển thị dữ liệu
if st.checkbox("📄 Hiển thị dữ liệu"):
    st.dataframe(df)

# Chọn đặc trưng và mục tiêu
feature_cols = ['reviews.text_length']
target_col = 'reviews.rating'

# Xử lý dữ liệu
X = df[feature_cols]
y = df[target_col]

# Huấn luyện mô hình
model = LinearRegression()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Dự đoán và đánh giá
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)

st.success(f"✅ Mô hình huấn luyện xong với R² = {score:.2f}")

# Nhập dữ liệu người dùng
st.subheader("🔢 Nhập độ dài review để dự đoán điểm rating:")
text_length = st.number_input("Độ dài review", min_value=1)

if st.button("📈 Dự đoán"):
    prediction = model.predict([[text_length]])[0]
    st.write(f"🎯 Dự đoán điểm đánh giá: **{prediction:.2f}**")
