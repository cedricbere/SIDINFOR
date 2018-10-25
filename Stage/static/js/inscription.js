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
	$('#id_etud-email').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verificationEmailPseudo([$('#id_etud-email'), 'Email']);
		} ,
	});
	$('#id_post-email').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verificationEmailPseudo([$('#id_post-email'), 'Email']);
		} ,
	});
	$('#id_matricule').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-pseudo').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verificationEmailPseudo([$('#id_etud-pseudo'), 'Pseudo']);
		} ,
	});
	$('#id_post-pseudo').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verificationEmailPseudo([$('#id_post-pseudo'), 'Pseudo']);
		} ,
	});

	$('#FormEtudiant').on({
		submit: function() {
			console.log('ok');
			//$('#FormPostulant').remove();
		},
	})

	displayRightForm();
	$('#typeProfile').change(displayRightForm);
	$('#id_ufr').change(chargerDpt);
	$('#id_dpts').change(chargerFormation);
	$('#id_niveaux').change(chargerFormation);
}

function verificationEmailPseudo(donnee) {
	// body...
	var valeur = donnee[0].val();
	$.ajax({
		url: '../verification'+donnee[1],
		type: 'GET',
		data: ({'valeur': valeur}),
		dataType: 'html',
		success: function(code_html, statut) {
			donnee[0].parent().parent().prev('p.message').remove();
			donnee[0].parent().parent().before(code_html);
		},
		error: function(resultat, statut, erreur) {
			console.log(erreur);
			
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