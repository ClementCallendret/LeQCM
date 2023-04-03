// crédit :  https://www.youtube.com/watch?v=wv7pvH1O5Ho

const draggable_list = document.getElementById('draggable-list');
const check = document.getElementById('check');
const form = document.getElementById("form");

// Store listitems
const listItems = [];

let dragStartIndex;
createList();

const inputT = document.getElementById('titleInput'); // get the input element
inputT.addEventListener('input', resizeInputT);
resizeInputT();

function resizeInputT() {
    inputT.style.width = inputT.value.length + "ch";
}

form.addEventListener("submit", (e) => {
    e.preventDefault();
});

function submitForm(destination) {
    orderedId = [];
    for (ele of listItems) {
        orderedId.push(parseInt(ele.querySelector('div').getAttribute("id")));
    }

    $("#orderedId").val(JSON.stringify(orderedId))

    if(destination == '/MesQuestions/PageQCM'){
        form.target = '_blank'
    }
    else{
        form.target = '_self'
    }

    form.action = destination;
    if (orderedId.length > 0)
        form.submit()
}

// Insert list items into DOM
function createList() {
    jsonQuestions = $("#questionJson").val();
    questions = JSON.parse(jsonQuestions);
    for (let index = 0; index < questions.length; index++) {
        $("#questionCard" + questions[index]["id"]).css("display", "none")
        $("#questionCard" + questions[index]["id"]).removeClass("selectable")

        const listItem = document.createElement('li');
        listItem.setAttribute('data-index', index);

        tagStr = ""
        for (t of questions[index]["tags"]) {
            tagStr += "<span class='etiquette'>" + t + "</span>"
        }

        listItem.innerHTML = `
        <div class="draggable card questionCard" id="${questions[index]["id"]}" draggable="true">
            <div class="card-header" >
                <span>${questions[index]["title"]}</span>
                <button type="button" onclick="removeQ(${questions[index]["id"]})" class="topRightBut btn btn-danger">X</button>
            </div>
            <div class="card-body">${questions[index]["state"]}</div>
            <div class="card-footer" style="color:blue">${tagStr}</div>
        </div>
      `;

        listItems.push(listItem);

        draggable_list.appendChild(listItem);
    }
    addEventListeners();
}

function removeQ(i) {
    parent = document.getElementById(i).parentElement;
    for (ele of listItems) {
        if (ele.getAttribute('data-index') > parent.getAttribute('data-index')) {
            ele.setAttribute('data-index', ele.getAttribute('data-index') - 1)
        }
    }
    listItems.splice(listItems.indexOf(parent), 1);
    parent.remove();
    $("#questionCard" + i).css("display", "block")
    $("#questionCard" + i).addClass("selectable")
}

function addtoSequence(id) {
    $("#questionCard" + id).css("display", "none")
    $("#questionCard" + id).removeClass("selectable")

    let index;
    if(listItems.length == 0)
        index = 0;
    else
        index = parseInt(listItems[listItems.length - 1].getAttribute('data-index')) + 1;
        
    index = index.toString();
    const listItem = document.createElement('li');
    listItem.setAttribute('data-index', index);
    
    tagStr = $("#questionCard" + id).find(".card-footer").html();
    state = $("#questionCard" + id).find(".card-body").html();
    title = $("#questionCard" + id).find(".card-header").find("span").html();

    listItem.innerHTML = `
        <div class="draggable card questionCard" id="${id}" draggable="true">
            <div class="card-header" >
                <span>${title}</span>
                <button type="button" onclick="removeQ(${id})" class="topRightBut btn btn-danger">X</button>
            </div>
            <div class="card-body">${state}</div>
            <div class="card-footer" style="color:blue">${tagStr}</div>
        </div>
      `;

    listItems.push(listItem);

    draggable_list.appendChild(listItem);
    addEventListeners();
}

function dragStart() {
    //console.log('Event: ', 'dragstart');
    dragStartIndex = +this.closest('li').getAttribute('data-index');
    console.log(dragStartIndex);
}

function dragEnter() {
    // console.log('Event: ', 'dragenter');
    this.classList.add('over');
}

function dragLeave() {
    // console.log('Event: ', 'dragleave');
    this.classList.remove('over');
}

function dragOver(e) {
    // console.log('Event: ', 'dragover');
    e.preventDefault();
}

function dragDrop() {
    // console.log('Event: ', 'drop');
    const dragEndIndex = +this.getAttribute('data-index');
    swapItems(dragStartIndex, dragEndIndex);

    this.classList.remove('over');
}

// Swap list items that are drag and drop
function swapItems(fromIndex, toIndex) {
    const movedItem = listItems[fromIndex].querySelector('.draggable');

    if (fromIndex < toIndex) {
        for (let i = fromIndex + 1; i <= toIndex; i++) {
            const item = listItems[i].querySelector('.draggable');
            listItems[i - 1].appendChild(item);
        }
    }
    else {
        for (let i = toIndex; i < fromIndex; i++) {
            const item = listItems[i].querySelector('.draggable');
            listItems[i + 1].appendChild(item);
        }
    }

    listItems[toIndex].appendChild(movedItem);
}

function addEventListeners() {
    const draggables = document.querySelectorAll('.draggable');
    const dragListItems = document.querySelectorAll('.draggable-list li');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', dragStart);
    });

    dragListItems.forEach(item => {
        item.addEventListener('dragover', dragOver);
        item.addEventListener('drop', dragDrop);
        item.addEventListener('dragenter', dragEnter);
        item.addEventListener('dragleave', dragLeave);
    });
}

// ------------------------------ Tri par tags ------------------------------ //

function filterByTags() {
    document.getElementById("selectAll").checked = false;
    questions = $("#questionCards").find(".questionCard.selectable");
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

function checkTag(c) {
    if (! c.checked) {
        document.getElementById("selectAll").checked = false;
    }
}