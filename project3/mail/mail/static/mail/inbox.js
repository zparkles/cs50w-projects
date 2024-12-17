document.addEventListener('DOMContentLoaded', function() {
  

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('form').onsubmit = function () 
    
  { 
    fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
    recipients: document.querySelector('#compose-recipients').value,
    subject: document.querySelector("#compose-subject").value,
    body: document.querySelector('#compose-body').value,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result

      console.log(result);
      
      
  });

}

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      document.querySelector('#emails-view').innerHTML = `
      <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`
    
      Object.keys(emails).forEach(key => {
        
        const email = document.createElement('div');
        email.className = 'mail';
        email.setAttribute("data-id", emails[key].id);
        const sender = emails[key].sender
        const subject = emails[key].subject
        const timestamp = emails[key].timestamp
        
        console.log(sender)
        console.log(emails[key].read)
        email.innerHTML = `
        <strong>${sender}</strong> <span style="margin-left: 5px">${subject}</span> 
        <div style="color:grey;" class="text-end">${timestamp}</div>`

        if (emails[key].read) {
           email.style.backgroundColor = "darkgray"
        }
        else {
           email.style.backgroundColor = "white"
        }
        document.querySelector('#emails-view').append(email)

        
        
      })

      document.addEventListener('click', (event)=> {
        const element = event.target;
        if (element.className === 'mail') {
          const emailID = element.getAttribute("data-id")
          fetch(`/emails/${emailID}`)
          .then(response => response.json())
          .then(email => {
              // Print email
              console.log(email);
              
              document.querySelector('#emails-view').innerHTML = `
              <p><strong> From: </strong> ${email.sender}</p>
              <p><strong> To: </strong> ${email.recipients}</p>
              <p><strong> Subject: </strong>${email.subject}</p> 
              <p><strong> Timestamp: </strong>${email.timestamp}</p>
              <hr>
              ${email.body}
              <br><br><br>
              <button class ='btn btn-sm btn-outline-primary' id="reply">Reply</button>`

            document.querySelector('#reply').addEventListener('click', ()=> {
              reply_email(email)
              
            }) 

              if (email.archived) {
                const button = document.createElement('button');
                button.className = 'btn btn-sm btn-outline-primary';
                button.setAttribute("data-id", `#unarchive-${email.id}`);
                button.innerHTML = `Unarchive`
                document.querySelector('#emails-view').append(button)
                  
                button.addEventListener('click', () => {
                  unarchiveMail(email)
                  load_mailbox('inbox')
                  
                
                })

              }
              else {
                const button = document.createElement('button');
                button.className = 'btn btn-sm btn-outline-primary';
                button.setAttribute("data-id", `#archive-${email.id}`);
                button.innerHTML = `Archive`
                document.querySelector('#emails-view').append(button)
                  
                button.addEventListener('click', () => {
                  archiveMail(email)
                  load_mailbox('inbox')
                  
                
                })
  
            
              
              }
              

              
              return fetch(`/emails/${emailID}`,{ 
                method: "PUT",
                body: JSON.stringify({
                  read: true
                })
}
              )

              
          });
        }
      })
    })
  }
  

  function archiveMail (email){
    fetch(`/emails/${email.id}`,
      {method: "PUT",
        body: JSON.stringify({
          archived: true} )}
    )
    load_mailbox('inbox')
    return console.log(email.archived)
  
   }

   function unarchiveMail (email){
    fetch(`/emails/${email.id}`,
      {method: "PUT",
        body: JSON.stringify({
          archived: false} )}
    )
  
    load_mailbox('inbox')
    return console.log(email.archived)
  
   }


   function reply_email(email) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp} ${email.sender}  wrote: ${email.body}`;
  
    document.querySelector('form').onsubmit = function ()
    { 
      fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector('#compose-body').value,
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
  
        console.log(result);
        
    });
  }
}
