document.addEventListener('DOMContentLoaded', function() {
    const navBtns = document.querySelectorAll('.nav-btn')
    const images = document.querySelectorAll('.home-image')
    let contentBtn = document.querySelector('.read-btn')
    let text = document.querySelector('.desc')

    const sliderNav = (number) => {
        navBtns.forEach((btn) => {
            btn.classList.remove("active")
        })
        images.forEach((img) => {
            img.classList.remove("active")
        })

        navBtns[number].classList.add("active")
        images[number].classList.add("active")


    }
    navBtns.forEach((btn, i) => {
        btn.addEventListener("click", ()=> {
            sliderNav(i)
            if (btn.getAttribute('id') === "btn-1") {
                console.log(btn.getAttribute('id'))
                text.innerHTML = 'Kids Regular Coding Class'
                contentBtn.innerHTML = `<a class="btn btn-primary" href="{% url 'programs' %}">Learn More</a>`
            }
            else if (btn.getAttribute('id') === "btn-2") {
                console.log(btn.getAttribute('id'))
                text.innerHTML = 'Kids Weekday Coding Class'
                contentBtn.innerHTML = '<a class="btn btn-primary" href="programs#1">Learn More</a>'
            }
            else if (btn.getAttribute('id') === "btn-3") {
                text.innerHTML = 'Coding Mum'
                contentBtn.innerHTML = '<a class="btn btn-primary" href="programs#6">Learn More</a>'
            }
            else if (btn.getAttribute('id') === "btn-4") {
                text.innerHTML = 'Online Private Class'
                contentBtn.innerHTML = '<a class="btn btn-primary" href="programs#3">Learn More</a>'
            }
            else if (btn.getAttribute('id') === "btn-5") {
                text.innerHTML = 'Crash Course & Customized Training'
                contentBtn.innerHTML = '<a class="btn btn-primary" href="programs#5">Learn More</a>'
            }
            else if (btn.getAttribute('id') === "btn-6") {
                console.log(btn.getAttribute('id'))
                text.innerHTML = 'Kids Coding Camp'
                contentBtn.innerHTML = '<a class="btn btn-primary" href="programs#2">Learn More</a>'
            }
            else if (btn.getAttribute('id') === "btn-7") {
                console.log(btn.getAttribute('id'))
                text.innerHTML = 'Tutoring Coding Class'
                contentBtn.innerHTML = '<a class="btn btn-primary" href="programs#4">Learn More</a>'
            }
        })
    })









})