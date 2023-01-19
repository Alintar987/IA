from flask import Flask, request, render_template
#from subprocess import check_output
from GPT3 import generate_response
import re
from os import system as cmd

app = Flask(__name__)

commands = {
    'ip': 'ipconfig /all',
    'programas': 'tasklist'
    
}
#----------------------------------------------------------------------
@app.route('/')
def search():
    inicio = "Aca se mostrara el comando o la ultima respuesta de la IA"
    data = "Aca se muestra la conversacion con la IA"

    return render_template('index.html', result=inicio, data=data)

#---------------------------------------------------------------------
@app.route('/', methods=['POST'])
def do_search():
    search_text = request.form['search']

    if search_text in commands:
        result = commands[search_text] + ">output.txt"
        cmd(result)
        
        with open('output.txt', 'r') as file:
            out = file.read()
        
        out = re.sub(r"\n", "<br>", out)
        return render_template('index.html', result=out, data="El resultado es un comando.")
    
    else:
        with open("data.txt", "a") as archivo: 
            archivo.write(f"\n-USUARIO-\n{search_text}\n") 

        with open('data.txt', 'r') as file:
            data = file.read()

        result = generate_response(data)

        with open("data.txt", "a") as archivo: 
            archivo.write(f"-IA-{result}\n") 

        result = re.sub(r"\n", "<br>", result)

        with open('data.txt', 'r') as file:
            data = file.read()

        data = re.sub(r"\n", "<br>", data)

        return render_template('index.html', result=result, data=data)

#-----------------------------------------------------------
@app.route('/reset')
def reset():

    with open("data.txt", "w") as archivo: 
        archivo.write("antes tuvimos una conversacion donde -IA- eres tu y yo soy -USUARIO- en base a la conversacion puedes responder a la ultima parte de -USUARIO-\n") 

    return '.        Inteligencia Artificial reiniciada'

#----------------------------------------------------------
@app.route('/ver_chat')
def ver_chat():
    
    with open('data.txt', 'r') as file:
        data = file.read()

    data = re.sub(r"\n", "<br>", data)

    return render_template('index.html', result="Abajo se muestra el Chat", data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8554)
