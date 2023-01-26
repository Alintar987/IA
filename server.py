from flask import Flask, request, render_template
from GPT3 import generate_response
import re
import os

app = Flask(__name__)

#----------------------------------------------------------------------
@app.route('/')
def search():
    inicio = """Bienvenido
<br>- La barra de busqueda sirve para introducir comandos.
<br>- si el comando no existe la peticion sera recibida por una Inteligencia Artificial en forma de pregunta. 
<br>- si sigue escribiendo se creara una conversacion donde la IA recordara todo lo anterior hablado.
<br>- Usa el boton de Reiniciar IA para empezar una conversacion nueva."""

    with open('chats/data.txt', 'r') as file:
        data = file.read()

    data = re.sub(r"\n", "<br>", data)

    data = re.sub(r"-IA-", '<strong style="color: cyan;">IA</strong>', data)
    data = re.sub(r"-USUARIO-", '<strong style="color: lightgreen;">USUARIO</strong>', data)


    return render_template('index.html', result=inicio, data=data)

#---------------------------------------------------------------------
@app.route('/', methods=['POST'])
def do_search():
    search_text = request.form['search']
#-------------------------------------------------------------------------------------------
    with open("chats/data.txt", "a") as archivo: 
        archivo.write(f"\n-USUARIO-\n{search_text}\n") 

    with open('chats/data.txt', 'r') as file:
        data = file.read()

    combinar = "antes tuvimos una conversacion donde -IA- eres tu y yo soy -USUARIO- en base a la conversacion puedes responder a la ultima parte de -USUARIO-\n"

    peticion = combinar + data

    result = generate_response(peticion)

    with open("chats/data.txt", "a") as archivo: 
        archivo.write(f"-IA-{result}\n") 

    result = re.sub(r"\n", "<br>", result)

    with open('chats/data.txt', 'r') as file:
        data = file.read()

    data = re.sub(r"\n", "<br>", data)
    data = re.sub(r"-IA-", '<strong style="color: cyan;">IA</strong>', data)
    data = re.sub(r"-USUARIO-", '<strong style="color: lightgreen;">USUARIO</strong>', data)

    return render_template('index.html', result=result, data=data)

#-----------------------------------------------------------
@app.route('/reset')
def reset():

    with open("chats/data.txt", "w") as archivo: 
        archivo.write("") 

    return render_template('info.html', result="El chat se reinicio ahora se iniciara una conversación nueva")

#----------------------------------------------------------
@app.route('/guardar')
def ver_chat():
    
    with open('chats/data.txt', 'r') as file:
        data = file.read()

    data = re.sub(r"\n", "<br>", data)

    data = re.sub(r"-IA-", '<strong style="color: cyan;">IA</strong>', data)
    data = re.sub(r"-USUARIO-", '<strong style="color: lightgreen;">USUARIO</strong>', data)

    return render_template('guardar.html', data=data)

#----------------------------------------------------------
@app.route('/guardar', methods=['POST'])
def guardar():
    text = request.form['search']

    with open('chats/data.txt', 'r') as file:
        out = file.read()

    with open(f"chats/{text}.txt", "w") as archivo: 
        archivo.write(out)

    return render_template('info.html', result=f'Se guardo la conversación <strong style="color: #FFFFFF;">{text}</strong>')

#----------------------------------------------------------
@app.route('/cargar', methods=['GET'])
def cargar():
    chats = []
    for filename in os.listdir('chats'):
        name, ext = os.path.splitext(filename) 
        with open(os.path.join('chats', filename)) as f:
            chat = f.read()

            chat = re.sub(r"\n", "<br>", chat)
            chat = re.sub(r"-IA-", '<strong style="color: cyan;">IA</strong>', chat)
            chat = re.sub(r"-USUARIO-", '<strong style="color: lightgreen;">USUARIO</strong>', chat)

            if filename == "data.txt":
                chats.append({'filename': "CHAT ACTUAL", 'content': chat})
            else:
                chats.append({'filename': name, 'content': chat})

    return render_template('cargar.html', chats=chats)

#----------------------------------------------------------
@app.route('/remplazar/<filename>', methods=['GET'])
def remplazar(filename):
    path = os.path.join('chats', filename)
    file_name, file_ext = os.path.splitext(path)
    path = f'{file_name}.txt'
    with open(path) as f:
        new_content = f.read()
    with open('chats/data.txt', 'w') as f:
        f.write(new_content)

    return render_template('info.html', result='Se Cargo correctamente la conversación')

#----------------------------------------------------------
@app.route('/eliminar/<filename>', methods=['POST'])
def eliminar(filename):
    if filename == "CHAT ACTUAL":
        boton = 'Para eliminar la conversacion Actual usa el boton  <button type="button" class="btn btn-danger" onclick="location.href='+"'/reset'"+';event.stopPropagation();">Eliminar Chat Actual</button> tambien puede usar el que esta en la pagina de inicio'
        return render_template('info.html', result=boton)
    
    else:
        os.remove(os.path.join('chats', filename + '.txt'))
        return render_template('info.html', result='Se Elimino correctamente la conversación')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8554, debug=True)
