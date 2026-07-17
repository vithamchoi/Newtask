# HƯỚNG DẪN DÁN NHÃN NHANH (LABELING QUICK-GUIDE)
## [DỰ ÁN: DATAGUARD] - [BÀI BÁO: DRAFT 02 - MISMATCH TAXONOMY]
### 🛠️ GIAO DIỆN KIỂM THỬ: PRISM WORKBENCH

Hướng dẫn này dành riêng cho các kiểm thử viên tham gia đánh giá trên hệ thống **PRISM workbench** (Draft 2 của nhóm nghiên cứu **DataGuard**). Nhiệm vụ của bạn là đối chiếu **Nhãn an toàn dữ liệu (cột trái)** của ứng dụng với **Chính sách bảo mật (cột phải)** và đưa ra phán quyết Đúng/Sai, Đầy đủ/Thiếu.

---

## ⚡ CHIẾN THUẬT DÁN NHÃN NHANH TRONG 4 BƯỚC

Để dán nhãn một ứng dụng nhanh chóng (dưới 2 phút), hãy thực hiện theo thứ tự ưu tiên sau:

### Bước 1: Kiểm tra Cảnh báo Đỏ (No-data Alert)
* **Hành động:** Nhìn nhanh xem trên giao diện có xuất hiện **Dòng cảnh báo màu đỏ** (No-data Alert) hay không.
* **Mẹo quyết định nhanh:** Nếu có cảnh báo này, nghĩa là ứng dụng tuyên bố *"Không thu thập/chia sẻ dữ liệu"* trên nhãn nhưng trong chính sách bảo mật lại viết là *"có sử dụng SDK bên thứ ba/thu thập dữ liệu"*. 
  * 👉 **Đánh giá ngay:** Chọn **Incorrect** cho mục tương ứng (Sharing hoặc Collection).

### Bước 2: Kiểm tra Danh sách bên thứ ba (Third-party Panel - D1)
* **Hành động:** Nhìn vào danh sách SDK bên thứ ba xuất hiện ở cột bên trái.
* **Mẹo quyết định nhanh:** 
  * Nếu xuất hiện các dòng có nhãn **[Unlinked]** (màu đỏ) nghĩa là chính sách nhắc tên các SDK này (như AdMob, Crashlytics, Firebase...) nhưng nhãn dữ liệu lại khai báo không chia sẻ.
  * 👉 **Đánh giá ngay:** Chọn **Incorrect** hoặc **Incomplete** cho mục **Sharing**.

### Bước 3: Tìm các đoạn được Highlight màu hổ phách (M3-Lexicon)
* **Hành động:** Cuộn nhanh văn bản chính sách ở cột phải và chú ý đến các từ được tô màu vàng (ví dụ: *“may collect”*, *“reserve the right”*, *“including but not limited to”*).
* **Mẹo quyết định nhanh:** Đây là những từ ngữ ngụy biện/mơ hồ. Nếu ứng dụng dùng các từ này để thu thập dữ liệu tùy tiện nhưng trên nhãn không khai báo rõ ràng.
  * 👉 **Đánh giá ngay:** Chọn **Incorrect** cho mục **Collection correctness** do tính không rõ ràng.

### Bước 4: Trích xuất bằng chứng (Evidence) siêu tốc
* **Hành động:** Khi bạn phát hiện câu văn bản nào trong chính sách chứng minh cho phán quyết sai lệch của ứng dụng, hãy **bôi đen (quét chuột)** câu đó trực tiếp trên màn hình chính sách.
* Hệ thống sẽ tự động ghim câu đó làm bằng chứng mà không cần bạn phải copy-paste thủ công.

---

## 📋 TÓM TẮT ĐỊNH NGHĨA 4 TIÊU CHÍ ĐÁNH GIÁ

Bạn phải tích vào 4 ô tròn trước khi nhấn **Submit verdict**:

| Tiêu chí | Chọn CORRECT / COMPLETE khi | Chọn INCORRECT / INCOMPLETE khi |
|---|---|---|
| **Sharing - correctness** (Độ chính xác chia sẻ) | Nhãn khai báo việc gửi dữ liệu ra ngoài trùng khớp hoàn toàn với thực tế chính sách mô tả. | Chính sách viết có chia sẻ dữ liệu (quảng cáo, SDK bên thứ ba) nhưng nhãn lại ghi "Không chia sẻ". |
| **Sharing - completeness** (Tính đầy đủ chia sẻ) | Khai báo đầy đủ tất cả các loại dữ liệu bị đem đi chia sẻ. | Nhãn khai báo thiếu các mục dữ liệu bị chia sẻ (ví dụ: có gửi ID thiết bị đi nhưng nhãn không ghi). |
| **Collection - correctness** (Độ chính xác thu thập) | Việc thu thập dữ liệu tự khai báo khớp với nội dung chính sách. | Khai báo sai sự thật (Ví dụ: ghi không thu thập Vị trí nhưng chính sách ghi có). |
| **Collection - completeness** (Tính đầy đủ thu thập) | Khai báo đủ tất cả các mục dữ liệu bị thu thập. | Khai báo thiếu các mục dữ liệu bị thu thập mà chính sách có nhắc tới. |

---

## ⚠️ LƯU Ý QUAN TRỌNG KHI LÀM NHIỆM VỤ

### 1. Cách vượt qua các bài hướng dẫn (Tutorial apps)
* **5 ứng dụng đầu tiên (App 1 đến App 5)** là các ứng dụng dùng thử (Tutorial).
* Tại 5 ứng dụng này, nút bấm ở góc phải sẽ hiển thị là **`Next (Tutorial)`**. Bạn chỉ cần chọn nhanh các đánh giá phán quyết và nhấn nút này để chuyển trang (kết quả bài hướng dẫn sẽ không được lưu vào cơ sở dữ liệu).
* Từ **ứng dụng thứ 6 trở đi**, nút sẽ tự động chuyển thành **`Submit verdict`** để ghi nhận kết quả dán nhãn chính thức của bạn vào hệ thống.

### 2. Tránh mở 2 giao diện song song trên cùng một trình duyệt
* **Không mở** link `?build=prism` và `?build=legacy` trên cùng một cửa sổ trình duyệt (ví dụ cùng mở 2 tab trên Chrome bình thường). Do hệ thống dùng chung Session (Cookie), khi bạn làm và chuyển trang ở tab này thì tab kia cũng sẽ tự động bị nhảy trang theo.
* **Cách khắc phục:** Nếu muốn mở song song cả 2 giao diện để đối chiếu và làm độc lập, hãy mở một link ở trình duyệt thường và link còn lại ở **Cửa sổ ẩn danh (Incognito - Ctrl + Shift + N)** hoặc mở bằng **một trình duyệt khác** (như Microsoft Edge, Firefox).

