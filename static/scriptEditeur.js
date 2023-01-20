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

function addTag() {
    let tagInput = $("#newTagName");
    let tagName = tagInput.val().trim();

    if (tagName != "") {
        let otherTags = $(".checkBoxTag");
        let newTag = true;
        let nbTag = otherTags.length;

        otherTags.each(function (index, element) {
            if ($(element).attr("name") == tagName)
                newTag = false;
        });

        if (newTag) {
            html = "<li><label for=\"" + tagName + "\"><input type=\"checkbox\" name=\"" + tagName + "\" class=\"checkBoxTag\">" + tagName + "</label></li>"
            $("#newTagPlace").append(html);
            $("#newTags").val($("#newTags").val() + tagName + ",");
        }
    }


}

function filterByTags() {
    questions = $("#questionCards").find(".questionCard");
    allTags = $("#tagList").find(".tagCheck");
    selectedTags = [];
    if (selectedTags == []) {
        question.each(function() {
            $(this).css("display:flex;")
        return;})
    }
    console.log(selectedTags)
    allTags.each(function () {
        if (this.value) {
            console.tim
            selectedTags.push(this.name);
        }
    });

    questions.each(function () {
        q = $(this)
        tags = q.find(".card-footer").text().split(";");
        hasTag = false;
        console.log(tags)
        for(t in tags) {
            if (t in selectedTags) {
                hasTag = true
                
            }
        }
        if (!hasTag) {
            q.css("display","none")
        }
    })
}