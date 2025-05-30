#This module parsing the txt file with questions
'''
question is a list of:
[
    {
        question_id: int() - question ID
        text: str() - question text
        type: str() - type of question - choice of fill
        answers - list of dictionaries with answers looks like:
        [
            {
                'text': here is the answer text - string,
                'is_correct': here is the boolean state of answer - bool 
            },
        ]
    }
]
'''
from random import shuffle

def parse_quiz_file(file):
    questions = list()
    current_question = None
    question_lines = str()
    is_question = False

    for line in file:
        line = line.decode('utf-8').strip()

        if line.startswith('S:'):
            is_question = True
            question_lines = ''
            current_question = {
                'id': int(),
                'text': '',
                'type': 'fill' if '###' in line[2:] else 'choice',
                'answers': list()
            }
            questions.append(current_question)
            question_lines += (line[2:])

        elif line.startswith(('+:', '-:')):
            is_question = False
            current_question['text'] = question_lines
            current_question['answers'].append({
                'text': line[2:].strip(),
                'is_correct': line.startswith('+:'),
            })

        elif is_question:
            question_lines += (f'\n{line}')
    
    shuffle(questions)
    for id, question in enumerate(questions, start=1):
        question['id'] = id
        shuffle(question['answers'])
    
    return questions
