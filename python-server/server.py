from flask import Flask, request, render_template, url_for
from recoco import *
from werkzeug.utils import secure_filename
from video import *

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = '/home/kabeone/python-server/static/'
client_l = auth()

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/face", methods=['POST'])
def face():
    image1 = request.files['image1']
    video = request.files['video']

    if not image1 or not video:
        return render_template("error_input.html")
        
    image1.save(os.path.join(app.config['IMAGE_UPLOADS'], image1.filename))
    video.save(os.path.join(app.config['IMAGE_UPLOADS'], video.filename))
    print("Files downloaded")
    
    l = videoFrame('./static/' + image1.filename, './static/' + video.filename, client_l)
    if len(l) == 0:
        return render_template("failure.html")
    return render_template("success.html", src=image1.filename, list=l)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=9080)
