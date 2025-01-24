document.addEventListener('DOMContentLoaded', function() {
    const calendar = document.querySelector('.calendar');
    const date = document.querySelector('.date');
    const daysContainer = document.querySelector('.days')
    const prev = document.querySelector('.prev')
    const next = document.querySelector('.next')
    const todayBtn = document.querySelector('.today-btn')
    const gotoBtn = document.querySelector('.goto-btn')
    const dateInput = document.querySelector('.date-input')
    const eventDay = document.querySelector('.event-day')
    const eventDate = document.querySelector('.event-date')
    const eventsContainer = document.querySelector('.events')


    let today = new Date();
    let activeDay;
    let month = today.getMonth();
    let year = today.getFullYear();

    const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    ];

async function initCalendar(){
        const firstDay = new Date(year, month, 1)
        const lastDay = new Date(year, month +1, 0)
        const prevLastDay = new Date(year, month, 0)
        const prevDays = prevLastDay.getDate()
        const lastDate = lastDay.getDate()
        const day = firstDay.getDay()
        const nextDays = 7 - lastDay.getDay() - 1

        console.log(day)

        date.innerHTML = `${months[month]} ${year}`

        let days = ''

        for (let x = day; x > 0; x --) {
            days += `<div class="day prev-date">${prevDays - x + 1}</div>`
        }
  
        for (let i = 1; i <= lastDate; i++) {
            const response = await fetch('/schedule')
            const eventObj = await response.json()
                let event = false;
                Object.keys(eventObj).forEach(key =>{
                    startDateDay = parseInt(eventObj[key].start_date_day)
                    startDateMonth = parseInt(eventObj[key].start_date_month)
                    startDateYear = parseInt(eventObj[key].start_date_year)
                    endDateDay= parseInt(eventObj[key].end_date_day)
                    endDateMonth = parseInt(eventObj[key].end_date_month)
                    endDateYear = parseInt(eventObj[key].end_date_year)
                    startDOTY = parseInt(eventObj[key].start_date_doty)
                    endDOTY = parseInt(eventObj[key].end_date_doty)

                    if (
                        startDateDay <= i &&
                        endDateDay >= i &&
                        startDateMonth <= month + 1 && endDateMonth >= month + 1 &&
                        startDateYear <= year && endDateYear >= year && !eventObj[key].weekly
                    ) {
                        event = true
                    }
                    const thisDate = new Date(year, month, i)
                    const thisDay = thisDate.getDay()

                    if (eventObj[key].weekly && thisDay === parseInt(eventObj[key].start_date_week_day) 
                    && startDateDay <= i &&
                    endDateDay >= i &&
                    startDateMonth <= month + 1 && endDateMonth >= month + 1 &&
                    startDateYear <= year && endDateYear >= year)
                    {
                        event = true
                    }
                


                })
                if (i === new Date().getDate() && year === new Date().getFullYear() && month === new Date().getMonth()) {
                    activeDay == i
                    getActiveDay(i)
                    updateEvents(i)
                    if (event) {
                        days += `<div class="day today event active">${i}</div>`
                    }
                    else {
                        days += `<div class="day today active">${i}</div>`
                    }
                 
                }
                else {
                     if (event){
                    days += `<div class="day event">${i}</div>`  
                    }
                    else {
                    days += `<div class="day">${i}</div>`
                    }
            
                }
                console.log(event)
                
            }
            
        
        for (let j = 1; j <= nextDays; j++) {
            days += `<div class="day next-date">${j}</div>`
        }

        daysContainer.innerHTML = days
        addListener()
    }


initCalendar()

function prevMonth () {
    month--;
    if (month < 0) {
        month = 11;
        year --
    }
    initCalendar()
}


function nextMonth () {
    month++;
    if (month > 11) {
        month = 0;
        year ++
    }
    initCalendar()
}


prev.addEventListener('click', prevMonth)
next.addEventListener('click', nextMonth)

todayBtn.addEventListener('click', ()=> {
    today = new Date();
    month = today.getMonth()
    year = today.getFullYear()
    initCalendar()
})

/*
dateInput.addEventListener('keyup', (e)=>{
    dateInput.value = dateInput.value.replace(/[^0-9/]/g, "");
    if (dateInput.value.length === 2) {
        dateInput.value += "/"
    }
    if (dateInput.value.length > 7) {
        dateInput.value = dateInput.value.slice(0, 7);
    }
    if (e.inputType === "deleteContentBackward") {
        if (dateInput.value.length === 3) {
            dateInput.value = dateInput.value.slice(0, 2);
        }
    }
})*/

gotoBtn.addEventListener('click', gotoDate) 

function gotoDate(){
    const dateArr = dateInput.value.split("-")
    console.log(dateArr)
    if (dateArr.length === 2) {
        if(dateArr[1]> 0 && dateArr[1] < 13 && dateArr[0].length === 4) {
            month = dateArr[1] - 1
            year = dateArr[0]
            initCalendar()
            dateInput.value = ''
            return
        }
    }
    alert("Invalid date")
}

function addListener (){
    const days = document.querySelectorAll('.day')
    days.forEach(day => {
        day.addEventListener('click', (e)=>{
            activeDay = Number(e.target.innerHTML)

            days.forEach(day => {
                day.classList.remove("active")
            })
            if (e.target.classList.contains('prev-date')){
                prevMonth()
                
                setTimeout(()=> {
                    
                    const days = document.querySelectorAll('.day')
                    days.forEach(day => {
                        day.classList.remove("active")
                        if (!day.classList.contains('prev-date') && 
                    day.innerHTML == e.target.innerHTML) {

                        day.classList.add('active')
                        getActiveDay(e.target.innerHTML)
                        updateEvents(activeDay)
                    }
                    });
                    
                }, 250)
            }
            else if (e.target.classList.contains('next-date')){
                nextMonth()
                setTimeout(()=> {
                    
                    const days = document.querySelectorAll('.day')
                    days.forEach(day => {
                        day.classList.remove("active")
                        if (!day.classList.contains('next-date') && 
                    day.innerHTML == e.target.innerHTML) {

                        day.classList.add('active')
                        getActiveDay(e.target.innerHTML)
                        updateEvents(activeDay)
                    }
                    });
                    
                }, 250)
            }
            else {
                e.target.classList.add('active')
                getActiveDay(e.target.innerHTML)
                updateEvents(activeDay)
            }

        })
    });
    
}

function getActiveDay(date){
    const day = new Date(year,month, date)
    const dayName = day.toString().split(' ')[0]
    eventDay.innerHTML = dayName
    eventDate.innerHTML = `${date} ${months[month]} ${year}`

}

async function updateEvents(date) {
    const response = await fetch('/schedule')
    const eventObj = await response.json()
    const thisDate = new Date(year, month, date)
    const thisDay = thisDate.getDay()

    let events = ''
    let event = false;
    let eventName = ''
    let eventDescription = ''
    let eventStartTime = ''
    let eventEndTime = ''
    Object.keys(eventObj).forEach(key =>{
        
        startDateDay = parseInt(eventObj[key].start_date_day)
        startDateMonth = parseInt(eventObj[key].start_date_month)
        startDateYear = parseInt(eventObj[key].start_date_year)
        endDateDay= parseInt(eventObj[key].end_date_day)
        endDateMonth = parseInt(eventObj[key].end_date_month)
        endDateYear = parseInt(eventObj[key].end_date_year)
        console.log("date:", date)
        console.log("key's date:", startDateDay)

        const dateRangeCondition = date >= startDateDay && date <= endDateDay &&
        month + 1 >= startDateMonth && month + 1 <= endDateMonth &&
        year >= startDateYear && year <= endDateYear 
        
        const weeklyCondition = eventObj[key].weekly && 
        thisDay === parseInt(eventObj[key].start_date_week_day) && dateRangeCondition 

        if (dateRangeCondition && !eventObj[key].weekly|| weeklyCondition
        ) {
            event = true
            eventName = eventObj[key].event_name
            eventDescription = eventObj[key].description
            eventStartTime = eventObj[key].start_time
            eventEndTime = eventObj[key].end_time

        }
    
    })
    if (event) {
        events += `<div class="event">
                        <div class = "title">
                            <i class="fa-solid fa-star"></i>
                            <h3 class = "event-title"> ${eventName}</h3>
                        </div>
                        <div class="event-time">
                        <span class="event-time">${eventDescription} </span> <br>
                        <span class="event-time">${eventStartTime} - ${eventEndTime}  </span>
                        </div>
                        </div>
                        `
            console.log(events)
    }
    if (events === '') {
        events = `<div class="no-event"> 
                    <h3> No Events </h3>
                    </div>`
    }
    eventsContainer.innerHTML = events
}

})

