import urllib.request
import json
from flask import Flask, render_template, request
from reportlab.pdfgen import canvas
from textwrap import wrap

apodurl = "https://api.nasa.gov/planetary/apod?"
mykey = "api_key=11sle07cie83nVD759TY086DjGJtA98NoguyfQ78"

apodurlobj = urllib.request.urlopen(apodurl + mykey)

apodread = apodurlobj.read()

decodeapod = json.loads(apodread.decode('utf-8'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

date = ''
decodeapod = {}

@app.route('/upload',methods = ['POST'])
def upload():
    try:
        global date
        if request.method == "POST":
            date = request.form['dateInput']
        apodurl = "https://api.nasa.gov/planetary/apod?"
        mykey = "api_key=11sle07cie83nVD759TY086DjGJtA98NoguyfQ78&date="+date

        apodurlobj = urllib.request.urlopen(apodurl + mykey)

        apodread = apodurlobj.read()
        global decodeapod
        decodeapod = json.loads(apodread.decode('utf-8'))
    except Exception as e:
        return render_template('index.html', title = "Error 404... Date not found.")

    return render_template('index.html', url = decodeapod['url'],title = decodeapod['title'],exp = decodeapod['explanation'])

@app.route('/download')
def download():
    c = canvas.Canvas("img.pdf")
    global decodeapod
    title = c.beginText()
    title.setTextOrigin(10,825)
    title.setFont("Helvetica-Oblique", 20)
    title.textLine(decodeapod['title'])
    c.drawText(title)
    c.drawImage(decodeapod['url'],10,300,width = 300,height=500)
    c.showPage()
    t = c.beginText()
    t.setTextOrigin(10,825)
    text = "Explanation : " + decodeapod['explanation']
    wrapped_text = "\n".join(wrap(text,80))
    t.textLines(wrapped_text)
    c.drawText(t)
    c.save()
    return render_template('index.html', url = decodeapod['url'],title = decodeapod['title'],exp = decodeapod['explanation'],extra = "Image saved as pdf")

if __name__ == '__main__':
    app.run(port = 5001)
