from flask import Flask , render_template, request, redirect, flash
from time import sleep
import numpy as np
import argparse
import imutils
import glob
import cv2
import os



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './/img/'


def image_finder(template, target):

    print('finder Trigered')

    template = cv2.imread(template)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (template_height, template_weight) = template.shape[:2]

    image = cv2.imread(target)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])
        if resized.shape[0] < template_height or resized.shape[1] < template_weight:
        	break
        edged = cv2.Canny(resized, 50, 50)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)
    (_, maxLoc, r) = found
    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    (endX, endY) = (int((maxLoc[0] + template_weight) * r), int((maxLoc[1] + template_height) * r))
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 0), 10)
    cv2.rectangle(image, (startX, startY), (endX, endY), (255, 255, 255), 5)
    new_name = 'found_'+target
    cv2.imwrite('./static/result.jpg', image)


@app.route('/', methods = ['POST', 'GET'] )
def main():
  if request.method == 'POST':

    template = request.files['template']
    target = request.files['target']

    target.save(os.path.join('static/target.jpg'))
    template.save(os.path.join('static/template.jpg'))

    sleep(1)

    try:
        image_finder('static/template.jpg', 'static/target.jpg')

        return render_template('index.html')
    except Exception as e:
        print(e)
        return render_template('index.html')
  else:
    return render_template('index.html')

app.run(debug=True, port=5406)