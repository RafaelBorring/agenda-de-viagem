$(document).ready(function() {

	$(".vTextField").keyup(function() {
		this.value = this.value.toUpperCase();
	});
	$("#id_cns").mask("999 9999 9999 9999");

	$("#list_form").validate({
	    rules: {
			cns: {required: true},
			local: {required: true},
			car: {required: true},
			goal: {required: true},
			date: {required: true},
	    },
	    messages: {
			cns: {required: "Qual o número do cartão SUS?"},
			local: {required: "Qual o destino?"},
			car: {required: "Qual o veículo?"},
			goal: {required: "Qual a finalidade?"},
			date: {required: "Qual a data?"},
	    },
	  });

	$("#id_cns").blur(function () {

		function sleep_focus(id, time) {
			setTimeout(function () {
				$(id).focus();
			}, time);
		}

		var cns = $(this).val();
		var obj_cns = new Object();
		obj_cns.value = cns.replace(/ /g, "")
		var invalido = "Número de cartão inválido!"

		if (cns) {

			if (cns[0] == 7 || cns[0] == 8 || cns[0] == 9) {

				if (ValidaCNS_PROV(obj_cns) == false) {
					alert(invalido);
					$("#id_cns").val("");
					sleep_focus("#id_cns", 500);
				}

			} else if (cns[0] == 1 || cns[0] == 2) {

				if (validaCNS(cns.replace(/ /g, "")) == false) {
					alert(invalido);
					$("#id_cns").val("");
					sleep_focus("#id_cns", 500);
				 }

			} else {
				alert(invalido);
				$("#id_cns").val("");
				sleep_focus("#id_cns", 500);
			}

		}

		$("#id_name").attr("readonly", true);
        $("#id_address").attr("readonly", true);
        $("#id_telephone").attr("readonly", true);

		if (cns) {

            $.getJSON("/core/getcns/", {cns: cns}, function(data) {
                var teste = $.isEmptyObject(data);

								function myFunction() {
										var myWindow = window.open("/core/userregister/add/?cns="+ cns, "_self");
								}

                if (! teste) {
                    $("#id_name").val(JSON.stringify(data[0]["fields"]["name"]).replace(/\"/g, ""));
					$("#id_reference").val(JSON.stringify(data[0]["fields"]["reference"]).replace(/\"/g, ""));
                    $("#id_address").val(JSON.stringify(data[0]["fields"]["address"]).replace(/\"/g, ""));
                    $("#id_telephone").val(JSON.stringify(data[0]["fields"]["telephone"]).replace(/\"/g, ""));
                } else {

                    if (confirm("Usuário não cadastrado!\nDeseja realizar o cadastro?")) {
												myFunction()
                    } else {
                        $("#id_cns").val("");
                        $("#id_name").val("");
						$("#id_reference").val("");
                        $("#id_address").val("");
                        $("#id_telephone").val("");
                        sleep_focus("#id_cns", 500);
                    }

                }

            });

        }

	});

});
