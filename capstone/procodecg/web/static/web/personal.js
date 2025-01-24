document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let modalView = document.querySelector('.modal.viewPopUp')
    let modalTitle = document.querySelector('.modal-title.view-task')
    let closeBtn2 = document.querySelector('.close.close-2')
    let modalBody = document.querySelector('.modal-body.view-task')
    let personalCards = document.querySelectorAll('.card.card-personal')
    let editTask = document.querySelector('.edit-task')
    let editView = document.querySelector('.modal-body.view-edit')
    let checklistContainer = document.querySelector('.checklist-container')
    const taskInput = document.querySelector('.taskInput')
    const taskList = document.querySelector('.taskList')
    const addBtn = document.querySelector('.btn.btn-sm.btn-primary.add-list')
    console.log(personalCards)

    editView.style.display = 'none';
    //checklistContainer.style.display = 'none';

    



    personalCards.forEach((card)=> {
        console.log(card)
        card.addEventListener('click', (event) => {
            openCard(event)
            const cardID = event.currentTarget.getAttribute("data-id")
            checklistContainer.setAttribute("data-id", cardID)
            loadTasks(cardID)
            console.log(loadTasks(cardID))
        
            
            
        })

        editTask.addEventListener('click', ()=> {
            modalBody.style.display = 'none';
            editView.style.display = 'block'; 
            checklistContainer.style.display = 'none'
            editCard()

        })
        /*checklistBtn.addEventListener('click', (event) => {

            checklistContainer.style.display = 'block'
            checklistBtn.style.display = 'none' */
            addBtn.addEventListener('click', () => {
                console.log('btn clicked')
                addTask(checklistContainer.getAttribute("data-id"))
            })


        //})

        closeBtn2.addEventListener('click', ()=> {
            modalView.style.display = 'none';
        })
        
    })

    function addTask(id){
        const taskText = taskInput.value.trim()
        if (taskText !== '') {
            const li = document.createElement('li')
            li.innerHTML = '<i class="fa-regular fa-square"></i> ' + taskText
            taskList.append(li)
            taskInput.value = ''
            li.addEventListener('click', completeTask)
        }
        saveTasks(id)
    }

    function completeTask (event) {
        const task = event.target
        task.classList.toggle('completed')
        const icon = task.querySelector('i')
        if (task.classList.contains('completed')) {
            icon.classList.remove('fa-regular', 'fa-square')
            icon.classList.add('fa-solid', 'fa-square-check')
        }
        else if (!task.classList.contains('completed')) {
            icon.classList.remove('fa-solid', 'fa-square-check')
            icon.classList.add('fa-regular', 'fa-square')

        }

        console.log(task.querySelector('i'))

        const id = checklistContainer.getAttribute("data-id")
        console.log(id)
        saveTasks(id)
    }

    function saveTasks (id) {
        const tasks = []
        const taskItems = taskList.querySelectorAll('li')
        
        for (let i=0; i < taskItems.length; i++){
            tasks.push({
                content:taskItems[i].innerHTML,
                completed: taskItems[i].classList.contains('completed') })
            console.log(taskItems[i].innerHTML)
        }
        console.log(tasks)
        console.log(id)
        localStorage.setItem(`tasks-${id}`, JSON.stringify(tasks))
    }

    function loadTasks (id) {
        const tasks = JSON.parse(localStorage.getItem(`tasks-${id}`))
        taskList.innerHTML = ''

        if(tasks) {
            tasks.forEach(task => {
                const li = document.createElement('li')
                li.innerHTML = task.content
                if (task.completed) {
                    li.classList.add('completed')
                    const icon = li.querySelector('i')
                    icon.classList.remove('fa-regular', 'fa-square')
                    icon.classList.add('fa-solid', 'fa-square-check')
                }
                taskList.appendChild(li)
                li.addEventListener('click', completeTask)

            })
        }
    }


    function openCard (event) {
        console.log("Card clicked");
            const cardID = event.currentTarget.getAttribute("data-id")
            fetch(`/cards/${cardID}`)
            .then(response => response.json())
            .then(card => {
              console.log(card);
            modalView.style.display = 'block';
            modalView.setAttribute("data-id", cardID)
            modalTitle.innerHTML = `${card.task_name}`
            modalBody.innerHTML = `<h6>Description</h6>
            <p>${card.description}</p>
            <h6>Students</h6>
            <p>${card.students}</p>
            <h6>Attachments</h6>
            <i class="fa-solid fa-paperclip"></i> 
            <a href = "${card.attachment_1}"> File 1 </a> `

            if (card.attachment_2 === null) {
                if (card.status === 'todo') {
                    modalBody.innerHTML += ` <br><br>
                    <div class="status-modal"> 
                    <i class="fa-solid fa-circle" style="color: #fde091; font-size:8px"></i>
                                    To Do
                    </div>`
                }
                else if (card.status === 'ongoing') {
                    modalBody.innerHTML += `<br><br>
                    <div class="status-modal"> 
                    <i class="fa-solid fa-circle" style="color: #fd9591; font-size:8px"></i>
                                    On Going
                    </div>`
                }
                else if (card.status === 'completed') {
                    modalBody.innerHTML += `<br><br>
                    <div class="status-modal"> 
                    <i class="fa-solid fa-circle" style="color: #8df8ac; font-size:8px"></i>
                                    Completed
                    </div>`
                }
            }
            else if (card.attachment_2 != null) {
                 modalBody.innerHTML += `<br>
                 <i class="fa-solid fa-paperclip"></i> 
            <a href = "${card.attachment_2}"> File 2 </a> <br>`
            if (card.status === 'todo') {
                modalBody.innerHTML += `<div class="status-modal"> 
                <i class="fa-solid fa-circle" style="color: #fde091; font-size:8px"></i>
                                 To Do
                </div>`
            }
            else if (card.status === 'ongoing') {
                modalBody.innerHTML += `<div class="status-modal"> 
                <i class="fa-solid fa-circle" style="color: #fd9591; font-size:8px"></i>
                                On Going
                </div>`
            }
            else if (card.status === 'completed') {
                modalBody.innerHTML += `<div class="status-modal"> 
                <i class="fa-solid fa-circle" style="color: #8df8ac; font-size:8px"></i>
                                Completed
                </div>`
            }}

            


            })
    }

    function editCard () {
        const cardID = modalView.getAttribute("data-id")
        console.log(cardID)
        fetch(`/cards/${cardID}`)
        .then(response => response.json())
        .then(c => {
            document.querySelector('.form-control.edit-title').value = c.task_name;
            document.querySelector('.form-control.edit-description').value = c.description;
            document.querySelector('.form-control.edit-students').value = c.students
            document.querySelector('.status').value = c.status
        })

        document.querySelector('.form-edit').onsubmit = function (event) {
            console.log("pressed submit")
            event.preventDefault()

            fetch(`/cards/${cardID}`, {
                method : "PUT",
                headers: {'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    task_name: document.querySelector('.form-control.edit-title').value,
                    description: document.querySelector(".form-control.edit-description").value,
                    students: document.querySelector(".form-control.edit-students").value,
                    status: document.querySelector(".status").value
                })
            }

            )
            .then(() => {
                window.location.reload();
                editView.style.display = 'none';
                modalBody.style.display = 'block';
                    
                

            })
            .catch(error => console.error('Error:', error)); 
    }}


})