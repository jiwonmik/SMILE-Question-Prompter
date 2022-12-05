const wordForm = document.querySelector('#words-form')
const wordInput1 = document.querySelector('#words-form #word1')
const wordInput2 = document.querySelector('#words-form #word2')
const simWord = document.querySelector('#most-sim-word')
const simValue = document.querySelector('#most-sim-value')

const sentForm = document.querySelector('#sents-form')
const sentInput1 = document.querySelector('#sents-form #sent1')
const sentInput2 = document.querySelector('#sents-form #word')
const sentSimil = document.querySelector('#sent-similarity')


const HIDDEN_CLASSNAME = "hidden";

function onWordSubmit(event){
    event.preventDefault();
    const word1 = wordInput1.value;
    const word2 = wordInput2.value;
    const values = {
        "question": word1,
        "keyword": word2
    }
    const url = `http://127.0.0.1:8000/word_similarity`

    axios.post(url, values)
        .then((res) => {
            console.log(res)
            console.log(res.data)
            most_sim_word = res.data.most_similars[0].word
            most_sim_value = res.data.most_similars[0].similarity
            simWord.innerText = `most similar word: ${most_sim_word}`;
            simWord.classList.remove(HIDDEN_CLASSNAME);
            simValue.innerText = `similarity: ${most_sim_value}`
            simValue.classList.remove(HIDDEN_CLASSNAME);
        })    
}

function onSentSubmit(event){
    event.preventDefault();
    const sent = sentInput1.value;
    const s_word = sentInput2.value;
    const values = {
        "question": sent,
        "keyword": s_word
    }
    const url = `http://127.0.0.1:8000/sentence_similarity`

    axios.post(url, values)
    .then((res) => {
        console.log(res)
        console.log(res.data)
        sim_value = res.data.similarity
        sentSimil.innerText = `similarity: ${sim_value}`;
        sentSimil.classList.remove(HIDDEN_CLASSNAME);
    })  
}

wordForm.addEventListener("submit", onWordSubmit)
sentForm.addEventListener("submit", onSentSubmit)