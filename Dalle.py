import openai
import requests

# Asigna tu API Key a la variable de entorno OPENAI_API_KEY
openai.api_key = ""

# Datos necesarios para crear la imagen
def create_image(prom, sice):

    # Genera la imagen usando openai.Image.create
    response = openai.Image.create(
      prompt=prom,
      n=1,
      size=sice #"1024x1024"
    )

    # Obtén la URL de la imagen generada
    image_url = response['data'][0]['url']

    # Descarga la imagen usando la URL
    response = requests.get(image_url)

    # Guarda la imagen en un archivo local
    with open("static/image.png", "wb") as f:
        f.write(response.content)

    print("Se guardo la imagen.")