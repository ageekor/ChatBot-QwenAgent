import urllib.parse
import json5
import requests
import pymysql
from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('my_image_gen')
class MyImageGen(BaseTool):
    description = 'AI painting (image generation) service, input text description, and return the image URL drawn based on text information.'
    parameters = [{
        'name': 'prompt',
        'type': 'string',
        'description': 'Detailed description of the desired image content, in English',
        'required': True
    }]

    def call(self, params: str, **kwargs) -> str:
        prompt = json5.loads(params)['prompt']
        prompt = urllib.parse.quote(prompt)
        return json5.dumps(
            {'image_url': f'https://image.pollinations.ai/prompt/{prompt}'},
            ensure_ascii=False)


@register_tool('mysql_query')
class MySQLQueryTool(BaseTool):
    description = '执行MySQL数据库查询，输入SQL语句，返回查询结果。'
    parameters = [
        {
            'name': 'sql',
            'type': 'string',
            'description': '要执行的SQL语句',
            'required': True
        }
    ]

    def call(self, params: str, **kwargs) -> str:
        args = json5.loads(params)
        sql = args['sql']
        conn = pymysql.connect(
            host='192.168.23.252',
            user='host',
            password='key',
            database='user',
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                if sql.strip().lower().startswith('select'):
                    result = cursor.fetchall()
                else:
                    conn.commit()
                    result = f"Rows affected: {cursor.rowcount}"
        finally:
            conn.close()
        return json5.dumps({'result': result}, ensure_ascii=False)


@register_tool('rag_search')
class RAGSearchTool(BaseTool):
    description = '基于知识库进行语义搜索，输入查询文本，返回相关的知识内容。'
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': '要查询的问题或关键词',
        'required': True
    }]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_url = "http://localhost:8000"

    def call(self, params: str, **kwargs) -> str:
        args = json5.loads(params)
        query = args['query']
        
        response = requests.post(
            f"{self.api_url}/search",
            json={"query": query}
        )
        
        if response.status_code != 200:
            return json5.dumps({
                'error': f'搜索失败: {response.text}'
            }, ensure_ascii=False)
            
        return json5.dumps(response.json(), ensure_ascii=False)
