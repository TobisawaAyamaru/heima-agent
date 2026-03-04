from chromadb import Client
from chromadb.config import Settings
import config_data as config

client = Client(
    Settings(
        persist_directory=config.persist_directory # 你的 chroma 存储路径
    )
)

collection = client.get_collection(config.collection_name)

print("向量条数：", collection.count())