# Khung slide (≤ 15 trang) — hồ sơ nộp vòng 1 (D17, bản nháp 02/11/2026)

Số liệu điền sau C5 / vòng 0 / vòng 1 (ô **[chờ]**), lấy từ `docs/BAO-CAO-DANH-GIA.md`. Mỗi trang một ý chính, ≤ 40 chữ trên slide.

| # | Tiêu đề | Nội dung chính | Hình / số |
|---|---|---|---|
| 1 | Telesale AI nhớ khách | Tên nhóm, một câu giá trị: "gọi lại không hỏi lại, không báo sai giá" | — |
| 2 | Bài toán | Khách gọi nhiều lần, nhiều kênh; nhân viên quên ngữ cảnh → hỏi lại, báo giá cũ, hứa sai | 3 chỉ số đề: RQR, TSR, HR |
| 3 | Kiến trúc một lượt | router → planner bằng code → generator → guardrails → extractor → bộ nhớ → trace; 2 MCP server | sơ đồ `docs/ARCHITECTURE.md` |
| 4 | Bộ nhớ & Call Brief | Fact có hạn dùng, fact bị thay thế vẫn lưu nguồn; Call Brief dựng < 100 ms | ảnh UI tab Bộ nhớ |
| 5 | Giá chỉ từ tool | Guardrail chặn số tiền không có trong kết quả tool; chặn đọc ngân sách khách như giá bán (B5) | ví dụ BTCL-031 trước/sau |
| 6 | Extractor lai có chứng chỉ | Luật → CERT (nhị phân, kiểm bằng mắt) → Jev chọn nhãn → Qwen trọng tài; định nghĩa slot D10 | tỉ lệ lượt bỏ qua LLM **[chờ]** |
| 7 | Dữ liệu: bộ để sửa tách khỏi bộ để đo | 3 tầng: dev (được nhìn, được sửa) / holdout (đóng băng sha256, chạy một lần) / chuyên dụng (mỗi bộ một chỉ số). Chi tiết ở mục "Trình bày dữ liệu với BTC" bên dưới | sơ đồ 3 tầng + bảng "bộ nào, sửa hay đo, đã chạy mấy lần" |
| 8 | Kết quả chính | full vs baseline trên dev (trung bình 3 lần C5) | TSR / RQR / CCR / HR **[chờ]** |
| 9 | HR có xét SKU | evaluator so giá phụ kiện với giá máy → báo 3 con số | `scripts/hr_by_sku.py` **[chờ]** |
| 10 | Cơ chế cải tiến | gap → đề xuất → người duyệt → nạp → đo → quay lui; chỉ feedback từ dev | sơ đồ `docs/HAM-IMPROVE.md` |
| 11 | Vòng 0 → vòng 1 | dev và **holdout chưa từng nhìn** | bảng `scripts/compare_rounds.py` **[chờ]** |
| 12 | Phân tích lỗi | 12 ca (bảng mục 4 báo cáo): nguyên nhân gốc, cách sửa, ca còn mở | — |
| 13 | Chi phí & latency | p95 ~15 s trên T4 8B-AWQ; chi phí mỗi cuộc gọi | `scripts/cost_report.py` **[chờ]** |
| 14 | Demo C.6 | 3 cuộc gọi: tư vấn → chốt đơn không hỏi lại → hỏi vận đơn | ảnh UI tab Demo |
| 15 | Hạn chế & bước tiếp | dữ liệu mô phỏng, bộ câu thật khác lĩnh vực, Jev là API ngoài, SAMPLE-03 chờ BTC | — |

Video demo 5–8 phút (đề C.6): quay tab Demo C.6 của UI (`streamlit run ui/app.py`, generator Qwen hoặc DeepSeek), sau đó chạy `eval/reference_eval.py` trực tiếp để cho thấy số so với baseline.

## Trình bày dữ liệu với BTC (trang 7, bổ sung 03/11/2026)

Nhóm có nhiều bộ dữ liệu: out_nat, BTC-like v1/v1_1/v2/v2_1, D-7, synth_slots, real_ref, bộ ASR. Liệt kê theo tên dễ khiến BTC nghi ngờ hai điều: chọn bộ nào cho số đẹp, hoặc sửa hệ thống theo chính bộ đo.

**Thông điệp chính:** "Mỗi bộ trả lời một câu hỏi khác nhau, và bộ dùng để sửa luôn tách khỏi bộ dùng để báo số."

### 1. Trên slide: sơ đồ 3 tầng

| Tầng | Bộ | Quy tắc |
|---|---|---|
| **Dev**: được nhìn, được sửa theo | `public_sample` (BTC), out_nat dev, BTC-like v1_1 dev và v2_1 dev, D-7 dev | Mọi sửa đổi chỉ dựa trên tầng này. `improve/collect.py` chặn cứng đường dẫn holdout và `out_nat/test` |
| **Holdout**: không nhìn, chạy một lần | Holdout BTC-like (40 scenario). Holdout v3 nếu D45 được duyệt | Đóng băng bằng sha256 trong `manifest.json`. Chạy sau ngày đóng băng cấu hình. Không sửa theo kết quả |
| **Chuyên dụng**: mỗi bộ đo đúng một năng lực | ASR tập A (sửa luật) / tập B (đo); `real_ref` (200 câu thật, CC BY-NC); `synth_slots`; `rag/qa_labeled.json` | Mỗi bộ gắn với một chỉ số: WER/CER/Entity, F1 slot, precision CERT, Recall@k |

Bảng phụ (cùng trang hoặc phụ lục): mỗi bộ có cột **vai trò, nguồn sinh, số kịch bản, đã chạy mấy lần, đã đóng băng chưa**. Số lần chạy lấy từ `docs/CAU-HINH-DA-CHAY.md`.

### 2. Bốn luận điểm khi nói (khoảng 1 phút)

1. **Không rò rỉ, có bằng chứng kiểm được:**
   - sha256 đóng băng trong manifest;
   - `scripts/check_overlap.py` so 8-gram giữa dữ liệu tự sinh và bộ đo (đợt synth_slots b1: 0 câu trùng; chạy lại cho mọi bộ mới trước khi báo);
   - code chặn feedback từ holdout;
   - con số trong kịch bản lấy từ `eval/mock_tools.py`, không từ LLM; `datagen/validate.py` báo 0 lỗi.
2. **Tự khai những bộ đã "mòn":**
   - `out_nat/test` đã chạy 25 lần với 14 cấu hình nên chỉ còn là số tham khảo, không dùng để chọn cấu hình;
   - holdout v2_1 đã chạy một lần ở D44, chỉ đọc số, không sửa theo;
   - `DATASET.md` mục 8.3 ghi sự cố lỡ thấy dòng template holdout.

   Nhóm tự nói ra thì thành điểm cộng ở tiêu chí 8 (trung thực về hạn chế).
3. **Báo khoảng, lấy mẫu BTC làm thước đo:**
   - đặt TSR Full trên `public_sample` cạnh TSR Full trên bộ tự sinh;
   - chênh lệch giữa hai số là mức sụt dự kiến trên bộ test ẩn;
   - số chính thức **[chờ]**;
   - lần chạy offline 03/11 (chỉ kiểm pipeline) cho thấy dạng chênh lệch: public_sample 85,7 so với 92,9–100 trên các bộ dev tự sinh.
4. **Mỗi bộ dẫn đến một quyết định cụ thể.** Bộ nào không dẫn đến quyết định nào thì gộp hoặc bỏ khỏi slide. Ba ví dụ:
   - D-7 làm lộ 3 lỗi (riêng tư, ý định đặt hàng, cắt địa chỉ). Sau khi sửa: D-7 60 → 93,3, không bộ nào giảm (D05).
   - ASR tập B: Entity Accuracy 42,9%. Nguyên nhân chính là số tiền dạng "1 triệu 590.000" → hướng sửa `asr/itn.py`.
   - `real_ref`: lexicon `approved` nâng F1 slot khách 23,5 → 57,1 trên câu thật (NHAT-KY-2026-11-03 mục 1.2).

### 3. Câu BTC có thể hỏi và cách trả lời

| Câu hỏi | Trả lời ngắn | Bằng chứng |
|---|---|---|
| "Sao nhiều bộ vậy, có chọn bộ cho số đẹp không?" | Báo số trên **mọi** bộ, kể cả bộ thấp nhất. Không so chéo các bộ có đáp án khác nhau (v1 / v1_1 / v2_1) | Bảng trang 8; `CAU-HINH-DA-CHAY.md` |
| "Có sửa hệ thống theo bộ test không?" | Không. Bộ để sửa và bộ để đo tách riêng, có code chặn và có hash đóng băng | `improve/collect.py`; `manifest.json` → `frozen.sha256` |
| "Dữ liệu tự sinh có dễ hơn thực tế không?" | Có, và nhóm đo được mức đó: chênh lệch public_sample so với bộ tự sinh; `real_ref` là câu thật khác lĩnh vực | Trang 8; `DATASET.md` mục 6 |
| "Dữ liệu thật lấy ở đâu, có hợp lệ không?" | Không dùng dữ liệu khách thật. Câu thật duy nhất là CSConDa (CC BY-NC, ghi nguồn, đã che PII, không đưa nguyên bộ vào repo) | `DATASET.md` mục 7, 8.1 |
| "Có train trên dữ liệu này không?" | Không. Dữ liệu chỉ dùng để rút luật, đo và tìm lỗi | `DATASET.md` mục 8.2 |
| "Giọng vùng miền?" | Chưa đạt bằng audio: edge-tts chỉ có 2 giọng chuẩn. Hướng xử lý: TTS vùng miền (D45 mục 3) | `DATASET.md` mục 1, 6 |

### 4. Không nên

- Đưa tên nội bộ (v1_1, v2_1, D-7, BTCL-…) lên slide mà không giải thích. Trên slide chỉ dùng tên vai trò ("dev", "holdout", "câu thật"); tên nội bộ để ở phụ lục.
- Báo một con số 100% đứng một mình. Luôn kèm baseline và số trên `public_sample`.
- Gộp số từ các bản code khác nhau vào một ô. Ghi commit hoặc nhãn lần chạy, như `CAU-HINH-DA-CHAY.md`.
