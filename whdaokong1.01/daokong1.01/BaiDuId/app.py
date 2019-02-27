from flask import Flask
from BaiduId import BaiduId
from flask import request
app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def baiduid():
    keyword = request.values.get('keyword')
    title = request.values.get('title')
    url = request.values.get('url')
    a = BaiduId(keyword, title, url).get_id()
    # return json.dumps(a, ensure_ascii=False)
    return a

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True, threaded=True)
