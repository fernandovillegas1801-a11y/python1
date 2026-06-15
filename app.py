from flask import Flask, render_template, request, session
import random
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave-super-secreta"  # Necesaria para manejar sesiones

@app.route("/", methods=["GET", "POST"])
def index():
    # Si no existe número en sesión, lo crea
    if "numero" not in session:
        session["numero"] = random.randint(1, 100)
    if "veces" not in session:
        session["veces"] = 0

    mensaje = ""
    
    if request.method == "POST":
        try:
            intento = int(request.form["intento"])
            numero = session["numero"]
            veces_actual = int(session.get("veces", 0))
            veces_actual += 1
            session["veces"] = veces_actual

            if intento < numero:
                mensaje = "El número es MAYOR."
            elif intento > numero:
                mensaje = "El número es MENOR."
            else:
                nombre = request.args.get("nombre", "")
                mensaje = "¡Adivinaste! "+nombre+" lo lograste en " + str(session["veces"]) + " oportunidades. Se generó un nuevo número."
                
                session["numero"] = random.randint(1, 100)
                session["veces"] = 0
        
        except ValueError:
            mensaje = "Ingresa un número válido."

    return render_template("index.html", mensaje=mensaje)



@app.route("/guardar", methods=["POST"])
def guardar():

    nombre = request.form["nombre"]

    intentos = str(session["veces"])

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos = {
        "nombre": nombre,
        "intentos": intentos,
        "fecha_hora": fecha_hora
    }

    print(datos)

"""
    try:
        requests.post(
            "https://tudominio.com/api/guardar_resultado.php",
            json=datos
        )
    except Exception as e:
        print(e)

    # Reiniciar juego
    session["numero"] = random.randint(1, 100)
    session["veces"] = 0
    session.pop("gano", None)
    session.pop("intentos_finales", None)

    return render_template(
        "index.html",
        mensaje=f"Resultado guardado correctamente para {nombre}. Se ha generado un nuevo número."
    )



"""


   
