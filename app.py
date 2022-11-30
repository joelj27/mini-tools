from flask import Flask,render_template,request,jsonify,send_file,after_this_request
from werkzeug.utils import secure_filename
import os
from PIL import Image
from queue import Queue
import time




app=Flask(__name__)

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
        return  jdata
    file = request.files['file']
    if file.filename == "":
        jdata={"error":"file not provided"}
        jsonify({"error":"file not provided"})
        return  jdata
    if file and allowed_extension(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        file_path=str(os.path.join(app.config["UPLOAD_FOLDER"],filename))
        out=image_conveter(file_path)
        jdata={"path":out}
        return jdata
    else:
        jdata={"error":"file not suported"}
        return  jdata

def image_conveter(file_path):
    if_image_folder_list=os.listdir("static\edited_images")
    for i in if_image_folder_list:
        os.remove("static\edited_images/"+i)
    img=Image.open(file_path)
    img=img.convert("RGBA")
    output_path=file_path.replace("static\images","static\edited_images").split(".")
    output_path=output_path[0]+".png"
    path_update.clear()
    path_update.append(output_path)
    img.save(output_path)
    os.remove(file_path)
    return output_path

@app.route("/wordcount")
def load_word_count():
    return render_template("word_count.html")

@app.route("/wordcount/wordcount_button", methods=['POST'])
def get_input():
    input_data=request.form["in_data"]
    output=get_word_count(input_data)
    return render_template("word_count.html",input_data=output)

@app.route("/camelcase")
def load_camelcase():
    return render_template("camelcase.html")

@app.route("/camelcase/camelcase_button", methods=['POST'])
def camel_case_out():
    input_data=request.form["in_data"]
    output=get_camel_case(input_data)
    return render_template("camelcase.html",input_data=output)

@app.route("/uppercase")
def load_uppercase():
    return render_template("uppercase.html")

@app.route("/uppercase/uppercase_button", methods=['POST'])
def upper_case_out():
    input_data=request.form["in_data"]
    output=get_upper_case(input_data)
    return render_template("uppercase.html",input1=input_data,output1=output)

@app.route("/imageconveter")
def load_imageconveter():
    return render_template("imageconveter.html",jdata=None)

@app.route("/imageconveter/imageconveter_button", methods=['POST'])
def updoad_image():
    response=check_file()
    if "path" in str(response):
        return  render_template("imageconveter.html",jdata=response["path"])
    else:
        jsonify({"data":response})
        return  render_template("imageconveter.html",jdata=response["error"])

@app.route("/imageconveter/imageconveter_button/download",  methods=['POST'])
def download():
    try:
        global path
        path = path_update[0]
        file_name=path.split("\\")[-1]
        return send_file(path,file_name,as_attachment=True)
    except Exception as e:
        return str(e)

    

if __name__ =="__main__":
    app.run()
    app.config.from_object(config.Config)