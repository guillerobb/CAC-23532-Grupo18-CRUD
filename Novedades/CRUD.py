import mysql.connector
#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import render_template
from flask import Flask,request, jsonify
from flask import request
#Instalar con pip install flask-cors
from flask_cors import CORS
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------

app = Flask(__name__)
CORS(app) # Esto habilitará CORS para todas las rutas
#-----------------------------------------------------------------------
class Catalogo:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
       # database=database
        )
        self.cursor = self.conn.cursor()#dictionary=True
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS novedades (
            codigo INT,
            descripcion VARCHAR(1000) NOT NULL,
            diario VARCHAR(255))''')
        self.conn.commit()
        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_novedad(self, codigo, descripcion, diario):
        self.cursor.execute(f"SELECT * FROM novedades WHERE codigo ={codigo}")
        novedad_existe = self.cursor.fetchone()
        if novedad_existe:
            return False
       # sql = f"INSERT INTO novedades (codigo, descripcion, diario) VALUES ({codigo}, '{descripcion}','{diario}')"
        sql = "INSERT INTO novedades (codigo, descripcion, diario) VALUES (%s, %s, %s)"
        valores = (codigo, descripcion, diario)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True
    
    def consultar_novedad(self, codigo):
        # Consultamos un novedad a partir de su código
        self.cursor.execute(f"SELECT * FROM novedades WHERE codigo = {codigo}")
        return self.cursor.fetchone()
    
    def modificar_novedad(self, codigo, nueva_descripcion,nuevo_diario):
        sql = "UPDATE novedades SET descripcion = %s, diario = %s WHERE codigo = %s" 
        valores = (nueva_descripcion, nuevo_diario, codigo)
        self.cursor.execute(sql,valores)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def mostrar_novedad(self, codigo):
        # Mostramos los datos de una novedad a partir de su código
        novedad = self.consultar_novedad(codigo)
        if novedad:
            print("-" * 40)
            print(f"Código.....: {novedad['codigo']}")
            print(f"Descripción: {novedad['descripcion']}")
            print(f"Diario.....: {novedad['diario']}")
            print("-" * 40)
        else:
            print("Novedad no encontrada.")
   # def mostrar_novedades(self):
        # Mostramos en pantalla un listado de todos los novedades en la tabla
    #    self.cursor.execute("SELECT * FROM novedades")
     #   novedades = self.cursor.fetchall()
     #   print("-" * 40)
      #  for novedad in novedades:
       #    print(f"Código.....: {novedad['codigo']}")
       #    print(f"Descripción: {novedad['descripcion']}")
       #    print(f"Diario.....: {novedad['diario']}")
       #    print("-" * 40)

    def listar_novedades(self):
        self.cursor.execute("SELECT * FROM novedades")
        novedades = self.cursor.fetchall()
        return novedades

    def eliminar_novedad(self, codigo):
        # Eliminamos un novedad de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM novedades WHERE codigo ={codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

#programa principal 

#catalogo = Catalogo(host='localhost', user='root', password='',database='miapp')
catalogo = Catalogo(host='guillermorobba.mysql.pythonanywhere-services.com', user='guillermorobba', password='Codo23532-Grupo18', database='guillermorobba$miapp')

# Carpeta para guardar las imagenes
ruta_destino = 'static/img/'

#@app.route('/novedades')
#def home():
 #   return render_template('prueba.html', title='Prueba Flask',heading='Bienvenidos a Flask!', items=['Item 1', 'Item 2', 'Item 3'])
#if __name__ == "__main__":
 #   app.run(debug=True)

@app.route("/novedades", methods=["GET"])
def listar_novedades():
    novedades = catalogo.listar_novedades()
    return jsonify(novedades)

@app.route("/novedades/<int:codigo>", methods=["GET"])
def mostrar_novedad(codigo):
    novedad = catalogo.consultar_novedad(codigo)
    if novedad:
        return jsonify(novedad)
    else:
        return "Novedad no encontrado", 404

@app.route("/novedades", methods=["POST"])
def agregar_novedad():
    # Recojo los datos del form
    codigo = request.form['codigo']
    descripcion = request.form['descripcion']
    diario = request.form['diario']
    if catalogo.agregar_novedad(codigo, descripcion, diario):
        return jsonify({"mensaje": "Novedad agregado"}), 201
    else:
        return jsonify({"mensaje": "Novedad ya existe"}), 400
    
@app.route("/novedades/<int:codigo>", methods=["PUT"])
def modificar_novedad(codigo):
    # Recojo los datos del form
    nueva_descripcion = request.form.get("descripcion")
    nuevo_diario = request.form.get("diario")
    # Actualización del novedad
    if catalogo.modificar_novedad(codigo, nueva_descripcion,nuevo_diario):
        return jsonify({"mensaje": "Novedad modificado"}), 200
    else:
        return jsonify({"mensaje": "Novedad no encontrado"}), 404

@app.route("/novedades/<int:codigo>", methods=["DELETE"])
def eliminar_novedad(codigo):
    # Primero, obtén la información del novedad para encontrar la imagen
    #novedad = catalogo.consultar_novedad(codigo)
    if catalogo.eliminar_novedad(codigo):
        return jsonify({"mensaje": "Novedad eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar la novedad"}),500


if __name__ == "__main__":
    app.run(debug=True)

