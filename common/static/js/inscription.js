function script(){
	// body...
	$('#id_etud-dateNaissance').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-numTel').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-nom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-sexe').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-promotion').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-filiere').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-prenom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-password').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-dPassword').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});

	$('#id_post-dateNaissance').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-nom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-sexe').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-pays').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	
	$('#id_post-prenom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-password').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-dPassword').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});

	$('#id_etud-email').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verification('email', $(this).val(), 'etud');
		} ,
	});
	$('#id_post-email').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verification('email', $(this).val(), 'post');
		} ,
	});
	$('#id_matricule').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_etud-pseudo').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verification('pseudo', $(this).val(), 'etud');
		} ,
	});
	$('#id_post-pseudo').popover({delay: {show: 500, hide: 200}, trigger: 'hover'}).on({
		focusout: function() {
			verification('pseudo', $(this).val(), 'post');
		} ,
	});

	
	displayRightForm();
	$('#typeProfile').change(displayRightForm);

	$('#id_ufr').change(function(){
		departement($(this).val(), $('#id_niveaux').val());});
	
	$('#id_dpts').change(function(){
		formation($(this).val(), $('#id_niveaux').val());});

	$('#id_niveaux').change(function(){
			formation($('#id_dpts').val(), $(this).val());});
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
	else 
	{
		$('#FormEtudiant').hide();
		$('#FormPostulant').hide();
	}
}

function verification(type, valeur, prefix){
	// body...
	$.get({
		url: '../verification',
		//url: '{% url verification %}',
		data: {'type': type, 'valeur': valeur},
		dataType: 'json',
		success: function(code_json, statut){
			var classe = null;
			if (code_json.statut == 'erreur') classe = 'bg-danger';
			else classe = 'bg-warning';
			var message = null
			if (type == 'email'){
				message = "<p class='"+classe+" email' style='text-align:center;'>"+code_json.message+"<p>";
				$('#div_id_'+prefix+'-email').parent().children('p.email').remove();
				$('#div_id_'+prefix+'-email').before(message);
			}
			else if (type == 'pseudo'){
				message = "<p class='"+classe+" pseudo' style='text-align:center;'>"+code_json.message+"<p>";
				$('#div_id_'+prefix+'-pseudo').parent().children('p.pseudo').remove();
				$('#div_id_'+prefix+'-pseudo').before(message)
			}
		},
		error: function(resultat, statut, erreur){console.log(erreur);}
	});
}

function departement(ufr, niveau) {
	// body...
	$.get({
		url: '../changer_departement',
		data: {'ufr': ufr, 'niveau': niveau},
		dataType: 'json',
		success : function(code_json, statut){
			var departement_json = JSON.parse(code_json.departement), formation_json = JSON.parse(code_json.formation);
			var departement = $('#id_dpts'), formation = $('#id_formation')

			departement.empty();
			departement.append('<option value="" selected>--------</option>');
			for (var i = 0; i < departement_json.length; i++) {
				departement.append('<option value="'+departement_json[i].pk+'">'+departement_json[i].fields.nom_dpt+'</option>')
			}
			if (niveau == 'Master'){
				formation.empty();
				formation.append('<option value="" selected>--------</option>');
				for (var i = 0; i < formation_json.length; i++) {
					formation.append('<option value="'+formation_json[i].pk+'">'+formation_json[i].fields.formation_master+'</option>')
				}
			}

		},
		error: function(resultat, statut, erreur){
			console.log(erreur);
		}
	});
}

function formation(dpt, niveau) {
	// body...
	$.get({
		url: '../changer_formation',
		data: {'dpt': dpt, 'niveau': niveau},
		dataType: 'json',
		success : function(code_json, statut){
			if (niveau == 'Master'){
				var formation_json = JSON.parse(code_json.formation), formation = $('#id_formation')
				formation.empty(); formation.append('<option value="" selected>--------</option>');
				for (var i = 0; i < formation_json.length; i++) {
					formation.append('<option value="'+formation_json[i].pk+'">'+formation_json[i].fields.formation_master+'</option>');
				}
			}

		},
		error: function(resultat, statut, erreur){
			console.log(erreur);
		}
	});
}


// $('#parent_proche').on('action', '#element', function(){});

$(document).ready(script);