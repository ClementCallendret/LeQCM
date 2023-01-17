function supprimerReponse(numR){
    let element = document.getElementById("divReponse" + numR);

    let idsElement = $("#idEachReps");
    let ids = idsElement.val().split(",");

    console.log(ids);

    let indexToRemove = ids.indexOf(numR.toString())
    console.log("pos : " + indexToRemove + " val : " + ids[indexToRemove] );
    ids.splice( indexToRemove, 1);

    console.log(ids);

    idsElement.val(ids.join());

    return element.parentNode.removeChild(element);
}

function ajouterReponse(){
    let container = $("#repListe");
    let nbRep = parseInt($("#nbRep").val());

    let newRep = "<div class=\"row\" id=\"divReponse" + nbRep + "\">"
    newRep += "<input type=\"checkbox\" name=\"checkReponse" + nbRep + "\" id=\"checkReponse" + nbRep + "\">";
    newRep += "<input type=\"text\" name=\"textReponse" + nbRep + "\" id=\"textReponse"+ nbRep +"\" value=\"\">";
    newRep += "<input type=\"button\" onclick=\"supprimerReponse("+ nbRep + ")\" value=\"Supprimer\"></div>";

    ids = $("#idEachReps");
    ids.val(ids.val() + nbRep + ",");

    container.append(newRep);   
    $("#nbRep").val(nbRep+1);
}

function checkTheBox(checkID){
    document.getElementById(checkID).checked = true;
}