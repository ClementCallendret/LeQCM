// crédit :  https://www.youtube.com/watch?v=wv7pvH1O5Ho

const draggable_list = document.getElementById('draggable-list');
const check = document.getElementById('check');
const form = document.getElementById("form");
const tagList = JSON.parse(document.getElementById("allTags").value);
const selectTag = document.getElementById("newTagSelect");

// Store listitems
const listItems = [];

let dragStartIndex;
//createList();

function intervalSetter(){

    if (document.getElementById("intervalle").checked) { // si intervalle est checked, c'est que on veut les range
        console.log("Les intervalles sont demandées");
        $('#inputRange').removeAttr("hidden");
        $('#inputRange').addAttr("required");
        $("#inputFixe").addAttr("hidden");
        $("#inputFixe").removeAttr("required");
    }
    else {
        $('#inputFixe').removeAttr("hidden");
        $('#inputFixe').addAttr("required");
        $("#inputRange").addAttr("hidden");
        $("#inputRange").removeAttr("required");
    }
}

function removeTag(tag) {
    parent = document.getElementById("divTag" + tag).parentElement;
    for (ele of listItems) {
        if (ele.getAttribute('data-index') > parent.getAttribute('data-index')) {
            ele.setAttribute('data-index', ele.getAttribute('data-index') - 1)
        }
    }
    listItems.splice(listItems.indexOf(parent), 1);
    parent.remove();
    document.getElementById("option" + tag).disabled = false
}

function addTag() {
    const tag = selectTag.value;
    if(tag == "default"){
        return;
    }
    let index;
    if (listItems.length == 0)
        index = 0;
    else
        index = parseInt(listItems[listItems.length - 1].getAttribute('data-index')) + 1;

    index = index.toString();

    const listItem = document.createElement('li');
    listItem.setAttribute('data-index', index);

    listItem.innerHTML = `
        <div id="divTag${tag}" class="draggable borderedDiv" draggable="true">
                <div id="area"> 
                
                    <h4 style="padding-top: 38px;"> nombre de questions de ${tag}</h4> 
        
                    <div class="inputFix" style="position: auto;">
                        <input type="number" min="1" class="inputQuantity form-control" name="${tag}" placeholder="quantité" style="width: 70px;">
                    </div>
                    <div class="inputRange" style="position: auto;">
                        <label>min : <input type="number" min="1" class="inputQuantity form-control" name="${tag}min" placeholder="quantité" style="width: 70px;"><label>
                        <label>max : <input type="number" min="1" class="inputQuantity form-control" name="${tag}max" placeholder="quantité" style="width: 70px;"><label>
                    </div>
                    <button type="button" onclick="removeTag('${tag}')" class="btn btn-danger">supprimer</button>
                </div>
        </div>
        `;

    listItems.push(listItem);

    draggable_list.appendChild(listItem);
    addEventListeners();
    document.getElementById("option" + tag).disabled = true;
    selectTag.value = "default";

    intervalSetter();
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

