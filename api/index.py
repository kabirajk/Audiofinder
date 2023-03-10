from flask import Flask, request , jsonify

app = Flask(__name__)

global globalImage
global count
globalImage=dict()
count=1

# @app.route('/')
# def home():
#     print(globalImage);
#     return 'Hello, World!'

@app.route('/image/<id>')
def getimage(id):
    global globalImage
    return '<img src="'+globalImage["image"+str(id)]+'">';

@app.route('/predict' , methods=['POST'])
def predict():
    global count
    global globalImage
    input_json=request.get_json(force=True)
    uri=input_json['imguri']
    count+=1
    globalImage["image"+str(count)]=uri
    print(globalImage);
    return jsonify({"imageId":"image/"+str(count)})

@app.route('/flush')
def flush():
    global globalImage
    globalImage=dict()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# if __name__ == '__main__':
# 	app.run(host="0.0.0.0", port=int("5000"), debug=True)