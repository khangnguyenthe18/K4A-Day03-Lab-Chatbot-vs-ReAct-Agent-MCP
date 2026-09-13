"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Chủ đề: Gym Workout Assistant (Hệ thống gợi ý & thiết lập lịch tập Gym cá nhân hóa)
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu hồ sơ thể trạng và mục tiêu hội viên
    {
        "name": "fitness_profile_query",
        "description": "Tra cứu hồ sơ thể trạng, mục tiêu tập luyện, mức độ kinh nghiệm và tiền sử chấn thương của hội viên gym bằng mã hội viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {
                    "type": "string",
                    "description": "Mã hội viên cần tra cứu (ví dụ: 'GYM001', 'GYM002')"
                }
            },
            "required": ["member_id"]
        }
    },
    
    # Tool 2: Thiết lập / Lưu lịch tập cá nhân hóa vào hệ thống
    {
        "name": "create_workout_plan",
        "description": "Thiết lập và lưu lịch tập gym, chương trình tập luyện cá nhân hóa vào hệ thống theo thể trạng và mục tiêu của hội viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "member_id": {
                    "type": "string",
                    "description": "Mã hội viên được cấp lịch tập (ví dụ: 'GYM001')"
                },
                "split_type": {
                    "type": "string",
                    "description": "Phương pháp phân chia lịch tập (ví dụ: 'Push-Pull-Legs', 'Upper-Lower', 'Full-Body')"
                },
                "days_per_week": {
                    "type": "integer",
                    "description": "Số buổi tập mỗi tuần (ví dụ: 3, 4, 5)"
                },
                "target_goal": {
                    "type": "string",
                    "description": "Mục tiêu tập luyện chính (ví dụ: 'Tăng cơ (Hypertrophy)', 'Giảm mỡ (Fat Loss)', 'Sức mạnh (Strength)')"
                },
                "safety_notes": {
                    "type": "string",
                    "description": "Lưu ý an toàn, thay thế bài tập nếu có chấn thương (ví dụ: 'Tránh Squat nặng và nhảy cao do chấn thương gối, thay bằng Leg Press nhẹ')"
                }
            },
            "required": ["member_id", "split_type", "days_per_week"]
        }
    },

    # Giữ tương thích ngược với starter code template nếu cần
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ hoặc lịch hẹn HLV cá nhân.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã định danh người dùng"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn hoặc HLV thể hình"
                }
            },
            "required": ["student_id", "datetime_str"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "GYM001": {
        "full_name": "Nguyễn Văn An",
        "age": 24,
        "weight_kg": 70,
        "height_cm": 175,
        "experience_level": "Intermediate (1 năm tập luyện)",
        "target_goal": "Tăng cơ (Hypertrophy)",
        "injuries": "Không có",
        "preferred_days_per_week": 4,
        "trainer": "HLV Tuấn Anh"
    },
    "GYM002": {
        "full_name": "Trần Thị Bình",
        "age": 22,
        "weight_kg": 58,
        "height_cm": 162,
        "experience_level": "Beginner (Mới bắt đầu)",
        "target_goal": "Giảm mỡ, săn chắc cơ thể",
        "injuries": "Chấn thương khớp gối nhẹ (tránh các bài nhảy mạnh hoặc Squat quá sâu)",
        "preferred_days_per_week": 3,
        "trainer": "HLV Mai Phương"
    },
    # Giữ mã cũ để hỗ trợ các test case tương thích
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    }
}


def execute_fitness_profile_query(member_id: str) -> str:
    """Thực thi tra cứu hồ sơ thể trạng hội viên theo mã hội viên"""
    member = MOCK_DATABASE.get(member_id.strip().upper())
    if member:
        return json.dumps({
            "status": "SUCCESS",
            "member_id": member_id.strip().upper(),
            "data": member
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu hội viên có mã '{member_id}' trong hệ thống."
        }, ensure_ascii=False)


def execute_create_workout_plan(member_id: str, split_type: str, days_per_week: int, target_goal: str = "Tăng cơ", safety_notes: str = "") -> str:
    """Thực thi lưu/thiết lập lịch tập cho hội viên"""
    member = MOCK_DATABASE.get(member_id.strip().upper())
    member_name = member.get("full_name", member_id) if member else member_id
    
    return json.dumps({
        "status": "SUCCESS",
        "plan_id": f"PLAN-{member_id.strip().upper()}-2026",
        "member_id": member_id.strip().upper(),
        "member_name": member_name,
        "split_type": split_type,
        "days_per_week": days_per_week,
        "target_goal": target_goal,
        "safety_notes": safety_notes or "Không có ghi chú đặc biệt",
        "message": f"Đã thiết lập thành công lịch tập {split_type} ({days_per_week} buổi/tuần) cho hội viên {member_name}."
    }, ensure_ascii=False)


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ (tương thích ngược)"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn (tương thích ngược)"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "fitness_profile_query": execute_fitness_profile_query,
    "create_workout_plan": execute_create_workout_plan,
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
