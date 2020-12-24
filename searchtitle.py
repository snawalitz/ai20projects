# -*- coding:UTF-8 -*-

import csv
from elasticsearch import Elasticsearch


# 创建索引
def create_index():
    _index_mappings = {
        "mappings": {
            "dynamic": "true",  # 设置索引为“动态的”
            "properties": {
                "id": {
                    "type": "text"    # 对应int
                },
                "title": {
                    "type": "text",
                    "analyzer": "ik_max_word"  # 使用IK分词（较细粒度分词）
                },
                "abstract": {
                    "type": "text"  # 对应string
                },
                "authors": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "journal-ref": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "license": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                }
            }
        }
    }
    # 判断索引是否存在
    if es.indices.exists(index=my_index) is not True:
        # 创建索引，指定索引名、索引·映射·
        res = es.indices.create(index=my_index, body=_index_mappings)
        print("无索引，创建:\n", res)
    else:
        print("索引已存在，跳过创建！")


# 从CSV文件中读取数据
def index_data_from_csv(csvfile):
    """
    :param csvfile: csv文件，包括完整路径
    """
    # 取CSV数据
    with open(csvfile, 'r', encoding='utf-8', newline='') as f:
        list_data = csv.reader(f)
        # 循环成字典形式，插入数据
        index = 0
        doc = {}
        # 将每一行数据拼接成字典
        for item in list_data:
            if index > 1:  # 第一行是标题
                doc['id'] = item[0]
                doc['title'] = item[1]
                doc['abstract'] = item[2]
                doc['authors'] = item[3]
                doc['journal-ref'] = item[4]
                doc['license'] = item[5]
                # 建立索引的数据，指定索引名、类型名、内容
                res = es.index(index=my_index, doc_type=my_doc_type, body=doc)
                print(res)
            # 下面没用，就是看看一共读了多少行



# 根据ID查询索引数据
def get_data_id(id):
    res = es.get(index=my_index, doc_type=my_doc_type, id=id)
    print(res)


# 查询所有索引数据
def query_all_index_data():
    query_all_body = {
        "query": {
            "match_all": {}
        },
        "from": 0,
        "size": 100
    } 
    all_data = es.search(index=my_index, body=query_all_body)
    print(all_data)


if __name__ == '__main__':
    # 0、索引con_pro 类型_doc
    my_index = 'con_pro'
    my_doc_type = '_doc'

    # 1、建立Python与ES的连接
    es = Elasticsearch(['127.0.0.1:9200'])

    # 2、创建索引
    create_index()

    # 3、导入CSV数据
    index_data_from_csv('arxiv-metadata-ext-paper.csv')

    # 查询所有0-100条数据（查）
    query_all_index_data()