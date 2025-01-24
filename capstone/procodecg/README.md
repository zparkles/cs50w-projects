# READ ME: CS50W Final Project


For this final project, I made a website for my mom’s teaching company, ProCodeCG. My mom had been wanting to update her company profile website and she also needed a tool for her to keep track of her students’ progress. So, I decided to make this website that shows all the information regarding her classes and programs, that also function as a place where students can see/ track their progress (this part is only accessible for logged in users).


### Distinctiveness and Complexity:
The distinctiveness of this website is that this website is specifically made for my mom’s company. Although this website is in a lot of ways similar to most companies’ profile website, the difference lays in the fact that it doubles as a website for my mom and her students to keep track of their progress and learning schedule. 

As for complexity, it’s shown in the calendar and students’ progress pages, which I will be explaining in detail below.


### Features & Pages:
**Home Page:**
This page is the main page where visitors can get an insight of what is on the website and also what ProCodeCG is. 

**Programs:**
For this page, I made a JSON file filled with the information on the programs offered by ProCodeCG. I decided to make a JSON file because putting them in a SQL model wouldn’t really be suitable because each program has slightly different information, but writing them down in HTML would be redundant because there are parts where the information are alike and using a for loop would be really helpful. So by using a JSON file, I can just use the for loop and conditions to show the information. 

**Calendar:**
I followed Open Source Coding’s calendar tutorial to make the calendar page, but mine isn’t exactly the same as I fetch the ‘events’ data from a model and there are also some parts I adapted. However, this calendar has a limitation, which is that ongoing or repetitive events can only be made within the range of the same month. 

Parts I adjusted:
- Use fetching method to get events from a Django model 
- Adding parts of the code so ongoing and repeating events can be made (before this, an event can only occur in one day)
- Filter by user, so students can only see their own schedules

This calendar feature is made so visitors can see the programs ProCodeCG offers and when is each program/ event scheduled.

**Students’ Progress:**
This page is inspired by Trello. Every student account will automatically have their own progress board once they have an account, each board can be filled with progress cards by the admin. A card can be assigned to more than one student, if necessary, and the card will be shown in both boards. The complexity in this is in the JS part because the card is shown as a pop-up modal and when the status change, it will immediately move to column that corresponds with the card’s new status. 

For the checklist part, I partly followed the tutorial here {[To Do List](https://dev.to/iamcymentho/implementing-to-do-list-using-javascript-32a7)}, but I improved some parts, I edited code so the checklist icon changes once clicked and the completion state is kept in the local storage. 


**Account:**
Each account has to be verified by the admin first before they’re able to log in, this is to make sure that only students can create accounts. 



### Files
The Django default files are filled with the usual contents, for example, views.py contains all the codes for the templates and APIs to fetch. The difference is that I have created a JSON file filled with program information (as I have explained before), media folder to keep the pictures shown in Home and attachments uploaded in Students’ Progress page, and I’ve created many JS files to load in different templates, as it would be confusing and probably raise errors if I put them in one file.


As to how the website works, I’ve demonstrate it here to make it easier to understand. 

