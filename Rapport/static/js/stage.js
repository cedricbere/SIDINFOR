function displayRightForm() {
	// body...
	var ancien1 = $('#st1');
	var ancien2 = $('#rp1');
	var ancien3 = $('#sout');

	$('#aStage').on({
		click: displayStage,
	});

	$('#aRapport').on({
		click: displayRapport,
	});

	$('#aSoutenance').on({
		click: displaySoutenance,
	});

	$('#modif1').on({
		click: modificationStage,
	});

	$('#modif2').on({
		click: modificationRapport,
	});

	$('#modif3').on({
		click: modificationSoutenance,
	});

	/*$('#ann1').on({
		click: annuler1(ancien1),
	});

	$('#ann2').on({
		click: modificationRapport,
	});

	$('#ann3').on({
		click: modificationSoutenance,
	});*/
}
/*
function annuler1(ancien) {
	// body...
	alert('appel réussit')
	$('#st1').replaceWith(ancien);
}*/

function modificationStage() {
	// body...
	$.ajax({
		url: '../modificationStage',
		type: 'GET',
		data: ({}),
		dataType: 'html',
		success: function(code_html, statut) {
			$('#st1').replaceWith(code_html);
		},
		error: function(resultat, statut, erreur) {
			// body...
			alert(erreur);
		},
		complete: function (resultat, statut) {
			// body...
		},
	});
}

function modificationRapport() {
	// body...
	$.ajax({
		url: '../modificationRapport',
		type: 'GET',
		data: ({}),
		dataType: 'html',
		success: function(code_html, statut) {
			
			$('#rp1').replaceWith(code_html);
		},
		error: function(resultat, statut, erreur) {
			// body...
			alert('Erreur');
		},
		complete: function (resultat, statut) {
			// body...
		},
	});
}

function modificationSoutenance() {
	// body...
	$.ajax({
		url: '../modificationSoutenance',
		type: 'GET',
		data: ({}),
		dataType: 'html',
		success: function(code_html, statut) {
			$('#sout1').replaceWith(code_html);
		},
		error: function(resultat, statut, erreur) {
			// body...
			alert('Erreur');
		},
		complete: function (resultat, statut) {
			// body...
			//alert('Complet');
		},
	});
}


function displayStage() {
	// body...
	$('#stage').show().addClass('active');
	$('#aStage').addClass('active').css({'background-color': 'lightblue'});

	$('#rapport').hide().removeClass('active');
	$('#aRapport').removeClass('active').css({'background-color': 'white'});

	$('#soutenance').hide().removeClass('active');
	$('#aSoutenance').removeClass('active').css({'background-color': 'white'});
}

function displayRapport() {
	// body...
	$('#rapport').show().addClass('active');
	$('#aRapport').addClass('active').css({'background-color': 'lightblue'});;

	$('#stage').hide().removeClass('active');
	$('#aStage').removeClass('active').css({'background-color': 'white'});

	$('#soutenance').hide().removeClass('active');
	$('#aSoutenance').removeClass('active').css({'background-color': 'white'});
}

function displaySoutenance() {
	// body...
	$('#rapport').hide().removeClass('active');
	$('#aRapport').removeClass('active').css({'background-color': 'white'});

	$('#stage').hide().removeClass('active');
	$('#aStage').removeClass('active').css({'background-color': 'white'});

	$('#soutenance').show().addClass('active')
	$('#aSoutenance').addClass('active').css({'background-color': 'lightblue'});;
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