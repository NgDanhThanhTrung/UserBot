# 🤖 Telegram UserBot: Web-to-Telegram Automation — Edition 2026
### 🛠 Phát triển bởi: [NgDanhThanhTrung](https://github.com/NgDanhThanhTrung)

![Tác giả](https://img.shields.io/badge/Author-NgDanhThanhTrung-blue?style=for-the-badge&logo=telegram)
![Ngôn ngữ](https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python)
![Trạng thái](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/NgDanhThanhTrung/UserBot?style=for-the-badge&color=gold)

Dự án này là một giải pháp tự động hóa đột phá được nghiên cứu và phát triển độc quyền bởi **NgDanhThanhTrung**. Hệ thống cho phép biến tài khoản Telegram cá nhân thành một công cụ thực thi lệnh mạnh mẽ, kích hoạt gửi tin nhắn thông qua các yêu cầu HTTP (URL).

---

## 💡 Bản Quyền & Chất Xám Tác Giả
Đây là sản phẩm trí tuệ dựa trên kinh nghiệm tối ưu hóa quy trình tương tác API của **NgDanhThanhTrung**. 

> **⚡ Thông điệp từ tác giả:** > "Mã nguồn này được chia sẻ với mục đích học tập và hỗ trợ cộng đồng. Tôi hy vọng bạn sẽ tôn trọng chất xám của tôi bằng cách giữ nguyên ghi chú bản quyền và không sử dụng cho các mục đích thương mại trái phép."

---

## 🌟 Tính Năng Nổi Bật (Cập nhật 2026)
* **HTTP Trigger 2.0**: Kích hoạt gửi tin nhắn tức thì bằng cách truy cập URL từ trình duyệt hoặc các dịch vụ hẹn giờ.
* **Multi-Target Control**: Điều khiển linh hoạt nhiều Bot mục tiêu cùng lúc (Ví dụ: `@NgDanhThanhTrung_BOT`).
* **Auto-Numbering Logic**: Tự động chèn số thứ tự `#1`, `#2`... vào nội dung để dễ dàng theo dõi tiến độ và tránh bị Telegram chặn do trùng lặp nội dung.
* **Smart Anti-Spam**: Cơ chế nghỉ ngẫu nhiên (1.5s - 3.5s) giữa các lần gửi nhằm mô phỏng hành vi người dùng thật.
* **Kill Switch**: Lệnh `/stop` giúp ngắt mọi tác vụ đang chạy ngay lập tức để bảo vệ tài khoản.

---

## 🛠 Hướng Dẫn Triển Khai Toàn Diện

### 1. Đẩy mã nguồn lên GitHub
* Khởi tạo Repository này (Khuyến khích để chế độ **Private** để bảo mật thông tin cá nhân).
* Tải các file `main.py` và `requirements.txt` lên.

### 2. Triển khai lên Render (Web Service)
* Kết nối GitHub của bạn với Render.
* Thiết lập các **Environment Variables** (Biến môi trường):
    * `API_ID` & `API_HASH`: Lấy từ [my.telegram.org](https://my.telegram.org).
    * `SESSION_STR`: Chuỗi phiên đăng nhập Telethon (StringSession).

### 3. Duy trì hoạt động (Cron-job.org)
* Sử dụng [cron-job.org](https://cron-job.org) gọi vào địa chỉ `/health` của bạn mỗi 5 phút để Render luôn luôn "thức".

---

## 📖 Cách Sử Dụng (Ví dụ mẫu)

Cấu trúc URL: `https://ten-cua-ban.onrender.com/{tên_bot}/{lệnh}/{số_lần}`

* **Lệnh đơn**: `/NgDanhThanhTrung_BOT/start/1` ➜ UserBot gửi `/start #1`.
* **Lệnh lặp**: `/NgDanhThanhTrung_BOT/work/5` ➜ UserBot gửi 5 tin nhắn từ `#1` đến `#5`.
* **Lệnh có dấu cách**: `/NgDanhThanhTrung_BOT/diem-danh/1` ➜ Hệ thống tự chuyển đổi thành `/diem danh #1`.

---

## 🎁 Ủng Hộ Dự Án

Dự án này hoàn toàn miễn phí và được duy trì bằng tâm huyết. Nếu bạn cảm thấy nó có ý nghĩa và giúp ích được cho công việc của bạn, hãy ủng hộ tác giả bằng cách:

1.  **Tặng 1 sao (Star) ⭐** cho Repository này để giúp dự án lan tỏa hơn.
2.  **Mời tác giả một ly cà phê ☕** qua cổng thanh toán: [https://ngdanhthanhtrung.github.io/Bank/](https://ngdanhthanhtrung.github.io/Bank/)

---

## 💬 Liên Hệ Hỗ Trợ
Mọi thắc mắc hoặc góp ý về tính năng, vui lòng liên hệ:
* **Telegram**: [@NgDanhThanhTrung](https://t.me/NgDanhThanhTrung)

---

## 📜 Điều Khoản Sử Dụng
© 2026 **NgDanhThanhTrung**. Bảo lưu mọi quyền.
1. Tuyệt đối không xóa hoặc chỉnh sửa thông tin bản quyền của tác giả trong mã nguồn.
2. Không sử dụng mã nguồn này cho các hành vi spam độc hại hoặc vi phạm chính sách của Telegram.
3. Tác giả không chịu trách nhiệm về bất kỳ rủi ro hay tổn thất nào phát sinh từ việc sử dụng của bạn.

---
**Cảm ơn bạn đã sử dụng và tôn trọng công lao sáng tạo của NgDanhThanhTrung!**
