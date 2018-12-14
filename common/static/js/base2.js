
function displayRightLinks() {
	// body...

	var lien1 = [$('#drapport'), $('#lien1')];
	var lien2 = [$('#telecharger'), $('#lien2')];
	var lien3 = [$('#inscription'), $('#lien3')];
	var lien4 = [$('#dossier'), $('#lien4')];
	var lien5 = [$('#contacts'), $('#lien5')];

	$('#lienRapport').on({
		click: function(){
			display_links(lien1, [lien2, lien3, lien4, lien5]);
		},
	});

	$('#lienTelecharger').on({
		click: function(){
			display_links(lien2, [lien3, lien4, lien5, lien1]);
		},
	});

	$('#lienInscription').on({
		click: function(){
			display_links(lien3, [lien4, lien5, lien1, lien2]);
		},
	});

	$('#lienDossier').on({
		click: function(){
			display_links(lien4, [lien5, lien1, lien2, lien3]);
		},
	});

	$('#lienContacts').on({
		click: function(){
			display_links(lien5, [lien1, lien2, lien3, lien4]);
		},
	});

	/*$('#recherche').on({
		submit: recherche,
	});*/
}


function display_links(liens_affichés, liste_liens_cachés)
{
	$(liens_affichés[0]).toggleClass('active');
	//$(liens_affichés[1]).addClass('active bd-sidenav-active');
	for (var i = 0; i < liste_liens_cachés.length; i++) {
		if ($(liste_liens_cachés[i][0]).hasClass('active'))
		{
			$(liste_liens_cachés[i][0]).removeClass('active');
			//$(liste_liens_cachés[i][1]).removeClass('active bd-sidenav-active');
		}
	}
}


function recherche() {
	// body...
	var donnees = $('input[name=champ]').val();
	$.ajax({
		url: '../recherche',
		type: 'GET',
		dataType: 'html',
		data: ({'donnees': donnees,}),
		success: function (code_html, statut) {
			// body...
			alert(statut);
		},
		error: function(resultat, statut, erreur) {
			alert(erreur);
		},
		complete: function(resultat, statut) {
			//alert(statut);
		},
	});
}



$('document').ready(displayRightLinks);