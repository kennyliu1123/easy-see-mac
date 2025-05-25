# state_init.py

def init():
    """
    初始化所有用于页面状态管理的变量。
    使用方式：
        from state_init import init
        state = init()
        state["valid_private_chats"].append(...)
    """
    return {
        "valid_private_chats": [],
        "skipped_private_chats": [],
        "valid_group_chats": [],
        "skipped_group_chats": [],
        "export_data": [],
        "message_rows": [],
    }
