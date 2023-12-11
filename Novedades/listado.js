const URL = "http://127.0.0.1:5000/"
// Realizamos la solicitud GET al servidor para obtener todos los

fetch(URL + 'novedades')
.then(function (response) {
if (response.ok) {
    return response.json();
} else {
// Si hubo un error, lanzar explícitamente una excepción
// para ser "catcheada" más adelante
throw new Error('Error al obtener las novedades.');
}
})
.then(function (data) {
let tablaNovedades = document.getElementById('tablaNovedades');
// Iteramos sobre los productos y agregamos filas a la tabla
for (let novedad of data) {
let fila = document.createElement('tr');
fila.innerHTML = '<td>' + novedad.codigo + '</td>' +
'<td>' + novedad.descripcion + '</td>' +
'<td align="right">' + novedad.diario +'</td>';


tablaNovedades.appendChild(fila);
}
})
.catch(function (error) {
// En caso de error
alert('Error al agregar la novedad.');
console.error('Error:', error);
})