function displayRightForm() {
	// body...

	var onglet1 = new Array($('#stage'), $('#ongletStage'));
	var onglet2 = new Array($('#rapport'), $('#ongletRapport'));
	var onglet3 = new Array($('#soutenance'), $('#ongletSoutenance'));

	/*colorerOnglet(onglet1);
	colorerOnglet(onglet2);
	colorerOnglet(onglet3);*/

	onglet1[1].on({
		click: function(){
			displayOnglet(onglet1, [onglet2, onglet3]);
		},
	});

	onglet2[1].on({
		click: function(){
			displayOnglet(onglet2, [onglet3, onglet1]);
		},
	});

	onglet3[1].on({
		click: function(){
			displayOnglet(onglet3, [onglet1, onglet2]);
		},
	});

}


/**
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({   headers: {  "X-CSRFToken": csrftoken  }  });
**/

$('document').ready(displayRightForm);