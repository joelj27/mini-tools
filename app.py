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

if __name__ =="__main__":
    app.run(debug=True)