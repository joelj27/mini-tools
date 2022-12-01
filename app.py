from flask import Flask,render_template,request,jsonify,send_file,after_this_request
from werkzeug.utils import secure_filename
import os
from PIL import Image
from queue import Queue
import time
from flask_pymongo import PyMongo
import configmodule
import io
import gridfs

app=Flask(__name__)
app.config.from_object(configmodule.DevelopmentConfig)
client = PyMongo(app, retryWrites=False)
db=client.db

path_update=[]
@app.route("/")
def home_page():
    return render_template("home.html")

def get_word_count(data):
    if len(str(data))  == 0:
        return 0
    else:
        data=data.split()
        length=len(data)
        return length

def get_camel_case(data):
    camel_case=data.title()
    return camel_case

def get_upper_case(data):
    upper_case=data.upper()
    return upper_case

def allowed_extension(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def check_file():
    if "file" not in request.files:
        jsonify({"error":"no file provided"})
        jdata={"error":"no file provided"}
        return  jdata,None
    global file
    file = request.files['file']
    if file.filename == "":
        jdata={"error":"file not provided"}
        jsonify({"error":"file not provided"})
        return  jdata,None
    if file and allowed_extension(file.filename):
        filename=secure_filename(file.filename)
        temp_file=file.read()
        db.upload_images.insert_one({'File_name':filename, 'File': temp_file})
        out=image_conveter(temp_file)
        jdata={"path":filename}
        return jdata, out
    else:
        jdata={"error":"file not suported"}
        return  jdata,None

def image_conveter(file_path):
    img=Image.open(io.BytesIO(file_path))
    img=img.convert("RGBA")
    buf = io.BytesIO()
    img.save(buf,format("png"))
    image=buf.getvalue()
    return image

@app.route("/wordcount")
def load_word_count():
    return render_template("word_count.html")

@app.route("/wordcount/wordcount_button", methods=['POST'])
def get_input():
    input_data=request.form["in_data"]
    output=get_word_count(input_data)
    db.word_count.insert_one({'Input':input_data, 'Word Count': output})
    return render_template("word_count.html",input_data=output)

@app.route("/camelcase")
def load_camelcase():
    return render_template("camelcase.html")

@app.route("/camelcase/camelcase_button", methods=['POST'])
def camel_case_out():
    input_data=request.form["in_data"]
    output=get_camel_case(input_data)
    db.camel_case.insert_one({'Input':input_data, 'Output': output})
    return render_template("camelcase.html",input_data=output)

@app.route("/uppercase")
def load_uppercase():
    return render_template("uppercase.html")

@app.route("/uppercase/uppercase_button", methods=['POST'])
def upper_case_out():
    input_data=request.form["in_data"]
    output=get_upper_case(input_data)
    db.upper_case.insert_one({'Input':input_data, 'Output': output})
    return render_template("uppercase.html",input1=input_data,output1=output)

@app.route("/imageconveter")
def load_imageconveter():
    return render_template("imageconveter.html",jdata=None)

@app.route("/imageconveter/imageconveter_button", methods=['POST'])
def updoad_image():
    global out_file
    response,out_file=check_file()
    if "path" in str(response):
        return  render_template("imageconveter.html",jdata=response["path"])
    else:
        jsonify({"data":response})
        return  render_template("imageconveter.html",jdata=response["error"])

@app.route("/imageconveter/imageconveter_button/download",  methods=['POST'])
def download():
    try:
        file_name=file.filename.split(".")[0]+".png"
        return send_file(io.BytesIO(out_file),mimetype="image/png",download_name=file_name,as_attachment=True)
    except Exception as e:
        return str(e)

    

if __name__ =="__main__":
    app.run()
    