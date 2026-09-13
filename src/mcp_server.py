"""
🔌 MODEL CONTEXT PROTOCOL (MCP) SERVER MODULE
Mô phỏng kiến trúc MCP Server (Client-Server Architecture) cung cấp công cụ chuẩn hóa.
"""

import json
import sys
from typing import Dict, Any, List
from tools import TOOLS_SCHEMA, dispatch_tool_call

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class MCPAcademicServer:
    """
    Giả lập MCP Server tuân thủ chuẩn giao thức Model Context Protocol
    """
    def __init__(self, server_name: str = "gym-fitness-mcp-server"):
        self.server_name = server_name
        self.version = "2026.1.0"
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """Trả về danh sách các Tools chuẩn giao thức MCP"""
        return TOOLS_SCHEMA
        
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        [TASK 2.1] HỌC VIÊN HOÀN THIỆN HÀM THỰC THI TOOL TRÊN MCP SERVER
        Thực thi request gọi Tool theo chuẩn MCP JSON-RPC 2.0
        """
        # 1. Gọi hàm dispatch_tool_call(tool_name, arguments) để lấy chuỗi JSON kết quả từ Tool Router
        result_json_str = dispatch_tool_call(tool_name, arguments)
        
        # 2. Chuyển đổi chuỗi JSON kết quả thành Python Dictionary
        try:
            content = json.loads(result_json_str)
        except Exception:
            content = {"raw": result_json_str}
            
        # 3. Đóng gói phản hồi và trả về Dict theo đúng chuẩn giao thức MCP JSON-RPC 2.0
        return {
            "jsonrpc": "2.0",
            "server": self.server_name,
            "tool": tool_name,
            "result": content
        }


if __name__ == "__main__":
    print("==========================================================")
    print("🔌 KIỂM THỬ ĐỘC LẬP MCP SERVER (gym-fitness-mcp-server)")
    print("==========================================================")
    
    server = MCPAcademicServer()
    tools = server.list_tools()
    print(f"✅ Khởi tạo thành công MCP Server: {server.server_name} (Version: {server.version})")
    print(f"📦 Số lượng Tools công bố: {len(tools)}")
    
    # Kiểm tra trạng thái Tool Schema
    fit_tool = next((t for t in tools if t.get("name") == "create_workout_plan"), None)
    if fit_tool and fit_tool.get("parameters", {}).get("properties"):
        print("✅ [TODO 1.2]: Tool 'create_workout_plan' đã có schema đầy đủ.")
    else:
        print("⏳ [TODO 1.2]: Tool 'create_workout_plan' chưa được định nghĩa hoàn chỉnh.")

    # Kiểm tra trạng thái TODO 2.1 (call_tool)
    test_result = server.call_tool("fitness_profile_query", {"member_id": "GYM001"})
    if not test_result or test_result.get("jsonrpc") != "2.0":
        print("⏳ [TODO 2.1]: Hàm call_tool() chưa đúng chuẩn MCP JSON-RPC!")
    else:
        print(f"✅ [TODO 2.1]: Test dispatch tool 'fitness_profile_query' thành công:")
        print(f"   Phản hồi JSON-RPC: {json.dumps(test_result, ensure_ascii=False)}")
