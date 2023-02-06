function changeQuestionMode(checkboxElem){
    if(checkboxElem.checked){
        document.getElementById("answerList").setAttribute("style", "");
        document.getElementById("addAnswerBut").setAttribute("style", "");
        document.getElementById("numeralAnswer").setAttribute("style", "display : None");
    }
    else{
        document.getElementById("answerList").setAttribute("style", "display : None");
        document.getElementById("addAnswerBut").setAttribute("style", "display : None");
        document.getElementById("numeralAnswer").setAttribute("style", "");
    }
}

function deleteAnswer(numR) {
    // Suppresion de l'id de la réponse
    let idAnswers = $("#idAnswers");
    let idRepTab = idAnswers.val().split(",");
    let indexToRemove = idRepTab.indexOf(numR.toString())
    idRepTab.splice(indexToRemove, 1);
    idAnswers.val(idRepTab.join());

    // Suppression de la réponse
    let divToRemove = document.getElementById("divAnswer" + numR);
    return divToRemove.parentNode.removeChild(divToRemove);
}

function addAnswer() {
    let answerContainer = $("#answerList");
    let nbAnswer = parseInt($("#nbAnswers").val());

    // Ajout de la nouvelle réponse au HTML avec le bon id
    let html = "<div id=\"divAnswer" + nbAnswer + "\" class=\"divAnswer row align-items-center\">"
    html += "<div class=\"col-sm-1\"><label class=\"switch\"><input type=\"checkbox\" name=\"checkAnswer" + nbAnswer + "\" id=\"checkAnswer" + nbAnswer + "\"><span class=\"slider round\"></span></label></div>";
    html += "<div class=\"col-sm-10\"><textarea class=\"inputAnswer form-control\" name=\"textAnswer" + nbAnswer + "\" id=\"textAnswer" + nbAnswer + "\" value=\"\" placeholder=\"Réponse\"></textarea></div>";
    html += "<div class=\"col-sm-1\"><button type=\"button\" class=\"btn btn-danger deleteButton\" onclick=\"deleteAnswer(" + nbAnswer + ")\" value=\"Supprimer\"><img src=\"/static/trash.png\"></button></div></div>";
    answerContainer.append(html);

    // Ajout du nouvel id à l'input caché idRéponses
    idRep = $("#idAnswers");
    debut = idRep.val();
    idRep.val(debut + nbAnswer.toString() + ",");

    // Incrémentation du nombre de réponses pour la réponse suivante
    $("#nbAnswers").val(nbAnswer + 1);
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
            $("#newTags").val($("#newTags").val() + tagName + ",");
        }
    }
}

function filterByTags() {

    questions = $("#questionCards").find(".questionCard");
    allTags = $("#tagListMesQuestions").find(".tagCheck");
    selectedTags = [];

    // récupération des tags cochés
    allTags.each(function () {
        if (this.checked) {
            selectedTags.push(this.name);
        }
    });

    // si aucun montrer toutes les questions
    if (selectedTags.length == 0) {
        questions.each(function() {
            this.setAttribute("style","");
        });
    }
    // sinon on verifie si le tag appartient à la question grace à la chaine de charactères
    else{
        console.log(selectedTags)
        questions.each(function () {
        q = $(this)
        tags = q.find(".card-footer").text().split(";");
        hasTag=false
        for(let i=0; i < tags.length-1; i++) {
            if (selectedTags.includes(tags[i])) {
                hasTag = true;
            }
        }
        if(!hasTag){
            this.setAttribute("style","display : none");
        }
        else{
            this.setAttribute("style","");
        }
    })
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

