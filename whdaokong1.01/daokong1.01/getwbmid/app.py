from flask import Flask
from get_wbmid import Get_Wbmid as gw
from flask import request
import json
app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def getwbmid():
    wburl = request.values.get('wburl')
    a = gw(wburl).main()
    return json.dumps(a, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
