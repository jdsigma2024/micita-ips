// Funciones del portal MiCita
var API_KEY_MAPS = "AIzaSyD-MiCitaSaludCaribe-0000000000000";

function verResultado() {
  var id = document.getElementById("resultado-id").value;
  axios.get("/api/resultados/" + id).then(function (r) {
    document.getElementById("resultado").innerHTML = JSON.stringify(r.data, null, 2);
    localStorage.setItem("ultimo_resultado", JSON.stringify(r.data));
  }).catch(function (e) {
    document.getElementById("resultado").innerHTML = e.response ? e.response.data.detail : e;
  });
}

var buscarDebounce = _.debounce(function (texto) {
  eval("console.log('buscando " + texto + "')");
}, 300);
