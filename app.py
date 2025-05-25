import streamlit as st
import pandas as pd
import chardet
import zipfile
import os
import shutil
from pathlib import Path
import io
import json

from state_init import init  # 导入初始化方法
state = init()               # 初始化所有状态变量


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
private_msg_dir = UPLOAD_DIR/ "Chat" / "Message" / "Private Chat"
from pathlib import Path


# 🔍 查找包含 chat_id 的消息文件（支持中文命名）
def find_message_file(chat_id: str, msg_dir: Path) -> Path | None:
    for file in msg_dir.glob("*.json"):
        if chat_id in file.stem:
            return file
    return None

# ✨ 提取消息内容（支持多种类型）
def extract_message_content(msg: dict) -> str:
    """
    提取并格式化 post_content / text_content / card_content 等消息字段，结构化输出。
    """
    for key, value in msg.items():
        if not key.endswith("_content"):
            continue

                # 🎯 POST 类型（你确认的结构）
        if key == "post_content" and isinstance(value, dict):
            title = value.get("title", "")
            text = value.get("text", "")
            sources = value.get("source_keys", [])

            parts = []
            if title:
                parts.append(f"【标题】{title}")
            if text:
                parts.append(f"📝 正文：\n{text}")
            if sources:
                parts.append("📎 附件引用：\n" + "\n".join(f"- {src}" for src in sources))

            return "\n\n".join(parts).strip()
            

        # 🧠 CARD 卡片结构
        elif key == "card_content" and isinstance(value, dict):
            title = value.get("title")
            brief = value.get("brief_text")
            return f"{title or ''} {brief or ''}".strip() or "[卡片无内容]"

        # 🧠 TEXT / SYSTEM / FILE 等常规结构
        elif isinstance(value, dict):
            if "text" in value:
                return value["text"]
            elif "file_name" in value:
                return f"[文件] {value['file_name']}"
            elif "title" in value:
                return value["title"]
            else:
                import json
                return json.dumps(value, ensure_ascii=False)

        # 🧠 如果内容是字符串
        elif isinstance(value, str):
            return value

    return "[无结构化内容]"




st.set_page_config(page_title="CSV/JSON 文件工具", layout="wide")


st.title("📂 上传会话文件夹（压缩包）")
uploaded_zip = st.file_uploader("请上传包含会话结构的 zip 文件", type=["zip"])

if uploaded_zip:
    with st.spinner("正在处理压缩包..."):

        # 清空上一次的内容
        if UPLOAD_DIR.exists():
            shutil.rmtree(UPLOAD_DIR)
        UPLOAD_DIR.mkdir(exist_ok=True)

        # 保存上传的 zip 文件
        zip_path = UPLOAD_DIR / "uploaded.zip"
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        # 解压
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(UPLOAD_DIR)

        # 展示解压后的文件结构
        st.success("解压完成，目录结构如下：")

        def show_structure(path: Path, indent: int = 0):
            for p in sorted(path.iterdir()):
                if p.is_dir():
                    st.text("  " * indent + f"📁 {p.name}")
                    show_structure(p, indent + 1)
                else:
                    st.text("  " * indent + f"📄 {p.name}")

        show_structure(UPLOAD_DIR)


        st.markdown("---")
st.header("📄 智能 CSV 上传与自动展示")

uploaded_csv = st.file_uploader("上传 CSV 文件（系统将自动检测编码并展示）", type=["csv"], key="csv_smart")

if uploaded_csv:
    # 原始二进制读取
    raw_data = uploaded_csv.read()

    # 使用 chardet 检测编码
    detected = chardet.detect(raw_data)
    detected_encoding = detected['encoding']
    confidence = detected['confidence']

    st.info(f"检测到编码为：**{detected_encoding}**（置信度：{confidence:.2f}）")

    try:
        # 如果不是 utf-8，则转码
        if detected_encoding.lower() != "utf-8":
            decoded_str = raw_data.decode(detected_encoding)
            utf8_bytes = decoded_str.encode("utf-8")
            csv_io = io.BytesIO(utf8_bytes)
            df = pd.read_csv(csv_io)
            st.warning("⚠️ 原文件编码不是 UTF-8，已自动转码展示。")
        else:
            csv_io = io.BytesIO(raw_data)
            df = pd.read_csv(csv_io)

        # 展示内容在一个“新标签页”中（模拟）
        tabs = st.tabs(["📋 上传页", "📄 CSV 查看页"])
        with tabs[1]:
            st.subheader("📄 CSV 内容预览")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 读取 CSV 时发生错误：{e}")


st.markdown("---")
st.header("💬 会话文件解析与展示")

# ⚠️ 解压后重新定义路径，确保获取到新解压的内容
base_dir = UPLOAD_DIR
chat_dir = base_dir / "Chat"
message_dir = chat_dir / "Message"
conv_dir = chat_dir / "conversation"
private_msg_dir = message_dir / "Private Chat"
group_msg_dir = message_dir / "Group Chat"

if chat_dir.exists():

    tab1, tab2 = st.tabs(["👤 单聊 Private Chat", "👥 群聊 Group Chat"])

    # 工具函数
    def find_message_file(chat_id: str, msg_dir: Path) -> Path | None:
        for file in msg_dir.glob("*.json"):
            if chat_id in file.stem:
                return file
        return None

    # ========= 单聊展示 =========
    private_chat_path = conv_dir / "Private Chat.json"
    if private_chat_path.exists():
        with open(private_chat_path, "r", encoding="utf-8") as f:
            private_chats = json.load(f)

        with tab1:
            st.subheader("📄 单聊会话信息")
            state["valid_private_chats"] = []
            state["skipped_private_chats"] = []
            # ✅ 搜索输入（放在这里）
            search_keyword = st.text_input("🔍 搜索关键词（支持多个词，空格分隔）", key="private_search_keyword")
            search_target = st.selectbox("🔎 搜索范围", ["全部", "发送者", "消息内容"], key="private_search_scope")

            for chat in private_chats:
                msg_path = find_message_file(chat["chat_id"], private_msg_dir)
                if not msg_path or not msg_path.exists():
                   state["skipped_private_chats"].append(chat)
                   continue
                state["valid_private_chats"].append((chat, msg_path))    

            for chat, msg_path in state["valid_private_chats"]:    
                st.markdown("---")
                st.markdown(f"### 💬 会话名称：{chat.get('name', '未知')}")
                st.markdown(f"👥 成员数量：{chat.get('member_count', 0)}")
                st.markdown(f"🌍 是否外部会话：{'是' if chat.get('is_external') else '否'}")

                st.markdown("#### 👤 会话成员：")
                for member in chat.get("members", []):
                    name = member.get("name", "未知成员")
                    ext = member.get("is_external_user", False)
                    tenant = member.get("tenant_name", "")
                    st.markdown(f"- {name} {'(外部成员)' if ext else ''} {'｜租户：' + tenant if tenant else ''}")

                msg_path = find_message_file(chat["chat_id"], private_msg_dir)
                if msg_path and msg_path.exists():
                    with open(msg_path, "r", encoding="utf-8") as f:
                        messages = json.load(f)

                    st.markdown("#### 📩 消息记录：")
                    for msg in messages:
                        sender = msg.get("sender_info", {}).get("name", "未知用户")
                        content = extract_message_content(msg)

                        # ✅ 搜索关键词处理
                        show = True
                        keywords = []
                        if search_keyword:
                           # 多关键词处理
                           keywords = [k.strip().lower() for k in search_keyword.split() if k.strip()]
                           sender_l = sender.lower()
                           content_l = content.lower()

                           # 判断搜索范围
                           if search_target == "发送者":
                              show = any(k in sender_l for k in keywords)
                           elif search_target == "消息内容":
                              show = any(k in content_l for k in keywords)
                           else:
                              show = any(k in sender_l or k in content_l for k in keywords)

                        if not show:
                           continue

                        # ✅ 高亮关键词（把关键词作为参数传入）
                        def highlight(text: str, keywords: list[str]) -> str:
                            import html
                            text = html.escape(text)  # 防止 HTML 注入，先转义原始文本
                            for k in keywords:
                                if k:
                                    k_escaped = html.escape(k)
                                    text = text.replace(
                                        k_escaped,
                                        f'<span style="background-color: #ffe4e1; color: red;"><b>{k_escaped}</b></span>'
                                    )
                            return text

                        sender_disp = highlight(sender, keywords)
                        content_disp = highlight(content, keywords)

                        # ✅ 展示
                        st.markdown("---")
                        st.markdown(f"👤 **发送者**：{sender_disp}", unsafe_allow_html=True)
                        st.markdown(f"📌 **类型**：{msg.get('message_type', '未知类型')}")
                        st.markdown(f"✏️ 编辑：{'是' if msg.get('is_modified') else '否'}")
                        st.markdown(f"❌ 撤回：{'是' if msg.get('is_recalled') else '否'}")
                        with st.expander("📄 消息内容（点击展开）"):
                             st.markdown(content_disp, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ 未找到对应的消息记录文件")
            if state["skipped_private_chats"]:
               with st.expander(f"📦 共跳过 {len(state['skipped_private_chats'])} 个无消息记录的单聊会话，点击展开查看"):
                   for chat in state["skipped_private_chats"]:
                        st.markdown(f"- {chat.get('name', '未知')}（chat_id: `{chat.get('chat_id', '')}`）")        

   # ========= 群聊展示 =========
group_chat_path = conv_dir / "Group Chat.json"
if group_chat_path.exists():
    with open(group_chat_path, "r", encoding="utf-8") as f:
        group_chats = json.load(f)

    with tab2:
        st.subheader("📄 群聊会话信息")
        state["valid_group_chats"] = []
        state["skipped_group_chats"] = []
        # ✅ 搜索输入（放在这里）
        search_keyword = st.text_input("🔍 搜索关键词（支持多个词，空格分隔）", key="group_search_keyword")
        search_target = st.selectbox("🔎 搜索范围", ["全部", "发送者", "消息内容"], key="group_search_scope")


        for chat in group_chats:
            msg_path = find_message_file(chat["chat_id"], group_msg_dir)
            if not msg_path or not msg_path.exists():
             continue  # 🚫 没找到群聊消息记录，跳过展示
        for chat in group_chats:
            msg_path = find_message_file(chat["chat_id"], group_msg_dir)
            if not msg_path or not msg_path.exists():
                state["skipped_group_chats"].append(chat)
                continue
            state["valid_group_chats"].append((chat, msg_path))

        for chat, msg_path in state["valid_group_chats"]:

            st.markdown("---")
            st.markdown(f"### 💬 会话名称：{chat['name']}")
            st.markdown(f"- 群主 ID：{chat.get('owner_user_id', '未知')}")
            member_count = chat.get("member_count", len(chat.get("Members", [])))
            st.markdown(f"- 成员数：{member_count}")
            st.markdown(f"- 是否外部会话：{'是' if chat.get('is_external') else '否'}")

            # 👥 群成员展示（10人以上折叠）
            members = chat.get("members", [])
            if len(members) > 10:
                with st.expander(f"👥 群成员（共 {len(members)} 人，点击展开）"):
                    for member in members:
                        name = member.get("name", "未知成员")
                        is_ext = member.get("is_external_user", False)
                        tenant = member.get("tenant_name", "")
                        st.markdown(f"- {name} {'(外部)' if is_ext else ''} {tenant if is_ext else ''}")
            else:
                st.markdown("#### 👥 群成员：")
                for member in members:
                    name = member.get("name", "未知成员")
                    is_ext = member.get("is_external_user", False)
                    tenant = member.get("tenant_name", "")
                    st.markdown(f"- {name} {'(外部)' if is_ext else ''} {tenant if is_ext else ''}")

            # 📩 群聊消息展示
            msg_path = find_message_file(chat["chat_id"], group_msg_dir)
            if msg_path and msg_path.exists():
                with open(msg_path, "r", encoding="utf-8") as mf:
                    messages = json.load(mf)

                    st.markdown("#### 📩 消息记录：")
                    for msg in messages:
                        sender = msg.get("sender_info", {}).get("name", "未知用户")
                        content = extract_message_content(msg)

                        # ✅ 搜索关键词处理
                        show = True
                        keywords = []
                        if search_keyword:
                           # 多关键词处理
                           keywords = [k.strip().lower() for k in search_keyword.split() if k.strip()]
                           sender_l = sender.lower()
                           content_l = content.lower()

                           # 判断搜索范围
                           if search_target == "发送者":
                              show = any(k in sender_l for k in keywords)
                           elif search_target == "消息内容":
                              show = any(k in content_l for k in keywords)
                           else:
                              show = any(k in sender_l or k in content_l for k in keywords)

                        if not show:
                           continue

                        # ✅ 高亮关键词（把关键词作为参数传入）
                        def highlight(text: str, keywords: list[str]) -> str:
                            import html
                            text = html.escape(text)  # 防止 HTML 注入，先转义原始文本
                            for k in keywords:
                                if k:
                                    k_escaped = html.escape(k)
                                    text = text.replace(
                                        k_escaped,
                                        f'<span style="background-color: #ffe4e1; color: red;"><b>{k_escaped}</b></span>'
                                    )
                            return text

                        sender_disp = highlight(sender, keywords)
                        content_disp = highlight(content, keywords)

                        # ✅ 展示
                        st.markdown("---")
                        st.markdown(f"👤 **发送者**：{sender_disp}", unsafe_allow_html=True)
                        st.markdown(f"📌 **类型**：{msg.get('message_type', '未知类型')}")
                        st.markdown(f"✏️ 编辑：{'是' if msg.get('is_modified') else '否'}")
                        st.markdown(f"❌ 撤回：{'是' if msg.get('is_recalled') else '否'}")
                        with st.expander("📄 消息内容（点击展开）"):
                             st.markdown(content_disp, unsafe_allow_html=True)
            else:
                st.warning("⚠️ 未找到对应的群聊消息记录文件")
        if state["skipped_group_chats"]:
            with st.expander(f"📦 共跳过 {len(state['skipped_group_chats'])} 个无消息记录的群聊会话，点击展开查看"):
                 for chat in state["skipped_group_chats"]:
                      st.markdown(f"- {chat.get('name', '未知')}（chat_id: `{chat.get('chat_id', '')}`）")
else:
    st.warning("⚠️ 请先上传并解压有效的会话压缩包")

st.markdown("---")
st.header("📤 导出会话统计")

import pandas as pd

# 合并导出数据
state["export_data"] = []

for chat, _ in state["valid_private_chats"]:
    state["export_data"].append({
        "会话名称": chat.get("name", "未知"),
        "类型": "单聊",
        "成员数": chat.get("member_count", len(chat.get("Members", []))),
        "是否外部会话": "是" if chat.get("is_external") else "否",
        "chat_id": chat.get("chat_id", "")
    })

for chat, _ in state["valid_group_chats"]:
    state["export_data"].append({
        "会话名称": chat.get("name", "未知"),
        "类型": "群聊",
        "成员数": chat.get("member_count", len(chat.get("Members", []))),
        "是否外部会话": "是" if chat.get("is_external") else "否",
        "chat_id": chat.get("chat_id", "")
    })

# 统计跳过数量（只显示不导出）
skipped_stats = {
    "跳过单聊会话数量": len(state["skipped_private_chats"]),
    "跳过群聊会话数量": len(state["skipped_group_chats"])
}

if state["export_data"]:
    df_export = pd.DataFrame(state["export_data"])
    csv_bytes = df_export.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 导出有效会话信息为 CSV",
        data=csv_bytes,
        file_name="有效会话列表.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ 暂无有效会话可导出")

# 展示统计信息
st.info(f"📊 跳过的会话数：单聊 {skipped_stats['跳过单聊会话数量']}，群聊 {skipped_stats['跳过群聊会话数量']}")


st.markdown("---")
st.header("📤 导出消息详情")
state["message_rows"] = []

# 单聊消息提取
for chat, msg_path in state["valid_private_chats"]:
    with open(msg_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
    for msg in messages:
        state["message_rows"].append({
            "会话类型": "单聊",
            "会话名称": chat.get("name", "未知"),
            "chat_id": chat.get("chat_id", ""),
            "发送者": msg.get("sender_info", {}).get("name", "未知用户"),
            "消息类型": msg.get("message_type", "未知"),
            "是否编辑": "是" if msg.get("is_modified") else "否",
            "是否撤回": "是" if msg.get("is_recalled") else "否",
            "消息内容": extract_message_content(msg)
        })

# 群聊消息提取
for chat, msg_path in state["valid_group_chats"]:
    with open(msg_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
    for msg in messages:
        state["message_rows"].append({
            "会话类型": "群聊",
            "会话名称": chat.get("name", "未知"),
            "chat_id": chat.get("chat_id", ""),
            "发送者": msg.get("sender_info", {}).get("name", "未知用户"),
            "消息类型": msg.get("message_type", "未知"),
            "是否编辑": "是" if msg.get("is_modified") else "否",
            "是否撤回": "是" if msg.get("is_recalled") else "否",
            "消息内容": extract_message_content(msg)
        })

# 如果有消息就导出
if state["message_rows"]:
    df_msg = pd.DataFrame(state["message_rows"])
    msg_csv = df_msg.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 导出所有有效消息详情为 CSV",
        data=msg_csv,
        file_name="消息详情导出.csv",
        mime="text/csv"
    )
else:
    st.warning("⚠️ 暂无有效消息可导出")
