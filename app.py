from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/api/settime", methods=["POST"])
def getTime():
    if request.method == "POST":
        print(request.json)
        return jsonify({"response":"response"})

if __name__ == '__main__':
    app.run(debug=True)