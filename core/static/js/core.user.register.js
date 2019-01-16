$(document).ready(function() {

	$(".vTextField").keyup(function() {
		this.value = this.value.toUpperCase();
	 });
	$("#id_cns").mask("999 9999 9999 9999");
	$("#id_birth").mask("99/99/9999");
	$("#id_telephone").mask("(99) ?99999-9999");
	$("#id_telephone").on("blur", function() {
	    var last = $(this).val().substr($(this).val().indexOf("-") + 1);

	    if (last.length == 3) {
	        var move = $(this).val().substr($(this).val().indexOf("-") - 1, 1);
	        var lastfour = move + last;
	        var first = $(this).val().substr(0, 9);
	        $(this).val(first + "-" + lastfour);
	    }

	 });

	$.validator.addMethod("data",

		    function(value, element) {
		        return value.match(/^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/]\d{4}$/);
		    }),

	$("#userregister_form").validate({
	    rules: {
	      cns: {required: true},
	      name: {required: true},
	      reference: {required: true},
	      birth: {required: true, data: true},
	      sex: {required: true},
	      address: {required: true},
	      telephone: {required: true},
	    },
	    messages: {
	      cns: {required: "Qual o número do cartão SUS?"},
	      name: {required: "Qual o nome?"},
	      reference: {required: "Qual a referência?"},
	      birth: {
	          required: "Qual a data de nascimento?",
	          data: "Informe uma data válida!",
	      },
	      sex: {required: "Qual o sexo?"},
	      address: {required: "Qual o endereço?"},
	      telephone: {required: "Qual o número do telefone?"},
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

		if (cns) {

            $.getJSON("/core/getcns/", {cns: cns}, function(data) {
                var test = $.isEmptyObject(data);

                if (! test) {

                    if (confirm("Usuário já cadastrado!\nDeseja atualizar o cadastro?")) {
                        window.open("/core/userregister/" + JSON.stringify(data[0]["pk"]).replace(/\"/g, "") + "/change/", "_self");
                    } else {
                        $("#id_cns").val("");
                        sleep_focus("#id_cns", 500);
                    }

                }

            });

	    }

	});

});
