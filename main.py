import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

st.set_page_config(page_title="Dự đoán Rating Amazon", layout="centered")

st.title("🔍 Dự đoán điểm đánh giá sản phẩm Amazon")
st.caption("Ứng dụng dùng mô hình học máy để dự đoán rating dựa trên giá và giảm giá.")

# ---------- Bước 1: Tải dữ liệu ----------
@st.cache_data
def load_data():
    return pd.read_csv("amazon.csv")

df = load_data()

# ---------- Bước 2: Tiền xử lý dữ liệu ----------
# Chuyển đổi kiểu dữ liệu
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# Xóa null
df = df.dropna(subset=['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count'])

# ---------- Bước 3: Tạo và huấn luyện mô hình ----------
@st.cache_resource
def train_model():
    features = ['discounted_price', 'actual_price', 'discount_percentage', 'rating_count']
    target = 'rating'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    return model, r2

model, r2 = train_model()

st.success(f"✅ Mô hình huấn luyện xong với độ chính xác (R²): {round(r2, 3)}")

# ---------- Bước 4: Nhập dữ liệu người dùng ----------
st.header("📥 Nhập thông tin sản phẩm")

discounted_price = st.number_input("Giá sau giảm (₹)", min_value=0)
actual_price = st.number_input("Giá gốc (₹)", min_value=0)
discount_percentage = st.slider("Giảm giá (%)", 0, 100, 20)
rating_count = st.number_input("Số lượng đánh giá", min_value=0)

# ---------- Bước 5: Dự đoán ----------
if st.button("Dự đoán"):
    input_data = pd.DataFrame({
        'discounted_price': [discounted_price],
        'actual_price': [actual_price],
        'discount_percentage': [discount_percentage],
        'rating_count': [rating_count]
    })
    prediction = model.predict(input_data)[0]
    st.subheader("📈 Kết quả dự đoán:")
    st.success(f"Điểm đánh giá dự đoán: {round(prediction, 2)} ⭐")
