from typing import Any, Set, Union

import jieba.analyse

from llama_index.core import BaseRetriever
from llama_index.indices.keyword_table.base import (
    BaseKeywordTableIndex,
    KeywordTableRetrieverMode,
)
from llama_index.prompts.default_prompts import DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE

DQKET = DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE


class ChineseKeywordTableIndex(BaseKeywordTableIndex):
    """Simple Keyword Table Index.

    This index uses a simple regex extractor to extract keywords from the text.

    """

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text."""

        keywords = jieba.analyse.extract_tags(text, topK=3)

        return keywords

    def as_retriever(
        self,
        retriever_mode: Union[
            str, KeywordTableRetrieverMode
        ] = KeywordTableRetrieverMode.SIMPLE,
        **kwargs: Any,
    ) -> BaseRetriever:
        return super().as_retriever(retriever_mode=retriever_mode, **kwargs)