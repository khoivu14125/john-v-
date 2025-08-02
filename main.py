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
    try:
        df = pd.read_csv("amazon.csv")
    except:
        # Dataset mẫu nếu không có file hoặc lỗi định dạng
        df = pd.DataFrame({
            'discounted_price': [599, 299, 999, 799, 399],
            'actual_price': [999, 499, 1999, 1499, 699],
            'discount_percentage': [40, 40, 50, 47, 43],
            'rating': [4.2, 3.8, 4.5, 4.1, 3.9],
            'rating_count': [2200, 1500, 3100, 5000, 1800]
        })
    return df

df = load_data()

# ---------- Bước 2: Tiền xử lý dữ liệu ----------
for col in ['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count'])

# ---------- Bước 3: Tạo và huấn luyện mô hình ----------
@st.cache_resource
def train_model():
    features = ['discounted_price', 'actual_price', 'discount_percentage', 'rating_count']
    target = 'rating'

    X = df[features]
    y = df[target]

    if len(X) < 5:
        return None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    return model, r2

model, r2 = train_model()

if model is None:
    st.error("❌ Dữ liệu không đủ để huấn luyện mô hình. Cần ít nhất 5 dòng dữ liệu hợp lệ.")
    st.stop()

st.success(f"✅ Mô hình đã huấn luyện xong với độ chính xác (R²): {round(r2, 3)}")

# ---------- Bước 4: Nhập thông tin sản phẩm ----------
st.header("📥 Nhập thông tin sản phẩm để dự đoán")

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
    st.success(f"⭐ Điểm đánh giá dự đoán: {round(prediction, 2)}")
