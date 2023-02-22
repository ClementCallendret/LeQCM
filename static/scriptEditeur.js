const idAnswers = JSON.parse($("#idAnswers").val());
const form = document.getElementById("questionForm");
const newTags = JSON.parse($("#newTags").val());

function changeQuestionMode(checkboxElem) {
    if (checkboxElem.checked) {
        document.getElementById("answerList").setAttribute("style", "");
        document.getElementById("addAnswerBut").setAttribute("style", "");
        document.getElementById("numeralAnswer").setAttribute("style", "display : None");
    }
    else {
        document.getElementById("answerList").setAttribute("style", "display : None");
        document.getElementById("addAnswerBut").setAttribute("style", "display : None");
        document.getElementById("numeralAnswer").setAttribute("style", "");
    }
}

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

function addAnswer() {
    let answerContainer = $("#answerList");
    let newId = maxOfTab(idAnswers) + 1;

    // Ajout de la nouvelle réponse au HTML avec le bon id
    let html = `
        <div id="divAnswer${newId}" class="divAnswer row align-items-center">
            <div class="col-sm-1">
                <input type="checkbox" name="checkAnswer${newId}" id="checkAnswer${newId}">
            </div>
            <div class="col-sm-9">
                <textarea class="inputAnswer form-control" name="textAnswer${newId}" id="textAnswer${newId}" value="" placeholder="Réponse"></textarea>
            </div>
            <div class="col-sm-2">
                <button type="button" class="btn btn-danger deleteButton" onclick="deleteAnswer(${newId})" value="Supprimer"><img src="/static/trash.png"></button>
            </div>
        </div>
    `
    answerContainer.append(html);
    idAnswers.push(newId);
}

//ajout d'un tag non existant
function addTag() {
    let tagInput = $("#newTagName");
    let tagName = tagInput.val().trim();

    if (tagName != "") {
        let otherTags = $(".checkBoxTag");
        let newTag = true;
        let nbTag = otherTags.length;

        // verification de la non existence
        otherTags.each(function (index, element) {
            if ($(element).attr("name") == tagName)
                newTag = false;
        });

        if (newTag) {
            html = "<li><label for=\"" + tagName + "\"><input type=\"checkbox\" name=\"" + tagName + "\" class=\"checkBoxTag\" checked>" + tagName + "</label></li>"
            $("#newTagPlace").append(html);
            newTags.push(tagName)
        }
    }
}

const inputTitre = document.getElementById("titleText");
inputTitre.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
    }
})

const inputTag = document.getElementById("newTagName");
inputTag.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        addTag();
    }
})

form.addEventListener("submit", (e) => {
    e.preventDefault();
});

function submitForm(mode) {
    $("#idAnswers").val(JSON.stringify(idAnswers))
    $("#newTags").val(JSON.stringify(newTags))

    $("<input />").attr("type", "hidden")
        .attr("name", "action")
        .attr("value", mode)
        .appendTo("#questionForm");

    form.submit()
}

document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        submitForm("Enregistrer");
    }
});