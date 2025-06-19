Enum Mapping Pattern
==============================================================================
*Demonstrates mapping between related enums using dictionary mapping with property access versus dataclass approaches*

When you need to map between related enums (e.g., database object types to table types), use **dictionary mapping with property access** (pattern 1) rather than embedding values in dataclasses (pattern 2). This provides cleaner syntax (`obj.table_type` vs `mapping[obj]`), better flexibility for partial mappings, and maintains enum independence while offering convenient cross-references.

.. dropdown:: enum_mapping_pattern_1.py

    .. literalinclude:: ./enum_mapping_pattern_1.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:

.. dropdown:: enum_mapping_pattern_2.py

    .. literalinclude:: ./enum_mapping_pattern_2.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:
