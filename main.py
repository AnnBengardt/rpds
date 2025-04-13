from flask import Flask, request, render_template
from joblib import load
from dotenv import dotenv_values
from process_file import pre_process, run_pipeline, llm_filter

app = Flask(__name__)

config = dotenv_values(".env")


def get_key_phrases(doc_name, doc, api_tkn, limit=20):
    doc = pre_process(doc)

    kws = run_pipeline(doc, limit)

    kws = llm_filter(api_tkn, doc_name, kws)

    return kws


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        doc_name = request.form["doc_name"]
        doc_text = request.form["doc_text"]
        result = get_key_phrases(doc_name, doc_text, config["tkn"])
        return render_template("index.html", result=result, doc_name=doc_name, doc_text=doc_text)
    return render_template("index.html", result=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context=(config["crt"], config["key"]), debug=True)