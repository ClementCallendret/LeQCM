const socket = io();

socket.on('connect', () => {
    socket.emit('joinRoom', { "rId": getCurrentSId() });
});

socket.on('addOneConnected', () => {
    console.log("nouvelle Connection")
    $("#nbStudents").html((parseInt($("#nbStudents").contents()) + 1).toString());
})

function getCurrentSId() {
    return window.location.href.split('/').slice(-1)[0]
}

function showLiveAnswers() {
    socket.emit("showLiveAnswers", getCurrentSId())
}

socket.on("showLiveAnswers", (data) => {
    data = JSON.parse(data)
    console.log("Affichage des réponses lives")
    if (data.length == 2) {
        div = $("#answers")
        for (let i = 0; i < 5; i++) {
            if (data[0][i] != "None") {
                html = `
                <div id="liveAnswer${i.toString()}" class="progress liveAnswer">
                <div class="progress-bar" style="width:${data[1][i].toString()}%">${data[1][i].toString()}%
                </div></div>
                `
                div.append(html);
            }
        }
    }
    else {
        allAnswers = document.getElementsByClassName("divAnswer")
        for (let i = 0; i < allAnswers.length; i++) {
            html = `
            <div id="liveAnswer${i.toString()}" class="progress liveAnswer">
            <div class="progress-bar" style="width:${data[i].toString()}%">${data[i].toString()}%
            </div></div>
            `
            allAnswers[i].innerHTML += html;
        }
    }
})

function showCorrection() {
    socket.emit("showCorrection", getCurrentSId())
}

socket.on('showCorrection', (corrects) => {
    corrects = JSON.parse(corrects)
    console.log("Affichage de la correction : " + corrects)
    if (Array.isArray(corrects)) {
        for (i of corrects) {
            ans = $("#divAnswer" + i);
            ans.css("border-width", "7px");
            ans.css("border-color", "green")
        }
    }
    else{
        $('#correctionNumeral').append(corrects.toString())
    }
})

function stopAnswers() {
    socket.emit("stopAnswers", getCurrentSId())
}

socket.on("desactivateAnswers", () => {
    $("#validation").addClass("disabled")
})

function stopSession() {
    socket.emit("stopSession", getCurrentSId())
}

function sendAnswers() {
    let numeralAns = $("#numeralAnswer");
    if(numeralAns.length){
        val = numeralAns.val();
        if(val.length){
            socket.emit("sendAnswers", { "answers" : parseInt(val), "rId" : getCurrentSId()});
        }
    }
    else{
        checks = document.getElementsByClassName("checkAnswer");
        checkeds = [];
        for (let i = 0; i < checks.length; i++){
            if(checks[i].checked){
                checkeds.push(parseInt(checks[i].id))
            }
        }
        socket.emit("sendAnswers", { "answers" : parseInt(val), "rId" : getCurrentSId()});
    }
}