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
    let html = "<div id=\"divAnswer" + nbAnswer + "\">"
    html += "<input type=\"checkbox\" name=\"checkAnswer" + nbAnswer + "\" id=\"checkAnswer" + nbAnswer + "\">";
    html += "<input type=\"text\" name=\"textAnswer" + nbAnswer + "\" id=\"textAnswer" + nbAnswer + "\" value=\"\" placeholder=\"Réponse\">";
    html += "<input type=\"button\" onclick=\"deleteAnswer(" + nbAnswer + ")\" value=\"Supprimer\"></div>";
    answerContainer.append(html);

    // Ajout du nouvel id à l'input caché idRéponses
    idRep = $("#idAnswers");
    debut = idRep.val();
    idRep.val(debut + nbAnswer.toString() + ",");

    // Incrémentation du nombre de réponses pour la réponse suivante
    $("#nbAnswers").val(nbAnswer + 1);
}

function openFormPopup() {
    document.getElementById("popupForm").style.display = "block";
}

function closeFormPopup() {
    document.getElementById("popupForm").style.display = "none";
}

function addTag() {
    let tagInput = $("#newTagName");
    let tagName = tagInput.val().trim();

    if (tagName != "") {
        let otherTags = $(".checkBoxTag");
        let newTag = true;
        let nbTag = otherTags.length;

        otherTags.each(function(index, element){
            if($(element).attr("name") == tagName)
                newTag = false;
        });

        if(newTag){
            html = "<li><label for=\""+tagName+"\"><input type=\"checkbox\" name=\""+tagName+"\" class=\"checkBoxTag\">"+ tagName +"</label></li>"
            $("#newTagPlace").append(html);
            $("#newTags").val($("#newTags").val() + tagName +",");
        }
    }


}
