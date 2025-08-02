# app.py
import streamlit as st
import pandas as pd
import joblib

# Load mô hình đã huấn luyện (đã lưu trước đó bằng joblib)
model = joblib.load("model.pkl")

st.title("🔍 Dự đoán điểm đánh giá sản phẩm Amazon")

# Nhập liệu
discounted_price = st.number_input("Giá sau giảm (₹)", min_value=0)
actual_price = st.number_input("Giá gốc (₹)", min_value=0)
discount_percentage = st.slider("Giảm giá (%)", 0, 100)
rating_count = st.number_input("Số lượng đánh giá", min_value=0)

if st.button("Dự đoán"):
    input_data = pd.DataFrame({
        'discounted_price': [discounted_price],
        'actual_price': [actual_price],
        'discount_percentage': [discount_percentage],
        'rating_count': [rating_count]
    })
    prediction = model.predict(input_data)[0]
    st.success(f"📈 Điểm đánh giá dự đoán: {round(prediction, 2)} 🌟")
