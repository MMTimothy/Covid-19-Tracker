$(document).ready(function()
{
    $("#btnLogin").click(function()
    {
        jQuery.ajax({
            type:"POST",
            url:"/login",
            enctype:"multipart/form-data",
            data:new FormData($("#formLogin")[0]),
            contentType:false,
            processData:false,
            success:new function()
            {
                window.location.reload();
            },
            error:function()
            {
                console.log("Error");
            },
        });
    });
});
