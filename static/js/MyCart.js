const updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(e){
        console.log('clicked');
        e.preventDefault()
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log('productId:', productId, '\nAction:', action);

        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else {
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productId,action) {
    console.log('Not logged in..')

    if (action == 'add') {
        if (cart[productId]==undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] +=1
        }
    }

    if (action == 'remove') {
        if (cart[productId]==undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] -=1
        }
    }
}

function updateUserOrder(productId,action){
    console.log('User is authenticated, sending data...');

    const url = '/shop/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then(res=>{
        return res.json()
    })
    .then(data=>{
        console.log(data);
        location.reload()
    })
}