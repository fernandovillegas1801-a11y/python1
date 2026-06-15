from flask import Flask, render_template, request, session
import random
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

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
    gane = False
        
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
                mensaje = "¡Adivinaste! Registra tu puntuación."
                gane = True
                
                session["numero"] = random.randint(1, 100)
                session["puntaje"] = session["veces"]
                session["veces"] = 0
        
        except ValueError:
            mensaje = "Ingresa un número válido."

    return render_template(
        "index.html",
        mensaje=mensaje,
        pedir_nombre=gane
    )


@app.route("/guardar", methods=["POST"])
def guardar():

    nombre = request.form["nombre"]

    intentos = session.get("puntaje", 0)

    fecha_hora = datetime.now(ZoneInfo("America/Bogota")).strftime("%Y-%m-%d %H:%M:%S")

    datos = {
        "nombre": nombre,
        "intentos": intentos,
        "fecha_hora": fecha_hora
    }

    print(datos)


    try:
        response = requests.post(
            "https://php1-production-46c4.up.railway.app/index.php",
            json=datos,
            timeout=30
        )
    
        print("Status:", response.status_code)
        print("Respuesta:", response.text)

    except Exception as e:
        print("Error:", str(e))
    
        # Reiniciar juego
        session["numero"] = random.randint(1, 100)
        session["veces"] = 0
        session.pop("gano", None)
        session.pop("intentos_finales", None)


    
    return render_template(
        "index.html",
        mensaje="Resultado guardado correctamente",
        pedir_nombre=False
    )


   





"""
    return render_template(
        "index.html",
        mensaje=f"Resultado guardado correctamente para {nombre}. Se ha generado un nuevo número."
    )
"""
  
