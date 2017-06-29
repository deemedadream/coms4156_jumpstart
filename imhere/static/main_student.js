$(document).ready(function(){
    $('#secretsignin').submit(function(e)
    {
        regx = /[^0-9]*/gi;
        secret = $("input[name=secret_code").val()
        $("input[name=secret_code").val(secret.replace(regx, ''))
        return true;    
    });
});
