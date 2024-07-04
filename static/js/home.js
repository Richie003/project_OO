// var openBtn = document.getElementById('openbut')
// var sideBar = document.getElementById('hidden-nav')
// const hero = document.querySelector('.hero')
// const bar_line = document.querySelector('.bar-line')
// const logo_text = document.querySelector('.logo-text')
// const logo_sm = document.querySelector('.logo-sm')
// const icn_bounce = document.querySelector('.imag1')
// const slider = document.querySelector('.slider')

// openBtn.addEventListener('click', ()=> {
//     sideBar.style = 'transform:translateY(-3.5px); transition: 0.5s ease-in-out; z-index:1;'
// })

// const tl = new TimelineMax()
// const tlm = new TimelineMax()

// tl.fromTo(hero,1,{width:"0%", height:"0%", opacity:"0"}, {width:"100%", height:"70%", opacity:"1", ease: Power2.easeInOut});
// tl.fromTo(logo_sm,0.5,{opacity:"0"}, {opacity:"1"});
// tl.fromTo(bar_line,0.5, {height:"0px"}, {height:"14px"}, '<1');
// tl.fromTo(logo_text,1, {transform:"translateX(-63px)"}, {transform:"translateX(0px)"});


// //const images = document.querySelectorAll('.imag1');
// //
// // observer = new IntersectionObserver((entries) => {
// //
// //   entries.forEach(entry => {
// //     if (entry.intersectionRatio > 0) {
// //       entry.target.style.animation = `tlm.fromTo(icn_bounce,1, {y:0}, {y:-20, yoyo:true, repeat:-1})`
// //     }
// //     else {
// //       entry.target.style.animation = 'none';
// //     }
// //   })
// // })
// //
// //
// //images.forEach(image => {
// //  observer.observe(image)
// //})
// observer = new IntersectionObserver((entries) => {forEach{
//     entries.forEach(icn_bounce => {
//         tlm.fromTo(icn_bounce,1, {y:0}, {y:-20, yoyo:true, repeat:-1})
//     })
//     }
// tlm.fromTo(icn_bounce,1, {y:0}, {y:-20, yoyo:true, repeat:-1})