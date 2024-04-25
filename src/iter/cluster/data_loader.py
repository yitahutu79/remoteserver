from typing import List
from llama_index import Document
import pandas as pd
import os

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jieba.analyse
from llama_index.schema import TextNode

def load_xlsx_nodes(dir: str) -> List[Document]:
    nodes = []

    for name in next(os.walk(dir))[2]:
        file_path = os.path.join(dir, name)
        df = pd.read_excel(file_path, index_col=False, dtype=str)

        for q, a in df[["q", "a"]].itertuples(index=False):
            q = q.strip()
            if q == "" or a == "":
                continue

            # q-q
            q_node = TextNode(metadata={"query": q, "answer": a})
            q_node.text_template = q
            nodes.append(q_node)

    return nodes


def load_xlsx_nodes_qa(dir: str) -> List[Document]:
    nodes = []

    for name in next(os.walk(dir))[2]:
        file_path = os.path.join(dir, name)
        df = pd.read_excel(file_path, index_col=False, dtype=str)

        for q, a in df[["q", "a"]].itertuples(index=False):
            q = q.strip()
            a = a.strip()
            if q == "" or a == "":
                continue

            # q-q
            q_node = TextNode(metadata={"query": q, "answer": a})
            q_node.text_template = q
            nodes.append(q_node)

            # q-a
            a_node = TextNode(metadata={"query": q, "answer": a})
            a_node.text_template = a
            nodes.append(a_node)

            # # q-k
            # key = jieba.analyse.extract_tags(q, topK=3, withWeight=True)
            # node = TextNode(text=q, metadata={"v": a})
            # node.text_template = "{content}"
            # nodes.append(node)

    return nodes

def load_xlsx_nodes_from_file(file_path: str) -> List[Document]:
    nodes = []

    df = pd.read_excel(file_path, index_col=False, dtype=str,sheet_name='Sheet1')
    
    for q, a in df[["que", "actual_send_answer"]].itertuples(index=False):
        q = q.strip()
        a = a.strip()
        if q == "" or a == "":
            continue

        # q-q
        q_node = TextNode(metadata={"query": q, "answer": a})
        q_node.text_template = q
        nodes.append(q_node)

        # q-a
        # a_node = TextNode(metadata={"query": q, "answer": a})
        # a_node.text_template = a
        # nodes.append(a_node)

        # # q-k
        # key = jieba.analyse.extract_tags(q, topK=3, withWeight=True)
        # node = TextNode(text=q, metadata={"v": a})
        # node.text_template = "{content}"
        # nodes.append(node)

    return nodes


