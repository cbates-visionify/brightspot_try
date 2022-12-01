import base64
import io
import os
import sys

from PIL import Image
from flask import Flask, render_template, request, jsonify, redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename

sys.path.insert(0, '/')

from source.compare_main import compute

app = Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists, delete folder and recreate if exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
else:
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/maskImage', methods=['POST'])
def mask_image():
    # print(request.files, file=sys.stderr)
    files = request.files.getlist('image')
    action = request.form.get('action')
    uploads = []

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        uploads.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    returned = compute(uploads[0], uploads[1], action)

    send_back = [None, None, None]

    for i, image in enumerate(returned):
        img = Image.fromarray(returned[i].astype("uint8"))
        raw_bytes = io.BytesIO()
        img.save(raw_bytes, "JPEG")
        raw_bytes.seek(0)
        send_back[i] = base64.b64encode(raw_bytes.read())

    return jsonify({'status': str(send_back[0]), 'status1': str(send_back[1]), 'status2': str(send_back[2])})


@app.route('/test', methods=['GET', 'POST'])
def test():
    print("log: got at test", file=sys.stderr)
    return jsonify({'status': 'succces'})


@app.route('/home')
def home():
    return render_template('index.jinja2')


@app.after_request
def after_request(response):
    print("log: setting cors", file=sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/favicon.ico')
def favicon():
    print('testing')
    print('root is {}'.format(os.path.join(app.root_path, 'static')), file=sys.stderr)
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def post_redirect_get():
    return redirect("home", code=303)


if __name__ == '__main__':
    app.run(debug=True)
