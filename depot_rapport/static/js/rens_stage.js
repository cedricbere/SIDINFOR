function displayRightForm() {
	// body...

	var onglet1 = new Array($('#stages'), $('#ongletStage'));
	var onglet2 = new Array($('#rapport'), $('#ongletRapport'));
	var onglet3 = new Array($('#soutenance'), $('#ongletSoutenance'));

	var url = window.location.href.split('/')
	var ancre = url[url.length-1]

	if (!ancre.localeCompare('#stages'))	displayOnglet(onglet1, [onglet2, onglet3]);
	else if (!ancre.localeCompare('#rapport')) displayOnglet(onglet2, [onglet3, onglet1]);
	else if (!ancre.localeCompare('#soutenance')) displayOnglet(onglet3, [onglet1, onglet2]);
	else displayOnglet(onglet1, [onglet2, onglet3]);

	colorerOnglet(onglet1);
	colorerOnglet(onglet2);
	colorerOnglet(onglet3);


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
	
/*
var barre_progression = $('#barre_progression')
$(barre_progression).progressbar({
	value: 0,
	change: function(){
		$('#pourcentage').text(($(barre_progression).progressbar('option', 'value')*100)/100+'%');
	},
});*/


/*
document.querySelector('#id_fichier_rapport').addEventListener('change', function(){
	$('#div_progress').removeClass('invisible');
	//rafraichir($(barre_progression));
	//progression($(barre_progression), this);
	
});*/


}

function rafraichir(barre){
	var progress = $(barre).progressbar('option', 'value');

	if(progress < 100){
		$(barre).progressbar('option', 'value', progress + 1);
		setTimeout(function(){
			rafraichir($(barre));
		}, 100);
	}
}


$(document).ready(displayRightForm);