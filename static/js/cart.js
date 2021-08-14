var updateBtns = document.getElementsByClassName('update-cart')


for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var sppId = this.dataset.spp
        var action = this.dataset.action
        console.log('sppId:', sppId, 'action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Anda Belum Login')
        }else{
            updateUserSpp(sppId, action)
        }
    })
}
function updateUserSpp(sppId, action){
    console.log('User is logged in, sending data....')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'sppId': sppId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}