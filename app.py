from flask import * 

app = Flask(__name__)


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
    




if __name__ == '__main__':
    app.run(debug=True)