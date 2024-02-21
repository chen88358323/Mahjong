from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
import logging
import jsonpickle
import json
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from test.util.cc.duplicateFIle.Conf import  Conf
import ssl

from test.util.cc.duplicateFIle.model import AlchemyEncoder

es_filedetail_name="filedetai"
es_filedetaildup_name="filedetaildup"
es_filedetail_docid="1"
es_filedetaildup_docid="1"

##忽视证书


cfg= Conf()
#https 方式
# context = ssl._create_unverified_context()
# context.check_hostname = False
# es = Elasticsearch(
#     [{
#         'host': cfg.readEsConf("es_address"),
#         'port': str(cfg.readEsConf("es_port")),
#         'scheme': "https"
#     }
#
#     ],
#     http_auth=(cfg.readEsConf("es_user"), cfg.readEsConf("es_passwd")),##账号密码
#     ssl_context=context,
# )
#http方式
es = Elasticsearch(
    [{
        'host': cfg.readEsConf("es_address"),
        'port': str(cfg.readEsConf("es_port")),
    }
    ],
    http_auth=(cfg.readEsConf("es_user"), cfg.readEsConf("es_passwd"))##账号密码

)

# `id` int(11) NOT NULL AUTO_INCREMENT,
#   `hcode` varchar(50) NOT NULL DEFAULT 'hashcode',
#   `isdir` int(1) NOT NULL,
#   `path` varchar(500) NOT NULL DEFAULT '存放路径',
#   `filename` varchar(500) NOT NULL DEFAULT '文件名',
#   `creattime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''扫描文件时间''',
#   `modifiedtime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3) COMMENT '''文件修改时间''',
#   `filetype` varchar(10) DEFAULT NULL,
#   `belong` varchar(45) DEFAULT NULL COMMENT '分类',
#   `keyword` varchar(200) DEFAULT NULL,
#   `systemdriver` varchar(50) DEFAULT NULL COMMENT '系统盘符',
#   `platformscan` varchar(10) DEFAULT NULL COMMENT '该文件扫描的系统',
#   `filesize` float NOT NULL DEFAULT '0' COMMENT '文件大小单位 Mb',

def creatDoc(indexname):
    res = es.index(index=indexname, document=doc)
    print('creat doc res:' + str(res))
    return  str(res)



#idxName 索引名称 类似表名
#obj对象
def createESIdx(idxName,obj,objid):
    json_object=json.dumps(obj, cls=AlchemyEncoder.AlchemyEncoder)
    print("creat index :"+json_object)
    # 将JSON对象存储在Elasticsearch中
    es.index(index=idxName, id=objid, body=json_object)

def batchCreateEsIdx(idxName,objlist):
    # 使用bulk()函数批量存储对象到Elasticsearch
    success, _ = bulk(es, objlist, index=idxName)

    print(f"{success} documents have been successfully indexed.")

def queryAll(idxName):
    doc_type = "_doc"  # 在Elasticsearch 7.x中，这通常是"_doc"，除非你有自定义的类型
    # 执行查询
    search_query = {
        "query": {
            "match_all": {}  # 匹配所有文档，你可以替换为其他查询条件
        }
    }
    resp = es.search(index=idxName,  body=search_query)
    # 打印查询结果
    # print("查询结果:")
    for hit in resp['hits']['hits']:
        print(hit['_source'])  # '_source'字段包含文档的实际内容
    # print(str(resp))
    print("Got %d Hits:" % resp['hits']['total']['value'])
    # for hit in resp['hits']['hits']:
    #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


    # 如果需要获取查询结果的总数
    # total_hits = response['hits']['total']['value']
    # print(f"总匹配文档数: {total_hits}")
def delDoc(idxName):
    if es.indices.exists(index=idxName):
        es.indices.delete(index=idxName)
        print(f"索引 {idxName} 已成功删除")
    else:
        print(f"索引 {idxName} 不存在")


def delAllDoc(idxName,docid):
    # 删除文档
    try:
        es.delete(index=idxName,  id=docid)
        print(f"文档 {docid} 在索引 {idxName} 中已成功删除")
    except Exception as e:
        print(f"删除文档时发生错误: {e}")
doc = {
    "mappings": {
        "properties": {
            "id": {
                "type": "long"
            },
            "hcode": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "isdir": {
                "type": "short"
            },
            "path": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "filename": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "creattime": {
                    "type": "date"
            },
            "modifiedtime": {
                    "type": "date"
            },
            "filetype": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "belong": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "keyword": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "systemdriver": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "platformscan": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "filesize": {
                "type": "float"

            }

        }
    }
}
if __name__ == '__main__':
    # print(es.info)
    # res = es.index(index='torr', document=doc)
    # print('creat res:'+str(res))
    print(es.ping())
    queryAll('torr')