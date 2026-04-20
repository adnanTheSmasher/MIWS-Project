from flask import Flask, render_template, jsonify, Response, request
import subprocess
import sys
import os
import webbrowser

app = Flask(__name__)

processes = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script(name, script):
    global processes

    if name in processes and processes[name].poll() is None:
        processes[name].terminate()
        processes[name].wait()

    processes[name] = subprocess.Popen(
        [sys.executable, script],
        cwd=BASE_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

# ═══════════════════════════════════════════
#   Air Canvas — ye sirf cv2 ki window ko show karega nothing else, as a subprocess in the background
# ═══════════════════════════════════════════

@app.route('/launch-canvas')
def launch_canvas():
    try:
        run_script('canvas', 'AI_VirtualPainter.py')
        return jsonify({'status': 'launched'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ═══════════════════════════════════════════
#   Snake Game — ye sirf SnakeGameUI wali python ki script run karega
# ═══════════════════════════════════════════
@app.route('/launch-game')
def launch_snakeGame():
    try:
        run_script('snake', 'snakeGameUI.py')
        return jsonify({"status": "launched"})
    except Exception as e:
        return jsonify({"status": 'Error', "message": str(e)}, 500)


# ═══════════════════════════════════════════
#   Quiz Game — ye sirf quizGameUi wali python ki script run karega
# ═══════════════════════════════════════════
@app.route('/launch-quiz')
def launch_quiz():
    try:
        run_script('quiz', 'quizGameUI.py')
        return jsonify({'status': 'launched'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}, 500)

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