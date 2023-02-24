const datas = [{ x: "12-02-21", id: 0, nbRep: 12, nbGood: 10 }, { x: "25-02-21", id: 1, nbRep: 19, nbGood: 18 }, { x: "01-03-21", id: 2, nbRep: 10, nbGood: 10 }, { x: "09-03-21", id: 3, nbRep: 5, nbGood: 2 },
{ x: "12-02-22", id: 0, nbRep: 12, nbGood: 10 }, { x: "25-02-22", id: 1, nbRep: 19, nbGood: 18 }, { x: "01-03-22", id: 2, nbRep: 10, nbGood: 10 }, { x: "09-03-22", id: 3, nbRep: 5, nbGood: 2 },
{ x: "12-02-23", id: 0, nbRep: 12, nbGood: 10 }, { x: "25-02-23", id: 1, nbRep: 19, nbGood: 18 }, { x: "01-03-23", id: 2, nbRep: 10, nbGood: 10 }, { x: "09-03-23", id: 3, nbRep: 5, nbGood: 2 },
{ x: "12-02-24", id: 0, nbRep: 12, nbGood: 10 }, { x: "25-02-24", id: 1, nbRep: 19, nbGood: 18 }, { x: "01-03-24", id: 2, nbRep: 10, nbGood: 10 }, { x: "09-03-24", id: 3, nbRep: 5, nbGood: 2 },
{ x: "12-02-25", id: 0, nbRep: 12, nbGood: 10 }, { x: "25-02-25", id: 1, nbRep: 19, nbGood: 18 }, { x: "01-03-25", id: 2, nbRep: 10, nbGood: 10 }, { x: "09-03-25", id: 3, nbRep: 5, nbGood: 2 }];

config = {
    type: 'bar',
    data: {
        labels: ["12-02-21", "25-02-21", "01-03-21", "09-03-21", "12-02-21", "25-02-21", "01-03-21", "09-03-21", "12-02-23", "25-02-23", "01-03-23", "09-03-23", "12-02-24", "25-02-24", "01-03-24", "09-03-24", "12-02-25", "25-02-25", "01-03-25", "09-03-25", "12-02-21", "25-02-21", "01-03-21", "09-03-21", "12-02-21", "25-02-21", "01-03-21", "09-03-21", "12-02-23", "25-02-23", "01-03-23", "09-03-23", "12-02-24", "25-02-24", "01-03-24", "09-03-24", "12-02-25", "25-02-25", "01-03-25", "09-03-25"],
        labelsLink: [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
        datasets: [{
            label: 'Number of Answers',
            data: [12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5, 12, 19, 10, 5],
            borderWidth: 1,
            borderColor: '#FF5733',
            backgroundColor: '#CA2B09'
        },
        {
            label: "Number of Good Answers",
            data: [10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2, 10, 18, 10, 2],
            borderWidth: 1,
            borderColor: '#3FEFE7',
            backgroundColor: '#28C2BB'
        }]
    },
    options: {
        scales: {
            x: {
                min: 0,
                max: 9
            },
            y: {
                beginAtZero: true
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

const ctx = document.getElementById('myChart');
const myChart = new Chart(ctx, config);


function clickHandler(click) {
    const points = myChart.getElementsAtEventForMode(click, 'nearest', { intersect: true }, true);
    if (points.length) {
        const firstPoint = points[0];
        const value = myChart.data.labelsLink[firstPoint.index];
        window.open("/stats/" + value.toString());
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
    if (e.deltaY < 0) {
        scrollSide(myChart, -1);
    }
    else if (e.deltaY > 0) {
        scrollSide(myChart, 1);
    }
})

var lastTouchEnd = 0;
var lastScrollLeft = false; // sens du dernier scroll tactile

myChart.canvas.addEventListener('touchmove', (e) => {
    // Iterate through the touch points that have moved and log each
    // of the pageX/Y coordinates. The unit of each coordinate is CSS pixels.
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
