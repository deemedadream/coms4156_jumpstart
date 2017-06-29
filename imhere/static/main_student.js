$(document).ready(function(){
    $('#secretsignin').submit(function(e)
    {

        regx = /[^a-z0-9\s\n]*/gi;
        secret = $("input[name=secret_code").val()
        console.log(secret);
        if (secret != '') {
            $("input[name=secret_code").val(secret.replace(regx, ''))
            return true;
        }
        else{
            alert('Cannot enter empty string');
            e.preventDefault(e);
        }
    });
});
