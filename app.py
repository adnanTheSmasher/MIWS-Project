from flask import Flask, render_template, jsonify, Response, request
import subprocess
import sys
import os
import webbrowser

app = Flask(__name__)

# ═══════════════════════════════════════════
#   Air Canvas — ye sirf cv2 ki window ko show karega nothing else as a subprocess in the background
# ═══════════════════════════════════════════
painter_process = None

@app.route('/launch-canvas')
def launch_canvas():
    global painter_process
    if painter_process and painter_process.poll() is None:
        painter_process.terminate()
    try:
        painter_process = subprocess.Popen(
            [sys.executable, 'AI_VirtualPainter.py'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return jsonify({'status': 'launched'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/canvas/stop')
def stop_canvas():
    global painter_process
    if painter_process and painter_process.poll() is None:
        painter_process.terminate()
        painter_process.wait()
        painter_process = None
    return jsonify({'status': 'stopped'})


# ═══════════════════════════════════════════
#   Quiz Game — ye sirf quizGameUi wali python ki script run karega
# ═══════════════════════════════════════════
@app.route('/launch-quiz')
def launch_quiz():
    global painter_process
    if painter_process and painter_process.poll() is None:
        painter_process.terminate()
        painter_process.wait()
    try:
        painter_process = subprocess.Popen(
            [sys.executable, 'quizGameUI.py'],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return jsonify({'status': 'launched'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}, 500)

@app.route('/quiz/stop')
def stop_quiz():
    global painter_process
    if painter_process and painter_process.poll() is None:
        painter_process.terminate()
        painter_process.wait()
        painter_process = None
    return jsonify({'status': 'stopped'})

# ═══════════════════════════════════════════
#   Page Routes
# ═══════════════════════════════════════════
@app.route('/')
def home():
    return render_template('index.html')




# ═══════════════════════════════════════════
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5500/')
    app.run(debug=False, threaded=True, port=5500)