function button_click(){
    const {
        questionType,
        answers,
        answersCount
    } = window.quizData;
    if (questionType === "choice")
        for (let i = 0; i < answersCount; i++){
            answer = document.getElementById("answer" + i);
            answer_label = document.getElementById("answer_label" + i);

            answer.setAttribute("onclick", "return false");
            if (answer.value === "True"){
                if (answer.checked)
                    answer_label.style.backgroundColor = '#008000';
                else
                    answer_label.style.backgroundColor = '#FFED29'; 
            } else if (answer.checked)
                answer_label.style.backgroundColor = '#C21807';
        }
    else{
        user_answer_text = document.getElementById("answer_text");
        is_correct = false;

        user_answer_text.setAttribute("readonly", "");
        for (let i = 0; i < answers.length; i++){
            if (answers[i].text.toLowerCase() === user_answer_text.value.toLowerCase()){
                user_answer_text.style.backgroundColor = '#008000';
                is_correct = true;
                break;
            }
        }
        if (!is_correct){
            user_answer_text.style.backgroundColor = '#C21807';
            document.getElementById("answer_text_right").hidden = false;
        }
    }
    document.getElementById("check_button").style.display = "none";
    document.getElementById("next_button").style.display = "block";
}