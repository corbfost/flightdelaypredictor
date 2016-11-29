
var carrier_lookup = {"Albuquerque International":{"CarrierName":["Alaska","Southwest"]},"Austin-Bergstrom International":{"CarrierName":["Southwest","Alaska"]},"Baltimore-Washington International":{"CarrierName":["Southwest","AirTran","Alaska"]},"Bellingham Intl":{"CarrierName":["Alaska"]},"Billings Logan Intl":{"CarrierName":["SkyWest"]},"Boise Air Terminal":{"CarrierName":["Southwest","SkyWest"]},"Bradley International":{"CarrierName":["JetBlue"]},"Burbank-Glendale-Pasadena":{"CarrierName":["Alaska"]},"Charleston AFB/International":{"CarrierName":["Alaska"]},"Charlotte/Douglas International":{"CarrierName":["American","US"]},"Chicago Midway":{"CarrierName":["Southwest"]},"Chicago O'Hare International":{"CarrierName":["United","Frontier","Alaska","Continental","American"]},"Cincinnati Northern Kentucky Intl":{"CarrierName":["Delta"]},"City of Colorado Springs Muni":{"CarrierName":["SkyWest","Frontier"]},"Cleveland-Hopkins Intl":{"CarrierName":["United","Frontier","Continental"]},"Dallas Love ":{"CarrierName":["Southwest"]},"Dallas-Fort Worth International":{"CarrierName":["American","Alaska"]},"Denver Intl":{"CarrierName":["Frontier","Southwest","United","Alaska","Delta","SkyWest"]},"Detroit Metropolitan-Wayne County":{"CarrierName":["Northwest","Delta","Alaska"]},"Eppley Airfield":{"CarrierName":["Alaska","SkyWest"]},"Fairbanks International":{"CarrierName":["Alaska","Delta"]},"Fort Lauderdale-Hollywood Int\'l":{"CarrierName":["Alaska"]},"Fresno Yosemite International":{"CarrierName":["SkyWest"]},"Gallatin ":{"CarrierName":["SkyWest"]},"Gen Edw L Logan Intl":{"CarrierName":["Alaska","JetBlue","Delta"]},"General Mitchell International":{"CarrierName":["Southwest","SkyWest","AirTran","Frontier"]},"George Bush Intercontinental":{"CarrierName":["United","Alaska","Continental"]},"Honolulu International":{"CarrierName":["Northwest","Hawaiian","Delta","Alaska"]},"Jackson Hole":{"CarrierName":["SkyWest"]},"John F Kennedy Intl":{"CarrierName":["JetBlue","Delta","Alaska","American"]},"John Wayne /Orange Co":{"CarrierName":["SkyWest","Alaska","Southwest"]},"Juneau International":{"CarrierName":["Alaska","Delta","SkyWest"]},"Kahului":{"CarrierName":["Delta","Hawaiian","Alaska","Northwest"]},"Kansas City International":{"CarrierName":["Southwest","Alaska","Frontier"]},"Ketchikan International":{"CarrierName":["SkyWest","Alaska"]},"Kona International At Keahole":{"CarrierName":["Alaska","Delta"]},"Lambert-St Louis International":{"CarrierName":["Alaska","American","Southwest"]},"Lewiston-Nez Perce County":{"CarrierName":["SkyWest"]},"Lihue":{"CarrierName":["Alaska"]},"Long Beach (Daugherty )":{"CarrierName":["SkyWest","JetBlue","Alaska"]},"Los Angeles International":{"CarrierName":["Virgin America","SkyWest","Spirit","United","Alaska","American","Delta"]},"McCarran International":{"CarrierName":["Southwest","US","SkyWest","Spirit","Delta","Alaska"]},"Memphis International":{"CarrierName":["Northwest","Delta"]},"Metropolitan Oakland International":{"CarrierName":["Southwest","SkyWest","Alaska"]},"Miami International":{"CarrierName":["American","Alaska"]},"Minneapolis-St Paul Intl":{"CarrierName":["Northwest","Alaska","Delta"]},"Missoula International":{"CarrierName":["SkyWest"]},"Nashville International":{"CarrierName":["Alaska","Southwest"]},"New Orleans International ":{"CarrierName":["Alaska"]},"Newark Intl":{"CarrierName":["United","US","Alaska","Continental"]},"Ontario International":{"CarrierName":["SkyWest","Alaska"]},"Orlando International":{"CarrierName":["Alaska","Delta"]},"Palm Springs International":{"CarrierName":["Alaska","SkyWest"]},"Philadelphia Intl":{"CarrierName":["US","Alaska","American"]},"Phoenix Sky Harbor International":{"CarrierName":["Southwest","US","United","SkyWest","Frontier","Delta","Alaska","American"]},"Portland Intl":{"CarrierName":["Alaska","Delta","Frontier","SkyWest"]},"Raleigh-Durham International":{"CarrierName":["Alaska"]},"Reno/Tahoe International":{"CarrierName":["Southwest"]},"Ronald Reagan Washington National":{"CarrierName":["Alaska"]},"Sacramento International":{"CarrierName":["Alaska","Delta","SkyWest","Southwest"]},"Salt Lake City Intl":{"CarrierName":["Alaska","Delta","SkyWest","Southwest"]},"San Antonio International":{"CarrierName":["Alaska"]},"San Diego International-Lindbergh":{"CarrierName":["SkyWest","JetBlue","Alaska","Southwest","Delta"]},"San Francisco International":{"CarrierName":["Alaska","Delta","SkyWest","United","Virgin America"]},"San Jose International":{"CarrierName":["Southwest","SkyWest","Alaska"]},"Santa Barbara Municipal":{"CarrierName":["SkyWest"]},"Sitka":{"CarrierName":["Alaska","SkyWest"]},"Spokane Intl":{"CarrierName":["SkyWest","Southwest","Alaska","Delta"]},"Tampa International ":{"CarrierName":["Alaska"]},"Ted Stevens Anchorage International":{"CarrierName":["JetBlue","Alaska","Continental","Delta","United"]},"Tri-Cities":{"CarrierName":["SkyWest"]},"Tucson International":{"CarrierName":["Alaska","SkyWest"]},"Washington Dulles International":{"CarrierName":["United","Alaska"]},"Will Rogers World":{"CarrierName":["SkyWest"]},"William B Hartsfield-Atlanta Intl":{"CarrierName":["Southwest","AirTran","Delta","Alaska"]},"William P Hobby":{"CarrierName":["Southwest"]},"Yampa Valley":{"CarrierName":["SkyWest"]}};

$(document).ready(function() {
    $("#results").hide();
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
    $("#checkflight").bind('click', function() {
      var dt = to_moment($('#datetime').val());
      var hour = dt.hour();
      var minutes = dt.minute();
      var month = dt.month() + 1;
      var dayofmonth = dt.date();
      var year = dt.year();
      console.log(month, dayofmonth, year);

      $.getJSON('/result', {
        origin:    $('select[name="origin"]').val(),
        dest:      $('select[name="dest"]').val(),
        airline:   $('select[name="airline"]').val(),
        hour: hour,
        minutes: minutes,
        month: month,
        dayofmonth: dayofmonth,
        year: year,
      }, function(d) {
        $("#flight_results").show();
        $("#model_predict").text(d.result);
        $("#likelihood").text(d.likelihood + '%');
        style_result(d.intensity, "#model_predict");
        style_result(d.intensity, "#likelihood");
      });
      return false;
    });
    $("#btnPicker").bind('click', function() {
      $("#results").hide();
      $("#picker").show();
    });
    $("#dest").on('change', function () {
      var selection = $("#dest").val();
      var carriers = carrier_lookup[selection].CarrierName;
      var options = $("#airline");
      options = options.empty();
      for (var i = 0; i < carriers.length; i++) {
        options.append($("<option />").val(carriers[i]).text(carriers[i]));
      };

    });
});

function style_result(intensity, element) {
    if (intensity == 'low'){
        $(element).css("color", "green");
    } else if (intensity == 'moderate') {
        $(element).css("color", "#f48c42");
    } else if (intensity == 'severe') {
        $(element).css("color", "red");
    };
};

function to_moment(datestring) {
  var tst = moment(datestring, "MM/DD/YYYY h:mm A");
  return tst;
}
