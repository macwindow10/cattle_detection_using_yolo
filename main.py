import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
import cv2
from cattle_detection import detect_image

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = '/static/images'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 1024

Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('POST')
        image = request.files['cattle_image']
        image.save(os.path.join('static/images', image.filename))
        print('image.filename: ', image.filename)
        print(os.path.join('static/images', image.filename));
        img = cv2.imread(os.path.join('static/images', image.filename), cv2.IMREAD_COLOR)
        # print(type(img))
        result_img = detect_image(img)
        full_filename = os.path.join('static/images', 'detected.jpg')
        return render_template('index.html',
                               selected=os.path.join('static/images', image.filename),
                               detected=full_filename)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
