import os
from flask import * 
from werkzeug.utils import secure_filename
from PIL import Image


app = Flask(__name__)
app.secret_key = 'asdfsdf'


# setting up upload and compressed folder 
UPLOAD_FOLDER = 'uploads/'
COMPRESSED_FOLDER = 'compressed/'

os.makedirs(UPLOAD_FOLDER , exist_ok=True)
os.makedirs(COMPRESSED_FOLDER , exist_ok=True)

# configure the upload folder 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

# allowed extension
ALLOWED_EXTENSIONS = {'jpg' , 'jpeg' , 'png','gif'}


def allowed_file(filename):
    return '.'in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def HomePage():
    return render_template('base.html')

@app.route('/dashboard/<action>')
def DasboardImageEditing(action):
    if action == 'image-editing':
       return render_template('imageediting.html')
    elif action == 'image-analysis':
        return render_template('imageanalysis.html')
    elif action == 'image-compression':
        return render_template('imagecompression.html')
    else:
        return 'error'
    

@app.route('/upload' , methods=['GET' , 'POST'])
def upload():
    if request.method == 'POST':
        if 'images' not in request.files:
            flash('No image provided')
            return redirect(request.url)

        quality = int(request.form.get('quality' , 100))
        images  = request.files.getlist('images')


        compressed_files = []

        for image in images : 
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                original_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                image.save(original_path)

                with Image.open(original_path) as img:
                    compressed_path = os.path.join(COMPRESSED_FOLDER, filename)
                    img.save(compressed_path , optimize=True , quality=quality)
                    compressed_files.append(compressed_path)

        return render_template('imagecompression.html',compressed_files=compressed_files)            


    else :
        return 'no post method'


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'] ,filename)

if __name__ == '__main__':
    app.run(debug=True)