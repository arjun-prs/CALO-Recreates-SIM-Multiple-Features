from flask import Flask, request, render_template
from Code.calo import *

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/result', methods=["POST"])
def result():
    if request.method == "POST":
        data = request.form["protocol"]
        f = request.files["outputFile"]
        line = f.read()
        line = line.decode("utf-8")
        lines = line.splitlines()
        if data == "MPLS":
            result = mpls(lines)
        elif data == "BGP":
            result = bgp(lines)
        elif data == "OSPF":
            result = ospf(lines)
        elif data == "ISIS":
            result = isis(lines)
        elif data == "EIGRP":
            result = eigrp(lines)
        elif data == "Multicast":
            result = multicast(lines)
        elif data == "Unified_MPLS":
            result = unified_mpls(lines)
        elif data == "Interface":
            result = interface(lines)
    return render_template("result.html", result=result)
