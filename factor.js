/**
 * Copyright (C) 2014 Leonardo Rossi <leonardo.rossi@studenti.unipr.it>
 *
 * This source code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This source code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this source code; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 *
 */

var factor = {
  /**
   * Check the input number inserted in text box by the user
   *
   * @param value number inserted by the user
   * @return true, if pass all checks
   */
  check_input: function(value){
    // test if is a number
    if(!$.isNumeric(value)){
      $('fieldset').addClass('error');
      $('fieldset').removeClass('success');
      $('#result').html("ERROR: insert a true number");
      return false;
    }

    // test if is a positive number 
    if(value < 0){
      $('fieldset').addClass('error');
      $('fieldset').removeClass('success');
      $('#result').html("ERROR: insert a positive number!");
      return false;
    }

    // test if is a integer
    if((parseFloat(value) != parseInt(value)) || isNaN(value)){
      $('fieldset').addClass('error');
      $('fieldset').removeClass('success');
      $('#result').html("ERROR: insert a integer number!");
      return false;
    }

    return true;
  },

  /**
   * Function that query the back-end and print the result.
   *
   */
  factor: function(algorithm) {

    $(document).ready(function() {
      var value = $('#number').val();
      var header = "Factoring '<i>" + value + "</i>': ";

      // check the input
      if(!factor.check_input(value)){
        return;
      }

      // ok, start ajax call
      $.ajax({
        url: 'cgi-bin/factor.cgi',
        data: 'number=' + value + '&algorithm=' + algorithm,
        dataType: 'json',
        timeout: 5 * 60 * 1000, // 5 min
        // called if beck-end return the result
        success: function(data){
          // print result
          $('fieldset').addClass('success');
          $('fieldset').removeClass('error');
          $('#result').html(header + '<b>'+ data.join(", ") + '</b>');
        },
        // called if ajax return a error
        fail: function(jqxhr, textStatus, error) {
          // print error
          $('fieldset').addClass('error');
          $('fieldset').removeClass('success');
          $('#result').html(header + textStatus + ", " + error);
        },
        error: function(jqxhr, textStatus){
          $('fieldset').addClass('error');
          $('fieldset').removeClass('success');
          $('#result').html(header + textStatus + " - HTTP " + jqxhr.status + " " + jqxhr.statusText);
        }
      });
    });
  }
};
