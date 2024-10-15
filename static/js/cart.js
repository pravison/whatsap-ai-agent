
var updateBtns = document.getElementsByClassName('update-cart')

for( var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var menuId = this.dataset.menu
        var action = this.dataset.action

        //console.log('menuId:', menuId, 'action:', action )
        // user = request.user
        // console.log('User:', user)
        // if(user === 'AnonymousUser'){
        // addCookieItem(menuId , action)
        // }else{
        updateUserOrder(menuId , action)

        // console.log('pravison')
        // }
    }) 
}

function addCookieItem(menuId , action){
    //console.log('user is not logged in')

    if (action == 'add'){
        if (cart[menuId] == undefined){
            cart[menuId] = {'quantity' : 1}
        }else{
            cart[menuId]['quantity'] += 1
        }
    }
    if (action == 'remove'){
        cart[menuId]['quantity'] -= 1
        if (cart[menuId]['quantity'] <= 0){
            console.log('remove item')
            delete cart[menuId]
        }
    }
    if (action == 'clear'){
        delete cart[menuId]
    }
    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateUserOrder(menuId , action){
    
    

    var url = '/customers/update_item/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            // 'X-CSRFToken': csrftoken
        },

        body:JSON.stringify({'menuId': menuId , 'action': action})
    })
    .then((response)=>{
        console.log('user is logged in sending data...')
        return response.json()
    })

    .then((data)=>{
        location.reload()
        console.log('data:', data)
    })
    
}

function addTocart(productId){
    const cart = JSON.parse(localStorage.getItem('cart')) || {}
    // check if product already in cart
    if (cart[productId]){
        cart[productId].quantity +=1;
    }else{
        fetch(`/store/product/${productId}/`)
        .then(response => response.json())
        .then(product => {
            cart[productId]={
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': 1
            };
            // save to localstorge
            localStorage.setItem('cart', JSON.stringify(cart));
            // update cart display on the page
            displayCart()
        })
    }
}

function displayCart(){
    const cart = JSON.parse(localStorage.getItem('cart')) || {}
    let cartHTml = '<ul>';
    for (const productId in cart){
        const item = cart[productId];
        cartHTml +=`<li>${item.name} - ${item.quantity} * $${item.price}</li>`;
    }
    cartHTml += '</ul>'

    document.getElementById('cart').innerHTML = cartHTml
}
document.addEventListener('DOMContentLoaded', displayCart)