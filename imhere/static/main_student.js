$(document).ready(function(){
    $('#secretsignin').submit(function()
    {

        regx = /[^a-z0-9\s\n]*/gi;
        secret = $("input[name=secret_code").val()
        $("input[name=secret_code").val(secret.replace(regx, ''))
        return true;

    });
});
