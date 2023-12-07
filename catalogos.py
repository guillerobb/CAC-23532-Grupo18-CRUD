import mysql.connector
from flask import Flask, request, jsonify
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os
import time

app = Flask(__name__)
CORS(app) 

class Seleccionado:

    def __init__(self, host, user, password, database):

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.conector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS seleccionados (
            codigo INT,
            nombre VARCHAR(255) NOT NULL,
            bandera VARCHAR(255))''')
        self.conn.commit()

        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_seleccionado(self, codigo, nombre, bandera):
        self.cursor.execute(f"SELECT * FROM seleccionados WHERE codigo = {codigo}")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False
        sql = "INSERT INTO seleccionados(codigo, nombre, bandera) VALUES (%s, %s, %s)"
        valores = (codigo, nombre, bandera)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True


    def consultar_seleccionado(self, codigo):
        self.cursor.execute(f"SELECT * FROM seleccionados WHERE codigo = {codigo}")
        seleccion = self.cursor.fetchone()
        return seleccion

    def modificar_seleccionado(self, codigo, nuevo_nombre, nueva_bandera):
        sql = "UPDATE seleccionados SET nombre = %s, bandera=%s WHERE codigo = %s"
        valores = (nuevo_nombre, nueva_bandera, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def mostrar_seleccionado(self, codigo):
        seleccionado = self.consultar_seleccionado(codigo)
        if seleccionado:
            print("-"*40)
            print(f"Código...: {seleccionado['codigo']}")
            print(f"Nombre...: {seleccionado['nombre']}")
            print(f"Bandera..: {seleccionado['bandera']}")
            print("-"*40)
        else:
            print("Producto No Encontrado.")

    def listar_seleccionados(self):
        sql = f"SELECT * FROM seleccionados"
        self.cursor.execute(sql)
        seleccionados = self.cursor.fetchall()
        return seleccionados

    def eliminar_seleccionado(self, codigo):
        sql = f"DELETE FROM seleccionados WHERE codigo = {codigo}"
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.rowcount > 0

# Programa principal

#catalogo = Seleccionado(host='localhost', user='root', password='root', database='miapp')
catalogo = Seleccionado(host='guillermorobba.mysql.pythonanywhere-services.com', user='guillermorobba', password='Codo23532-Grupo18', database='guillermorobba$miapp')

#ruta_destino = 'static/img/'
ruta_destino = '/home/guillermorobba/mysite/static/img/'

@app.route("/seleccionados", methods=["GET"])
def listar_seleccionados():
    seleccionados = catalogo.listar_seleccionados()
    return jsonify(seleccionados)

@app.route("/seleccionados/<int:codigo>", methods=["GET"])
def mostrar_seleccionado(codigo):
    seleccionado = catalogo.consultar_seleccionado(codigo)
    if seleccionado:
        return jsonify(seleccionado)
    else:
        return "Seleccionado no encontrado", 404


@app.route("/seleccionados", methods=["POST"])
def agregar_seleccionado():
    print(request.form)
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    bandera = request.files['bandera']
    nombre_imagen_bandera = secure_filename(bandera.filename)

    nombre_base, extension = os.path.splitext(nombre_imagen_bandera)
    nombre_imagen_bandera = f"{nombre_base}_{int(time.time())}{extension}"
    bandera.save(os.path.join(ruta_destino, nombre_imagen_bandera))

    if catalogo.agregar_seleccionado(codigo, nombre, nombre_imagen_bandera):
        return jsonify({"mensaje":"Seleccionado agregado"}), 201
    else:
        return jsonify({"mensaje":"Seleccionado ya existe"}), 400


@app.route("/seleccionados/<int:codigo>", methods=["PUT"])
def modificar_producto(codigo):    
    print(request)
    nombre = request.form.get("nombre")
    bandera = request.files['bandera']
    nombre_imagen_bandera = secure_filename(bandera.filename)

    nombre_base, extension = os.path.splitext(nombre_imagen_bandera)
    nombre_imagen_bandera = f"{nombre_base}_{int(time.time())}{extension}"
    bandera.save(os.path.join(ruta_destino, nombre_imagen_bandera))

    if catalogo.modificar_seleccionado(codigo, nombre, nombre_imagen_bandera):
        return jsonify({"mensaje":"Producto modificado"}), 200
    else:
        return jsonify({"mensaje":"Producto no encontrado"}), 404
    
@app.route("/seleccionados/<int:codigo>", methods=["DELETE"])
def eliminar_seleccionado(codigo):
    seleccionado = catalogo.consultar_seleccionado(codigo)
    if seleccionado:
        ruta_imagen = os.path.join(ruta_destino, seleccionado['bandera'])
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        if catalogo.eliminar_seleccionado(codigo):
            return jsonify({"mensaje":"Producto Eliminado"}), 200
        else:
            return jsonify({"mensaje":"Error al intentar eliminar el producto"}), 500
    else:
        return jsonify({"mensaje":"Producto no encontrado"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
    #CORS(app, origins=["http://127.0.0.1:5501"])  