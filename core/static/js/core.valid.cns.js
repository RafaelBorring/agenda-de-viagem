// Rotina de validação de Números que iniciam com “1” ou “2”

// JavaScript Document
<!--
/*
	*Chamar a rotina em um evento do form. Exemplo:
		<input name="cns" type="text" title="cns" onChange="validaCNS(this.value)" value="cns" size="15" maxlength="15" />
*/

// Validação CNS
function validaCNS(vlrCNS) {
	// Formulário que contem o campo CNS
	var soma = new Number;
    var resto = new Number;
	var dv = new Number;
    var pis = new String;
    var resultado = new String;
	var tamCNS = vlrCNS.length;
	console.log(vlrCNS);
	if ((tamCNS) != 15) {
		return false;
	}
	pis = vlrCNS.substring(0,11);
	soma = (((Number(pis.substring(0,1))) * 15) +   
	        ((Number(pis.substring(1,2))) * 14) +
		    ((Number(pis.substring(2,3))) * 13) +
		    ((Number(pis.substring(3,4))) * 12) +
            ((Number(pis.substring(4,5))) * 11) +
            ((Number(pis.substring(5,6))) * 10) +
            ((Number(pis.substring(6,7))) * 9) +
            ((Number(pis.substring(7,8))) * 8) +
            ((Number(pis.substring(8,9))) * 7) +
            ((Number(pis.substring(9,10))) * 6) +
            ((Number(pis.substring(10,11))) * 5));
	resto = soma % 11;
    dv = 11 - resto;
	if (dv == 11) {
		dv = 0;
    }
	if (dv == 10) {
		soma = (((Number(pis.substring(0,1))) * 15) +   
	            ((Number(pis.substring(1,2))) * 14) +
		    	((Number(pis.substring(2,3))) * 13) +
		    	((Number(pis.substring(3,4))) * 12) +
            	((Number(pis.substring(4,5))) * 11) +
            	((Number(pis.substring(5,6))) * 10) +
            	((Number(pis.substring(6,7))) * 9) +
            	((Number(pis.substring(7,8))) * 8) +
            	((Number(pis.substring(8,9))) * 7) +
            	((Number(pis.substring(9,10))) * 6) +
            	((Number(pis.substring(10,11))) * 5) + 2);
		resto = soma % 11;
        dv = 11 - resto;
        resultado = pis + "001" + String(dv);
	} else { 
		resultado = pis + "000" + String(dv);
	}
	if (vlrCNS != resultado) {
      return false;
    } else {
       return true;
	}
}

// Rotina de validação de Números que iniciam com “7”, “8” ou “9”

function ValidaCNS_PROV(Obj)
{
    var pis;
    var resto;
    var dv;
    var soma;
    var resultado;
    var result;
    result = 0;

	pis = Obj.value.substring(0,15);

	if (pis == "")
	   {
	      return false
	   }
	    
	if ( (Obj.value.substring(0,1) != "7")  && (Obj.value.substring(0,1) != "8") && (Obj.value.substring(0,1) != "9") )
	   {
              return false
  	   }
 
 	soma = (   (parseInt(pis.substring( 0, 1),10)) * 15)
			+ ((parseInt(pis.substring( 1, 2),10)) * 14)
			+ ((parseInt(pis.substring( 2, 3),10)) * 13)
			+ ((parseInt(pis.substring( 3, 4),10)) * 12)
			+ ((parseInt(pis.substring( 4, 5),10)) * 11)
			+ ((parseInt(pis.substring( 5, 6),10)) * 10)
			+ ((parseInt(pis.substring( 6, 7),10)) * 9)
			+ ((parseInt(pis.substring( 7, 8),10)) * 8)
			+ ((parseInt(pis.substring( 8, 9),10)) * 7)
			+ ((parseInt(pis.substring( 9,10),10)) * 6)
			+ ((parseInt(pis.substring(10,11),10)) * 5)
			+ ((parseInt(pis.substring(11,12),10)) * 4)
			+ ((parseInt(pis.substring(12,13),10)) * 3)
			+ ((parseInt(pis.substring(13,14),10)) * 2)
			+ ((parseInt(pis.substring(14,15),10)) * 1);

	resto = soma % 11;
	
	if (resto == 0)
	   {
	     return true;
	   }
	else
	   {
         return false;  
	   }   
}
