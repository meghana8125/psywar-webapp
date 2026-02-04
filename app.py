from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PsyWar Detection</title>
</head>
<body style="font-family:Arial;text-align:center;">
<h2>Fake News / Fear Detector</h2>

<textarea id="text" rows="6" cols="50" placeholder="Paste news text here"></textarea><br><br>

<button onclick="check()">Analyze</button>

<p id="result"></p>

<script>
function check(){
fetch('/analyze',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({text:document.getElementById("text").value})
})
.then(r=>r.json())
.then(d=>{
document.getElementById("result").innerHTML=d.result;
})
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json["text"].lower()

    fear_words = ["attack","kill","war","danger","terror","death"]

    score = sum([1 for w in fear_words if w in text])

    if score >= 2:
        res = "⚠️ High Fear / Possible Propaganda"
    else:
        res = "✅ Looks Normal"

    return jsonify({"result":res})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
