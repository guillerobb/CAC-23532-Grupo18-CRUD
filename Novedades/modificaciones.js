const URL = "http://127.0.0.1:5000/"
const app = Vue.createApp({
data() {
return {
codigo: '',
descripcion: '',
diario: '',
mostrarDatosNovedad: false,
};
},
methods: {
obtenerNovedad() {
fetch(URL + 'novedades/' + this.codigo)
.then(response => {
if (response.ok) {
    return response.json()
} else {
//Si la respuesta es un error, lanzamos una excepción para ser "catcheada" más adelante en el catch.

    throw new Error('Error al obtener los datos de la novedad')
}
    })
.then(data => {
this.descripcion = data.descripcion;
this.diario = data.diario;
this.mostrarDatosNovedad = true;
})
.catch(error => {
console.log(error);
alert('Código no encontrado.');
})
},

guardarCambios() {
const formData = new FormData();
formData.append('codigo', this.codigo);
formData.append('descripcion', this.descripcion);
formData.append('diario', this.diario);
//Utilizamos fetch para realizar una solicitud PUT a la API y guardar los cambios.
fetch(URL + 'novedades/' + this.codigo, {method: 'PUT',body: formData,})
.then(response => {
//Si la respuesta es exitosa, utilizamos response.json() para parsear la respuesta en formato JSON.
if (response.ok) {
return response.json()
} else {
//Si la respuesta es un error, lanzamos una excepción.

throw new Error('Error al guardar los cambios de la novedad')
}
})
.then(data => {
alert('Producto actualizado correctamente.');
this.limpiarFormulario();
})
.catch(error => {
console.error('Error:', error);
alert('Error al actualizar la novedad.');
});
},
limpiarFormulario() {
this.codigo = '';
this.descripcion = '';
this.diario = '';
this.mostrarDatosNovedad = false;
}
}
});
app.mount('#app');