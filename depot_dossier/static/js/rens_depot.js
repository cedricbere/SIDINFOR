
function main() {
	// body...
	//$('#id_post-nom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	//$('#id_post-prenom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	//$('#id_post-sexe').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-ville').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-lieu_naissance').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-num_tel').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-region').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_type_doc').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_num_doc').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_lieuEtablissement').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_dateEtablissement').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_dateExpiration').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});

	var onglet1 = new Array($('#idContenu'), $('#id'));
	var onglet2 = new Array($('#docContenu'), $('#doc'));
	var onglet3 = new Array($('#formationContenu'), $('#formation'));
	var onglet4 = new Array($('#curriculumContenu'), $('#curriculum'));
	var onglet5 = new Array($('#piecesContenu'), $('#pieces'));

	var ongleta = new Array($('#univContenu'), $('#universitaire'));
	var ongletb = new Array($('#stageContenu'), $('#stage'));
	var ongletc = new Array($('#proContenu'), $('#professionnel'));
	var ongletd = new Array($('#autreContenu'), $('#autre'));

	colorerOnglet(onglet1);
	colorerOnglet(onglet2);
	colorerOnglet(onglet3);
	colorerOnglet(onglet4);
	colorerOnglet(onglet5);

	var url = window.location.href.split('/')
	var ancre = url[url.length-1]

	if (!ancre.localeCompare('#idContenu'))	displayOnglet(onglet1, [onglet2, onglet3, onglet4, onglet5]);
	else if (!ancre.localeCompare('#docContenu')) displayOnglet(onglet2, [onglet3, onglet4, onglet5, onglet1]);
	else if (!ancre.localeCompare('#formationContenu')) displayOnglet(onglet3, [onglet4, onglet5, onglet1, onglet2]);
	else if (!ancre.localeCompare('#piecesContenu')) displayOnglet(onglet5, [onglet1, onglet2, onglet3, onglet4]);
	else
	{
		if (!ancre.localeCompare('#curriculumContenu')) displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
		else if (!ancre.localeCompare('#univContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#universitaire').attr('checked', true)
			displayOnglet(ongleta, [ongletb, ongletc, ongletd,]);
		}
		else if (!ancre.localeCompare('#stageContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#stage').attr('checked', true)
			displayOnglet(ongletb, [ongletc, ongletd, ongleta]);
		}
		else if (!ancre.localeCompare('#proContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#professionnel').attr('checked', true)
			displayOnglet(ongletc, [ongletd, ongleta, ongletb]);
		}
		else if (!ancre.localeCompare('#autreContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#autre').attr('checked', true)
			displayOnglet(ongletd, [ongleta, ongletb, ongletc]);
		}
		else
		{
			displayOnglet(onglet1, [onglet2, onglet3, onglet4, onglet5]);
			//location.href = url[url.length-1].join('/')+'#idContenu';
			//console.log(location.href);
		}
	}

/*
	$('#id_ufr').change(function(){
		departement($(this).val(), $('#id_niveau').val());});
	
	$('#id_dpt').change(function(){
		formation($(this).val(), $('#id_niveau').val());});

	$('#id_niveau').change(function(){
			formation($('#id_dpt').val(), $(this).val());});
*/	



	$('#add-form_univ').on({
		click: function() {
			cloner_ajouter($('#univ_forms'), $('#univ-empty_form'), 'univ');
		},
	});

	$('#add-form_stage').on({
		click: function() {
			cloner_ajouter($('#stage_forms'), $('#stage-empty_form'), 'stage');
		},
	});

	$('#add-form_pro').on({
		click: function() {
			cloner_ajouter($('#pro_forms'), $('#pro-empty_form'), 'pro');
		},
	});

	$('#add-form_autre').on({
		click: function() {
			cloner_ajouter($('#autre_forms'), $('#autre-empty_form'), 'autre');
		},
	});


	onglet1[1].on({
		click: function() {
			displayOnglet(onglet1, [onglet2, onglet3, onglet4, onglet5]);
		},
	});


	onglet2[1].on({
		click: function() {
			displayOnglet(onglet2, [onglet3, onglet4, onglet5, onglet1]);
		},
	});

	onglet3[1].on({
		click: function(){
			displayOnglet(onglet3, [onglet4, onglet5, onglet1, onglet2]);
		},
	});

	onglet4[1].on({
		click: function() {
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
		},
	});

	onglet5[1].on({
		click: function() {
			displayOnglet(onglet5, [onglet1, onglet2, onglet3, onglet4]);
			
		},
	});

	ongleta[1].on({
		click: function() {
			displayOnglet(ongleta, [ongletb, ongletc, ongletd]);
		},
	});

	ongletb[1].on({
		click: function() {
			displayOnglet(ongletb, [ongletc, ongletd, ongleta]);
		},
	});

	ongletc[1].on({
		click: function() {
			displayOnglet(ongletc, [ongletd, ongleta, ongletb]);
		},
	});

	ongletd[1].on({
		click: function() {
			displayOnglet(ongletd, [ongleta, ongletb, ongletc]);
		},
	});

	bande_coloree($('#infoDos'), $('#etatDos').text().trim());

	var barre = $('#progressbar');
	$(barre).progressbar()

	var fichier = document.getElementById('form_fichier');
	fichier.addEventListener('submit', function(event){
		event.preventDefault();
		$(barre).removeClass('invisible').addClass('visible');
		envoi_donnees($(barre), fichier, uploader_fichier_traitement);
	});
}

function bande_coloree(zone_a_colore, zone_info) {
	// body...

	if (!zone_info.localeCompare("En attente du remplissage")) 
	{
		zone_a_colore.css({'background-color': 'lightblue'});
	}
	else if (!zone_info.localeCompare("Encours de traitement"))
	{
		zone_a_colore.css({'background-color': 'lightgrey'});
	}
	else if (!zone_info.localeCompare("Validé"))
	{
		zone_a_colore.css({'background-color': 'lightgreen'});
	}
	else if (!zone_info.localeCompare("Rejeté"))
	{
		zone_a_colore.css({'background-color': 'red'});
	}
	else if (!zone_info.localeCompare("Annulé"))
	{
		zone_a_colore.css({'background-color': 'yellow'});
	}
}

/*
function periode(champs, sous) {
	// body...
	var valeur = champs.val();
	var annnee1 = valeur.substr(0,4);
	var annnee2 = valeur.substr(7,4);
	annnee1 = parseInt(annnee1); 
	annnee2 = parseInt(annnee2);
	
	return ((annnee1 - sous)+' - '+(annnee2 - sous));
}*/

function displayOnglet(visible, invisible) {
	// body...
	$(visible[0]).show().addClass('active');
	$(visible[1]).addClass('active').css({'font-weight': 'bold', color: 'white',});

	for (var i = 0; i < invisible.length; i++) {
		if ($(invisible[i][1]).hasClass('active')) {
			$(invisible[i][0]).hide().removeClass('active');
			$(invisible[i][1]).removeClass('active').css({'font-weight': '', color: '',});;
		}
	}
}

function parcoursContenuOnglet(arg) {
	// body...
	var bool = true;
	arg.find('input, select').not('input:submit, input[type=hidden], input:reset').each(function(){
		if (!$(this).val())
		{
			bool = false;
			return false;
		}
});
	if (bool)
		return true;
	else
		return false;
}

function colorerOnglet(onglet) {
	// body...
	var bool = parcoursContenuOnglet(onglet[0]);
	if (bool)
		onglet[1].css({'background-color': '#adff2f'});
	else
		onglet[1].css({'background-color': '#ffd700'});
}

function augmenter_totals(prefix) {
	// body...
	var $id_index = $('#id_'+prefix+'-TOTAL_FORMS');
	//var $id_max_num = $('#id_'+prefix+'-MAX_NUM_FORMS');
	var total = parseInt($id_index.val());
	$id_index.val(total+1);
	//$id_max_num.val(total+1)
}

function cloner_ajouter(forms, empty_form, prefix) {
	// body...
	augmenter_totals(prefix);
	var $id_index = $('#id_'+prefix+'-TOTAL_FORMS');
	var total = parseInt($id_index.val());
	var clone = empty_form.clone(true);
	clone.find('input, select, div, label').each(function() {
		// body...

		if ($(this).attr('id'))
		{
			var id_clone = new String($(this).attr('id'));
			id_clone = id_clone.replace('__prefix__', ''+(total-1)+'');
			$(this).attr('id', id_clone);
		}

		if ($(this).attr('for'))
		{
			var for_clone = new String($(this).attr('for'));
			for_clone = for_clone.replace('__prefix__', ''+(total-1)+'');
			$(this).attr('for', for_clone);
		}
		
		if ($(this).attr('name'))
		{
			var name_clone = new String($(this).attr('name'));
			name_clone = name_clone.replace('__prefix__', ''+(total-1)+'');
			$(this).attr('name', name_clone);
			/*
			if (name_clone.search('annee') != -1)
			{
				var champs = recherche_input(forms); var sous = 1;
				if (typeof champs == 'undefined')
				{
					var date = new Date(); date = parseInt(date.getFullYear());
					var annee = ((date - 1)+' - '+date);
					$(this).attr('value', annee);
				}
				else  $(this).attr('value', periode(champs, sous));	
			}*/
		}
		/*if ($(this).attr('dp_config')){
			var dernier = null
			$(forms).children('div:last').find('input').each(function(){
				if ($(this).attr('dp_config'))
				{
					dernier = JSON.parse($(this).attr('dp_config'));
				}
			});
			var val = parseInt(dernier.id.substr(3));
			dernier.id = 'dp_'+(val+1)
			$(this).attr('dp_config', JSON.stringify(dernier));
			
		}*/
	});
	forms.append(clone.html());
}

/*
function recherche_input(forms)
{
	var $champs;
	$(forms).children('div:last').find('input').each(function() {
		if (String($(this).attr('name')).search('annee') != -1) 
			$champs = $(this);
	});
	return $champs;
}*/

function ajout_dernier_form(forms, prefix) {
	// body...
	augmenter_totals(prefix);
	var $dernier = dernier_form($(forms));
	
	var html = '<div classe="form-row">'+$dernier.html()+'</div>'
	
	//var id = window.open().document;
	//$(id).white(html);
	//alert(html);
	//$(forms).append(html);
}

function dernier_form(forms) {
	// body...
	return $(forms).children('div.form-row:last').clone(true);
}

function envoi_fichier(){}

function envoi_donnees(barre, files, callback)
{	
	$(barre).progressbar({
		value: 0,
	});

	var xhr = getXMLHttResquest();
	xhr.open('POST', '/sidinfor/depot_dossier/ajax/uploader_fichier/', true);
	xhr.setRequestHeader('X-CSRFToken', csrftoken);

	xhr.onprogress = function(e){
		var loaded = Math.round((e.loaded/e.total)*100);
		$(barre).progressbar('value', loaded);
		$('#valeur_progress').html(loaded+'%');
	};

	xhr.onload = function(){
		$(barre).progressbar('value', 100);
	};

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 0)){
			resultat = xhr.responseText;
			if (!resultat.localeCompare('ok'))
			{
				//window.location.reload();
				$('#ms_sauve').removeClass('invisible');
				$('#erreurs_attestations').empty();
				$('#attestation_master').empty();
				$('#attestation_licence').empty();	
				$('#diplome_bac').empty();
				$('#curriculum_file').empty();
				$('#passeport').empty();
				$('#carteid_verso').empty();
				$('#carteid_recto').empty();
				$('#photo_id').empty();
			}
			else callback(xhr.responseText);
		}
	};

	var form = new FormData(files);
	xhr.send(form);
}


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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getXMLHttResquest() {
	// body...
	xhr = null;

	if (window.XMLHttpRequest || window.ActiveXObject)
	{
		if (window.ActiveXObject)
		{
			try
			{
				xhr = new ActiveXObject("Msxml2.XMLHTTP");
			}
			catch(e)
			{
				xhr = new ActiveXObject("Microsoft.XMLHTTP");
			}
		}
		else
			xhr = new XMLHttpRequest();
	}
	return xhr
}

function uploader_fichier_traitement(contenu_json) {
	// body...
	var liste_erreur = JSON.parse(contenu_json);

	$('.color_champs').empty();
	if (liste_erreur.photo_id)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.photo_id.length; i++) {
			erreur += liste_erreur.photo_id[i].message;
		}
		$('#photo_id').empty();
		$('#photo_id').html(erreur);
	}
	if (liste_erreur.carteid_recto)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.carteid_recto.length; i++) {
			erreur += liste_erreur.carteid_recto[i].message;
		}
		$('#carteid_recto').empty();
		$('#carteid_recto').html(erreur);
	}
	if (liste_erreur.carteid_verso)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.carteid_verso.length; i++) {
			erreur += liste_erreur.carteid_verso[i].message;
		}
		$('#carteid_verso').empty();
		$('#carteid_verso').html(erreur);
	}
	if (liste_erreur.passeport)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.passeport.length; i++) {
			erreur += liste_erreur.passeport[i].message;
		}
		$('#passeport').empty();
		$('#passeport').html(erreur);
	}
	if (liste_erreur.curriculum_file)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.curriculum_file.length; i++) {
			erreur += liste_erreur.curriculum_file[i].message;
		}
		$('#curriculum_file').empty();
		$('#curriculum_file').html(erreur);
	}
	if (liste_erreur.attestation_licence)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.attestation_licence.length; i++) {
			erreur += liste_erreur.attestation_licence[i].message;
		}
		$('#attestation_licence').empty();
		$('#attestation_licence').html(erreur);
	}
	if (liste_erreur.diplome_bac)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.diplome_bac.length; i++) {
			erreur += liste_erreur.diplome_bac[i].message;
		}
		$('#diplome_bac').empty();
		$('#diplome_bac').html(erreur);
	}
	if (liste_erreur.attestation_master)
	{
		var erreur = [];
		for (var i = 0; i < liste_erreur.attestation_master.length; i++) {
			erreur += liste_erreur.attestation_master[i].message;
		}
		$('#attestation_master').empty();
		$('#attestation_master').html(erreur);
	}
	if (liste_erreur.attestation_travail || liste_erreur.attestation_stage || liste_erreur.attestation_autre || liste_erreur.emploi || liste_erreur.stage || liste_erreur.emploi_autre)
	{
		var erreur = [];
		if (liste_erreur.attestation_travail){
			for (var i = 0; i < liste_erreur.attestation_travail.length; i++) {
				erreur.push('Attestation de travail: '+liste_erreur.attestation_travail[i].message);
			}
		}

		if (liste_erreur.emploi){
			for (var i = 0; i < liste_erreur.emploi.length; i++) {
				erreur.push('Emploi: '+liste_erreur.emploi[i].message);
			}
		}

		if (liste_erreur.attestation_stage){
			for (var i = 0; i < liste_erreur.attestation_stage.length; i++) {
				erreur.push('Attestation de stage: '+liste_erreur.attestation_stage[i].message);
			}
		}

		if (liste_erreur.stage){
			for (var i = 0; i < liste_erreur.stage.length; i++) {
				erreur.push('Stage: '+liste_erreur.stage[i].message);
			}
		}

		if (liste_erreur.attestation_autre){
			for (var i = 0; i < liste_erreur.attestation_autre.length; i++) {
				erreur.push('Attestation autre occupation: '+liste_erreur.attestation_autre[i].message);
			}
		}

		if (liste_erreur.emploi_autre){
			for (var i = 0; i < liste_erreur.emploi_autre.length; i++) {
				erreur.push('Autre: '+liste_erreur.emploi_autre[i].message);
			}
		}

		$('#erreurs_attestations').empty();
		for (var i = 0; i < erreur.length; i++) {
			$('#erreurs_attestations').append(erreur[i]);
			$('#erreurs_attestations').append('<br>');
		}
		
	}
}

/*
function controleur_annee(periode_annee) {
	// body...
	var regex_expression = "^\d{4} - \d{4}$";
	var regex = new RegExp(regex_expression, 'i');
	if (!regex.test(periode_annee))
	{
		var an1 = periode_annee.substr(0,4); var an2 = periode_annee.substr();
	}
	return periode_annee;
}*/

$(document).ready(main);

