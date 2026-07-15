# HƯỚNG DẪN THAM GIA KHẢO SÁT NGƯỜI DÙNG (USER STUDY GUIDE)
## [DỰ ÁN: DATAGUARD] - [BÀI BÁO: DRAFT 01 - AUDITABILITY GAP]
### 📊 GIAO DIỆN KHẢO SÁT: DATAGUARD USER STUDY PROTOTYPE

Hướng dẫn này giúp người tham gia thực nghiệm (Crowd workers hoặc chuyên gia kiểm thử) nắm bắt quy trình làm khảo sát thực nghiệm đánh giá ba giao diện hỗ trợ kiểm toán nhãn an toàn dữ liệu (**C0 - Cơ bản**, **C1 - Sắp xếp đối chiếu**, và **C2 - Trợ lý AI gợi ý bằng chứng**).

---

## ⚡ QUY TRÌNH THỰC HIỆN KHẢO SÁT QUA 4 BƯỚC KHÁCH QUAN

Trang thực nghiệm chạy trực tuyến Single Page App sẽ đưa bạn qua các bước theo trình tự chuẩn sau:

### Bước 1: Đăng nhập (PID) & Đồng ý tham gia (Consent)
* Nhập mã định danh (PID) được cấp bởi nền tảng tuyển dụng hoặc tự nhập mã định danh cá nhân.
* Đọc thông tin đồng ý tham gia nghiên cứu (Consent).
* Trả lời các câu hỏi ngắn về kinh nghiệm phát triển phần mềm (Developer Experience) và thói quen bảo mật.
* Xem qua một bài hướng dẫn ngắn (Tutorial) để làm quen với cách đối chiếu mã nguồn thực tế của ứng dụng với các tuyên bố nhãn bảo mật trên Google Play.

### Bước 2: Thực hiện kiểm toán ứng dụng qua 3 khối giao diện (C0, C1, C2)
Bạn sẽ lần lượt trải qua 3 khối thực nghiệm (Block) tương ứng với 3 loại giao diện khác nhau:

1. **Khối C0 (Giao diện Cơ bản):** Bạn phải tự tìm kiếm và đối chiếu thông tin thủ công giữa nhãn khai báo và mã nguồn ứng dụng.
2. **Khối C1 (Giao diện Sắp xếp đối chiếu):** Các mục dữ liệu khai báo và bằng chứng mã nguồn được xếp thẳng hàng cạnh nhau để bạn dễ quan sát.
3. **Khối C2 (Giao diện Trợ lý AI):** Giao diện cung cấp thêm gợi ý bằng chứng từ AI. Bạn cần kiểm tra xem các gợi ý này của AI là chính xác (Accept) hay cần chỉnh sửa (Override).

#### 📝 Với mỗi ứng dụng trong mỗi khối, bạn cần đánh giá 4 trục chính (Judgment Axes):
* **Chia sẻ đúng (Share Correctness):** Ứng dụng khai báo chia sẻ dữ liệu có đúng thực tế không?
* **Chia sẻ đủ (Share Completeness):** Ứng dụng khai báo có bị thiếu loại dữ liệu nào bị chia sẻ không?
* **Thu thập đúng (Collection Correctness):** Ứng dụng khai báo thu thập dữ liệu có đúng thực tế không?
* **Thu thập đủ (Collection Completeness):** Ứng dụng khai báo có bị thiếu loại dữ liệu nào bị thu thập không?

*Đồng thời điền mức độ tự tin của bạn (Confidence) và nhập lý do đánh giá ngắn gọn.*

### Bước 3: Trả lời khảo sát phụ sau mỗi khối
* **Khảo sát gánh nặng công việc (NASA-TLX):** Sau khi kết thúc mỗi khối giao diện, bạn cần kéo thanh trượt đánh giá mức độ mệt mỏi về trí óc (Mental Demand), áp lực thời gian (Temporal Demand), và mức độ nỗ lực (Effort).
* **Khảo sát độ tin cậy AI (Thang đo TPA):** Chỉ xuất hiện sau khi kết thúc khối **C2** để đánh giá mức độ tin tưởng của bạn đối với trợ lý AI.

### Bước 4: Đóng góp ý kiến chuyên gia & Nhận Completion Code
* Nhập các phản hồi định tính về ưu/nhược điểm của từng giao diện.
* Hệ thống sẽ hiển thị mã hoàn thành khảo sát (Completion Code) để bạn xác nhận trên hệ thống.

---

## 💡 MẸO ĐỂ LÀM BÀI ĐẠT CHẤT LƯỢNG CAO
1. **Kiểm tra kỹ gợi ý của AI ở khối C2:** AI không phải lúc nào cũng đúng 100%. Hãy chú ý đối chiếu bằng chứng mã nguồn được highlight để đưa ra phán quyết chính xác nhất.
2. **Trả lời đầy đủ tất cả các trục:** Hệ thống yêu cầu bạn phải chọn lựa đủ 4 trục đánh giá và thang điểm tự tin mới cho phép nhấn nút "Next Trial".
3. **Không tải lại trang giữa chừng:** Để tránh làm mất tiến trình và mã PID đang làm, vui lòng không tắt tab hoặc nhấn F5 trong lúc đang làm dở bài khảo sát.

---

## 📊 HƯỚNG DẪN XUẤT DỮ LIỆU DÀNH CHO ADMIN
Dữ liệu khảo sát được lưu trực tiếp vào cơ sở dữ liệu SQLite trên máy chủ Render. Bạn có thể tải file kết quả bằng cách truy cập:
* **Link tải:** `https://dataguard-user-study.onrender.com/api/export?token=tung0903`
* Dữ liệu trả về sẽ chứa đầy đủ 5 bảng: `participants` (Thông tin người làm), `trials` (Kết quả từng lượt test), `tlx` (Chỉ số mệt mỏi), `trust` (Độ tin cậy AI) và `expert_feedback` (Ý kiến đóng góp).
