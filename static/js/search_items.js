const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const suggestionBox = document.getElementById('suggestion-box')
const suggestionCont = document.getElementById('suggestion-cont')
const suggestionReal = document.getElementById('original')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (products) => {
    $.ajax({
        type: 'POST',
        url: '/shop/search/',
        data: {
            'csrfmiddlewaretoken': csrf,
            'products': products,
        },
        success: (res)=> {
            // console.log(res.data)
            const data = res.data
            if (Array.isArray(data)){
                suggestionCont.innerHTML = ""
                data.forEach(products=> {
                    suggestionCont.innerHTML += `
                        <div class="col mb-5">
                            <a class="mt-auto" href="/shop/${products.pk}/${products.pr_name}">
                            <div class="card h-100 border-0">
                                <div class="badge bg-dark text-white position-absolute" style="top: 0.5rem; right: 0.5rem">
                                    Sale
                                </div>
                                <!-- Product image-->
                                <img class="card-img-top" src="${products.image}" alt="...">
                                <!-- Product details-->
                                <div class="card-body p-4">
                                    <div class="text-center">
                                        <!-- Product name-->
                                        <h5 class="fw-bolder h4 text-dark">${products.pr_name}</h5>
                                        <!-- Product price-->
                                        <span class="text-dark mt-3 font-weight-bold">N${products.price}</span>
                                    </div>
                                </div>
                                <!-- Product actions-->
                            </div>
                        </a>
                    </div>
                    `
                })
            }else{
                if(searchInput.value.length > 0){
                    suggestionCont.innerHTML = `<h5 class="text-xs font-weight-bold text-dark text-uppercase mb-1">${data}</h5>`
                }else{
                    suggestionBox.classList.add('d-none')
                    suggestionReal.classList.remove('d-none')
                }
            }
        },
        error: (err)=> {
            console.log(err)
        }
    })
}

searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)
    
    if(suggestionBox.classList.contains('d-none')){
        suggestionBox.classList.remove('d-none')
        suggestionReal.classList.add('d-none')
    }

    sendSearchData(e.target.value)
})