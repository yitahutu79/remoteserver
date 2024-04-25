from llama_index.query_engine import CustomQueryEngine
from llama_index.retrievers import BaseRetriever, VectorIndexRetriever
from llama_index.response_synthesizers import (
    get_response_synthesizer,
    BaseSynthesizer,
)



class RAGQueryEngine(CustomQueryEngine):
    """RAG Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer

    def custom_query(self, query_str: str, retriever: BaseRetriever=None):
        retriever = self.retriever if retriever is None else retriever
        nodes = retriever.retrieve(query_str)

        rec = set()
        new_nodes = []
        for node in nodes:
            if node.metadata["query"] in rec:
                continue
            else:
                rec.add(node.metadata["query"])
                new_nodes.append(node)
        
        new_nodes.sort(key=lambda x: x.score, reverse=True)
        new_nodes = new_nodes

        for node in new_nodes:
            node.node.text_template = "{metadata_str}"
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)

        return response_obj


if __name__=="__main__":
    import openai
    openai.base_url = 'https://openkey.cloud/v1/'

    engine = RAGQueryEngine()
    response = engine.query("What did the author do growing up?")
    print(response)

