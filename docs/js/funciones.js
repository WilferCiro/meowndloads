$(document).ready(function(){
	esconder_secciones();
	$('.mostrar_dialogo').click(muestra_actual);
});

function esconder_secciones(){
	for (var i = 0; i<=2; i++){
		$('#muestra_dialogo_'+i).hide();
	}
}

function muestra_actual(){
	esconder_secciones();
	var id = $(this).attr('dialogo');
	$('#muestra_dialogo_'+id).show();	
}
