# import os
# from elasticsearch import Elasticsearch


# class ElasticsearchRepository:
#     def __init__(self):
#         self.client = Elasticsearch(os.getenv('ELASTICSEARCH_URL'))

#     def search(self, item: str):
#         query = {"query": {"match": {"ingredients": item}}}
#         result = self.client.search(index="foods", body=query)
#         return result['hits']['hits']
