//Selecionar e agrupar colunas via javascript
//https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Array


function agrupar(agrupa) {
   
    var ls_agrupa = [];
    for (let i = 0; i < agrupa.length; i++) {
        agrupa[i].addEventListener('change', function () {
            if (agrupa[i].checked) {
                agrupa[i].checked = true;

                console.log("check");
                ls_agrupa.push(agrupa[i].value)

            }
            else {
                agrupa[i].checked = false;
                let pos = ls_agrupa.indexOf(agrupa[i].value)
                console.log(pos);
                ls_agrupa.splice(pos, 1);
                console.log("uncheck");
            }
           
        });
    }
    return ls_agrupa;
}

function selecionarColunas() {
    var ls_col = [];
    const selcol = document.getElementsByClassName("coluna");
    for (let i = 0; i < selcol.length; i++) {
        selcol[i].addEventListener('change', function () {
            if (selcol[i].checked) {
                selcol[i].checked = true;

                // console.log("check");
                
                ls_col.push(selcol[i].value)
                $("#param"+selcol[i].value).attr('disabled',false)

               

            }
            else {
                selcol[i].checked = false;
                let pos = ls_col.indexOf(selcol[i].value)
                console.log(pos);
                ls_col.splice(pos, 1);
                $("#param"+selcol[i].value).attr('disabled',true)

                // console.log("uncheck");
            }
            // console.log(ls_col);
        });
    }

    return ls_col;
}
