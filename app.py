from flask import Flask, render_template, jsonify, Response, request
import subprocess
import sys
import os
import random
import quizGame
import webbrowser

app = Flask(__name__)







#===============================================
#   Air Canvas Logic
#===============================================

painter_process = None

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
    webbrowser.open("http://127.0.0.1:5500/")
    app.run(debug=False, port=5500, use_reloader=False)

#===============================================
#   Air Canvas Logic - End
#===============================================


#===============================================
#   Quiz Game Logic 
#===============================================
QUESTIONS = [
    {"category": "Artificial Intelligence", "question": "Which algorithm is inspired by the human brain?",           "options": ["Decision Tree", "Neural Network", "Linear Regression", "K-Means"],                                                        "answer": 1},
    {"category": "Artificial Intelligence", "question": "Which search uses a heuristic to find the shortest path?", "options": ["BFS", "DFS", "A* Search", "Greedy Search"],                                                                               "answer": 2},
    {"category": "Artificial Intelligence", "question": "What does 'ML' stand for?",                                "options": ["Machine Logic", "Meta Learning", "Machine Learning", "Model Language"],                                                    "answer": 2},
    {"category": "Artificial Intelligence", "question": "MediaPipe detects how many hand landmarks?",               "options": ["10", "15", "21", "33"],                                                                                                    "answer": 2},
    {"category": "Computer Science",        "question": "Which data structure uses LIFO order?",                    "options": ["Queue", "Array", "Stack", "Linked List"],                                                                                  "answer": 2},
    {"category": "Computer Science",        "question": "What is the time complexity of Binary Search?",            "options": ["O(n)", "O(n^2)", "O(log n)", "O(1)"],                                                                                     "answer": 2},
    {"category": "Computer Science",        "question": "What does HTTP stand for?",                                "options": ["HyperText Transfer Protocol", "High Tech Transfer Process", "Host Transfer Text Protocol", "HyperText Transmission Path"], "answer": 0},
    {"category": "Computer Science",        "question": "Which language is used for web styling?",                  "options": ["JavaScript", "Python", "HTML", "CSS"],                                                                                    "answer": 3},
    {"category": "Python",                  "question": "What keyword defines a function in Python?",               "options": ["func", "define", "def", "function"],                                                                                       "answer": 2},
    {"category": "Python",                  "question": "Which library is used for computer vision in Python?",     "options": ["NumPy", "Pandas", "OpenCV", "Matplotlib"],                                                                                "answer": 2},
    {"category": "Python",                  "question": "What does len() return?",                                  "options": ["Last element", "List type", "Length of object", "Logic value"],                                                           "answer": 2},
    {"category": "General Knowledge",       "question": "Which planet is called the Red Planet?",                  "options": ["Venus", "Jupiter", "Mars", "Saturn"],                                                                                      "answer": 2},
    {"category": "General Knowledge",       "question": "What is the chemical symbol for Gold?",                   "options": ["Go", "Gd", "Au", "Ag"],                                                                                                    "answer": 2},
    {"category": "General Knowledge",       "question": "How many continents are on Earth?",                       "options": ["5", "6", "7", "8"],                                                                                                        "answer": 2},
    {"category": "General Knowledge",       "question": "What is the largest ocean on Earth?",                     "options": ["Atlantic", "Indian", "Arctic", "Pacific"],                                                                                "answer": 3},
    {"category": "General Knowledge",       "question": "What is the approximate speed of light?",                 "options": ["300 km/s", "3,000 km/s", "300,000 km/s", "30,000 km/s"],                                                                  "answer": 2},
]

quiz_session = {'questions': [], 'index': 0, 'score': 0, 'done': False}

def reset_quiz():
    q = random.sample(QUESTIONS, min(10, len(QUESTIONS)))
    quiz_session.update({'questions': q, 'index': 0, 'score':0, 'done': False})

reset_quiz()

#===============================================
#   Quiz Game Logic - End
#===============================================


#===============================================
#   Page Changing logic
#===============================================

# Home-Page
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/canvas')
def canvas_page():
    return render_template('canvas.html')


@app.route('/quiz')
def quiz_page():
    quizGame.start()
    reset_quiz()
    return render_template('quiz.html')

#===============================================
#   Page Changing logic - End
#===============================================

#===============================================
#   Quiz Game Logic Gesture Logic
#===============================================

@app.route('/quiz/gesture')
def get_quiz_gesture():
    return jsonify(quizGame.get_gesture())

@app.route('/quiz/question')
def get_questions():
    s = quiz_session
    if s['done'] or s['index'] >= len(s['questions']):
        return jsonify({'done': True, 'score':s['score'], 'total': len(s['questions'])})
    q = s["questions"][s['index']]
    return jsonify({
         'done':     False,
        'index':    s['index'],
        'total':    len(s['questions']),
        'score':    s['score'],
        'category': q['category'],
        'question': q['question'],
        'options':  q['options']
    })

@app.route('/quiz/answer', methods=['POST'])
def submit_answer():
    s = quiz_session
    selected = request.get_json().get('answer', -1)
    if s['done'] or s['index'] >= len(s['questions']):
        return jsonify({'done': True, 'score': s['score'], 'total': len(s['questions'])})
    q = s["questions"][s["index"]]
    is_correct = (selected == q['answer'])
    if is_correct:
        s['score'] += 1
    s['index'] += 1
    done = s['index'] >= len(s["questions"])
    if done:
        s["done"] = True
    return jsonify({
        'is_correct': is_correct,
        'correct':    q['answer'],
        'score':      s['score'],
        'done':       done,
        'total':      len(s['questions']),
    })

@app.route('/quiz/restart', methods=['POST'])
def restart_quiz():
    reset_quiz()
    return jsonify({'status': 'ok'})

#===============================================
#   Quiz Game Logic Gesture Logic - End
#===============================================


if __name__ == "__main__":
    #webbrowser.get()
    app.run(debug=False, threaded=True, port=5500)