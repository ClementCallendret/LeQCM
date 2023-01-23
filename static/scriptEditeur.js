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
    html += "<div class=\"col-sm-1\"><input type=\"checkbox\" name=\"checkAnswer" + nbAnswer + "\" id=\"checkAnswer" + nbAnswer + "\"></div>";
    html += "<div class=\"col-sm-9\"><textarea class=\"inputAnswer form-control\" name=\"textAnswer" + nbAnswer + "\" id=\"textAnswer" + nbAnswer + "\" value=\"\" placeholder=\"Réponse\"></textarea></div>";
    html += "<div class=\"col-sm-2\"><input type=\"button\" class=\"btn btn-danger\" onclick=\"deleteAnswer(" + nbAnswer + ")\" value=\"Supprimer\"></div></div>";
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
    allTags = $("#tagList").find(".tagCheck");
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