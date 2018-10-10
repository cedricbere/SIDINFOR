function script(){
	// body...
	$('#id_dateNaissance').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_numTel').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_nom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_sexe').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_pays').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_promotion').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_filiere').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
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

	displayRightForm();
	$('#typeProfile').change(displayRightForm);

	$('#id_ufr').change(chargerDpt);
	$('#id_dpts').change(chargerFormation);
	$('#id_niveaux').change(chargerFormation);
}

function verificationEmail() {
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

function verificationPseudo() {
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
		$('#FormPostulant').hide();
		$('#FormEtudiant').show();
	}
	else if ($('#typeProfile').val() == 'postulant')
	{
		$('#FormEtudiant').hide();
		$('#FormPostulant').show();
	}
}

function chargerDpt() {
	// body...
	var ufr = $('#id_ufr').val();
	$.ajax({
		url: '../chargerDpt',
		type: 'GET',
		data: ({'ufr': ufr}),
		dataType: 'html',
		success: function(code_html, statut) {
			$('#id_dpts').parent().parent().replaceWith(code_html);
			$(document).ready(script);
		},
		error: function(resultat, statut, erreur) {
			
		},
		complete: function(resultat, statut) {

		}
	});
}


function chargerFormation() {
	// body...
	var dpt = $('#id_dpts').val();
	var niveau = $('#id_niveaux').val();
	$.ajax({
		url: '../chargerFormation',
		type: 'GET',
		data: ({'dpt': dpt, 'niveau': niveau}),
		dataType: 'html',
		success: function(code_html, statut) {
			$('#id_formation').parent().parent().replaceWith(code_html);
			//$(document).ready(script);
		},
		error: function(resultat, statut, erreur) {
			
		},
		complete: function(resultat, statut) {

		}
	});
}


$(document).ready(script);