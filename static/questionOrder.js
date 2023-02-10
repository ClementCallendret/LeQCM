// on va pas se mytho https://www.youtube.com/watch?v=wv7pvH1O5Ho

const draggable_list = document.getElementById('draggable-list');
const check = document.getElementById('check');

// Store listitems
const listItems = [];

let dragStartIndex;

createList();

// Insert list items into DOM
function createList() {
    for (let index = 0; index < 5; index++) {
        const listItem = document.createElement('li');

        listItem.setAttribute('data-index', index);

        listItem.innerHTML = `
        <div class="draggable card questionCard" draggable="true">
            <div class="card-header" >
                <input type="checkbox" name="1" class="checkBoxQuestion">
                <a href="/editeur/1" class="link-dark">${index}</a>
            </div>
            <div class="card-body"></div>
            <div class="card-footer" style="color:blue">2;</div>
        </div>
      `;

        listItems.push(listItem);

        draggable_list.appendChild(listItem);
    }
    addEventListeners();
}

function dragStart() {
    //console.log('Event: ', 'dragstart');
    dragStartIndex = +this.closest('li').getAttribute('data-index');
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
            listItems[i-1].appendChild(item);
        }
    }
    else{
        for (let i = toIndex ; i < fromIndex; i++) {
            const item = listItems[i].querySelector('.draggable');
            listItems[i+1].appendChild(item);
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