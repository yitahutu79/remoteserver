from llama_index.indices.keyword_table.retrievers import KeywordTableSimpleRetriever
from llama_index.indices.keyword_table.simple_base import SimpleKeywordTableIndex
from llama_index.query_engine import CustomQueryEngine
from llama_index.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.retrievers import BaseRetriever, VectorIndexRetriever
from llama_index.response_synthesizers import (
    get_response_synthesizer,
    BaseSynthesizer,
)
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.service_context import ServiceContext, set_global_service_context
from llama_index.text_splitter import TokenTextSplitter
from llama_index.vector_stores.faiss import FaissVectorStore
import openai
import faiss
import os

from .cn_keywords import ChineseKeywordTableIndex
from .data_loader import load_xlsx_nodes, load_xlsx_nodes_from_file, load_xlsx_nodes_qa
from .multi_retriever import MultiRetriever
from .query_engine import RAGQueryEngine
import numpy as np
import json
import datetime

def _gen_report_dir_path(iter_num):
    today = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    base_path = os.path.join(os.getcwd(),f'data/post_data/newkb/iter{iter_num}')
    
    # name = f'{today_cluster}'
    # p = os.path.join(base_path,name)
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
    return today,base_path

def kmeans(path, embeddings, labels, n_clusters,key, iter_num):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans

    # Apply K-means clustering
    # n_clusters is the number of clusters you want
    kmeans = KMeans(n_clusters=n_clusters, max_iter=1200)
    kmeans.fit(embeddings)
    cluster_labels = kmeans.labels_

    # Organize the data
    clustered_data = {}
    for i in range(kmeans.n_clusters):
        cluster_name = f"Cluster {i}"
        clustered_data[cluster_name] = labels[cluster_labels == i].tolist()

    # Convert to JSON
    json_data = json.dumps(clustered_data, indent=4, ensure_ascii=False)

    # Write to a file
    today,done_path = _gen_report_dir_path(iter_num)
    with open(f"{done_path}/{key}_{n_clusters}.json", 'w') as file:
        file.write(json_data)
    print(f"Clustering results saved to {done_path}/{key}_{n_clusters}.json")

    import pandas as pd
    # 查找qa对
    df=pd.read_excel(path)
    q = df['que'].str.strip()
    a = df['actual_send_answer']
    # 使用zip函数将问题和答案转换为字典
    qa_dict = dict(zip(q, a))

    json.dump(qa_dict,open('/root/autodl-tmp/cxl_workspace/com/evaluate/recall_evaluate/sim/data/temp.json','w',encoding='utf8'),ensure_ascii=False)
    cluster = json.load(open(f"{done_path}/{key}_{n_clusters}.json",'r',encoding='utf8'))

    def check(qa_dict,cluster):
        with pd.ExcelWriter(path) as writer:
            for k,values in cluster.items():
                i = 0
                res_dict={}
                for v in values:
                    if qa_dict.get(v, '无此键值') == "无此键值":
                        print(v)
                    else:
                        res_dict[v] = qa_dict[v]
                df2=pd.DataFrame.from_dict(res_dict,orient='index',columns=['a'])
                # 写入目标excel文件中的多个sheet
                df2.to_excel(writer,sheet_name=f"{key}_{k}")
            # df2.to_excel(f"{done_path}/{key}_{k}.xlsx")
    check(qa_dict,cluster)






def main(path:str,cluster_num:int,key,iter_num):
    service_context = ServiceContext.from_defaults(
        # chunk_size=2048,
        embed_model="local:/root/autodl-tmp/models/bge-large-zh"
        # embed_model=HuggingFaceEmbedding(SentenceTransformer('/root/autodl-tmp/models/bge-large-zh')) 
        )
    set_global_service_context(service_context)
    embedding_dim = service_context.embed_model._model.embeddings.word_embeddings.embedding_dim

    nodes = load_xlsx_nodes_from_file(path)
    embeddings = np.array(service_context.embed_model.get_text_embedding_batch([i.metadata["query"] for i in nodes]))
    labels = np.array([i.metadata["query"] for i in nodes])

    kmeans(path, embeddings, labels, cluster_num,key,iter_num)


if __name__=="__main__":
    # initialize service context (set chunk size)
    
    path = '/root/autodl-tmp/cxl_workspace/com/evaluate/recall_evaluate/diedai/data/pre_data/tbu问答库.xlsx'
    cluster_num = 4
    main(path,cluster_num)
    