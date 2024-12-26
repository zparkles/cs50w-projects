document.addEventListener('DOMContentLoaded', function() {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    document.querySelectorAll('.edit-view').forEach(el => el.style.display = 'none');

    let flag = true

    
    window.addEventListener('load', ()=> {
        fetch('/allposts')
        .then(response => { 
            return response.json()})
        .then(posts => {
      Object.keys(posts).forEach(key => {
        
        const post_id = posts[key].id
        const button = document.createElement('button');
        button.classList= 'btn like-btn';
        button.innerHTML = `<i class="fa-regular fa-heart"></i>`
        let likeBtnDiv = document.querySelector(`#like-btn-div-${post_id}`)
        if(likeBtnDiv) {
            likeBtnDiv.append(button)
            
        }
        else {
            console.log("div not found")
        }

        countLike(post_id).then (count => {
            document.querySelector(`#count-${post_id}`).innerHTML = count.like_count
        })
        fetch('/like')
        .then(response => response.json())
        .then (likes => {
            /*
            if (likes.length === 0) {
            if (button) {
                button.addEventListener('click', () => {
                    likeFunction(post_id)
                    location.reload();
            
                }) }
            }
            else { */
            let flag_like = false
            Object.keys(likes).forEach(key => {
                const element = document.querySelector('.profile-nav')
                const user_id = element.getAttribute("data-id")
                const post_liked_id = likes[key].post_liked
                const status = likes[key].status
                
                if (likes[key].user == user_id && post_liked_id == post_id && status == true) {
            
                    button.innerHTML = `<i class="fa-solid fa-heart" style="color: #ff0505;"></i>`
                    console.log(document.querySelector(`#like-btn-div-${post_id}`));
                    document.querySelector(`#like-btn-div-${post_id}`).append(button)
                    button.addEventListener('click', () => {
                        unlikeFunction(likes[key].id)
                        location.reload();
                
                    }) 
                    flag_like = true
                }
                
                else if (!flag_like && likes[key].user == user_id && post_liked_id == post_id && status == false) {
                    button.innerHTML = `<i class="fa-regular fa-heart"></i>`
                    console.log(document.querySelector(`#like-btn-div-${post_id}`));
                    document.querySelector(`#like-btn-div-${post_id}`).append(button)
                    button.addEventListener('click', () => {
                        returnLikeFunction(likes[key].id)
                        location.reload();
                
                    })
                    flag_like = true
                }
                
            })
            if (!flag_like) {
                    
                button.innerHTML = `<i class="fa-regular fa-heart"></i>`
                console.log(document.querySelector(`#like-btn-div-${post_id}`));
                document.querySelector(`#like-btn-div-${post_id}`).append(button)
                button.addEventListener('click', () => {
                    likeFunction(post_id)
                    location.reload();
            
                })
                flag_like = true
            }
        } 
        )
        
        
      })
        })
        
        const element1 = document.querySelector('.profile')
        const element2 = document.querySelector('.profile-nav')
        const user_id = element2.getAttribute("data-id")
        const account_id = element1.getAttribute("data-id")
        console.log(user_id)
        fetch('follow')
        .then(response => response.json())
        .then(foll => {
            flag = false
            Object.keys(foll).forEach(key => {
                if (foll[key].user == user_id && foll[key].account == account_id && foll[key].follow == true) {
                    flag= true
                    const button = document.createElement('button');
                    button.className = 'btn btn-sm btn-block';
                    button.setAttribute("data-id", `#follow-${foll[key].id}`);
                    button.innerHTML = `<i class="fa-solid fa-check"></i> Following`
                    button.style.color = "black";
                    button.style.background = "lightgrey";
                    document.querySelector('#follow-btn').innerHTML = ''
                    document.querySelector('#follow-btn').append(button)     
                    
                    button.addEventListener('click', () => {
                    unfollow(foll[key].id)
                    
                  
                
                }) }
                
                else if (!flag && foll[key].user == user_id && foll[key].account == account_id && foll[key].follow == false) {
                    flag= true
                    const button = document.createElement('button');
                    button.className = 'btn btn-sm btn-block';
                    button.setAttribute("data-id", `#follow-${foll.id}`);
                    button.innerHTML = '<i class="fa-solid fa-plus"></i> Follow'
                    button.style.color = "white";
                    button.style.background = "#0d6efd";
                    document.querySelector('#follow-btn').innerHTML = ''
                    document.querySelector('#follow-btn').append(button)
                    
                    
                    button.addEventListener('click', () => {
                    refollow(foll[key].id)
                  
                  
                
                })

                }
                else if (!flag) {
                    flag= true
                    const button = document.createElement('button');
                    button.className = 'btn btn-sm btn-block';
                    button.innerHTML = '<i class="fa-solid fa-plus"></i> Follow'
                    button.style.color = "white";
                    button.style.background = "#0d6efd";
                    document.querySelector('#follow-btn').innerHTML = ''
                    document.querySelector('#follow-btn').append(button)
                    const element = document.querySelector('.profile')
                    const user_id = element.getAttribute("data-id")
                    
                    button.addEventListener('click', () => {
                    follow(user_id)

                
            })
         }

          
            })
                 } ) 

                 

    })


document.querySelector('#new-post').onsubmit = function () {
    document.querySelector('.edit-view').style.display = 'none';
}

document.querySelectorAll('.content-edit').forEach(a => {

    a.addEventListener('click', (event)=>{
        const postElement = event.target.closest('.card')
        postElement.querySelector('.edit-view').style.display = 'block';
        postElement.querySelector('.post-view').style.display = 'none';
        const element = postElement.querySelector('.edit')

        if (element){
        const post_id = element.getAttribute("data-id")

        fetch(`/${post_id}/edit`)
            .then(response => response.json())
            .then(p => {
        console.log(p)
        document.querySelector(`#text-edit-${post_id}`).value = p.post
        })
        const editViewElement = postElement.querySelector('.edit-view');
        console.log('Edit view element:', editViewElement);
            if (editViewElement){
                editViewElement.onsubmit = function (event) {
                    event.preventDefault()
                    fetch(`/${post_id}/edit`,
                        {method: "PUT",
                        headers: {'X-CSRFToken': csrftoken},
                          body: JSON.stringify({
                            post: document.querySelector(`#text-edit-${post_id}`).value} )}
                      )
                      .then(() => {
                        window.location.reload();
                        document.querySelector('.edit-view').style.display = 'none';
                        
                    }); 
            }
            
        
        }
}})

})

function follow (user_id){
    fetch('follow', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
        account: user_id,
        follow: true,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
    
          console.log(result);
          location.reload();


}) 
}

function refollow (follow_id){
    fetch(`follow/${follow_id}`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
        follow: true,
        })
      })
    console.log("You are following this account");
    location.reload();

 
}

function unfollow (follow_id){
    fetch(`follow/${follow_id}`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
        follow: false,
        })
      })
    console.log("You unfollowed this account");
    location.reload();

 
}
function likeFunction (post_id){
    fetch('/like', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
        post_liked: post_id,
        status: true,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
    
          console.log(result);

}) 
}

function returnLikeFunction (like_id){
    fetch(`/like/${like_id}`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
        status: true,
        })
      })
    console.log("You liked this post");

 
}

function unlikeFunction (like_id){
    fetch(`/like/${like_id}`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
        status: false,
        })
      })
    console.log("You unliked this post");

 
}

async function countLike (post_id){
    const response = await fetch(`/count/${post_id}`)
    const count = await response.json()
    console.log(count)
    return count

 
}

})

