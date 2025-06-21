from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import parsers
from users.models import Journal, CustomUser, Class
from datetime import datetime
import json

def upload_file(request):
    # POST request uploading the file (if exist),
    # parse it (see parsers.py), and save it to DB
    # in "session" table as 'questions', creating 'score'
    # to make a results and redirect to "start_quiz" (see urls.py).
    if request.user.is_authenticated:
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
    else:
        return redirect('/')


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

        Journal.objects.create(
            student = request.user,
            score = round(score, 2),
            questions_count = total,
            datetime = datetime.now()
        )
    except:
        return redirect('upload_file')

    return render(request, 'result.html', {
        'score': round(score, 2),
        'total': total,
        'percent': int((score / total) * 100 if total > 0 else 0),
    })
    
def journal_view(request):
    student = request.GET.get('student')
    from_class = request.GET.get('from_class')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    min_score = request.GET.get('min_score')
    
    sort_by = request.GET.get('sort', '-datetime')
        
    results = Journal.objects.all()
    
    if student:
        results = results.filter(student_id=student)
    if from_class:
        results = results.filter(student__classID=from_class)
    if date_from:
        results = results.filter(datetime__gte=date_from)
    if date_to:
        results = results.filter(datetime__lte=date_to)
    if min_score:
        results = results.filter(score__gte=float(min_score))
    
    if sort_by == 'student':
        results = results.order_by('student__first_name')
    elif sort_by == '-student':
        results = results.order_by('-student__first_name')
    elif sort_by == 'class':
        results = results.order_by('student__classID_id')
    elif sort_by == '-class':
        results = results.order_by('-student__classID_id')
    else:
        results = results.order_by(sort_by)

    students = CustomUser.objects.filter(is_staff=False).order_by('first_name')
    classes = Class.objects.all()

    return render(request, 'journal.html', {
        'results': results,
        'students': students,
        'classes': classes,
        'current_student': student,
        'date_from': date_from,
        'date_to': date_to,
        'min_score': min_score,
        'current_sort': sort_by,
    })