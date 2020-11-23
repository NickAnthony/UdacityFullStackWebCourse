const deleteButtons = document.querySelectorAll('.button-delete');
for (let i = 0; i < deleteButtons.length; i++) {
  const deleteButton = deleteButtons[i];
  deleteButton.onclick = function(e) {
    console.log(e);
    const todoId = e.target.dataset['id'];
    fetch('/todos/' + todoId, {
      method: 'DELETE'
    }).catch(function() {
      document.getElementById('error').className = '';
    })
  }
}
const checkBoxes = document.querySelectorAll('.check-completed');
for (let i = 0; i < checkBoxes.length; i++) {
 const checkBox = checkBoxes[i];
 checkBox.onchange = function(e) {
   console.log(e);
   const newCompletedState = e.target.checked;
   const todoId = e.target.dataset['id'];
   fetch('/todos/' + todoId + '/set-completed', {
     method: 'POST',
     body: JSON.stringify({
       'completed': newCompletedState
     }),
     headers: {
       'Content-Type': 'application/json'
     }
   })
   .then(response => response.json())
   .then(jsonResponse => {
     console.log('response', jsonResponse);
     li = document.createElement('li');
     li.innerText = desc;
     document.getElementById('todos');
     document.getElementById('error').className = 'hidden';
   }).catch(function() {
     document.getElementById('error').className = '';
   })
 }
}
const descInput = document.getElementById('description');
document.getElementById('todo-input-form').onsubmit = function(e) {
 e.preventDefault();
 const desc = descInput.value;
 descInput.value = '';
 fetch('/todos/create', {
   method: 'POST',
   body: JSON.stringify({
     'description': desc,
   }),
   headers: {
     'Content-Type': 'application/json',
   }
 })
 .then(response => response.json())
 .then(jsonResponse => {
   console.log('response', jsonResponse);
   li = document.createElement('li');
   li.innerText = desc;
   document.getElementById('todos').appendChild(li);
   document.getElementById('error').className = 'hidden';
 })
 .catch(function() {
   document.getElementById('error').className = '';
 })
}
