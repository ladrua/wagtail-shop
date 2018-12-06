(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";

// hei
$(document).ready(function () {
    $('.order-list tbody tr').on("click", function (e) {
        window.location = "inspect/" + $(this).data("object-pk") + "/";
    });
    $('.products-list tbody tr').on("click", function (e) {
        window.location = "edit/" + $(this).data("object-pk") + "/";
    });
    $('.resendconfirmation').on('click', function (e) {
        e.preventDefault();
        $(this).prev('p').html('Resend Confirmation e-mail:');
        $(this).css('display', 'none');
        $('.resendconfirmation-input').css('display', 'flex');
    });
    $('.resendconfirmation-input button.no').on('click', function (e) {
        $('.resendconfirmation-input').css('display', 'none');
        $('.resendconfirmation').css('display', 'block');
        $('.resendconfirmation').prev('p').html('Other Actions:');
    });
    $('.resendconfirmation-form').on('submit', function (e) {
        e.preventDefault();

        $('.loading').css('display', 'flex');
        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function beforeSend(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === name + '=') {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };
        var inputdata = { email: $('.emailinput').val() };
        $.ajax({
            url: $('button.yes', this).data("url"),
            type: "POST",
            data: inputdata,
            success: function success(data, textStatus, jqXHR) {
                window.location = data;
            },
            error: function error(jqXHR, textStatus, errorThrown) {
                console.log(textStatus);
                console.log(errorThrown);
                $('.resendconfirmation-input').css('display', 'block');
                $('.loading').css('display', 'none');
            }
        });
    });
});

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJqcy9zaG9wYWRtaW4uanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7OztBQ0FBO0FBQ0EsRUFBRSxRQUFGLEVBQVksS0FBWixDQUFrQixZQUFVO0FBQ3hCLE1BQUUsc0JBQUYsRUFBMEIsRUFBMUIsQ0FBNkIsT0FBN0IsRUFBc0MsVUFBUyxDQUFULEVBQVk7QUFDOUMsZUFBTyxRQUFQLEdBQWtCLGFBQWEsRUFBRSxJQUFGLEVBQVEsSUFBUixDQUFhLFdBQWIsQ0FBYixHQUF5QyxHQUEzRDtBQUNILEtBRkQ7QUFHQSxNQUFFLHlCQUFGLEVBQTZCLEVBQTdCLENBQWdDLE9BQWhDLEVBQXlDLFVBQVMsQ0FBVCxFQUFZO0FBQ2pELGVBQU8sUUFBUCxHQUFrQixVQUFVLEVBQUUsSUFBRixFQUFRLElBQVIsQ0FBYSxXQUFiLENBQVYsR0FBc0MsR0FBeEQ7QUFDSCxLQUZEO0FBR0EsTUFBRSxxQkFBRixFQUF5QixFQUF6QixDQUE0QixPQUE1QixFQUFxQyxVQUFTLENBQVQsRUFBWTtBQUM3QyxVQUFFLGNBQUY7QUFDQSxVQUFFLElBQUYsRUFBUSxJQUFSLENBQWEsR0FBYixFQUFrQixJQUFsQixDQUF1Qiw2QkFBdkI7QUFDQSxVQUFFLElBQUYsRUFBUSxHQUFSLENBQVksU0FBWixFQUF1QixNQUF2QjtBQUNBLFVBQUUsMkJBQUYsRUFBK0IsR0FBL0IsQ0FBbUMsU0FBbkMsRUFBOEMsTUFBOUM7QUFFSCxLQU5EO0FBT0EsTUFBRSxxQ0FBRixFQUF5QyxFQUF6QyxDQUE0QyxPQUE1QyxFQUFxRCxVQUFTLENBQVQsRUFBWTtBQUM3RCxVQUFFLDJCQUFGLEVBQStCLEdBQS9CLENBQW1DLFNBQW5DLEVBQThDLE1BQTlDO0FBQ0EsVUFBRSxxQkFBRixFQUF5QixHQUF6QixDQUE2QixTQUE3QixFQUF3QyxPQUF4QztBQUNBLFVBQUUscUJBQUYsRUFBeUIsSUFBekIsQ0FBOEIsR0FBOUIsRUFBbUMsSUFBbkMsQ0FBd0MsZ0JBQXhDO0FBQ0gsS0FKRDtBQUtBLE1BQUUsMEJBQUYsRUFBOEIsRUFBOUIsQ0FBaUMsUUFBakMsRUFBMkMsVUFBUyxDQUFULEVBQVk7QUFDbkQsVUFBRSxjQUFGOztBQUVBLFVBQUUsVUFBRixFQUFjLEdBQWQsQ0FBa0IsU0FBbEIsRUFBNkIsTUFBN0I7QUFDQSxZQUFJLFlBQVksVUFBVSxXQUFWLENBQWhCO0FBQ0EsVUFBRSxTQUFGLENBQVk7QUFDUix3QkFBWSxvQkFBUyxHQUFULEVBQWMsUUFBZCxFQUF3QjtBQUNoQyxvQkFBSSxnQkFBSixDQUFxQixhQUFyQixFQUFvQyxTQUFwQztBQUVIO0FBSk8sU0FBWjtBQU1BLGlCQUFTLFNBQVQsQ0FBbUIsSUFBbkIsRUFBeUI7QUFDdkIsZ0JBQUksY0FBYyxJQUFsQjtBQUNBLGdCQUFJLFNBQVMsTUFBVCxJQUFtQixTQUFTLE1BQVQsS0FBb0IsRUFBM0MsRUFBK0M7QUFDM0Msb0JBQUksVUFBVSxTQUFTLE1BQVQsQ0FBZ0IsS0FBaEIsQ0FBc0IsR0FBdEIsQ0FBZDtBQUNBLHFCQUFLLElBQUksSUFBSSxDQUFiLEVBQWdCLElBQUksUUFBUSxNQUE1QixFQUFvQyxHQUFwQyxFQUF5QztBQUNyQyx3QkFBSSxTQUFTLE9BQU8sSUFBUCxDQUFZLFFBQVEsQ0FBUixDQUFaLENBQWI7QUFDQTtBQUNBLHdCQUFJLE9BQU8sU0FBUCxDQUFpQixDQUFqQixFQUFvQixLQUFLLE1BQUwsR0FBYyxDQUFsQyxNQUEwQyxPQUFPLEdBQXJELEVBQTJEO0FBQ3ZELHNDQUFjLG1CQUFtQixPQUFPLFNBQVAsQ0FBaUIsS0FBSyxNQUFMLEdBQWMsQ0FBL0IsQ0FBbkIsQ0FBZDtBQUNBO0FBQ0g7QUFDSjtBQUNKO0FBQ0QsbUJBQU8sV0FBUDtBQUNIO0FBQ0MsWUFBSSxZQUFZLEVBQUUsT0FBTyxFQUFFLGFBQUYsRUFBaUIsR0FBakIsRUFBVCxFQUFoQjtBQUNBLFVBQUUsSUFBRixDQUFPO0FBQ0gsaUJBQU0sRUFBRSxZQUFGLEVBQWdCLElBQWhCLEVBQXNCLElBQXRCLENBQTJCLEtBQTNCLENBREg7QUFFSCxrQkFBTSxNQUZIO0FBR0gsa0JBQU8sU0FISjtBQUlQLHFCQUFTLGlCQUFTLElBQVQsRUFBZSxVQUFmLEVBQTJCLEtBQTNCLEVBQ1Q7QUFDSSx1QkFBTyxRQUFQLEdBQWtCLElBQWxCO0FBQ0gsYUFQTTtBQVFQLG1CQUFPLGVBQVUsS0FBVixFQUFpQixVQUFqQixFQUE2QixXQUE3QixFQUNQO0FBQ0ksd0JBQVEsR0FBUixDQUFZLFVBQVo7QUFDQSx3QkFBUSxHQUFSLENBQVksV0FBWjtBQUNBLGtCQUFFLDJCQUFGLEVBQStCLEdBQS9CLENBQW1DLFNBQW5DLEVBQThDLE9BQTlDO0FBQ0Esa0JBQUUsVUFBRixFQUFjLEdBQWQsQ0FBa0IsU0FBbEIsRUFBNkIsTUFBN0I7QUFFSDtBQWZNLFNBQVA7QUFpQkgsS0E1Q0Q7QUE2Q0gsQ0FoRUQiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbigpe2Z1bmN0aW9uIHIoZSxuLHQpe2Z1bmN0aW9uIG8oaSxmKXtpZighbltpXSl7aWYoIWVbaV0pe3ZhciBjPVwiZnVuY3Rpb25cIj09dHlwZW9mIHJlcXVpcmUmJnJlcXVpcmU7aWYoIWYmJmMpcmV0dXJuIGMoaSwhMCk7aWYodSlyZXR1cm4gdShpLCEwKTt2YXIgYT1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK2krXCInXCIpO3Rocm93IGEuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixhfXZhciBwPW5baV09e2V4cG9ydHM6e319O2VbaV1bMF0uY2FsbChwLmV4cG9ydHMsZnVuY3Rpb24ocil7dmFyIG49ZVtpXVsxXVtyXTtyZXR1cm4gbyhufHxyKX0scCxwLmV4cG9ydHMscixlLG4sdCl9cmV0dXJuIG5baV0uZXhwb3J0c31mb3IodmFyIHU9XCJmdW5jdGlvblwiPT10eXBlb2YgcmVxdWlyZSYmcmVxdWlyZSxpPTA7aTx0Lmxlbmd0aDtpKyspbyh0W2ldKTtyZXR1cm4gb31yZXR1cm4gcn0pKCkiLCIvLyBoZWlcbiQoZG9jdW1lbnQpLnJlYWR5KGZ1bmN0aW9uKCl7XG4gICAgJCgnLm9yZGVyLWxpc3QgdGJvZHkgdHInKS5vbihcImNsaWNrXCIsIGZ1bmN0aW9uKGUpIHtcbiAgICAgICAgd2luZG93LmxvY2F0aW9uID0gXCJpbnNwZWN0L1wiICsgJCh0aGlzKS5kYXRhKFwib2JqZWN0LXBrXCIpICsgXCIvXCI7XG4gICAgfSk7XG4gICAgJCgnLnByb2R1Y3RzLWxpc3QgdGJvZHkgdHInKS5vbihcImNsaWNrXCIsIGZ1bmN0aW9uKGUpIHtcbiAgICAgICAgd2luZG93LmxvY2F0aW9uID0gXCJlZGl0L1wiICsgJCh0aGlzKS5kYXRhKFwib2JqZWN0LXBrXCIpICsgXCIvXCI7XG4gICAgfSk7XG4gICAgJCgnLnJlc2VuZGNvbmZpcm1hdGlvbicpLm9uKCdjbGljaycsIGZ1bmN0aW9uKGUpIHtcbiAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAkKHRoaXMpLnByZXYoJ3AnKS5odG1sKCdSZXNlbmQgQ29uZmlybWF0aW9uIGUtbWFpbDonKTtcbiAgICAgICAgJCh0aGlzKS5jc3MoJ2Rpc3BsYXknLCAnbm9uZScpO1xuICAgICAgICAkKCcucmVzZW5kY29uZmlybWF0aW9uLWlucHV0JykuY3NzKCdkaXNwbGF5JywgJ2ZsZXgnKTtcblxuICAgIH0pO1xuICAgICQoJy5yZXNlbmRjb25maXJtYXRpb24taW5wdXQgYnV0dG9uLm5vJykub24oJ2NsaWNrJywgZnVuY3Rpb24oZSkge1xuICAgICAgICAkKCcucmVzZW5kY29uZmlybWF0aW9uLWlucHV0JykuY3NzKCdkaXNwbGF5JywgJ25vbmUnKTtcbiAgICAgICAgJCgnLnJlc2VuZGNvbmZpcm1hdGlvbicpLmNzcygnZGlzcGxheScsICdibG9jaycpO1xuICAgICAgICAkKCcucmVzZW5kY29uZmlybWF0aW9uJykucHJldigncCcpLmh0bWwoJ090aGVyIEFjdGlvbnM6Jyk7XG4gICAgfSk7XG4gICAgJCgnLnJlc2VuZGNvbmZpcm1hdGlvbi1mb3JtJykub24oJ3N1Ym1pdCcsIGZ1bmN0aW9uKGUpIHtcbiAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICBcbiAgICAgICAgJCgnLmxvYWRpbmcnKS5jc3MoJ2Rpc3BsYXknLCAnZmxleCcpO1xuICAgICAgICB2YXIgY3NyZnRva2VuID0gZ2V0Q29va2llKCdjc3JmdG9rZW4nKTtcbiAgICAgICAgJC5hamF4U2V0dXAoe1xuICAgICAgICAgICAgYmVmb3JlU2VuZDogZnVuY3Rpb24oeGhyLCBzZXR0aW5ncykge1xuICAgICAgICAgICAgICAgIHhoci5zZXRSZXF1ZXN0SGVhZGVyKFwiWC1DU1JGVG9rZW5cIiwgY3NyZnRva2VuKTtcblxuICAgICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgICAgZnVuY3Rpb24gZ2V0Q29va2llKG5hbWUpIHtcbiAgICAgICAgICB2YXIgY29va2llVmFsdWUgPSBudWxsO1xuICAgICAgICAgIGlmIChkb2N1bWVudC5jb29raWUgJiYgZG9jdW1lbnQuY29va2llICE9PSAnJykge1xuICAgICAgICAgICAgICB2YXIgY29va2llcyA9IGRvY3VtZW50LmNvb2tpZS5zcGxpdCgnOycpO1xuICAgICAgICAgICAgICBmb3IgKHZhciBpID0gMDsgaSA8IGNvb2tpZXMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgICAgICAgICAgIHZhciBjb29raWUgPSBqUXVlcnkudHJpbShjb29raWVzW2ldKTtcbiAgICAgICAgICAgICAgICAgIC8vIERvZXMgdGhpcyBjb29raWUgc3RyaW5nIGJlZ2luIHdpdGggdGhlIG5hbWUgd2Ugd2FudD9cbiAgICAgICAgICAgICAgICAgIGlmIChjb29raWUuc3Vic3RyaW5nKDAsIG5hbWUubGVuZ3RoICsgMSkgPT09IChuYW1lICsgJz0nKSkge1xuICAgICAgICAgICAgICAgICAgICAgIGNvb2tpZVZhbHVlID0gZGVjb2RlVVJJQ29tcG9uZW50KGNvb2tpZS5zdWJzdHJpbmcobmFtZS5sZW5ndGggKyAxKSk7XG4gICAgICAgICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgICAgcmV0dXJuIGNvb2tpZVZhbHVlO1xuICAgICAgfTtcbiAgICAgICAgdmFyIGlucHV0ZGF0YSA9IHsgZW1haWw6ICQoJy5lbWFpbGlucHV0JykudmFsKCkgfVxuICAgICAgICAkLmFqYXgoe1xuICAgICAgICAgICAgdXJsIDogJCgnYnV0dG9uLnllcycgLHRoaXMpLmRhdGEoXCJ1cmxcIiksXG4gICAgICAgICAgICB0eXBlOiBcIlBPU1RcIixcbiAgICAgICAgICAgIGRhdGEgOiBpbnB1dGRhdGEsXG4gICAgICAgIHN1Y2Nlc3M6IGZ1bmN0aW9uKGRhdGEsIHRleHRTdGF0dXMsIGpxWEhSKVxuICAgICAgICB7XG4gICAgICAgICAgICB3aW5kb3cubG9jYXRpb24gPSBkYXRhO1xuICAgICAgICB9LFxuICAgICAgICBlcnJvcjogZnVuY3Rpb24gKGpxWEhSLCB0ZXh0U3RhdHVzLCBlcnJvclRocm93bilcbiAgICAgICAge1xuICAgICAgICAgICAgY29uc29sZS5sb2codGV4dFN0YXR1cyk7XG4gICAgICAgICAgICBjb25zb2xlLmxvZyhlcnJvclRocm93bik7XG4gICAgICAgICAgICAkKCcucmVzZW5kY29uZmlybWF0aW9uLWlucHV0JykuY3NzKCdkaXNwbGF5JywgJ2Jsb2NrJyk7XG4gICAgICAgICAgICAkKCcubG9hZGluZycpLmNzcygnZGlzcGxheScsICdub25lJyk7XG5cbiAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICB9KTtcbn0pO1xuIl19
