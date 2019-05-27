function MarcarTodos() {
  for (var i = 0; i < document.formulario.elements.length; i++) {
    var x = document.formulario.elements[i];
    if (x.name == "selall") {
      x.checked = true;
    }
  }
}

cont = 0;

function CheckAll() {
  for (var i = 0; i < document.formulario.elements.length; i++) {
    var x = document.formulario.elements[i];
    if (x.name == "UIDL[]") {
      x.checked = document.formulario.selall.checked;
    }
  }
  if (cont == 0) {
    var elem = document.getElementById("checar");
    elem.innerHTML = "Desmarcar Todos";
    cont = 1;
  } else {
    var elem = document.getElementById("checar");
    elem.innerHTML = "Marcar Todos";
    cont = 0;
  }
}


function UmServidor(element){
  $(element).html(``).html(`
    <div class="row row1-formulario-posse ">
      <div class="col-lg-6">
        <div class="form-group mb-0">
          <label for="id-data-portaria" hidden><strong>Quantidade de servidores:</strong></label>
          <input type="number" class="form-control mb-3" name="qtde-servidores" id="id-qtde-servidores" 
          placeholder="Ex: 5" value="1" hidden>
        </div>
      </div>
    </div><!-- row1-formulario-posse primeira linha do formulário termo de posse -->  
  `)
}


function VariosServidores(element) {
  $(element).html(`
    <div class="row row1-formulario-posse ">
      <div class="col-lg-6">
        <div class="form-group mb-0">
          <label for="id-qtde-servidores"><strong>Quantidade de servidores:</strong></label>
          <input type="number" class="form-control mb-3" name="qtde-servidores" id="id-qtde-servidores" 
          min="2" placeholder="Ex: 2 ou mais" value="2">
        </div>
      </div>
    </div><!-- row1-formulario-posse primeira linha do formulário termo de posse -->   
  `);
}


function VariasSecretarias(element) {
  $(element).append(`
  `);
}

function exibirAdicionar() {}

function onFormUmServidorSelect() {
  $("[pmmc-termo-posse]").each((i, e) => new UmServidor(e));
}

function onFormVariosServidoresSelect() {
  $("[pmmc-termo-posse]").each((i, e) => new VariosServidores(e));
}

function onFormAdicionaServidor() {
  $("[pmmc-adiciona-servidor]").each((i, e) => new ComplementoVariosServidores(e));
}