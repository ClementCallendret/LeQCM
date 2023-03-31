const idAnswers = JSON.parse($("#idAnswers").val());

function maxOfTab(tab) {
    if (tab.length == 0)
        return 0;
    return Math.max.apply(null, tab);
}


function deleteAnswer(numR) {
    // Suppresion de l'id de la réponse
    let indexToRemove = idAnswers.indexOf(numR)
    idAnswers.splice(indexToRemove, 1);

    // Suppression de la réponse
    let divToRemove = document.getElementById("divAnswer" + numR);
    return divToRemove.parentNode.removeChild(divToRemove);
}

