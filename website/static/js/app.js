$(document).ready(function() {
    $("#results").hide();
    $("#picker").hide();
    $("#btnSubmit").bind('click', function() {
      $.getJSON('/_get_data', {
      }, function(data) {
        $("#results").show();
        $("#picker").hide();
        $("#airline_result").text(data.airline);
        $("#date_result").text(data.date);
        $("#time_result").text(data.time);
        $("#actual_delay").text(data.actual);
        $("#destination").text(data.dest);
        $("#prediction").text(data.pred);
        $("#percentage").text(data.percentage);
        style_result(data.actual, data.pred, "#performance")
      });
      return false;
    });
    $("#btnPicker").bind('click', function() {
      $("#results").hide();
      $("#picker").show();
    });
    $('.datething').datepicker({
    });
});

function style_result(actual, pred, element) {
    if ((actual >= 15 && pred == 'delayed') ||
        (actual < 15 && pred == 'on-time')) {
          $(element).css("color", "green");
          $(element).text("RIGHT");
    } else {
          $(element).css("color", "red");
          $(element).text("WRONG!");
    };
};
