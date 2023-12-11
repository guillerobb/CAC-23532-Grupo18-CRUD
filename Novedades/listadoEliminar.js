const URL = "http://127.0.0.1:5000/"
const app = Vue.createApp({
data() {
return {
novedades: []
}
},
methods: {
obtenerNovedades() {// Obtenemos el contenido del inventario
fetch(URL + 'novedades')
.then(response => {
// Parseamos la respuesta JSON
if (response.ok) { return response.json(); }
})
.then(data => {
// El código Vue itera este elemento para generar la tabla
this.novedades = data;
})
.catch(error => {
console.log('Error:', error);


alert('Error al obtener las novedades.');
});
},
eliminarNovedad(codigo) {
if (confirm('¿Estás seguro de que quieres eliminar esta novedad?')) {fetch(URL + `novedades/${codigo}`, { method: 'DELETE' })
.then(response => {if (response.ok) {
this.novedades =this.novedades.filter(novedad => novedad.codigo !== codigo);
alert('Novedad eliminada correctamente.');
}
})
.catch(error => {
alert(error.message);
});
}
}
},
mounted() {
//Al cargar la página, obtenemos la lista de novedad
this.obtenerNovedades();
}
});
app.mount('body');