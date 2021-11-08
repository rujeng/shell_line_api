function handleOrderDetail(event, restaurantId, action){
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    const menuId = event.id;
    const url = '/delivery/api/order/';
    const data = {
        'menu_id': parseInt(menuId),
        'action': action,
        'restaurant_id': parseInt(restaurantId),
        'user_id': userId
    }
    const body = {
        method: 'PATCH',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    //confirm action
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
        if (result.isConfirmed) {
            fetch(url, body)
            .then(res => res.json())
            .then(data => {
                // TODO check status ok from server
                get_notify(); // refresh notify
                Swal.fire(
                'Deleted!',
                'Your file has been deleted.',
                'success'
                )
            })
        }
        })
}

function get_notify(){
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
       fetch('/delivery/api/order/?user_id='+userId)
       .then(res => res.json())
       .then(data => {
           $('#notify').html(data.count)
       })
}

function myCart(){
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    const url = `/delivery/mycart?user_id=${userId}`;
    window.location = url;
}

function getQueryParam(name){
    const urlParams = new URLSearchParams(window.location.search);
    const param = urlParams.get(name);
    return param;
}