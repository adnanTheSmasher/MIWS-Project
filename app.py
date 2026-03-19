from flask import Flask, render_template, jsonify
import subprocess
import sys
import os

app = Flask(__name__)
painter_process = None

# Home-Page
@app.route('/')
def home():
    return render_template("index.html")

# Air Canvas Launcher
@app.route('/launch-canvas')
def launch_canvas():
    global painter_process

    # if agr pehle se open hai canvas to destroy kardo
    if painter_process and painter_process.poll() is None:
        painter_process.terminate()
    
    try:
        # iske niche wala code isko properly launch karega
        painter_process = subprocess.Popen(
            [sys.executable, 'AI_VirtualPainter.py'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return jsonify({'status': 'launched'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5500)

