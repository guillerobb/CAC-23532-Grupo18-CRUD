const URL = "http://127.0.0.1:5000/"
// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function(event) {
event.preventDefault(); // Evitamos que se envie el form
var formData = new FormData();
formData.append('codigo', document.getElementById('codigo').value);
formData.append('descripcion',document.getElementById('descripcion').value);
formData.append('diario',document.getElementById('diario').value);
// Realizamos la solicitud POST al servidor
fetch(URL + 'novedades', {method: 'POST',body: formData // Aquí enviamos formData en lugar de JSON
})
//Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.
.then(function (response) {
if (response.ok) {
return response.json();
} else {
// Si hubo un error, lanzar explícitamente una excepción
// para ser "catcheada" más adelante
throw new Error('Error al agregar la novedad.');
}
})
// Respuesta OK
.then(function () {
    // En caso de éxito
    alert('Novedad agregado correctamente.');
    })
    .catch(function (error) {
    // En caso de error
    alert('Error al agregar el novedad.');
    console.error('Error:', error);
    })
    .finally(function () {
    // Limpiar el formulario en ambos casos (éxito o error)
    document.getElementById('codigo').value = "";
    document.getElementById('descripcion').value = "";
    document.getElementById('diario').value = "";
    });
    })