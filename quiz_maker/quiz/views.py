from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import parsers


def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        try:
            questions = parsers.parse_quiz_file(file)
            request.session['questions'] = questions
            return redirect('start_quiz')
        except Exception as e:
            return render(request, 'upload_file.html', {'error': str(e)})
    return(render(request, 'upload_file.html'))

def start_quiz(request):
    questions = request.session.get('questions', [])
    if not questions:
        return redirect('upload_file')
    return render(request, 'start_quiz.html', {'questions': questions})

def result(request):
    if request.method == 'POST':
        questions = request.session.get('questions', [])
        score = 0
        total = len(questions)
        
        for i, question in enumerate(questions, start=1):
            user_answer = request.POST.get(f'answer_{i}', '').strip()
            if question['type'] == 'fill':
                if user_answer == '':
                    continue
                if user_answer.lower() in [answer['text'].lower() for answer in question['answers']]:
                    score += 1
            else:
                correct_answers = [answer['text'] for answer in question['answers'] if answer['is_correct']]
                user_answers = request.POST.getlist(f'answer_{i}')
                if user_answer == '':
                    continue
                if set(user_answers) == set(correct_answers):
                    score += 1
        
        return render(request, 'result.html', {
            'score': score,
            'total': total,
            'percent': int((score / total) * 100 if total > 0 else 0),
        })
    return redirect('upload_file')
