$(document).ready(function(){
    
    //quick to verify jquery load
    $('h1').on('click', function() { 
        $(this).hide();
    });
    
    $('.testerButton').on('click', function() {
        let printerName = $(this).attr('name');
        console.log(printerName + " button pressed");

        req = $.ajax({
            url : '/cmd',
            type : 'POST',
            data : { name : printerName }
        });
    });
});
