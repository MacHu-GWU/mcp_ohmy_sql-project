.. _query-result-encoding:

Query Result Encoding: Why Markdown Tables Win
==============================================================================
*Demonstrates why markdown tables are superior to JSON for encoding SQL query results in LLM contexts*

When returning SQL query results to AI assistants, **markdown tables significantly outperform JSON** in both token efficiency and readability. Our analysis of 200 sample records shows markdown tables use **24% fewer tokens** (9,621 vs 12,305) compared to NDJSON format.

**Key Advantages of Markdown Tables:**

- **Token Efficiency**: 24% reduction in token usage compared to JSON
- **Visual Structure**: Tabular format matches how humans naturally read data
- **LLM Comprehension**: AI models excel at interpreting structured markdown tables
- **Immediate Readability**: No parsing required - data is instantly comprehensible

**Why JSON Falls Short:**

- **Verbose Syntax**: Repeated field names and JSON punctuation increase token count
- **Poor Readability**: Requires mental parsing to understand data relationships
- **Limited Structure**: No visual alignment or column-based comprehension

The `query_result_encoding_example.py` script demonstrates this comparison using 200 fake customer records, proving that markdown tables are the optimal format for SQL result encoding in MCP servers.

.. dropdown:: query_result_encoding_example.py

    .. literalinclude:: ./query_result_encoding_example.py
       :language: python
       :linenos:
