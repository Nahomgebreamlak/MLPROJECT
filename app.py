from math import perm
from flask import Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import classifier
from train_models import trainmaltifeatue,trainpermission
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = './static/upload/'

if os.path.exists(app.config['UPLOAD_FOLDER']):
    print("directory exists")
else:
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print("directory created")

@app.route("/", methods=["GET", "POST"])
def homePage():
    algorithms = {'SVM with Multi Feature': '95 %', 'SVM with Permission': '98 %'}
    result, accuracy, name, sdk, size ,perm= '', '', '', '', '',''
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.apk'):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if request.form['algorithm'] == 'SVM with Multi Feature':
                accuracy = algorithms['SVM with Multi Feature']
                result, name, sdk, size,perm = classifier.predict(os.path.join(app.config['UPLOAD_FOLDER'], filename), 0)
            elif request.form['algorithm'] == 'SVM with Permission':
                accuracy = algorithms['SVM with Permission']
                result, name, sdk, size,perm = classifier.predict(os.path.join(app.config['UPLOAD_FOLDER'], filename), 1)
    
    
    return render_template("index.html",result=result, algorithms=algorithms.keys(), accuracy=accuracy, name=name,
                           sdk=sdk, size=size,perm=perm)
    
    
    
@app.route("/train")
def trainmodel():
    report=trainpermission()
    return render_template("trainmodel.html", report=report)
      
@app.route("/multitrain")
def trainmodelmulti():
    report=trainmaltifeatue()
    return render_template("trainmodel.html", report=report)
    
if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
