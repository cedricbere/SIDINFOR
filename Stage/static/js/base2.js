
function displayRightLinks() {
	// body...
	$('#lienRapport').on({
		click: displayLinkRapport,
	});

	$('#lienTelecharger').on({
		click: displayLinkTelecharger,
	});

	$('#lienInscription').on({
		click: displayLinkInscription,
	});

	$('#lienDossier').on({
		click: displayLinkDossier,
	});

	$('#lienContacts').on({
		click: displayLinkContacts,
	});

	/*$('#recherche').on({
		submit: recherche,
	});*/

	$('svg#profile').hover(iconeProfile1);
	$('svg#profile').mouseleave(iconeProfile2);

	/*$('svg#profile').on({
		hover: iconeProfile1,
		mouseleave: iconeProfile2,
	});*/

}

function iconeProfile1() {
	// body...
	$('svg#profile').attr({
		width: 8,
		height: 8,
	}).css({
		top: 0,
	});
	//var html = "<p> {{user.prenom|capfirst}} {{user.nom|capfirst}} </p>"
	//$('svg#profile').parent().after(html);
}

function iconeProfile2() {
	// body...
	$('svg#profile').attr({
		width: 15,
		height: 15,
	});
	//$('svg#profile').parent().next('p').remove();
}

function displayLinkRapport() {
	// body...
	$('#drapport').toggleClass('active');
	$('#lien1').toggleClass('active bd-sidenav-active');

	$('#telecharger').removeClass('active');
	$('#lien2').removeClass('active bd-sidenav-active');

	$('#inscription').removeClass('active');
	$('#lien3').removeClass('active bd-sidenav-active');

	$('#dossier').removeClass('active');
	$('#lien4').removeClass('active bd-sidenav-active');

	$('#contacts').removeClass('active');
	$('#lien5').removeClass('active bd-sidenav-active');
}

function displayLinkTelecharger() {
	// body...
	$('#telecharger').toggleClass('active');
	$('#lien2').toggleClass('active bd-sidenav-active');

	$('#drapport').removeClass('active');
	$('#lien1').removeClass('active bd-sidenav-active');

	$('#inscription').removeClass('active');
	$('#lien3').removeClass('active bd-sidenav-active');

	$('#dossier').removeClass('active');
	$('#lien4').removeClass('active bd-sidenav-active');

	$('#contacts').removeClass('active');
	$('#lien5').removeClass('active bd-sidenav-active');
}

function displayLinkInscription() {
	// body...
	$('#inscription').toggleClass('active');
	$('#lien3').toggleClass('active bd-sidenav-active');

	$('#drapport').removeClass('active');
	$('#lien1').removeClass('active bd-sidenav-active');

	$('#telecharger').removeClass('active');
	$('#lien2').removeClass('active bd-sidenav-active');

	$('#dossier').removeClass('active');
	$('#lien4').removeClass('active bd-sidenav-active');

	$('#contacts').removeClass('active');
	$('#lien5').removeClass('active bd-sidenav-active');
}

function displayLinkDossier() {
	// body...
	$('#dossier').toggleClass('active');
	$('#lien4').toggleClass('active bd-sidenav-active');

	$('#drapport').removeClass('active');
	$('#lien1').removeClass('active bd-sidenav-active');

	$('#inscription').removeClass('active');
	$('#lien3').removeClass('active bd-sidenav-active');

	$('#telecharger').removeClass('active');
	$('#lien2').removeClass('active bd-sidenav-active');

	$('#contacts').removeClass('active');
	$('#lien5').removeClass('active bd-sidenav-active');
}

function displayLinkContacts() {
	// body...
	$('#contacts').toggleClass('active');
	$('#lien5').toggleClass('active bd-sidenav-active');

	$('#drapport').removeClass('active');
	$('#lien1').removeClass('active bd-sidenav-active');

	$('#inscription').removeClass('active');
	$('#lien3').removeClass('active bd-sidenav-active');

	$('#dossier').removeClass('active');
	$('#lien4').removeClass('active bd-sidenav-active');

	$('#telecharger').removeClass('active');
	$('#lien2').removeClass('active bd-sidenav-active');
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