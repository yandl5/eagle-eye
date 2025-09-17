from flask import Flask, render_template_string, request
from zeep import Client

app = Flask(__name__)

SOAP_URL = "http://soap-service:8000/?wsdl"

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CyberNews Client</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f9f9f9;
            font-size: 18px; /* aumenta a fonte geral */
        }
        h1 {
            color: #333;
            font-size: 28px;
        }
        form {
            margin-bottom: 20px;
        }
        input[type=text] {
            padding: 10px;
            font-size: 18px;
            width: 300px;
        }
        input[type=submit] {
            padding: 10px 20px;
            font-size: 18px;
            margin-left: 10px;
        }
        .result {
            margin-bottom: 15px;
            padding: 12px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            line-height: 1.6;
        }
        .result strong {
            color: #d9534f; /* vermelho para trending */
        }
        a {
            color: #0275d8;
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>CyberNews Client</h1>
    <form method="POST">
        <input type="text" name="keyword" placeholder="Digite a palavra-chave" required>
        <input type="submit" value="Buscar">
    </form>

    {% if results %}
        <h2>Resultados:</h2>
        {% for r in results %}
            <div class="result">
                {% if "[TRENDING]" in r %}
                    <strong>{{ r.split("->")[0] }}</strong> <br>
                {% else %}
                    {{ r.split("->")[0] }} <br>
                {% endif %}
                📎 <a href="{{ r.split('->')[1].strip() }}" target="_blank">Acessar notícia</a>
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        keyword = request.form.get("keyword")
        try:
            client = Client(SOAP_URL)
            results = client.service.search_news(keyword)
        except Exception as e:
            results = [f"Erro: {str(e)}"]
    return render_template_string(TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
