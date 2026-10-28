# Hướng 2 — Knowledge Graph + LLM Recommendation

**Người thực hiện:** Lê Trần Nhật Huy (Member 2)  
**Thời điểm tổng hợp:** 24/10/2026  

**Mục tiêu:** Kế thừa baseline và danh sách ứng viên từ Member 1, tích hợp tri thức từ Knowledge Graph (KG) và thông tin ngữ nghĩa từ Large Language Model (LLM) nhằm cải thiện khả năng biểu diễn quan hệ sản phẩm và chất lượng xếp hạng gợi ý.

---

## 1. Đặt vấn đề (Problem Statement)
- Các phương pháp Lọc cộng tác (Collaborative Filtering - CF) truyền thống chỉ dựa vào lịch sử tương tác giữa Người dùng - Sản phẩm.
- **Hạn chế:** Bỏ qua các thông tin mô tả phong phú từ metadata của sản phẩm (thương hiệu, danh mục, thuộc tính) và dễ gặp phải sự cố "Khởi động lạnh" (Cold-start) khi dữ liệu tương tác còn ít.

---

## 2. Quá trình thực hiện & Phương pháp triển khai
1. **Thu thập & Tiền xử lý dữ liệu:** Xử lý tập dữ liệu Amazon (`All_Beauty`) gồm metadata (`brand`, `category`) và lịch sử tương tác (`user_id`, `parent_asin`, `rating`, `timestamp`).
2. **Xây dựng Knowledge Graph (KG):** Tạo các bộ ba tri thức (*Triples*) kết nối `(Product, HAS_BRAND, Brand)` và `(Product, BELONGS_TO, Category)` bằng `NetworkX`.
3. **Tích hợp LLM (Review & Mô tả):** Sử dụng LLM để trích xuất embedding ngữ nghĩa từ các bài đánh giá (Reviews) và mô tả chi tiết sản phẩm.
4. **Cơ chế Xếp hạng Gợi ý:** Tích hợp điểm tương đồng đồ thị KG và điểm ngữ nghĩa LLM vào danh sách sản phẩm ứng viên từ Baseline (Member 1).

---

## 3. Nội dung & Mã nguồn (Source Code)
- `Direction2_KnowledgeGraph.ipynb`: Mã nguồn Python xử lý, vẽ đồ thị tri thức NetworkX, đánh giá 3 cấu hình và xuất file bàn giao.
- `kg_triples_csv.ipynb`: Mã nguồn tự động trích xuất file bộ ba tri thức (`kg_triples.csv`).
- `All_Beauty_Cleaned_Merged_GitHub.xlsx`: Tập dữ liệu chuẩn đã làm sạch dùng cho huấn luyện và liên kết đồ thị.

---

## 4. Thực nghiệm & Đánh giá (So sánh 3 cấu hình)
Thực nghiệm đo lường trên cùng giao thức đánh giá Top-K ($K \in \{5, 10\}$):

| Chỉ số (Metric) | Baseline (Member 1) | Baseline + KG | Baseline + KG + LLM | Mức cải thiện (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Precision@5** | 0.0420 | 0.0680 | **0.0850** | **+102.38%** |
| **Recall@5** | 0.0650 | 0.1120 | **0.1450** | **+123.08%** |
| **NDCG@5** | 0.0510 | 0.0890 | **0.1180** | **+131.37%** |
| **Precision@10** | 0.0310 | 0.0510 | **0.0640** | **+106.45%** |
| **Recall@10** | 0.0980 | 0.1540 | **0.1920** | **+95.92%** |
| **NDCG@10** | 0.0620 | 0.1050 | **0.1380** | **+122.58%** |

### Biểu đồ So sánh 3 Cấu hình:
![So sánh Baseline vs KG vs LLM](comparison_baseline_vs_kg.png)

---

## 5. Đầu ra & Điều kiện bàn giao cho Member 3
- **KG & Triples Data:** Tập bộ ba tri thức (`kg_triples.csv`) và file metadata làm sạch (`All_Beauty_Cleaned_Merged_GitHub.xlsx`).
- **Source Code:** Notebook `Direction2_KnowledgeGraph.ipynb` thực hiện dựng KG, trích xuất ngữ nghĩa LLM và tính chỉ số Top-K.
- **Danh sách bàn giao Member 3:** File kết quả xếp hạng (`kg_llm_recommendations_for_member3.csv`) chứa danh sách gợi ý, điểm số (`score`), và schema định dạng chuẩn để Member 3 tái sử dụng đánh giá *Popularity Bias* và thử nghiệm *Reranking*.

---

## 6. Khoảng trống nghiên cứu & Định hướng phát triển (Chuyển sang Hướng 3)
- **Khoảng trống của Hướng 2:** Đồ thị tri thức tĩnh chưa phản ánh được sự thay đổi theo thời gian của hành vi người dùng và chưa tối ưu hoàn toàn ngữ nghĩa văn bản phức tạp.
- **Định hướng phát triển:** Nâng cấp lên **Hướng 3: Đồ thị tri thức theo thời gian (Temporal Knowledge Graph - TKG) kết hợp LLM** để bổ sung nhãn thời gian (*Timestamp*) giúp hệ thống gợi ý thích ứng tốt hơn theo từng giai đoạn.


---

## 7. Hướng 3 — Popularity Bias Mitigation & Reranking (Hoàn tất)

**Mục tiêu:** Nhận kết quả gợi ý từ Hướng 2 (KG + LLM), đánh giá mức độ thiên lệch sản phẩm phổ biến và áp dụng thuật toán Reranking nâng cao sự xuất hiện của sản phẩm ít phổ biến (Tail items).

### Bảng Kết Quả Thực Nghiệm Reranking Theo Hệ Số $\lambda$:

| Lambda ($\lambda$) | NDCG@10 | Recall@10 | ARP (Độ phổ biến TB) | TailShare (%) | TailCoverage (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.0 (Gốc Hướng 2)** | 0.1380 | 0.1920 | 1204.06 | 23.50% | 20.00% |
| **0.1 (Nhẹ)** | 0.1372 | 0.1910 | 1200.12 | 26.80% | 23.50% |
| **0.3 (Tối ưu)** | **0.1356** | **0.1890** | **1142.50** | **32.40%** | **28.00%** |
| **0.5 (Mạnh)** | 0.1340 | 0.1870 | 1085.20 | 38.10% | 34.20% |
| **0.7 (Rất mạnh)** | 0.1324 | 0.1850 | 1020.15 | 42.50% | 38.00% |

### Đầu ra Hướng 3 đã đóng gói:
- `Direction3_Popularity_Bias.py`: Code thực thi quy trình Reranking.
- `reranked_top10_direction3.csv`: Danh sách Top-10 gợi ý sau khi Reranking ($\lambda = 0.3$).
- `reranking_comparison_metrics.csv`: Bảng tổng hợp số liệu đo lường theo từng giá trị $\lambda$.
- `arp_by_lambda.png` & `tail_metrics_by_lambda.png`: Biểu đồ phân tích thiên lệch độ phổ biến.
