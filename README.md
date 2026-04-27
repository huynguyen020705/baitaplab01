# Bài Hello World - Mạng cảm biến
 
Sinh viên: Nguyễn Cao Quốc Huy
MSSV: N23DCCI032
Lớp: D23CQCI01-N
 
## Mô tả
 
Project này chứa script sinh dữ liệu cảm biến giả lập (nhiệt độ,
độ ẩm, ánh sáng) cho bài thực hành đầu tiên của môn Mạng cảm biến.
 
## Cách chạy
 
```bash
python sinh_du_lieu_cam_bien.py
```
 
Script sẽ tạo file `du_lieu_cam_bien.csv` với 200 mẫu dữ liệu.
 
## Cấu trúc dữ liệu
 
| Cột | Đơn vị | Mô tả |
|---|---|---|
| timestamp | giây | Thời điểm đo |
| nhiet_do | độ C | Nhiệt độ môi trường |
| do_am | % | Độ ẩm tương đối |
| anh_sang | lux | Cường độ ánh sáng |
