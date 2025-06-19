Pydantic Tagged Union Pattern
==============================================================================
*Demonstrates discriminated unions for type-safe configuration using Pydantic's discriminator field*

When you need to handle multiple connection types or configuration variants, use **Pydantic tagged unions** with a discriminator field. This pattern enables type-safe deserialization where the `type` field determines which specific subclass to instantiate, providing compile-time type checking and runtime validation for polymorphic configurations.

.. dropdown:: pydantic_tagged_union_pattern.py

    .. literalinclude:: ./pydantic_tagged_union_pattern.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:
