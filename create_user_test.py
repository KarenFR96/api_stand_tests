import sender_stand_request
import data

# Función de prueba positiva
def positive_assert(first_name):
    # La versión actualizada del cuerpo de solicitud se guarda en la variable "user_body"
    user_body = sender_stand_request.get_user_body(first_name)
    # El resultado de la solicitud relevante se guarda en la variable "user_response"
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # ✅ Se verifica antes de acceder
    assert "authToken" in user_response.json()
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()
    # El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1

# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Prueba 2. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Función de prueba negativa
def negative_assert_symbol(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = sender_stand_request.get_user_body(first_name)

    # Comprueba si la variable "response" almacena el resultado de la solicitud.
    response = sender_stand_request.post_new_user(user_body)

    # Muestra la respuesta real antes de los asserts para depuración
    print("Mensaje real del servidor:", response.json().get("message"))

    # Comprueba si la respuesta contiene el código 400.
    assert response.status_code == 400

    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400.
    assert response.json()["code"] == 400
    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres."


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Prueba 8. Error
# La solicitud no contiene el parámetro "firstName"
def negative_assert_no_firstname(user_body):
    # Envía la solicitud sin "firstName"
    response = sender_stand_request.post_new_user(user_body)

    # Depuración: Imprimir la respuesta para ver qué devuelve la API
    print("Código de estado recibido:", response.status_code)
    print("Cuerpo de la respuesta:", response.json())

    # Esperamos que la API devuelva un error 400
    assert response.status_code == 400

    # Verificar si el mensaje de error es correcto
    expected_message = "No se han aprobado todos los parámetros requeridos"
    assert response.json().get("message") == expected_message

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")  # Elimina "firstName" de la solicitud
    negative_assert_no_firstname(user_body)  # Llama a la función corregida

# Prueba 9. Error
# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = sender_stand_request.get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = sender_stand_request.get_user_body(12)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)
    # Comprobar el código de estado de la respuesta
    assert response.status_code == 400