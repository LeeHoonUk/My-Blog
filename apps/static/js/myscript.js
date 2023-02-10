function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

let btnAjax = document.querySelector('.btnAjax');


btnAjax.addEventListener('click', e => {
    let ajaxname = document.getElementById('userid');    
    $.ajax({
        url : '/user/check?userid='+ajaxname.value,
        headers: {'X-CSRFToken': csrftoken},
        type : 'GET',
        success:function(data){
            Swal.fire(data.msg, '',data.check)
            document.getElementById('checker').value = 'True';
            ajaxname.readOnly=true;
        },
        error: function(e){
            console.log(e)
            Swal.fire(e.responseJSON.msg,'',e.responseJSON.check)
            
        }
    })
});

if (document.getElementById('checker').value == 'True') {
    document.getElementById('userid').readOnly=true;
}