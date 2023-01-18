function supprimerReponse(numR){
    // Suppresion de l'id de la réponse
    let idReponses = $("#idReponses");
    let idRepTab = idReponses.val().split(",");
    let indexToRemove = idRepTab.indexOf(numR.toString())
    idRepTab.splice( indexToRemove, 1);
    idReponses.val(idRepTab.join());

    // Suppression de la réponse
    let divToRemove = document.getElementById("divReponse" + numR);
    return divToRemove.parentNode.removeChild(divToRemove);
}

function ajouterReponse(){
    let repContainer = $("#repListe");
    let nbRep = parseInt($("#nbReponses").val());

    // Ajout de la nouvelle réponse au HTML avec le bon id
    let html = "<div id=\"divReponse" + nbRep + "\">"
    html += "<input type=\"checkbox\" name=\"checkReponse" + nbRep + "\" id=\"checkReponse" + nbRep + "\">";
    html += "<input type=\"text\" name=\"textReponse" + nbRep + "\" id=\"textReponse"+ nbRep +"\" value=\"\" placeholder=\"Réponse\">";
    html += "<input type=\"button\" onclick=\"supprimerReponse("+ nbRep + ")\" value=\"Supprimer\"></div>";
    repContainer.append(html);  

    // Ajout du nouvel id à l'input caché idRéponses
    idRep = $("#idReponses");
    debut = idRep.val();
    idRep.val(debut + nbRep.toString() + ",");

    // Incrémentation du nombre de réponses pour la réponse suivante
    $("#nbReponses").val(nbRep+1);
}

