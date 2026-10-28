# Hướng 3 — Popularity Bias Mitigation & Reranking

**Người thực hiện:** Thành viên 3 (Giảng Nguyên)  
**Thời điểm tổng hợp:** 28/10/2026  

**Mục tiêu:** Nhận kết quả gợi ý và ma trận điểm số từ Hướng 2 (Knowledge Graph + LLM), đánh giá mức độ thiên lệch sản phẩm phổ biến (Popularity Bias), và áp dụng thuật toán Reranking nhằm gia tăng sự xuất hiện của các sản phẩm ít phổ biến (Tail items) nhưng vẫn duy trì chất lượng xếp hạng.

---

## 1. Đặt vấn đề & Câu hỏi nghiên cứu
- **Hạn chế của Hướng 2:** Các mô hình gợi ý thường thiên vị quá mức các sản phẩm phổ biến (Head items), khiến sản phẩm ít tương tác (Tail items) bị bỏ quên.
- **Mục tiêu Reranking:**
  1. Giảm độ phổ biến trung bình (**ARP**) trong danh sách gợi ý Top-10.
  2. Tăng tỷ lệ vị trí (**TailShare**) và độ bao phủ sản phẩm ít phổ biến (**TailCoverage**).
  3. Duy trì chất lượng gợi ý cao (**NDCG@10**, **Recall@10**).

---

## 2. Cấu trúc thư mục mã nguồn
- `All_Beauty_Cleaned_Merged_GitHub.xlsx` : Dataset chuẩn đã làm sạch dùng để tính toán độ phổ biến.
- `kg_llm_recommendations_for_member3.csv` : Tập dữ liệu ứng viên bàn giao từ Hướng 2.
- `Direction3_Popularity_Bias.ipynb` : Notebook chính thực thi quy trình Reranking.
- `Direction3_Popularity_Bias.py` : Mã nguồn Python thực thi tự động[span_2](start_span)[span_2](end_span).
- `reranked_top10_direction3.csv` : File kết quả Top-10 gợi ý sau khi Reranking ($\lambda = 0.3$).
- `reranking_comparison_metrics.csv` : Bảng tổng hợp số liệu đo lường theo từng giá trị $\lambda$.

---

## 3. Thuật toán Reranking Đề xuất
Công thức điều chỉnh điểm xếp hạng mới:
$$NewScore(u, i) = Rel(u, i) + \lambda \times TailBonus(i)$$

Trong đó:
- $Rel(u, i)$: Điểm số tương đồng ban đầu từ mô hình Hướng 2 (đã chuẩn hóa Min-Max).
- $TailBonus(i) = \frac{1}{\log(1 + popularity(i))}$: Điểm thưởng bổ sung dựa trên nghịch đảo logarit độ phổ biến của sản phẩm $i$.
- $\lambda$: Hệ số kiểm soát cường độ Reranking ($\lambda \in \{0.0, 0.1, 0.3, 0.5, 0.7\}$).

---

## 4. Kết quả Thực nghiệm & Đánh giá

### Bảng So sánh Chỉ số theo Hệ số Reranking ($\lambda$):

| Hệ số Lambda ($\lambda$) | NDCG@10 | Recall@10 | ARP (Độ phổ biến TB) | TailShare (%) | TailCoverage (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **0.0 (Gốc Hướng 2)** | 0.1380 | 0.1920 | 1204.06 | 23.50% | 20.00% |
| **0.1 (Điều chỉnh nhẹ)** | 0.1372 | 0.1910 | 1200.12 | 26.80% | 23.50% |
| **0.3 (Cấu hình Tối ưu)** | **0.1356** | **0.1890** | **1142.50** | **32.40%** | **28.00%** |
| **0.5 (Mạnh)** | 0.1340 | 0.1870 | 1085.20 | 38.10% | 34.20% |
| **0.7 (Rất mạnh)** | 0.1324 | 0.1850 | 1020.15 | 42.50% | 38.00% |

---

## 5. Biểu đồ trực quan hóa
Biểu đồ phân tích hiệu năng và sự tăng trưởng các chỉ số Tail được lưu tại:
- `arp_by_lambda.png`[span_3](start_span)[span_3](end_span)
- `tail_metrics_by_lambda.png`[span_4](start_span)[span_4](end_span)

![Tăng trưởng TailShare và TailCoverage](tail_metrics_by_lambda.png)

---

## 6. Kết luận & Bàn giao
- Khi chọn cấu hình tối ưu **$\lambda = 0.3$**: Tỷ lệ sản phẩm hiếm xuất hiện (`TailShare`) tăng từ **23.50% lên 32.40%** và độ bao phủ (`TailCoverage`) tăng lên **28.00%**, trong khi chất lượng gợi ý (`NDCG@10`) vẫn được giữ vững ở mức rất cao ($0.1356$).
