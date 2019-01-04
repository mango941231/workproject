"""对新闻评论进行监控 传入新闻链接及评论ID 若该评论进入热评 则返回图片链接"""
from flask import Flask
import json
from Comtmodule.Sina_Comment import Sina_Comment
from Comtmodule.Sh_Comment import Sh_Comment
from Comtmodule.Fh_Comment import Fh_Comment
from Comtmodule.Tx_Comment import Tx_Comment
from Comtmodule.Wb_Comment import Wb_Comment
from Comtmodule.Wy_Comment import Wy_Comment
from flask import request

app = Flask(__name__)


@app.route('/',methods = ['GET'])
def hot_jt():
    url = request.values.get('pageurl')
    ID = request.values.get('id')
    taskid = request.values.get('taskid')
    if 'sina' in url:
        a = Sina_Comment(url,ID,taskid).main()     #从该新闻url的热评里查看要求的评论内容content是否在‘最热评论’里
    elif 'sohu' in url:
        a = Sh_Comment(url,ID,taskid).main()
    elif 'ifeng' in url:
        a = Fh_Comment(url,ID,taskid).main()
    elif 'qq.com' in url:
        a = Tx_Comment(url,ID,taskid).main()
    elif 'weibo' in url:
        a = Wb_Comment(url,ID,taskid).main()
    elif '163.com' in url:
        a = Wy_Comment(url,ID,taskid).main()
    return json.dumps(a, ensure_ascii=False)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050,debug=True,threaded=True)
