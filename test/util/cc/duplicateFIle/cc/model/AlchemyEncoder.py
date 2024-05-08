# sqlalchemy to json
# 只写方法，具体实现流程、数据库连接、数据库表这些内容看前面的文章
# 注：仅供参考，具体情况需具体编写
import json,datetime
from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):
    """
    SqlAlchemy对象转换为json格式
    """

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if type(data) is datetime.datetime:
                        data = data.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)