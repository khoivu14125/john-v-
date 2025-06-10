import streamlit as st

# Tiêu đề và mô tả
st.title("Chào MÀY NHÌN CHÓ J")
st.write("Ứng dụng web đầu tiên của John")

# Biểu mẫu đăng nhập
st.subheader("Đăng nhập")

# Nhập tên người dùng và mật khẩu
username = st.text_input("Tên người dùng")
password = st.text_input("Mật khẩu", type="password")

# Nút đăng nhập
if st.button("Đăng nhập"):
    # Kiểm tra đơn giản
    if username == "admin" and password == "123":
        st.success("Đăng nhập thành công!")
        st.write(f"Chào mừng {username} đến với hệ thống.")
    else:
        st.error("Sai tên đăng nhập hoặc mật khẩu.")
