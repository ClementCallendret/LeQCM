let myLabels = [];
let myLabelsLink = [];
let nbParticipant = [[], []];
let maxNbAnswers = 0;

getDatas();

function getDatas(){
    mySessions = JSON.parse(document.getElementById("datasJson").value);
    for(myS of mySessions){
        myLabels.push(myS.date);
        myLabelsLink.push(myS.id);
        nbParticipant[0].push(myS.nbAnswers[0]);
        nbParticipant[1].push(myS.nbAnswers[1]);
        if (myS.nbAnswers[0] > maxNbAnswers){
            maxNbAnswers = myS.nbAnswers[0];
        }
    }
}

// configuration pour l'affichage du diagramme 
config = {
    type: 'bar',
    data: {
        labels: myLabels,
        labelsLink: myLabelsLink,
        datasets: [{
            label: 'Nb de réponses par question',
            data: nbParticipant[0],
            borderWidth: 2,
            borderColor: 'rgba(40, 165, 175, 0.75)',
            backgroundColor: "rgba(50, 197, 209, 0.6)"
        },
        {
            label: "Nb de bonnes réponses par question",
            data: nbParticipant[1],
            borderWidth: 2,
            borderColor: "rgba(38, 145, 29, 0.75)",
            backgroundColor: "rgba(47, 186, 35, 0.6)"
        }]
    },
    options: {
        scales: {
            x: {
                min: 0,
                max: 9
            },
            y: {
                beginAtZero: true,
                max: maxNbAnswers
            }
        },
        tailleIntervale: 10,
        layout: {
            padding: 20
        },
        responsive: true,
        maintainAspectRatio: false,
    }
};
Chart.defaults.color = '#424646';
Chart.defaults.font.size = 14;
const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, config);

// redirige sur la page de la session cliquée
function clickHandler(click) {
    const points = myChart.getElementsAtEventForMode(click, 'nearest', { intersect: true }, true);
    if (points.length) {
        const firstPoint = points[0];
        const value = myChart.data.labelsLink[firstPoint.index];
        window.open("/archives/stats/" + value.toString());
    }
}
ctx.onclick = clickHandler;

function changeTailleIntervalle(input) {
    nbData = myChart.config.data.labels.length;
    newSize = Math.min(input.value, nbData);
    actualSize = myChart.config.options.tailleIntervale;
    sizeGap = newSize - actualSize;
    x = myChart.config.options.scales.x;

    if (sizeGap < 0) {
        x.max += sizeGap;
    }
    else if (sizeGap > 0) {
        if (x.max + sizeGap >= nbData) {
            x.max = nbData - 1;
            x.min = nbData - (newSize);
        }
        else {
            x.max += sizeGap;
        }
    }
    myChart.config.options.tailleIntervale = newSize;
    myChart.update();
}

// défilage sur le diagramme
function scrollButton(sens) {
    scrollSide(myChart, sens * myChart.config.options.tailleIntervale);
}

function scrollSide(chart, gap) {
    x = chart.config.options.scales.x;
    tailleIntervale = chart.config.options.tailleIntervale;
    nbData = chart.config.data.labels.length;
    if (gap > 0) {
        if (x.max + gap >= nbData) {
            x.max = nbData - 1;
            x.min = nbData - (tailleIntervale);
        }
        else {
            x.min += gap;
            x.max += gap;
        }
    } else if (gap < 0) {
        if (x.min + gap <= 0) {
            x.max = tailleIntervale - 1;
            x.min = 0;
        }
        else {
            x.max += gap;
            x.min += gap;
        }
    }
    myChart.update();
}

myChart.canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    if (e.deltaY < 0) {
        scrollSide(myChart, -1);
    }
    else if (e.deltaY > 0) {
        scrollSide(myChart, 1);
    }
})

let lastTouchEnd = 0;
let lastScrollLeft = false; // sens du dernier scroll tactile

// décalage sur le diagramme (tactile)
myChart.canvas.addEventListener('touchmove', (e) => {
    for (let i = 0; i < e.changedTouches.length; i++) {
        if (lastTouchEnd - e.changedTouches[i].pageX > 60) {
            if (!lastScrollLeft) {
                scrollSide(myChart, 1);
            }
            lastTouchEnd = e.changedTouches[i].pageX;
            lastScrollLeft = false;

        }
        else if (lastTouchEnd - e.changedTouches[i].pageX < -60) {
            if (lastScrollLeft) {
                scrollSide(myChart, -1);
            }
            lastTouchEnd = e.changedTouches[i].pageX;
            lastScrollLeft = true;
        }
    }
}, false);
