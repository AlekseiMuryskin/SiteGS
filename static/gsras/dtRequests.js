$(document).ready(function () {
  $("#dtRequests").tablesorter({theme:"blue"});
   $( "#export" ).click(function() {
          $('#dtRequests').csvExport();
        });
});

