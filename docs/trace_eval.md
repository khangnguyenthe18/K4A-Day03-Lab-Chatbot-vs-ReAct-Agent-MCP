# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** [Nguyễn Thế Khang]  
> **Mã Sinh Viên / Mã Học viên:** [2A202602964]  
> **Chủ đề Lựa chọn:** [Gym Workout Assistant]  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5/ 5 | có, bước 1: cần nhận diện người dùng, thu thông thông tin về kinh nghiệm tập luyện, chiều cao cân nặng của người dùng, bước 2:  cần xác định lịch tập phù hợp mà người dùng có thể theo vd:3-4 ngày/tuần ,thời gian 1-2 tiếng/ngày, bước 3: cần biết được nơi người dùng có thể tập ví dụ: phòng gym, công viên, ở nhà dùng body weight, bước 4: cần thu thập nhu cầu của người dùng ví dụ: giảm cân, tăng cân, tăng cơ,giảm mỡ..., bước 5: đưa ra lịch tập phù hợp với nhu cầu của người dùng.
| **2. Tool Interaction** | 5/ 5 |có cần kết nối với dữ liệu người tập và hệ thống lưu trữ lịch tập qua MCP server |
| **3. Dynamic Decision**  |4 / 5 | có cần linh hoạt , ví dụ người dùng có thể bận,chấn thương -> đổi lịch tập mới phù hợp . cần thay thế các bài tập để phù hợp cho mỗi người vd:người mới nên tập các bài tập dễ ít chấn thương  |
| **4. Long Horizon Goal** |4 / 5 | có cần duy trì mục tiêu cải thiện xuyên suốt lịch tập
| **TỔNG ĐIỂM AGENTIC FIT** | **18 / 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu hồ sơ thể trạng và mục tiêu tập luyện của hội viên GYM001.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "fitness_profile_query",
    "arguments": {
      "member_id": "GYM001"
    },
    "observation": {
      "status": "SUCCESS",
      "member_id": "GYM001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "age": 24,
        "weight_kg": 70,
        "height_cm": 175,
        "experience_level": "Intermediate (1 năm tập luyện)",
        "target_goal": "Tăng cơ (Hypertrophy)",
        "injuries": "Không có",
        "preferred_days_per_week": 4,
        "trainer": "HLV Tuấn Anh"
      }
    },
    "latency_ms": 115.2
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt (TC02, TC03, TC04, TC05).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
