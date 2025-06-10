import tkinter as tk
from tkinter import ttk

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Fakebook UI")
root.geometry("1200x700")
root.configure(bg="#18191a")  # Dark mode màu nền

# ========== Sidebar Trái ==========
sidebar = tk.Frame(root, bg="#242526", width=200)
sidebar.pack(side="left", fill="y")

sidebar_items = [
    "Khôi Vũ",
    "Meta AI",
    "Bạn bè",
    "Kỷ niệm",
    "Đã lưu",
    "Nhóm",
    "Thước phim",
    "Marketplace",
    "Bảng feed",
    "Xem thêm"
]

for item in sidebar_items:
    label = tk.Label(sidebar, text=item, fg="white", bg="#242526", anchor="w", padx=10, pady=8)
    label.pack(fill="x")

# ========== Vùng Giữa ==========
main_area = tk.Frame(root, bg="#18191a")
main_area.pack(side="left", expand=True, fill="both")

status_frame = tk.Frame(main_area, bg="#3a3b3c", pady=10)
status_frame.pack(fill="x", padx=20, pady=10)

status_entry = tk.Entry(status_frame, width=80)
status_entry.insert(0, "Khôi ơi, bạn đang nghĩ gì thế?")
status_entry.pack(padx=10)

story_frame = tk.Frame(main_area, bg="#18191a")
story_frame.pack(fill="x", padx=20, pady=10)

for i in range(5):
    story = tk.Label(story_frame, text=f"Story {i+1}", bg="#3a3b3c", fg="white", width=15, height=6)
    story.pack(side="left", padx=5)

post_frame = tk.Frame(main_area, bg="#242526", pady=10)
post_frame.pack(fill="x", padx=20, pady=10)

post_text = tk.Label(post_frame, text="Trang Nguyen\nShare ngay !!! kkk", fg="white", bg="#242526", anchor="w", justify="left")
post_text.pack(fill="x", padx=10)

# ========== Sidebar Phải ==========
right_sidebar = tk.Frame(root, bg="#242526", width=200)
right_sidebar.pack(side="right", fill="y")

online_friends = [
    "Đăng Khoa", "Nguyễn Anh Nhật", "Thanh Đồng", "Thiện Master",
    "Nguyễn Nam", "Nguyễn Quốc Hậu", "Đạt Lại", "Nguyễn Khánh", "Hoàng Phước"
]

header = tk.Label(right_sidebar, text="Người liên hệ", fg="white", bg="#242526", anchor="w", padx=10, pady=8)
header.pack(fill="x")

for friend in online_friends:
    friend_label = tk.Label(right_sidebar, text=friend + " ●", fg="lightgreen", bg="#242526", anchor="w", padx=10, pady=4)
    friend_label.pack(fill="x")

# Chạy ứng dụng
root.mainloop()
