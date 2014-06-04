var factor = {

  factor: function() {

    $(document).ready(function() {
      var value = $('#number').val();
      var header = "Factoring '" + value + "': ";

      // test if is a number
      if(!$.isNumeric(value)){
        $('#result').html("ERROR: insert a true number");
        return;
      }

      // test if is a positive number 
      if(value < 0){
         $('#result').html("ERROR: insert a positive number!");
        return;
      }

      // test if is a integer
      if((parseFloat(value) != parseInt(value)) || isNaN(value)){
         $('#result').html("ERROR: insert a integer number!");
        return;
      }

      // call back-end
      $.getJSON("cgi-bin/fact02.cgi?number="+value+"&callback=?", function(data) {
        // print result
        $('#result').html(header + data.join(", "));
      }) 
      .fail(function(jqxhr, textStatus, error) {
       // print error
       var err = textStatus + ", " + error;
       $('#result').html(header + err);
      });
    });


    }
 };
