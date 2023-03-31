const socket = io();
let nbAnswers;
let totalAnswers;
let percentAnswers;
let myAnswer;
let layout;
const colors = ['#F9801D', '#C74EBD', '#3AB3DA', '#FED83D', '#80C71F', '#ED6DAC', '#474F52', '#168B89', '#AA5DA1', '#3F4BA6', '#835432', '#5E7C16', '#B02E26', '#1D1D21']

//totalAnswers = { caca : 10, pipi : 25, popo: 15, algerie : 8, baleine : 39, orchide : 28, pissenlit : 2, weed : 20, raviolits : 55}

// append the svg object to the body of the page
let svg = d3.select("#wordCloud").append("svg")
    .attr("width", "100%")
    .attr("height", 500)

// This function takes the output of 'layout' above and draw the words
// Wordcloud features that are THE SAME from one word to the other can be here
function draw(words) {
    svg.selectAll("*").remove();
    svg
        .append("g")
        .attr("transform", "translate(" + window.innerWidth / 2 + "," + layout.size()[1] / 2 + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function (d) { return d.size; })
        .style("fill", function () { return colors[Math.floor(Math.random() * 14)]; })
        .attr("text-anchor", "middle")
        .style("font-family", "Impact")
        .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) { return d.text; });
}

function updateCloud() {
    // Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
    // Wordcloud features that are different from one word to the other must be here
    layout = d3.layout.cloud()
        .size([$("#wordCloud").width(), $("#wordCloud").height()])
        .words(JSON.parse(JSON.stringify(percentAnswers)))
        .padding(5)        //space between words
        .rotate(function () { return 0; })
        .fontSize(function (d) { return 10*Math.sqrt(d.size); })      // font size of words
        .canvas( function() { return document.createElement("canvas").attr("id", "myCanvas"); })
        .on("end", draw);
    layout.start();
}


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
    else if (typeAnswer == 1){
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
    else {
        n = Object.values(totalAnswers).reduce((a, b) => a + b, 0);;
        percentAnswers = [];
        for (key in totalAnswers)
            percentAnswers.push({text : key, size : totalAnswers[key] / n * 1000})
    }
}

function showLiveAnswers() {
    console.log("Demande des réponses lives")
    socket.emit("showLiveAnswers", getCurrentSId())
}

socket.on("showLiveAnswers", (data) => {
    console.log("Affichage des réponses lives");
    console.log(data)
    $(".liveAnswer").removeClass("hidden");
    totalAnswers = data.answers;
    nbAnswers = data.nbAnswers;
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
    else if (typeAnswer == 1) {
        for (let i = 0; i < percentAnswers.length; i++) {
            $("#divAnswer" + i).removeClass("hidden");
            $("#liveNumAns" + i).html(percentAnswers[i][0].toString());
            $("#liveBar" + i).css("width", percentAnswers[i][1].toString() + "%");
            $("#liveBar" + i).html(percentAnswers[i][1].toString() + "%");
        }
    }
    else {
        updateCloud();
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

    if (typeAnswer == 0) {
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
    else {
        let val = $("#inputAnswer").val();
        if (val.length) {
            if (typeAnswer == 1)
                val = parseInt(val);
            socket.emit("sendAnswers", { "answers": val, "rId": getCurrentSId() });
        }
        myAnswer = val;
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
    console.log("arret de la session")
    socket.emit("stopSession", getCurrentSId());
}
socket.on("stopSession", (url) => {
    socket.emit("quitSession", getCurrentSId());
    window.location = url;
});