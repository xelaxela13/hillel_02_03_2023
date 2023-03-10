import os

import openai
from flask import Flask, render_template, request

app = Flask(__name__)
openai.api_key = "YOUR_KEY"


@app.route("/", methods=['GET', 'POST'])
def index():
    context = {}
    if request.method == 'POST':
        text = request.form.get('text')

        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=text,
                                            temperature=0,
                                            max_tokens=4000)
        context.update({'result': response.choices[0].text})
    return render_template('index.html', **context)
