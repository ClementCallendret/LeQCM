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
        questions.each(function () {
            this.setAttribute("style", "");
        });
    }
    // sinon on verifie si le tag appartient à la question grace à la chaine de charactères
    else {
        console.log(selectedTags)
        questions.each(function () {
            q = $(this)
            tags = q.find(".card-footer").text().split(";");
            hasTag = false
            for (let i = 0; i < tags.length - 1; i++) {
                if (selectedTags.includes(tags[i])) {
                    hasTag = true;
                }
            }
            if (!hasTag) {
                this.setAttribute("style", "display : none");
            }
            else {
                this.setAttribute("style", "");
            }
        })
    }
}

function submitForm(destination) {
    let form = document.getElementById("questionsForm");
    form.action = destination;

    selectedQ = []
    $(".checkQuestion").each((i, v) => {
        if(v.checked){
            selectedQ.push(parseInt(v.name))
        }
    })
    selectedS = []
    $(".checkSequence").each((i, v) => {
        if(v.checked){
            selectedS.push(parseInt(v.name))
        }
    })

    $("#selectedQ").val(JSON.stringify(selectedQ))
    $("#selectedS").val(JSON.stringify(selectedS))

    form.submit()
}