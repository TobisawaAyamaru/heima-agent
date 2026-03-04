
"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_md5(md5_str: str):
	"""
	检查传入md5字符串是否创建过
	"""
	if not os.path.exists(config.md5_path):
		#文件不存在
		open(config.md5_path,'w',encoding='utf-8').close()
		return False
	else:
		for line in open(config.md5_path,'r',encoding='utf-8').readlines():
			line = line.strip()
			if line == md5_str:
				return True
		return False


def save_md5(md5_str: str):
	"""保存字符串"""
	with open(config.md5_path,'a',encoding="utf-8") as f:
		f.write(md5_str+'\n')
	pass


def get_string_md5(input_str: str,encoding='utf-8'):
	"""将字符串转为md5字符串"""
	str_bytes = input_str.encode(encoding=encoding)

	md5_obj = hashlib.md5()
	md5_obj.update(str_bytes)
	md5_hex = md5_obj.hexdigest()
	return md5_hex


class KnowledgeBaseService(object):
	def __init__(self):
		os.makedirs(config.persist_directory,exist_ok=True)

		self.chroma = Chroma(
			collection_name=config.collection_name,
			embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
			persist_directory=config.persist_directory
		)

		self.spliter = RecursiveCharacterTextSplitter(
			chunk_size=config.chunk_size ,# 分隔文本段最大长度
			chunk_overlap=config.chunk_overlap,
			separators=config.separators  #分隔符号
		)

	def upload_by_str(self,data,filename):
		"""将字符串向量化并存入数据库"""
		md5_hex=get_string_md5(data)

		if check_md5(md5_hex):
			return "[跳过]内容已经存在"
			
		if len(data) > config.max_split_char_number:
			knowledge_chunk: list[str] = self.spliter.split_text(data)
		else:
			knowledge_chunk=[data]

		metadata = {
			"source": filename,
			"create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"operator":"张三"
		}
		
		#存入数据库
		self.chroma.add_texts(
			knowledge_chunk,
			metadatas = [metadata for _ in knowledge_chunk]
		)
		save_md5(md5_hex)

		return "[成功]内容已经成功载入"

