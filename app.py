from flask import Flask, render_template, jsonify, request
import numpy as np
import cv2


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play')
def play():
    return render_template('play.html')

@app.route('/ai_play', methods=['POST'])
def ai_play(ai):
    state = np.array(request.json['state']).reshape(1, 120, 160, 1)
    action = ai.predict(state)
    return jsonify({"action": action.argmax()})

if __name__ == "__main__":
    app.run(debug=True)
