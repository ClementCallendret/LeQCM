// crédit :  https://www.youtube.com/watch?v=wv7pvH1O5Ho

const draggable_list = document.getElementById('draggable-list');
const check = document.getElementById('check');
const form = document.getElementById("form");
const maxTags = JSON.parse(document.getElementById("allTags").value);
const selectTag = document.getElementById("newTagSelect");

// Store listitems
const listItems = [];

let dragStartIndex;
//createList();

function intervalSetter() {

    if (document.getElementById("intervalle").checked) { // si intervalle est checked, c'est que on veut les range
        console.log("Les intervalles sont demandées");
        $('.inputRange').each((i, e) => {
            $(e).removeAttr("hidden");
            $(e).prop("required", true);
        });
        $(".inputFixe").each((i, e) => {
            $(e).prop("hidden", true);
            $(e).removeAttr("required");
        });
        $("#text_nbr_questions").removeAttr("hidden");
        $("#nbr_questions").prop("required", true);
    }
    else {
        console.log("Les intervalles ne sont pas demandées");
        $('.inputFixe').each((i, e) => {
            $(e).removeAttr("hidden");
            $(e).prop("required", true);
        });
        $(".inputRange").each((i, e) => {
            $(e).prop("hidden", true);
            $(e).removeAttr("required");
        });
        $("#text_nbr_questions").prop("hidden", true);
        $("#nbr_questions").removeAttr("required");
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
    if (tag == "default") {
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
                        <label class="inputFixe">quantité : <input type="number" value="1" min="1" max="${maxTags[tag]}" class="inputQuantity inputFixe form-control" name="${tag}" style="width: 70px;"></label>
                        <label class="inputRange">min : <input type="number" value="1" min="1" max="${maxTags[tag]}" class="inputQuantity inputRange form-control" name="${tag}min" style="width: 70px;"></label>
                        <label class="inputRange">max : <input type="number" value="1" min="1" max="${maxTags[tag]}" class="inputQuantity inputRange form-control" name="${tag}max" style="width: 70px;"></label>
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