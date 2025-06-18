from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import parsers
import json

@login_required(login_url="/")
def upload_file(request):
    # POST request uploading the file (if exist),
    # parse it (see parsers.py), and save it to DB
    # in "session" table as 'questions', creating 'score'
    # to make a results and redirect to "start_quiz" (see urls.py).
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        try:
            questions = parsers.parse_quiz_file(file)
            request.session['questions'] = questions
            request.session['score'] = 0
            return redirect('start_quiz', 1)
        except Exception as e:
            return render(request, 'upload_file.html', {'error': str(e)})
    # GET request rendering the upload_file page
    return(render(request, 'upload_file.html'))

def start_quiz(request, question_id):
    # The function is checking if there is questions in "session" table in DB.
    # If there is not, function redirect the user to upload_file page (see urls.py).

    # Next_question function redirect the user to start_quiz with incrimented question_id
    # If questions has been ended, redirect to result page (see urls.py).
    def next_question():
        return redirect('start_quiz', question_id+1) if question_id < questions_len else redirect('result')
    try:
        question = request.session.get('questions', [])[question_id - 1]
    except:
        return redirect('upload_file')
    questions_len = len(request.session.get('questions', []))
        
    if not question:
        return redirect('upload_file')
    
    # POST request checking the user answers and adding score between 0 and 1
    # (1 - user answer(s) is totaly right, 0 - user answer(s) is totaly wrong).
    # After answers checked, next_question function is calling.
    if request.method == 'POST':
        if question['type'] == 'fill':
            user_answer: str = request.POST.get(f'answer', '').strip()
            if not user_answer:
                return next_question()
            elif user_answer.lower() in [answer['text'].lower().strip() for answer in question['answers']]:
                request.session['score'] += 1
            return next_question()
        else:
            user_answers: list = request.POST.getlist('answer', '')
            if not user_answers:
                return next_question()
            else:
                request.session['score'] += sum([int(ans == 'True') for ans in user_answers]) / len(user_answers) if len(user_answers) > 0 else 0
            return next_question()
    # GET request is rendering the start_quiz page, params:
    # 'question': current question,
    # 'answers_json': json type of answers (for visual JS script).
    answers_json = json.dumps([{'text': answer['text']} for answer in question['answers']], ensure_ascii=False)
    return render(request, 'start_quiz.html', {'question': question, 'answers_json': answers_json})

def result(request):
    # GET request is rendering the results page, which shows information
    # such as: score, total questions and percent of right answered questions.
    try:
        total = len(request.session.get('questions', []))
        score = request.session.get('score', [])
        request.session['score'] = 0

        return render(request, 'result.html', {
            'score': round(score, 2),
            'total': total,
            'percent': int((score / total) * 100 if total > 0 else 0),
        })
    except:
        return redirect('upload_file')
