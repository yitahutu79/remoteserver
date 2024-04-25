# import QueryBundle
from llama_index import QueryBundle

# import NodeWithScore
from llama_index.schema import NodeWithScore

# Retrievers
from llama_index.retrievers import (
    BaseRetriever,
    VectorIndexRetriever,
    KeywordTableSimpleRetriever,
)

import jieba.analyse

from typing import List, Literal


class MultiRetriever(BaseRetriever):
    """Custom retriever that performs both semantic search and hybrid search."""

    def __init__(
        self,
        vector_retrievers: List[BaseRetriever],
        weights: List = None,
    ) -> None:
        """Init params."""

        assert weights is None or len(weights) == len(vector_retrievers)
        self._vector_retrievers = vector_retrievers
        self._weights = weights
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query."""

        combined_dict = {}
        for i, retriever in enumerate(self._vector_retrievers):
            temp = retriever.retrieve(query_bundle)

            if self._weights is not None:
                for node in temp:
                    node.score *= self._weights[i]
            
            for node in temp:
                if node.node_id not in combined_dict:
                    combined_dict[node.node_id] = node
                else:
                    combined_dict[node.node_id].score += node.score

        retrieve_nodes = list(combined_dict.values())
        retrieve_nodes.sort(key=lambda x: x.score, reverse=True)

        return retrieve_nodes
