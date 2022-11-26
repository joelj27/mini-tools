from flask import Flask,render_template,request

app=Flask(__name__)

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
    return render_template("uppercase.html",input_data=output)

@app.route("/uppercase")
def load_uppercase():
    return render_template("uppercase.html")

@app.route("/uppercase/uppercase_button", methods=['POST'])
def upper_case_out():
    input_data=request.form["in_data"]
    output=get_upper_case(input_data)
    return render_template("uppercase.html",input1=input_data,output1=output)

if __name__ =="__main__":
    app.run(debug=True)