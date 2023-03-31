// crédit :  https://www.youtube.com/watch?v=wv7pvH1O5Ho

const draggable_list = document.getElementById('draggable-list');
const check = document.getElementById('check');
const form = document.getElementById("form");
const tagList = JSON.parse(document.getElementById("allTags").value);

// Store listitems
const listItems = [];

let dragStartIndex;
//createList();

// Insert list items into DOM
function createList() {
    $('#submitButton').removeAttr("hidden");
    $('#viewButton').addClass("hidden");
    for (let index = 0; index < tagList.length; index++) {
        const listItem = document.createElement('li');
        listItem.setAttribute('data-index', index);

        listItem.innerHTML = `
        <div id="divTag${tagList[index]}" class="draggable" draggable="true">
            </br>
                <div id="area"> 
                
                    <h4 style="padding-top: 38px;"> nombre de questions de ${tagList[index]}</h4> 
        
                    <div style="position: auto;">
                        <input type="number" min="0" class="inputQuantity form-control" name="${tagList[index]}" placeholder="0" style="width: 70px;">
                    </div>
                </div>
                </br></br>
        </div>
      `;

        listItems.push(listItem);

        draggable_list.appendChild(listItem);
    }
    addEventListeners();
}
/*
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
}

function addtoSequence(id) {
    $("#questionCard" + id).css("display", "none")

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
*/

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

