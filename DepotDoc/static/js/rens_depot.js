
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
	colorerOnglet(onglet4);
	colorerOnglet(onglet5);

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
	arg.children('input').each(function(){
		if ($(this).val() == null)
		{
			return false;
		}
	return true;
});
}

function colorerOnglet(onglet) {
	// body...
	var bool = parcoursContenuOnglet(onglet[0]);
	if (bool)
		onglet[1].css({'background-color': 'green'});
	else
		onglet[1].css({'background-color': 'orange'});
}

$('document').ready(Script);

