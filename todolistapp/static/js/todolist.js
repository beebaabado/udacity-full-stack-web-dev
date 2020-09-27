// Scripts to handle updating view
//

// UPDATE: does this script need to handle the return json?
// Loop through checkboxes and get find checked item send
// request to update completed value in database
//should refresh view
//todo complete checkboxes
const itemcheckboxes = document.querySelectorAll('.checkbox-completed-item');
     
for (let i = 0; i < itemcheckboxes.length; i++) {
 
  const checkbox = itemcheckboxes[i];
  checkbox.onchange = function(e) {
    const newCompleted = e.target.checked;
    const todoId = e.target.dataset['id'];
    fetch('/todos/' + todoId + '/set-completed', {
      method: 'POST',
      body: JSON.stringify({
        'completed': newCompleted
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function() {
      document.getElementById('error').className = 'hidden';
    })
    .catch(function() {
      document.getElementById('error').className = '';
    });
  };
}
// List complete checkboxes
const listcheckboxes = document.querySelectorAll('.checkbox-completed-list');
     
for (let i = 0; i < listcheckboxes.length; i++) {
 
  const checkbox = listcheckboxes[i];
  checkbox.onchange = function(e) {
    const newCompleted = e.target.checked;
    const listId = e.target.dataset['id'];
    document.getElementById(listId).classList.add("list-link:active");
  
    fetch('/lists/' + listId + '/set-completed', {
      method: 'POST',
      body: JSON.stringify({
        'completed': newCompleted
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function() {
      document.getElementById('error').className = 'hidden';
    })
    .catch(function() {
      document.getElementById('error').className = '';
    });
  };
}
// DELETE: Loop through delete buttons to find item(s) to delete
// send request to delete item from data base
// and remove the list element from page
// could try reloading page if response sends OK but
// faster just to remove item from view.
const deleteItems = document.querySelectorAll('.delete-item-button');
     
for (let i = 0; i < deleteItems.length; i++) {
 
  const item = deleteItems[i];
  item.onclick = function(e) {
    const todoId = e.target.dataset['id'];
    fetch('/todos/' + todoId + '/delete', {
      method: 'DELETE'
    })
    .then(function() {
      const itemToDelete = e.target.parentElement;  // get the List item
      console.log(itemToDelete);
      itemToDelete.remove();                 
    });
  };
}

const deleteList = document.querySelectorAll('.delete-list-button');
     
for (let i = 0; i < deleteList.length; i++) {
 
  const item = deleteList[i];
  item.onclick = function(e) {
    const listId = e.target.dataset['id'];
    fetch('/lists/' + listId + '/delete', {
      method: 'DELETE'
    })
    .then(function() {
      const listToDelete = e.target.parentElement;  // get the List item
      console.log(listToDelete);
      listToDelete.remove();                 
    });
  };
}


// CREATE: get description for new item and
// send request to add item to database
// only update by adding single item to view  but
// this code does not add cheeckbox and delete button
//  need to fix this...
document.getElementById('form-add-todo').onsubmit = function(e) {
    e.preventDefault();
    
    fetch('/todos/create', {
         method: 'POST',
         body: JSON.stringify({
           'description': document.getElementById('description').value,
           'todolist_id': document.getElementById('description').dataset['id']
         }),
         headers: {
           'Content-Type': 'application/json'
         }
     })
     .then(function(response) {
         return response.json();
     })
     .then(function(jsonResponse) {
             document.getElementById("error").className="hidden";
             console.log(jsonResponse);  
             const id = jsonResponse.id;                               
             const liItem = document.createElement('li');
             liItem.className="list-item";
             liItem.innerHTML = `<div class="todo-content-wrapper"><input type="checkbox" data-id=${id} class="checkbox-completed-item">${jsonResponse.description}<button class="delete-item-button" data-id=${id}>&cross;</button></div>`;
             console.log(liItem);
             document.getElementById("todolist").appendChild(liItem);
             console.log(document.getElementById("todos"));
             location.reload();
             })
     .catch(function() {
         document.getElementById("error").className="";
     });
};

document.getElementById('form-add-list').onsubmit = function(e) {
  e.preventDefault();
  
  fetch('/lists/create', {
       method: 'POST',
       body: JSON.stringify({
         'name': document.getElementById('listname').value
       }),
       headers: {
         'Content-Type': 'application/json'
       }
   })
   .then(function(response) {
       return response.json();
   })
   .then(function(jsonResponse) {
           document.getElementById("error").className="hidden";
           //console.log(jsonResponse);  

           const id = jsonResponse.id;                               
           const liItem = document.createElement('li');
           liItem.innerHTML = jsonResponse['name'];
           document.getElementById('lists').appendChild(liItem);
           location.reload();


           
           //liItem.className="list";
           //liItem.innerHTML = `<div class="list-content-wrapper"><input type="checkbox" data-id=${id} class="checkbox-completed-list">${jsonResponse.name}<button class="delete-list-button" data-id=${id}>&cross;</button></div>`;
           //console.log(liItem);
           //document.getElementById("lists").appendChild(liItem);
           //window.location(true);
           //console.log(document.getElementById("todolist"));
           })
   .catch(function() {
       document.getElementById("error").className="";
   });
};

