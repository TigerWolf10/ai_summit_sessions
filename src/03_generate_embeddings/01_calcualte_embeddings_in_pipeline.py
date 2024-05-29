# Copyright (c) Diego Colombo. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
from llama_index.core.schema import Document, BaseNode
from llama_index.core import Settings
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SemanticSplitterNodeParser, MarkdownNodeParser, JSONNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
import os

json_documents:list[Document] = []
markdown_documents:list[Document] = []
nodes:list[BaseNode] = []

embed_model = OpenAIEmbedding(
    api_key=os.getenv("OPENAI_API_KEY"),
)

Settings.embed_model = embed_model

semanticSplitterNodeParser = SemanticSplitterNodeParser(embed_model=embed_model)
semanticSplitterNodeParser.breakpoint_percentile_threshold = 95

markdownPipeline = IngestionPipeline(
    transformations=[
        MarkdownNodeParser(),
        semanticSplitterNodeParser,
        embed_model,
    ]
)

nodes.extend(markdownPipeline.run(markdown_documents))

jsonPipeline = IngestionPipeline(
    transformations=[
        JSONNodeParser(),
        semanticSplitterNodeParser,
        embed_model,
    ]
)

nodes.extend(jsonPipeline.run(json_documents))

