const sentForm = document.querySelector('#sents-form')
const sentInput1 = document.querySelector('#sents-form #sent1')
const sentInput2 = document.querySelector('#sents-form #word')
const sentSimil = document.querySelector('#sent-similarity')

const HIDDEN_CLASSNAME = "hidden";

function onSentSubmit(event) {
    event.preventDefault();
    const sent = sentInput1.value;
    const s_word = sentInput2.value;
    const values = {
        "id_": "sw",
        "question": sent,
        "keywords": s_word
    }
    const url = `http://45.32.89.216/similarity/sentence`

    axios.post(url, values)
        .then((res) => {
            console.log(res)
            console.log(res.data)
            sim_value = res.data.similarity
            sentSimil.innerText = `similarity: ${sim_value}`;
            sentSimil.classList.remove(HIDDEN_CLASSNAME);
        })
}

const questionFrom = document.querySelector('#question-form')
const question = document.querySelector('#question-form #question')
const keywords = document.querySelector('#question-form #keywords')
const isValid = document.querySelector('#is-valid')

function onQuestionSubmit(event) {
    event.preventDefault();
    isValid.classList.add(HIDDEN_CLASSNAME);
    const question_ = question.value;
    const keyword_ = keywords.value;
    const values = {
        "id_": "qk",
        "question": question_,
        "keywords": keyword_
    }
    const url = `http://45.32.89.216/similarity/question`

    axios.post(url, values)
        .then((res) => {
            console.log(res)
            console.log(res.data)
            data = res.data
            included = res.data.included[0]
            if (data.is_valid)
                isValid.innerText = `It is a valid question.`;
            else
                isValid.innerText = `It is not a valid question.`;

            isValid.classList.remove(HIDDEN_CLASSNAME);
        })
}

const kquestionFrom = document.querySelector('#k-question-form')
const kquestion = document.querySelector('#k-question-form #k-question')
const kkeywords = document.querySelector('#k-question-form #k-keywords')
const kisValid = document.querySelector('#k-is-valid')

function onkQuestionSubmit(event) {
    event.preventDefault();
    kisValid.classList.add(HIDDEN_CLASSNAME);
    const question_ = kquestion.value;
    const keyword_ = kkeywords.value;
    const values = {
        "id_": "qk",
        "question": question_,
        "keywords": keyword_
    }
    const url = `http://45.32.89.216/similarity/question/korean`

    axios.post(url, values)
        .then((res) => {
            console.log(res)
            console.log(res.data)
            data = res.data
            included = res.data.included[0]
            if (data.is_valid)
                kisValid.innerText = `It is a valid question.`;
            else
                kisValid.innerText = `It is not a valid question.`;

            kisValid.classList.remove(HIDDEN_CLASSNAME);
        })
}

sentForm.addEventListener("submit", onSentSubmit)
questionFrom.addEventListener("submit", onQuestionSubmit)
kquestionFrom.addEventListener("submit", onkQuestionSubmit)