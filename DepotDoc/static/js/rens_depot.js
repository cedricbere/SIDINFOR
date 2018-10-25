
function Script() {
	// body...

	var onglet1 = new Array($('#idContenu'), $('#id'));
	var onglet2 = new Array($('#docContenu'), $('#doc'));
	var onglet3 = new Array($('#formationContenu'), $('#formation'));
	var onglet4 = new Array($('#curriculumContenu'), $('#curriculum'));
	var onglet5 = new Array($('#pieceContenu'), $('#piece'));

	colorerOnglet(onglet1);
	colorerOnglet(onglet2);
	colorerOnglet(onglet3);
	/*colorerOnglet(onglet4);
	colorerOnglet(onglet5);*/

	//parcours(onglet3[0]);

	onglet1[1].on({
		click: function() {
			displayOnglet(onglet1, [onglet2, onglet3, onglet4, onglet5]);},
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


	/*alert($('#etatDos').text() == "En attente du remplissage");

	if ($('#etatDos').text() == "En attente du remplissage") 
	{
		$('#infoDos').css({'background-color': 'lightgrey'});
	}
	else if ($('#etatDos').text() == "Encours de traitement")
	{
		$('#infoDos').css({'background-color': 'lightblue'});
	}
	else if ($('#etatDos').text() == "validé")
	{
		$('#infoDos').css({'background-color': 'green'});
	}
	else if ($('#etatDos').text() == "rejeté")
	{
		$('#infoDos').css({'background-color': 'red'});
	}*/
}


function displayOnglet(visible, invisible) {
	// body...
	visible[0].show().addClass('active');
	visible[1].addClass('active');

	for (var i = 0; i < invisible.length; i++) {
		invisible[i][0].hide().removeClass('active');
		invisible[i][1].removeClass('active');
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
		return false
}

/*
function parcours(arg) {
	// body...
	arg.find('input, select').not('input[type=hidden], input:submit').each(function(){
		if ($(this).val())
		{
			//console.log('il ya une valeur nulle');
			//return false;
			console.log($(this).val())
		}
});
}*/

function colorerOnglet(onglet) {
	// body...
	var bool = parcoursContenuOnglet(onglet[0]);
	if (bool)
		onglet[1].css({'background-color': '#adff2f'});
	else
		onglet[1].css({'background-color': '#ffd700'});
}

$('document').ready(Script);

