# huan_luyen_mlflow.py
# Bài Hello World với MLflow
# Mô phỏng "huấn luyện" model phân loại bất thường trên dữ liệu cảm biến
# Mọi metric đều giả lập - mục tiêu là thấy MLflow ghi nhật ký
 
import csv
import os
import random
 
import mlflow
 
 
def doc_du_lieu(duong_dan_csv: str):
    """Đọc file CSV dữ liệu cảm biến đã sinh ở phần trước."""
    mau_list = []
    with open(duong_dan_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mau_list.append(row)
    return mau_list
 
 
def huan_luyen_gia_lap(
    so_mau: int,
    learning_rate: float,
    so_epoch: int,
):
    """Hàm 'huấn luyện' giả - sinh metric ngẫu nhiên có xu hướng giảm dần.
 
    Trả về danh sách metric theo từng epoch.
    """
    metrics = []
    # Loss khởi đầu phụ thuộc learning_rate (lr lớn -> loss giảm nhanh hơn
    # nhưng không ổn định, lr nhỏ -> loss giảm chậm)
    he_so_giam = learning_rate * 10  # ép cho dễ thấy ảnh hưởng
 
    for epoch in range(so_epoch):
        # Loss giảm dần kiểu hàm mũ
        loss = (1.0 / (1 + he_so_giam * epoch)) + random.uniform(-0.02, 0.02)
        # Accuracy tăng dần, max 0.95
        acc = min(0.95, 0.5 + 0.04 * epoch * (learning_rate / 0.01))
        acc += random.uniform(-0.01, 0.01)
        metrics.append({"loss": loss, "accuracy": acc})
    return metrics
 
 
def main():
    # 1. Đọc dữ liệu giả đã sinh ở Phần VIII
    duong_dan_csv = "du_lieu_cam_bien.csv"
    if not os.path.exists(duong_dan_csv):
        print("Chưa có file du_lieu_cam_bien.csv.")
        print("Hãy chạy sinh_du_lieu_cam_bien.py trước.")
        return
 
    du_lieu = doc_du_lieu(duong_dan_csv)
    print(f"Đã đọc {len(du_lieu)} mẫu dữ liệu.")
 
    # 2. Cấu hình MLflow trỏ tới server đang chạy ở cổng 5000
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("hello-mang-cam-bien")
 
    # 3. Cấu hình thực nghiệm
    learning_rate = 0.1
    so_epoch = 20
    batch_size = 16
 
    # 4. Bắt đầu một run trong MLflow
    ten_run = "run-thu-nghiem-3"
    with mlflow.start_run(run_name=ten_run):
        # Ghi siêu tham số
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("so_epoch", so_epoch)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("so_mau_du_lieu", len(du_lieu))
 
        # Ghi tag (nhãn) cho run
        mlflow.set_tag("mssv", "N21DCDT001")
        mlflow.set_tag("loai_model", "phan-loai-bat-thuong-gia-lap")
 
        # Huấn luyện giả lập và ghi metric mỗi epoch
        random.seed(42)
        metrics = huan_luyen_gia_lap(
            so_mau=len(du_lieu),
            learning_rate=learning_rate,
            so_epoch=so_epoch,
        )
        for epoch, m in enumerate(metrics):
            mlflow.log_metric("loss", m["loss"], step=epoch)
            mlflow.log_metric("accuracy", m["accuracy"], step=epoch)
 
        # Ghi accuracy cuối cùng làm metric tổng kết
        mlflow.log_metric("accuracy_cuoi", metrics[-1]["accuracy"])
 
        # Lưu một artifact - file kết quả tổng hợp
        os.makedirs("outputs", exist_ok=True)
        duong_dan_kq = "outputs/ket_qua_run.txt"
        with open(duong_dan_kq, "w", encoding="utf-8") as f:
            f.write("KẾT QUẢ HUẤN LUYỆN GIẢ LẬP\n")
            f.write(f"learning_rate = {learning_rate}\n")
            f.write(f"so_epoch = {so_epoch}\n")
            f.write(f"batch_size = {batch_size}\n")
            f.write(f"accuracy cuối cùng = {metrics[-1]['accuracy']:.4f}\n")
            f.write(f"loss cuối cùng = {metrics[-1]['loss']:.4f}\n")
        mlflow.log_artifact(duong_dan_kq)
 
        # Lưu cả file dữ liệu đầu vào để truy vết
        mlflow.log_artifact(duong_dan_csv)
 
        print(f"Đã ghi run '{ten_run}' vào MLflow.")
        print("Mở http://localhost:5000 để xem chi tiết.")
 
 
if __name__ == "__main__":
    main()
