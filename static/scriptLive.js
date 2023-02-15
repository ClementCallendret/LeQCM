var socket = io();
socket.on('connect', () => {
    socket.emit('message', { m : 'I\'m connected!'});
});

socket.on("messageToClient", (data) => {
    $("#diviv").append(data.m);
})

function addLiveAnswersQCM(){
    allAnswers = $("#answers").find(".divAnswer");
    let html = "";
    allAnswers.each((i, v) => {
        let nbAnswered = 50; // inserer le nombre de personnes ayants proposés la réponse i
        html = "<div id=\"liveAnswer" + i.toString() + "\" class=\"progress liveAnswer\">";
        html += "<div class=\"progress-bar\" style=\"width:" + nbAnswered.toString() + "%\">" + nbAnswered.toString() + "</div></div>";
        v.append(html);
        html = "";
    });
}

function showCorrection(corrects){ // passer la liste des indexes des réponses correctes
    for(i in corrects){
        ans = $("#divAnswer" + i);
        ans.css("border-width", "7px");
        ans.css("border-color", "green")
    }
}