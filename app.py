
'''
Flash webapp
model : TFLite Edge model, uses TensorFlow package
input : json request/payload
output : json object
'''


# http://blog.luisrei.com/articles/flaskrest.html
# https://stackoverflow.com/questions/56333395/problem-curl-7-failed-to-connect-to-localhost-port-1080-connection-refused
# https://stackoverflow.com/questions/54908079/flask-api-failing-to-decode-json-data-error-message-failed-to-decode-json/54908539

# https://stackoverflow.com/questions/48607198/how-to-send-an-image-to-a-flask-server-using-postman/48607411
# https://www.techiediaries.com/python-requests-upload-file-post-multipart-form-data/



import os
import sys
import base64
import cv2
import numpy as np
import tensorflow as tf

# os.environ['HTTPS_PROXY'] = 'http://internet.proxy.fedex.com:3128' # this is required
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\3879326\Software\fxs-cast-rpa-poc-1-a6dec4b52e06_feb26.json"

# from google.cloud import storage
# from google.cloud import automl_v1beta1
# from google.cloud.automl_v1beta1.proto import service_pb2

# prediction_client = automl_v1beta1.PredictionServiceClient()

# PROJECT_ID="615585608112"
# MODEL_ID='ICN3993914415245164544'  # this is second model
# url = 'projects/{}/locations/us-central1/models/{}'.format(PROJECT_ID, MODEL_ID)

# def get_prediction(content, url, threshold, client):
#     payload = {'image': {'image_bytes': content }}
#     params = {'score_threshold': threshold}
#     request = client.predict(url, payload, params) #### error is
#     return request


# def display_result(pred):
#     if not pred.payload:
#         #print(ff.name, 'confidence is below threshold', sep=',')
#         return('unknown', 'NaN')
#     # elif 'error' in pred:
#     #     print(pred['error']['message'])
#     elif pred.payload:
#         name = [i.display_name for i in pred.payload][0]
#         score = [i.classification.score for i in pred.payload][0]
#         return(name, score)
#     else:
#         #print(ff, 'unknown', 'NaN', sep=',')
#         return('unknown error', 'NaN')


def convert_bytes_cv2(img):
    nparr = np.frombuffer(img, dtype=np.uint8)    
    img2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img2

def convert_cv2_base64(img):
    string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode() # from array to base64
    #data = 'data:image/jpeg;base64,{}'.format(string)
    return string

def get_image_from_request(r):
    if r.files.get('file'):
        file_storage = r.files.get('file')
        img_name = file_storage.filename
        print('inside filestorage') # this is called while testing in postman
        print(file_storage) # <FileStorage: '090dbba9d63bce9c-1.jpg' ('image/jpeg')>
        img_0 = convert_bytes_cv2(file_storage.read())
        return({'img': img_name, 'data': img_0})
    elif r.get_json(force=True):
        print('inside json object')
        data = r.get_json(force=True) # works, class dict
        img_name = data.get('file')
        img_0 = cv2.imread(img_name)
        #print("img_0 : ", img_name)
        
        if type(img_0).__name__ == 'ndarray':
            #print("img_0.shape : ", img_0.shape)
            return({'img': img_name, 'data': img_0})
        else:
            return({'img': img_name, 'data': None})
    else:
        return({'img': 'not found', 'data': None})


dir = r"C:\Users\3879326\Desktop\work\Freight_Dim_scan\Freight_Approved_photos\EdgeModel"

with open(dir+os.sep+'dict.txt', 'r') as f:
    labels_names = f.read().splitlines()

interpreter = tf.lite.Interpreter(model_path=dir+os.sep+'model.tflite')

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.allocate_tensors()



from flask import Flask, render_template, redirect
from flask import request, json, jsonify
app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload/')
def upload_file():
    return render_template('uploadfile.html')

#http://127.0.0.1:5000/name/file.img
@app.route('/name/<img>')
def get_image(img):
    #with open(img, 'rb') as ff:
    #    content = ff.read()

    threshold = '0.5'
    #pred = get_prediction(content, url, threshold, prediction_client)
    #result = display_result(pred)

    #return (img, result[0], result[1])
    #output = "{},{},{}".format(img, result[0], result[1])
    #output = jsonify({'img': img, 'pred':result[0], 'prob': result[1]})
    #return output
    return 'Input image : {} '.format(img)


@app.route('/pred', methods=['POST'])
def model_pred():
    #print(request.headers['Content-Type'])  # application/json
    #data = json.dumps(request.json) # class is string
    #data = request.json # class is dict
    
    #print(request) # <Request 'http://127.0.0.1:5000/pred' [POST]>

    # this is working incase of json request, but fails if file doesn't exist
    # data = request.get_json(force=True) # works, class dict
    # img_name = data['file']
    # img_0 = cv2.imread(img_name)
    
    #img_bytes = request.form.get('file') # not working


    # file_storage = request.files.get('file')
    # img_name = file_storage.filename
    # #print(img_bytes) # <FileStorage: '090dbba9d63bce9c-1.jpg' ('image/jpeg')>
    # img_0 = convert_bytes_cv2(file_storage.read())

    input = get_image_from_request(request)
    img_name, img_0 = input['img'], input['data']
    #print('name 0 ', img_name)
    
    if type(img_0).__name__ == 'ndarray':
        #print('name 0 ', img_name)
        #print('img_0 shape ', img_0.shape)
        img_base64 = convert_cv2_base64(img_0)

        img_1 = cv2.resize(img_0, (224, 224))
        interpreter.set_tensor(input_details[0]['index'], [img_1])
        interpreter.invoke()

        output_data = interpreter.get_tensor(output_details[0]['index'])
        scores = np.squeeze(output_data)
        prob = scores/np.sum(scores)
        output = {l:s for l,s in zip(labels_names, prob)}

        high_label = labels_names[np.argmax(prob)]
        high_prob = output.get(high_label)

        #print(data)
        #print(type(data))
        #pred = 'Approved'
        #prob = 0.98
        result_1 = {'img': img_name, 'prob': output, 'label': high_label, 'conf':high_prob}
        result = jsonify(result_1)
    else:
        result_1 = {'img': img_name, 'prob': "", 'label': "", 'conf':""}
        result = jsonify(result_1)

    #return result
    #return render_template("index.html", name=img_name, image=img_base64, result=json.dumps(result_1))
    return render_template("index.html", name=img_name, image=img_base64, result=result_1)



if __name__ == '__main__':
    app.run(debug=True)

# curl: (7) Failed to connect to internet.proxy.fedex.com port 3128: Timed out

# curl "http://127.0.0.1:5000/"
# set HTTP_PROXY=
# echo %HTTP_PROXY%
# curl http://localhost:5000/name/img.jpg
# curl http://localhost:5000/name/C:\Users\3879326\Desktop\work\Freight_Dim_scan\UAT_Testing\Freight_UI\090dbba9d63bce9c-1.jpg

# curl -X POST http://localhost:5000/pred
# empty file
# curl -H "Content-type: application/json" -X POST http://localhost:5000/pred -d "{\"file\":\"\"}"
# curl -H "Content-type: application/json" -X POST http://localhost:5000/pred -d "{\"file\":\"file.jpg\"}"

# not working
#curl -X POST -H "Content-type: application/json" http://localhost:5000/pred -d '{"file":"file.jpg"}'
# working
# curl -X POST -H "Content-type: application/json" http://localhost:5000/pred -d "{\"file\":\"file.jpg\"}"
# curl -H "Content-type: application/json" -X POST http://localhost:5000/pred --data "{\"file\":\"C:\\Users\\3879326\\Desktop\\work\\Freight_Dim_scan\\UAT_Testing\\Freight_UI\\090dbba9d63bce9c-1.jpg\"}"


# url : http://127.0.0.1:5000/pred
# curl -H "Content-type: application/json" -X POST http://localhost:5000/pred -d "{\"file\":\"090dbba9d63bce9c-1.jpg\"}"
# curl -H "Content-type: application/json" -X POST http://localhost:5000/pred -d "{\"file\":\"C:\\Users\\3879326\\Desktop\\work\\Freight_Dim_scan\\UAT_Testing\\Freight_UI\\090dbba9d63bce9c-1.jpg\"}"


# {
# 	"file" : "C:\\Users\\3879326\\Desktop\\work\\Freight_Dim_scan\\UAT_Testing\\Freight_UI\\090dbba9d63bce9c-1.jpg"
# }

