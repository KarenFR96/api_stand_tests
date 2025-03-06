import configuration
import requests
import data


# ✅ Función para generar dinámicamente el cuerpo de la solicitud con un nombre personalizado
def get_user_body(first_name):
    current_body = data.user_body.copy()  # Se copia el diccionario original
    current_body["firstName"] = first_name  # Se cambia el nombre
    return current_body

#Función para genera la solicitud de recepción de datos de la tabla "user_model"
def get_users_table():
    url = configuration.URL_SERVICE + configuration.USERS_TABLE_PATH
    return requests.get(url, headers=data.headers)


# Función para enviar una solicitud POST y crear un usuario
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # inserta la dirección URL completa
                         json=body,  # inserta el cuerpo de solicitud
                         headers=data.headers)  # inserta los encabezados

response = post_new_user(data.user_body)
print(response.status_code)



