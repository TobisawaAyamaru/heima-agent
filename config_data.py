
md5_path = "./md5.text"


#Chroma
collection_name = "rag"
persist_directory = "./chroma_db"



#spliter
chunk_size = 100
chunk_overlap = 20
separators = ["\n\n","\n",",","|","?",".","。","，","\r\n"]


max_split_char_number=1000


#
similarity_threshold = 1  #返回检索的数量