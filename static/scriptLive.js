const socket = io();
var nbAnswers;
var totalAnswers;
var percentAnswers;
var liveAnswers = false;
var typeAnswer;
var myAnswer;

socket.on('connect', () => {
    socket.emit('joinRoom', { "rId": getCurrentSId() });
});

socket.on('addOneConnected', () => {
    console.log("Nouvelle Connexion")
    $("#nbStudents").html((parseInt($("#nbStudents").text()) + 1).toString());
})
socket.on('rmOneConnected', () => {
    console.log("Nouvelle Déconnexion")
    $("#nbStudents").html((parseInt($("#nbStudents").text()) - 1).toString());
})
socket.on("addOneAnswer", () => {
    console.log("Nouvelle réponse")
    $("#nbAnswers").html((parseInt($("#nbAnswers").text()) + 1).toString());
});

function getCurrentSId() {
    return window.location.href.split('/').slice(-1)[0]
}

socket.on('newAnswer', (data) => {
    nbAnswers += 1;
    if (typeAnswer == 0) {
        for (a of data) {
            totalAnswers[a] += 1;
        }
    }
    else {
        if (data in totalAnswers) {
            totalAnswers[data] += 1;
        }
        else {
            totalAnswers[data] = 1;
        }
    }
    calculatePercentAnswers();
    actualiseLiveAnswers();
});

function calculatePercentAnswers() {
    if (typeAnswer == 0) {
        percentAnswers = [];
        for (let i = 0; i < totalAnswers.length; i++) {
            percentAnswers[i] = Math.round(totalAnswers[i] / nbAnswers * 100);
        }
    }
    else {
        percentAnswers = [];
        if (Object.keys(totalAnswers).length <= 5) {
            for (key in totalAnswers) {
                percentAnswers.push([key, Math.round(totalAnswers[key] / nbAnswers * 100)]);
            }
            percentAnswers.sort(function (a, b) {
                return b[1] - a[1];
            });
        }
        else {
            for (let i = 0; i < 4; i++) {
                let max = 0;
                let index;
                max = 0;
                for (key in totalAnswers) {
                    if (totalAnswers[key] > max && ![key, Math.round(totalAnswers[key] / nbAnswers * 100)] in percentAnswers) {
                        max = totalAnswers.key;
                        index = key;
                    }
                }
                percentAnswers.push([index, Math.round(max / nbAnswers * 100)]);
            }
            others = 0;
            for (key in totalAnswers) {
                if (![key, Math.round(totalAnswers[key] / nbAnswers * 100)] in percentAnswers) {
                    others += totalAnswers[key] / nbAnswers * 100;
                }
            }
            percentAnswers.autres = Math.round(max / nbAnswers * 100);
        }
    }
}

function showLiveAnswers() {
    console.log("Demande des réponses lives")
    socket.emit("showLiveAnswers", getCurrentSId())
}

socket.on("showLiveAnswers", (data) => {
    console.log("Affichage des réponses lives");
    console.log(data)
    if (data.typeAnswer == 0)
        $(".liveAnswer").removeClass("hidden");
    totalAnswers = data.answers;
    nbAnswers = data.nbAnswers;
    typeAnswer = data.typeAnswer;
    $("#nbAnswers").html(nbAnswers.toString());
    calculatePercentAnswers();
    actualiseLiveAnswers();
})

function actualiseLiveAnswers() {
    if (typeAnswer == 0) {
        for (let i = 0; i < percentAnswers.length; i++) {
            $("#liveBar" + i).css("width", percentAnswers[i].toString() + "%");
            $("#liveBar" + i).html(percentAnswers[i].toString() + "%");
        }
    }
    else {
        for (let i = 0; i < percentAnswers.length; i++) {
            $("#divAnswer" + i).removeClass("hidden");
            $("#liveNumAns" + i).html(percentAnswers[i][0].toString());
            $("#liveBar" + i).css("width", percentAnswers[i][1].toString() + "%");
            $("#liveBar" + i).html(percentAnswers[i][1].toString() + "%");
        }
    }
}

function showCorrection() {
    console.log("Demande de la correction")
    socket.emit("showCorrection", getCurrentSId())
}

socket.on('showCorrection', (corrects) => {
    console.log("Affichage de la correction");
    if (Array.isArray(corrects)) {
        for (i of corrects) {
            ans = $("#divAnswer" + i);
            ans.css("border-width", "7px");
            ans.css("border-color", "green")
        }
    }
    else {
        $('#correctionNumeral').removeClass("hidden")
        $('#correctionNumeral').html(corrects.toString())
    }
})

function stopAnswers() {
    console.log("Fermeture des réponses")
    socket.emit("stopAnswers", getCurrentSId())
}

socket.on("desactivateAnswers", () => {
    console.log("Désactivation de la réponse")
    $("#validation").addClass("disabled")
})

function sendAnswers() {
    console.log("Envoie des/de la réponses")
    let numeralAns = $("#numeralAnswer");
    if (numeralAns.length) {
        val = numeralAns.val();
        if (val.length) {
            socket.emit("sendAnswers", { "answers": parseInt(val), "rId": getCurrentSId() });
        }
        myAnswer = parseInt(val);
    }
    else {
        checks = document.getElementsByClassName("checkAnswer");
        checkeds = [];
        for (let i = 0; i < checks.length; i++) {
            if (checks[i].checked) {
                checkeds.push(parseInt(checks[i].id))
            }
        }
        socket.emit("sendAnswers", { "answers": checkeds, "rId": getCurrentSId() });
        myAnswer = checkeds;
    }
}

function nextQuestion() {
    console.log("Demande de la question suivante")
    socket.emit("nextQuestion", getCurrentSId());
}

socket.on("nextQuestion", () => {
    window.location.reload();
});

function stopSession() {
    socket.emit("stopSession", getCurrentSId());
}
socket.on("stopSession", (url) => {
    socket.emit("quitSession", getCurrentSId());
    window.location = url;
});