function show() {


    var datas = $('form').serializeArray();

    var hostname = document.getElementsByName("hostname");
    var start = document.getElementById("datepicker-start");
    var end = document.getElementById("datepicker-end");
    var resultsContainer = document.getElementById("diagram");

    resultsContainer.style.display = "block";
    console.log("block~~~~~~~~~~~~~~~~");

   /*$.ajax({
     type: "POST",
     url: "/process",
     data: JSON.stringify(datas),
     contentType: "application/json",
     dataType: 'json',
     success: function(result) {
        document.write(result)
     
     } 
   });*/

}