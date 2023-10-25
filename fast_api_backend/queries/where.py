from dataclasses import dataclass
from typing import List, Optional


@dataclass
class WeaviateWhereQuery:
    @dataclass
    class Operand:
        path: List[str]
        operator: str
        valueType: str
        value: str

        def __str__(self) -> str:
            return """
                            {
                                path: [%s],
                                operator: %s,
                                %s: %s
                            }
            """ % (
                ", ".join([f"\"{p}\"" for p in self.path]),
                self.operator,
                self.valueType,
                self.value,
            )

    operands: List[Operand]
    operator: str

    def __str__(self) -> str:
        if not self.operands:
            return ""

        return """
                {
                        operator: %s,
                        operands: [
                            %s
                        ]
                }
            """ % (self.operator, ',\n'.join(str(op) for op in self.operands))


#################### MERGE ####################


def merge_weaviate_where_queries(
    weaviate_query_1: Optional[WeaviateWhereQuery],
    weaviate_query_2: Optional[WeaviateWhereQuery],
) -> Optional[WeaviateWhereQuery]:
    if weaviate_query_1 and weaviate_query_2:
        return WeaviateWhereQuery(
            operator="And",
            operands=weaviate_query_1.operands + weaviate_query_2.operands
        )
    if weaviate_query_1:
        return weaviate_query_1
    return weaviate_query_2