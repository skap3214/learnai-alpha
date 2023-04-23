from flask import Flask, request, jsonify
from text_conversions import Converter
from text_grabber import Text

app = Flask(__name__)

@app.route('/transcript', methods=['POST'])
def text():
    data = request.get_json()
    youtube_url = data.get('url')
    text_grabber = Text()
    transcript = text_grabber.youtube(youtube_url)
    return jsonify({"response": transcript})

@app.route('/mcq', methods=['POST'])
def mcq():
    data = request.get_json()
    text = data.get('text')
    converter = Converter(text)
    result = converter.mcq()
    return jsonify(result)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    print("chatbot")
    text = request.json['text']
    question = request.json['question']
    converter = Converter(text)
    result = converter.chatbot(question)
    return jsonify({"response": result})

@app.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    text = data.get('text')
    converter = Converter(text)
    result = converter.summary()
    return jsonify({"response": result})

@app.route('/cheat_sheet', methods=['POST'])
def cheat_sheet():
    data = request.get_json()
    text = data.get('text')
    converter = Converter(text)
    result = converter.cheat_sheet()
    return jsonify({"response": result})

@app.route('/generate_code', methods=['POST'])
def generate_code():
    data = request.get_json()
    youtube_url = data.get('youtube_url')
    converter = Converter('')
    result = converter.generate_code(youtube_url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
