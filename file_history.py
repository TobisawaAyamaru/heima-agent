import json
import os
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


def get_history(session_id: str):
	return FileChatMessageHistory(session_id, "./chat_history")


class FileChatMessageHistory(BaseChatMessageHistory):
	def __init__(self, session_id: str, storage_path: str):
		self.session_id = session_id
		self.storage_path = storage_path
		# 完整的文件路径
		self.file_path = os.path.join(self.storage_path, self.session_id)

		# 确保目录存在
		os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

	def add_message(self, message: BaseMessage) -> None:
		"""追加单条消息（RunnableWithMessageHistory 会调用该方法）"""
		all_messages = list(self.messages)
		all_messages.append(message)
		new_messages = [message_to_dict(m) for m in all_messages]

		with open(self.file_path, "w", encoding="utf-8") as f:
			json.dump(new_messages, f, ensure_ascii=False)

	def add_messages(self, messages: Sequence[BaseMessage]) -> None:
		"""批量追加消息"""
		all_messages = list(self.messages)
		all_messages.extend(messages)
		new_messages = [message_to_dict(m) for m in all_messages]

		with open(self.file_path, "w", encoding="utf-8") as f:
			json.dump(new_messages, f, ensure_ascii=False)


	@property
	def messages(self) -> list[BaseMessage]:
		try:
			with open(self.file_path, "r", encoding="utf-8") as f:
				messages_data = json.load(f)
				return messages_from_dict(messages_data)
		except FileNotFoundError:
			return []


	def clear(self) -> None:
		with open(self.file_path, "w", encoding="utf-8") as f:
			json.dump([], f)
