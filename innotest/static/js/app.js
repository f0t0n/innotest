$(function() {
    var geocoder = new google.maps.Geocoder(),
        $from = $('#from'),
        $to = $('#to'),
        $submit = $('#submit'),
        $result = $('#result');

    var getLatLng = function(address) {

        return $.Deferred(function(dfrd) {
            geocoder.geocode({'address': address}, function(res, status) {
                if(status != 'OK') {
                    alert('Wrong address "' + address + '"');
                    dfrd.reject();
                    return;
                }
                dfrd.resolve(res[0].geometry.location);
            });
        }).promise();
    };

    var getRideDetails = function(callback) {
        var from = $from.val(),
            to = $to.val(),
            rideDetails = {};

        if(!(from && to)) {
            alert("Please fill the form.");
            return false;
        }


        $.when(getLatLng(from), getLatLng(to)).done(function(fromLoc, toLoc) {
            callback({
                start_latitude: fromLoc.lat(),
                start_longitude: fromLoc.lng(),
                end_latitude: toLoc.lat(),
                end_longitude: toLoc.lng()
            });
        });
    };

    var renderPrice = function(data) {
        var $ul = $('<ul>');
        $.each(data, function(i, item) {
            var $li = $('<li>');
            $li.text(item);
            $ul.append($li);
        });
        $result.html($ul);
    };

    var getPrice = function(e) {
        e.preventDefault();
        getRideDetails(function(rideDetails) {
            if(!rideDetails) {
                return;
            }
            $.getJSON(getPriceUrl, rideDetails, renderPrice);
        });
    };

    $('#car-order-form').on('submit', getPrice);
});

