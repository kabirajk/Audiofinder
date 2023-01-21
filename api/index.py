from flask import Flask , request , jsonify
import os , sys
import numpy as np 
import base64
import cv2
from cv2 import dnn_superres

app = Flask(__name__)


def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def Upscale(uri,scale=3):
    sr = dnn_superres.DnnSuperResImpl_create()
    image =  readb64(uri)#cv2.imread('/content/drive/MyDrive/Colab Notebooks/img upscaler/image.jpg')
    sr.readModel(f"EDSR_x{scale}.pb")#path for model
    sr.setModel("edsr", scale)
    result = sr.upsample(image)
    # cv2.imwrite("D:/Development/EDSR_Tensorflow/models/upscaled_x3.png", result)
    retval, buffer = cv2.imencode('.jpg', result)
    jpg_as_text = base64.b64encode(buffer)
    # print("render")
    # print("data:image/jpeg;base64,"+str(jpg_as_text, 'UTF-8'))
    return "data:image/jpeg;base64,"+str(jpg_as_text, 'UTF-8')
    
@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/upscale' , methods=['POST'])
def upsclaeImage():
    input_json=request.get_json(force=True)
    uri=input_json['imguri']
    scale=3#input_json['scale']
    return jsonify({"image":Upscale(uri=uri,scale=scale)});

@app.route('/test' , methods=['GET','POST'])
def test():
	print("log: got at test" , file=sys.stderr)
	return jsonify({'status':'succces'})

@app.after_request
def after_request(response):
    print("log: setting cors" ,os.curdir, file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/about')
def about():
    return 'About'

# if __name__ == '__main__':
# 	app.run(debug = True)