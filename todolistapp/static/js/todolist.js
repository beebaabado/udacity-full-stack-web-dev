// UPDATE: does this script need to handle the return json?
// Loop through checkboxes and get find checked item send
// request to update completed value in database
//should refresh view
const checkboxes = document.querySelectorAll('.checkbox-completed');
     
for (let i = 0; i < checkboxes.length; i++) {
 
  const checkbox = checkboxes[i];
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
    fetch('/todos/' + todoId + '/delete-item', {
      method: 'DELETE'
    })
    .then(function() {
      const itemToDelete = e.target.parentElement;  // get the List item
      console.log(itemToDelete);
      itemToDelete.remove();                 
    });
  };
}

// CREATE: get description for new item and
// send request to add item to database
// only update by adding single item to view  but
// this code does not add cheeckbox and delete button
//  need to fix this...
document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    
    fetch('/todos/create', {
         method: 'POST',
         body: JSON.stringify({
           'description': document.getElementById('description').value
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
             liItem.innerHTML = `<input type="checkbox" data-id=${id} class="checkbox-completed">${jsonResponse.description}<button class="delete-item-button" data-id=${id}>&cross;</button>`;
             console.log(liItem);
             document.getElementById("todolist").appendChild(liItem);
             console.log(document.getElementById("todolist"));
             })
     .catch(function() {
         document.getElementById("error").className="";
     });
};

