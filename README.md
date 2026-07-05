# Personal site & digital card — Ngan Nguyen Hoang Thanh

Trang cá nhân kiêm danh thiếp điện tử, **1 file HTML** (`index.html`), giao diện "bầu trời" xanh da trời — ban ngày trời mây, ban đêm trời sao (nút 🌙/☀️ góc phải để đổi).

## Cấu trúc
```
namecard/
├─ index.html        ← toàn bộ trang (sửa ở đây)
├─ assets/
│  ├─ avatar.jpg     ← ảnh đại diện (đã copy từ "ảnh đại diện.jpg")
│  ├─ cover.jpg      ← ảnh bìa mèo (đã copy từ "cat wallpaper.jpg")
│  ├─ qr-phone.png   ← (tùy chọn) ảnh QR số điện thoại
│  ├─ qr-whatsapp.png← (tùy chọn) ảnh QR WhatsApp
│  ├─ qr-line.png    ← (tùy chọn) ảnh QR LINE
│  ├─ qr-zalo.png    ← (tùy chọn) ảnh QR Zalo
│  └─ qr-viber.png   ← (tùy chọn) ảnh QR Viber
└─ README.md
```

## Xem thử
Nhấp đúp `index.html`. Cần có mạng để hiển thị mã QR.

## Sửa thông tin
Mở `index.html`, tìm `const profile = { ... }` gần cuối file — sửa trực tiếp: tên, tagline, About, lĩnh vực, công bố, liên hệ, link (Scholar, LinkedIn...).

## Thêm ảnh QR thật của từng app (quan trọng)
Hiện các mã QR đang **tự sinh từ đường link**. WhatsApp / Zalo / Phone thì quét là thêm được bạn. Riêng **LINE và Viber** nên dùng ảnh QR riêng của bạn:
1. Chụp/lưu ảnh QR trong từng app (WhatsApp, LINE, Zalo, Viber, QR số điện thoại).
2. Lưu vào thư mục `assets/` đúng tên: `qr-whatsapp.png`, `qr-line.png`, `qr-zalo.png`, `qr-viber.png`, `qr-phone.png`.
3. Xong — trang sẽ tự dùng ảnh đó thay cho QR tạm.

## Đưa lên GitHub Pages (giống trang tham khảo `*.github.io`)
1. Tạo repo tên `<username>.github.io` (hoặc repo bất kỳ).
2. Đẩy toàn bộ thư mục này lên nhánh `main`.
3. Settings → Pages → Source: `main` / `/root` → Save.
4. Truy cập `https://<username>.github.io/`.

**Nhanh hơn:** kéo-thả cả thư mục `namecard` vào https://app.netlify.com/drop → có link ngay.

## Mã QR "Open my card"
Mã QR lớn mã hóa **đường dẫn của trang này**, nên hãy deploy trước rồi mở bằng link công khai — khi đó người khác quét sẽ mở đúng trang online của bạn.

## Ghi chú
- Hai ảnh gốc `ảnh đại diện.jpg` và `cat wallpaper.jpg` đã được copy vào `assets/` (tên không dấu để deploy không lỗi); có thể xóa bản gốc nếu muốn.
- LinkedIn đã được thêm thật.
