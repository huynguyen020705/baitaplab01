# sinh_du_lieu_cam_bien.py
# Bài Hello World - Sinh dữ liệu giả lập từ nút cảm biến môi trường
# Môn: Mạng cảm biến (ELE14102)
#
# Mỗi mẫu gồm 4 trường:
#   - timestamp: thời điểm đo (giây kể từ lúc bắt đầu)
#   - nhiet_do: nhiệt độ (độ C), dao động quanh 28
#   - do_am:    độ ẩm (%), dao động quanh 65
#   - anh_sang: cường độ ánh sáng (lux), thay đổi theo chu kỳ ngày-đêm
 
import csv
import math
import random
 
 
def sinh_mau(t: int) -> dict:
    """Sinh một mẫu dữ liệu tại thời điểm t (giây).
 
    Dữ liệu mô phỏng có chu kỳ ngày 24h (ở đây ta nén 24h thành 100 mẫu)
    và có nhiễu ngẫu nhiên để giống cảm biến thật.
    """
    # Chu kỳ giả định: 100 mẫu = 1 ngày
    pha = 2 * math.pi * t / 100.0
 
    # Nhiệt độ: trung bình 28 độ, dao động ±3 độ theo chu kỳ ngày
    nhiet_do = 28.0 + 3.0 * math.sin(pha) + random.gauss(0, 0.3)
 
    # Độ ẩm: ngược pha với nhiệt độ (trời nóng thì khô hơn)
    do_am = 65.0 - 5.0 * math.sin(pha) + random.gauss(0, 1.0)
 
    # Ánh sáng: chỉ có ban ngày (bán chu kỳ dương của sin)
    anh_sang_co_so = max(0.0, 800.0 * math.sin(pha))
    anh_sang = anh_sang_co_so + random.gauss(0, 20.0)
    anh_sang = max(0.0, anh_sang)  # ánh sáng không âm
 
    return {
        "timestamp": t,
        "nhiet_do": round(nhiet_do, 2),
        "do_am": round(do_am, 2),
        "anh_sang": round(anh_sang, 2),
    }
 
 
def main():
    # Cố định seed để dữ liệu tái lập được giữa các lần chạy
    random.seed(42)
 
    so_mau = 200  # 2 ngày dữ liệu (mỗi ngày 100 mẫu)
    duong_dan_csv = "du_lieu_cam_bien.csv"
 
    with open(duong_dan_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "nhiet_do", "do_am", "anh_sang"]
        )
        writer.writeheader()
        for t in range(so_mau):
            mau = sinh_mau(t)
            writer.writerow(mau)
 
    print(f"Đã sinh {so_mau} mẫu dữ liệu cảm biến giả lập.")
    print(f"File đầu ra: {duong_dan_csv}")
    print("\nXem 5 mẫu đầu:")
    with open(duong_dan_csv, "r", encoding="utf-8") as f:
        for i, dong in enumerate(f):
            if i > 5:
                break
            print("  " + dong.strip())
 
 
if __name__ == "__main__":
    main()
