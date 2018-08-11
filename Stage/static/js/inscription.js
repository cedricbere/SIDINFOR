function script(){
	// body...
	$('#id_dateNaissance').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_numTel').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_nom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_prenom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_password').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_dPassword').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_email').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: verificationEmail,
	});
	$('#id_matricule').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_pseudo').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: verificationPseudo,
	});
	$('#typeProfile').change(displayRightForm);
}

function verificationEmail(argument) {
	// body...
	var email = $('#id_email').val();
	$.ajax({
		url: '../verificationEmail',
		type: 'GET',
		data: ({'email': email}),
		dataType: 'html',
		success: function(code_html, statut) {
			$('#id_email').parent().prev('p.message').remove();
			$('#id_email').parent().before(code_html);
		},
		error: function(resultat, statut, erreur) {
			
		},
		complete: function(resultat, statut) {

		}
	});
}

function verificationPseudo(argument) {
	// body...
	var pseudo = $('#id_pseudo').val();
	$.ajax({
		url: '../verificationPseudo',
		type: 'GET',
		data: ({'pseudo': pseudo}),
		dataType: 'html',
		success: function(code_html, statut) {
			$('#id_pseudo').parent().prev('p.message').remove();
			$('#id_pseudo').parent().before(code_html);
		},
		error: function(resultat, statut, erreur) {
			
		},
		complete: function(resultat, statut) {

		}
	});
}

function displayRightForm() {
	// body...
	if ($('#typeProfile').val() == 'etudiant')
	{
		$('#FormEmploye').hide();
		$('#FormEtudiant').show();
	}
	else
	{
		$('#FormEtudiant').hide();
		$('#FormEmploye').show()
	}
}

$(document).ready(script);