import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

st.set_page_config(page_title="Dự đoán Rating Amazon", layout="centered")
st.title("🔍 Dự đoán điểm đánh giá sản phẩm Amazon")

# ---------- Bước 1: Load dữ liệu ----------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("amazon.csv")
    except:
        # Dữ liệu mẫu fallback
        df = pd.DataFrame({
            'discounted_price': [599, 299, 999, 799, 399],
            'actual_price': [999, 499, 1999, 1499, 699],
            'discount_percentage': [40, 40, 50, 47, 43],
            'rating': [4.2, 3.8, 4.5, 4.1, 3.9],
            'rating_count': [2200, 1500, 3100, 5000, 1800]
        })
    return df

# GỌI load_data() TRƯỚC KHI DÙNG df
df = load_data()

# ---------- Bước 2: Tiền xử lý ----------
numeric_cols = ['discounted_price', 'actual_price', 'discount_percentage', 'rating', 'rating_count']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=numeric_cols)

# ---------- Bước 3: Huấn luyện mô hình ----------
@st.cache_resource
def train_model():
    X = df[['discounted_price', 'actual_price', 'discount_percentage', 'rating_count']]
    y = df['rating']

    if len(df) < 5:
        return None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    return model, r2

model, r2 = train_model()

if model is None:
    st.error("❌ Không đủ dữ liệu hợp lệ để huấn luyện mô hình.")
    st.stop()

st.success(f"✅ Mô hình huấn luyện thành công. R²: {round(r2, 3)}")

# ---------- Bước 4: Dự đoán ----------
st.header("📥 Nhập thông tin sản phẩm")

discounted_price = st.number_input("Giá sau giảm (₹)", min_value=0)
actual_price = st.number_input("Giá gốc (₹)", min_value=0)
discount_percentage = st.slider("Giảm giá (%)", 0, 100, 20)
rating_count = st.number_input("Số lượt đánh giá", min_value=0)

if st.button("Dự đoán"):
    input_df = pd.DataFrame({
        'discounted_price': [discounted_price],
        'actual_price': [actual_price],
        'discount_percentage': [discount_percentage],
        'rating_count': [rating_count]
    })

    prediction = model.predict(input_df)[0]
    st.subheader("⭐ Dự đoán điểm đánh giá:")
    st.success(f"{round(prediction, 2)} / 5.0")
