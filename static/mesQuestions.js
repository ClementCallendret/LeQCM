function filterByTags() {
    document.getElementById("selectAll").checked = false;
    questions = $("#questionCards").find(".questionCard");
    allTags = $("#tagList").find(".tagCheck");
    selectedTags = [];

    // récupération des tags cochés
    allTags.each(function () {
        if (this.checked) {
            selectedTags.push(this.name);
            this.checked = false;
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
        questions.each(function () {
            q = $(this)
            tags = getTags(q.find(".card-footer"));
            hasTag = false
            for (let i = 0; i < tags.length; i++) {
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

// trouve tous les tags d'une question
function getTags(cardFooter){
    tagsJQ = cardFooter.find(".etiquette")
    tags = []
    tagsJQ.each((i, v) => {
        tags.push(v.innerText)
    })
    return tags
}

function selectAllTag(c) {
    val = c.checked;
    $(".tagCheck").each((i, v) => {
        v.checked = val
    })
}
function selectAllSeq(c) {
    val = c.checked;
    $(".checkSequence").each((i, v) => {
        v.checked = val
    })
}
function selectAllQ(c) {
    val = c.checked;
    $(".checkQuestion").each((i, v) => {
        v.checked = val
    })
}

//si on décheck une question on décheck le selectAll
function checkTag(c) {
    if (! c.checked) {
        document.getElementById("selectAll").checked = false;
    }
}

//si on décheck une séquence on décheck le selectAll
function checkSeq(c) {
    if (! c.checked) {
        document.getElementById("selectAllSeq").checked = false;
    }
}

//si on décheck une question on décheck le selectAll
function checkQ(c) {
    if (! c.checked) {
        document.getElementById("selectAllQ").checked = false;
    }
}

function submitForm(destination) {
    let form = document.getElementById("questionsForm");
    form.action = destination;

    selectedQ = []
    $(".checkQuestion").each((i, v) => {
        if (v.checked) {
            selectedQ.push(parseInt(v.name))
        }
    })
    selectedS = []
    $(".checkSequence").each((i, v) => {
        if (v.checked) {
            selectedS.push(parseInt(v.name))
        }
    })

    $("#selectedQ").val(JSON.stringify(selectedQ))
    $("#selectedS").val(JSON.stringify(selectedS))

    form.submit()
}