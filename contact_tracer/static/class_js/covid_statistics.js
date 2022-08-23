$(document).ready(function()
{
    $("#btnSubmit").click(function()
    {
        jQuery.ajax({
            type:"POST",
            url:"/covid_statistics",
            enctype:"multipart/form-data",
            data:new FormData($("#formCases")[0]),
            contentType:false,
            processData:false,
            success:new function()
            {
                window.location.reload();
            },
            error:new function(e)
            {
                console.log(e);
            }
        });
    });

    const Http = new XMLHttpRequest();
    const url = "/get_cases";
    Http.open("GET",url);
    Http.send();
    var req
    Http.onreadystatechange=(e)=>{
        console.log(Http.responseText);
        req = Http.responseText;
        plotGraph(req);
            }

    $("#btnProvinces").click(function()
    {
        var len = document.getElementById("selectedProvinces").options.length;
        for(var i = 0; i < len; i++)
        {
            var options = document.getElementById("selectedProvinces").options[i].text;
            console.log(options);
            $.post("/post_province",
            {
                Province:options
            },
            function(data,status)
            {
                console.log(data);
            }
            );
        }
    });

});

function plotGraph(test)
{
    var models = JSON.parse(test);
    for(var i in models)
    {
        console.log(models[i]);
    }

}