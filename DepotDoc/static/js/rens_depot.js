
function Script() {
	// body...

	$('#id').on({
		click: displayID,
	});

	$('#formation').on({
		click: displayFormation,
	});

	$('#curriculum').on({
		click: displayCurriculum,
	});

	$('#piece').on({
		click: displayPiece,
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

function displayID() {
	// body...
	$('#idContenu').show().addClass('active');
	$('#id').addClass('active').css({'background-color': 'lightblue'});

	$('#formationContenu').hide().removeClass('active');
	$('#formation').removeClass('active').css({'background-color': 'white'});

	$('#curriculumContenu').hide().removeClass('active');
	$('#curriculum').removeClass('active').css({'background-color': 'white'});

	$('#pieceContenu').hide().removeClass('active');
	$('#piece').removeClass('active').css({'background-color': 'white'});
}

function displayFormation() {
	// body...
	$('#formationContenu').show().addClass('active');
	$('#formation').addClass('active').css({'background-color': 'lightblue'});

	$('#idContenu').hide().removeClass('active');
	$('#id').removeClass('active').css({'background-color': 'white'});

	$('#curriculumContenu').hide().removeClass('active');
	$('#curriculum').removeClass('active').css({'background-color': 'white'});

	$('#pieceContenu').hide().removeClass('active');
	$('#piece').removeClass('active').css({'background-color': 'white'});
}

function displayCurriculum() {
	// body...
	$('#curriculumContenu').show().addClass('active');
	$('#curriculum').addClass('active').css({'background-color': 'lightblue'});

	$('#idContenu').hide().removeClass('active');
	$('#id').removeClass('active').css({'background-color': 'white'});

	$('#formationContenu').hide().removeClass('active');
	$('#formation').removeClass('active').css({'background-color': 'white'});

	$('#pieceContenu').hide().removeClass('active');
	$('#piece').removeClass('active').css({'background-color': 'white'});
}

function displayPiece() {
	// body...
	$('#pieceContenu').show().addClass('active');
	$('#piece').addClass('active').css({'background-color': 'lightblue'});

	$('#formationContenu').hide().removeClass('active');
	$('#formation').removeClass('active').css({'background-color': 'white'});

	$('#idContenu').hide().removeClass('active');
	$('#id').removeClass('active').css({'background-color': 'white'});

	$('#curriculumContenu').hide().removeClass('active');
	$('#curriculum').removeClass('active').css({'background-color': 'white'});
}

$('document').ready(Script);