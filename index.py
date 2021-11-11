from flask import Flask, request
import json
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
 
#Crear objeto Flask
app = Flask(__name__)
 
#Cargar la informacion del archivo config.json
f = open("config.json", "r")
env = json.loads(f.read())
 
#Crear primer servicio web
@app.route('/test', methods=['GET'])
def test():
    return "hello world"

#Crear el API de mensajes
@app.route('/send_sms', methods=['POST'])
def send_sms():
    try:
        #Variables de configuración
        account_sid = env['TWILIO_ACCOUNT_SID']
        auth_token = env['TWILIO_AUTH_TOKEN']
        origen = env['TWILIO_PHONE_NUMBER']
        
        #Validar cuenta de twilio
        client = Client(account_sid, auth_token)
        
        #Capturar los datos de la solicitud
        data = request.json
        contenido = data["contenido"]
        destino = data["destino"]
       
       #Enviar mensaje
        message = client.messages.create(
                            body=contenido,
                            from_=origen,
                            to='+57' + destino
                        )
        print(message)
        return "send success"
    except Exception as e:
        print(e)
        return "error"

#Crear el API de correo
@app.route('/send_email', methods=['POST'])
def send_email():
    
    #Capturar los datos de la solicitud
    data = request.json
    contenido = data["contenido"]
    destino = data["destino"]
    asunto = data["asunto"]
    print(contenido, destino, asunto)
    
    #Crear mensaje a enviar
    message = Mail(
    from_email= env['SENDGRID_FROM_EMAIL'],
    to_emails= destino,
    subject= asunto,
    html_content= contenido)
    try:
        sg = SendGridAPIClient(env['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "send success"
    except Exception as e:
        print(e)
        return "error"
    

#Ejecutar el servidor
if __name__ == '__main__':
    app.run()