"The composition of classes in this file make up a Weaviate query."

from dataclasses import dataclass
from typing import List, Optional

from search.query_lang.weaviate.vector import (
    merge_weaviate_bm25_queries,
    merge_weaviate_near_text_queries,
    WeaviateBM25Query,
    WeaviateNearTextQuery,
)
from search.query_lang.weaviate.where import (
    merge_weaviate_where_queries,
    WeaviateWhereQuery,
)


RETRIEVAL_INDIVIDUAL_LIMIT = 100


class WeaviateQueryFormatter:
    def __init__(self, object_queries: List["WeaviateObjectQuery"]):
        self.object_queries = object_queries

    def get(self) -> str:
        return """
        {
            Get {
                %s
            }
        }
        """ % "\n".join(
            [str(object_query) for object_query in self.object_queries]
        )


@dataclass
class WeaviateObjectQuery:
    weaviate_class: str
    properties: Optional[List[str]] = None
    references: Optional[List["WeaviateReferenceQuery"]] = None
    additional: Optional[List[str]] = None
    near_text: Optional[WeaviateNearTextQuery] = None
    where: Optional[WeaviateWhereQuery] = None
    bm25: Optional[WeaviateBM25Query] = None
    limit: int = RETRIEVAL_INDIVIDUAL_LIMIT

    def __str__(self) -> str:
        additional_query = ""
        if self.additional:
            additional_query = """
                _additional {
                    %s
                }
            """ % "\n".join(self.additional)

        return """
            %s(
                limit: %i
                %s 
                %s 
                %s
            ) {
                %s
                %s
                %s
            }
        """ % (
            self.weaviate_class,
            self.limit,
            self.near_text if self.near_text and self.additional else "",
            self.bm25 if self.bm25 else "",
            f"where: {self.where}" if self.where and self.where.operands else "",
            additional_query,
            "\n".join(self.properties) if self.properties else "",
            "\n".join(
                [str(reference_query) for reference_query in self.references]
            ) if self.references else "",
        )


@dataclass
class WeaviateReferenceQuery:
    property: str
    referenced_object: str
    referenced_properties: List[str]
    referenced_references: Optional[List["WeaviateReferenceQuery"]] = None

    def __str__(self) -> str:
        return """
            %s {
                ... on %s {
                    %s
                    %s
                }
            }
        """ % (
            self.property,
            self.referenced_object,
            "\n".join(self.referenced_properties)
            if self.referenced_properties else "",
            "\n".join([
                str(reference_query)
                for reference_query
                in self.referenced_references
            ]) if self.referenced_references else "",
        )


#################### PROPERTIES ####################


USER_BASIC_PROPERTIES = [
    "user_id",
    "user_name",
    "user_description",
    "user_job_title",
    "user_city",
    "user_country_code",
    "user_url",
]

EDUCATION_BASIC_PROPERTIES = [
    "education_university",
    "education_degree",
    "education_field",
    "education_description",
    "education_start_date",
    "education_end_date",
]
EXPERIENCE_BASIC_PROPERTIES = [
    "experience_company",
    "experience_title",
    "experience_description",
    "experience_start_date",
    "experience_end_date",
]
ADDITIONAL_PROPERTIES = ["distance"]


#################### MERGE ####################


def merge_weaviate_object_queries(
    weaviate_query_1: WeaviateObjectQuery,
    weaviate_query_2: WeaviateObjectQuery,
) -> WeaviateObjectQuery:
    "NOTE: Instead of merging here, a better idea might be to merge the filters"

    assert weaviate_query_1.weaviate_class == weaviate_query_2.weaviate_class, (
        "WeaviateObjectQuery.weaviate_class must be of the same type, "
        f"got :: {weaviate_query_1.weaviate_class} and "
        f"{weaviate_query_2.weaviate_class}"
    )

    return WeaviateObjectQuery(
        weaviate_class=weaviate_query_1.weaviate_class,
        properties=(weaviate_query_1.properties or []) + (weaviate_query_2.properties or []),
        references=(weaviate_query_1.references or []) + (weaviate_query_2.references or []),
        additional=(weaviate_query_1.additional or []) + (weaviate_query_2.additional or []),
        near_text=merge_weaviate_near_text_queries(
            weaviate_query_1.near_text,
            weaviate_query_2.near_text,
        ),
        bm25=merge_weaviate_bm25_queries(weaviate_query_1.bm25, weaviate_query_2.bm25),
        where=merge_weaviate_where_queries(
            weaviate_query_1.where,
            weaviate_query_2.where,
        ),
        limit=max(weaviate_query_1.limit, weaviate_query_2.limit),
    )



