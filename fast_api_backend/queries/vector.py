from dataclasses import dataclass
from typing import List, Optional


@dataclass
class WeaviateNearTextQuery:
    @dataclass
    class Concept:
        property: Optional[str]
        values: List[str]

        def __str__(self) -> str:
            if not self.values:
                return ""

            values_str = " ".join(self.values)
            if not self.property:
                return f"{values_str}"
            return f"{self.property} {values_str}"

    @dataclass
    class MoveAwayFrom:
        concepts: List
        force: float

        def __str__(self) -> str:
            if not self.concepts:
                return ""

            return """
            moveAwayFrom: {
                concepts: ["%s"]
                force: %i
            }
            """ % (
                " ".join([str(c) for c in self.concepts]),
                self.force
            )

    concepts: List[Concept]
    distance: Optional[float] = None
    move_away_from: Optional[MoveAwayFrom] = None

    def __str__(self) -> str:
        if not self.concepts:
            return ""

        distance_query = f"distance: {self.distance}" if self.distance else ""
        return """
        nearText: {
            concepts: ["%s"]
            %s
            %s
        }""" % (
            " ".join([str(c) for c in self.concepts]),
            distance_query,
            self.move_away_from if self.move_away_from else "",
        )


@dataclass
class WeaviateBM25Query:
    query: str
    properties: List[str]

    def __str__(self) -> str:
        if not self.query:
            return ""

        return """
        bm25: {
            query: "%s"
            properties: [%s]
        }
        """ % (
            self.query,
            ", ".join([f'"{p}"' for p in self.properties])
        )


#################### MERGE ####################


def merge_weaviate_near_text_queries(
    weaviate_query_1: Optional[WeaviateNearTextQuery],
    weaviate_query_2: Optional[WeaviateNearTextQuery],
) -> Optional[WeaviateNearTextQuery]:
    if not weaviate_query_1 and not weaviate_query_2:
        return None

    if weaviate_query_1 and weaviate_query_2:
        move_away_query = None
        if weaviate_query_1.move_away_from and weaviate_query_1.move_away_from:
            # Merge moveAwayFrom query
            move_away_query = WeaviateNearTextQuery.MoveAwayFrom(
                concepts=(
                    weaviate_query_1.move_away_from.concepts
                    + weaviate_query_1.move_away_from.concepts
                ),
                force=(
                    weaviate_query_1.move_away_from.force + weaviate_query_1.move_away_from.force
                ),
            )
        elif weaviate_query_1.move_away_from:
            move_away_query = weaviate_query_1.move_away_from
        else:
            move_away_query = weaviate_query_2.move_away_from

        return WeaviateNearTextQuery(
            concepts=weaviate_query_1.concepts + weaviate_query_2.concepts,
            move_away_from=move_away_query,
        )
    elif weaviate_query_1:
        return weaviate_query_1
    return weaviate_query_2


def merge_weaviate_bm25_queries(
    weaviate_query_1: Optional[WeaviateBM25Query],
    weaviate_query_2: Optional[WeaviateBM25Query],
) -> Optional[WeaviateBM25Query]:
    if not weaviate_query_1 and not weaviate_query_2:
        return None

    if weaviate_query_1 and weaviate_query_2:
        return WeaviateBM25Query(
            query=f"{(weaviate_query_1.query or '')} {(weaviate_query_2.query or '')}",
            properties=list(set(
                (weaviate_query_1.properties or []) +
                (weaviate_query_2.properties or [])
            )),
        )

    if weaviate_query_1:
        return weaviate_query_1
    return weaviate_query_2