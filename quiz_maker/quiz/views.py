from django.shortcuts import render, redirect
from . import parsers


def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        try:
            questions = parsers.parse_quiz_file(file)
            request.session['questions'] = questions
            request.session['score'] = 0
            return redirect('start_quiz', 1)
        except Exception as e:
            return render(request, 'upload_file.html', {'error': str(e)})
    return(render(request, 'upload_file.html'))

def start_quiz(request, question_id):
    def next_question():
        return redirect('start_quiz', question_id+1) if question_id < questions_len else redirect('result')
    
    question = request.session.get('questions', [])[question_id - 1]
    questions_len = len(request.session.get('questions', []))
        
    if not question:
        return redirect('upload_file')
    
    if request.method == 'POST':
        if question['type'] == 'fill':
            user_answer: str = request.POST.get(f'answer', '').strip()
            if not user_answer:
                return next_question()
            elif user_answer.lower() in [answer['text'].lower() for answer in question['answers']]:
                request.session['score'] += 1
                return next_question()
        else:
            user_answers: list = request.POST.getlist('answer', '')
            if not user_answers:
                return next_question()
            else:
                user_answers = [int(ans == 'True') for ans in user_answers]
                request.session['score'] += sum(user_answers) / len(user_answers) if len(user_answers) > 0 else 0
                return next_question()
    return render(request, 'start_quiz.html', {'question': question})

def result(request):
    total = len(request.session.get('questions', []))
    score = request.session.get('score', [])
    request.session['score'] = 0

    return render(request, 'result.html', {
        'score': round(score, 2),
        'total': total,
        'percent': int((score / total) * 100 if total > 0 else 0),
    })
