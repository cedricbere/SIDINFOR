
function main() {
	// body...
	//$('#id_post-nom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	//$('#id_post-prenom').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	//$('#id_post-sexe').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-ville').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-lieuNaissance').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-nationalite').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
	$('#id_post-numTel').popover({delay: {show: 500, hide: 200}, trigger: 'hover'});
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
	var onglet5 = new Array($('#pieceContenu'), $('#piece'));

	var ongleta = new Array($('#scoContenu'), $('#scolaire'));
	var ongletb = new Array($('#univContenu'), $('#universitaire'));
	var ongletc = new Array($('#stageContenu'), $('#stage'));
	var ongletd = new Array($('#proContenu'), $('#professionnel'));
	var onglete = new Array($('#autreContenu'), $('#autre'));

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
	else if (!ancre.localeCompare('#pieceContenu')) displayOnglet(onglet5, [onglet1, onglet2, onglet3, onglet4]);
	else
	{
		if (!ancre.localeCompare('#curriculumContenu')) displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
		else if (!ancre.localeCompare('#scoContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#scolaire').attr('checked', true)
			displayOnglet(ongleta, [ongletb, ongletc, ongletd, onglete]);
		}
		else if (!ancre.localeCompare('#univContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#universitaire').attr('checked', true)
			displayOnglet(ongletb, [ongletc, ongletd, onglete, ongleta]);
		}
		else if (!ancre.localeCompare('#stageContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#stage').attr('checked', true)
			displayOnglet(ongletc, [ongletd, onglete, ongleta, ongletb]);
		}
		else if (!ancre.localeCompare('#proContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#professionnel').attr('checked', true)
			displayOnglet(ongletd, [onglete, ongleta, ongletb, ongletc]);
		}
		else if (!ancre.localeCompare('#autreContenu'))
		{
			displayOnglet(onglet4, [onglet5, onglet1, onglet2, onglet3]);
			$('#autre').attr('checked', true)
			displayOnglet(onglete, [ongleta, ongletb, ongletc, ongletd]);
		}
		else
		{
			displayOnglet(onglet1, [onglet2, onglet3, onglet4, onglet5]);
			//location.href = url[url.length-1].join('/')+'#idContenu';
			//console.log(location.href);
		}
	} 
		

	
	$('#dup-form_sco').on({
		click: function() {
			ajout_dernier_form($('#sco_forms'), 'sco');
		},
	});

	$('#add-form_sco').on({
		click: function() {
			cloner_ajouter($('#sco_forms'), $('#sco-empty_form'), 'sco');
		},
	});

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
			displayOnglet(ongleta, [ongletb, ongletc, ongletd, onglete]);
		},
	});

	ongletb[1].on({
		click: function() {
			displayOnglet(ongletb, [ongletc, ongletd, onglete, ongleta]);
		},
	});

	ongletc[1].on({
		click: function() {
			displayOnglet(ongletc, [ongletd, onglete, ongleta, ongletb]);
		},
	});

	ongletd[1].on({
		click: function() {
			displayOnglet(ongletd, [onglete, ongleta, ongletb, ongletc]);
		},
	});

	onglete[1].on({
		click: function() {
			displayOnglet(onglete, [ongleta, ongletb, ongletc, ongletd]);
		},
	});

	bande_coloree($('#infoDos'), $('#etatDos').text().trim());
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

function periode(champs, sous) {
	// body...
	var valeur = champs.val();
	var annnee1 = valeur.substr(0,4);
	var annnee2 = valeur.substr(7,4);
	annnee1 = parseInt(annnee1); 
	annnee2 = parseInt(annnee2);
	
	return ((annnee1 - sous)+' - '+(annnee2 - sous));
}

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
	clone.find('input, select, div').each(function() {
		// body...

		if ($(this).attr('id'))
		{
			var id_clone = new String($(this).attr('id'));
			id_clone = id_clone.replace('__prefix__', ''+(total)+'');
			$(this).attr('id', id_clone);
		}
		
		if ($(this).attr('name'))
		{
			var name_clone = new String($(this).attr('name'));
			name_clone = name_clone.replace('__prefix__', ''+(total)+'');
			$(this).attr('name', name_clone);
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
			}
		} 
	});
	forms.append(clone.html());
}

function recherche_input(forms)
{
	var $champs;
	$(forms).children('div:last').find('input').each(function() {
		if (String($(this).attr('name')).search('annee') != -1) 
			$champs = $(this);
	});
	return $champs;
}

function ajout_dernier_form(forms, prefix) {
	// body...
	augmenter_totals(prefix);
	var $dernier = dernier_form($(forms));
	var html = '<div classe="form-row">'+$dernier.html()+'</div>'
	alert(html);
	//$(forms).append(html);
}

function dernier_form(forms) {
	// body...
	return $(forms).children('div.form-row:last').clone(true);
}

function progression(barre, file)
{	
	$(barre).progressbar({
		value: 0,
	});

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/depot_rapport/upload_fichier/', true);
	xhr.setRequestHeader('X-CSRFToken', csrftoken);

	xhr.onprogress = function(e){
		var loaded = Math.round((e.loaded/e.total)*100);
		$(barre).progressbar('value', loaded);
	};

	xhr.onload = function(){
		$(barre).progressbar('value', 100);
	};

	var form = new FormData();
	form.append('filename', file.files[0].name);
	form.append('fichier', file.files[0]);

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

