from flask import Flask
from BaiduId import BaiduId
from flask import request
import json
app = Flask(__name__)


@app.route('/')
def baiduid():
    keyword = request.form.get('keyword')
    title = request.form.get('title')
    url = request.form.get('url')
    a = BaiduId(keyword, title, url).get_id()
    return json.dumps(a,ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True, threaded=True)
