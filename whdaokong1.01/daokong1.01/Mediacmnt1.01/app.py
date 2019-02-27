from flask import Flask
import json
from flask import request
from Crawlmodule.Wy_Comment import Wy_Comment
from Crawlmodule.Wb_Comment import Crawl_WB_Commenthtml
from Crawlmodule.Tx_Comment import Tx_Comment
from Crawlmodule.Fh_Comment import Fh_Comment
from Crawlmodule.Sh_Comment import Sh_Comment
from Crawlmodule.Sina_Comment import Sina_Comment

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def abc():
    url = request.values.get('pageurl')
    if 'sina' in url:
        a = Sina_Comment(url).main()
    elif 'sohu' in url:
        a = Sh_Comment(url).main()
    elif 'ifeng' in url:
        a = Fh_Comment(url).main()
    elif '163.com' in url:
        a = Wy_Comment(url).main()
    elif 'qq.com' in url:
        a = Tx_Comment(url).main()
    elif 'weibo' in url:
        a = Crawl_WB_Commenthtml(url).main()
    return json.dumps(a,ensure_ascii=False)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
