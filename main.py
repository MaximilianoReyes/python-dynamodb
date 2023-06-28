from uuid import uuid4
import boto3
from boto3.dynamodb.conditions import Key

#Llamar a la tabla
def get_db_table():
    dynamodb_resource = boto3.resource("dynamodb")

    return dynamodb_resource.Table("academia")

#Registrar cuentas
def register_account(user_email: str, user_name: str, user_address: str) -> dict:
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": "PROFILE#",
            "name": user_name,
            "address": user_address,
        }
    )

    return response

#Agregar una cuenta de invitado
def invite_account(user_email: str, invited_user_email: str, invited_user_name: str):
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": f"USER#{invited_user_email}",
            "name": invited_user_name,
        }
    )

    return response

#Registrar un elemento en el inventario
def register_inventory(user_email: str, inventory_name: str, inventory_price: int):
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": f"INVENTORY#{str(uuid4())}",
            "name": inventory_name,
            "price": inventory_price,
        }
    )

    return response

#Llamar los elementos del inventario de algun correo
def get_inventory(user_email: str):
    ddb_table = get_db_table()

    response = ddb_table.query(
        KeyConditionExpression=Key("PK").eq(user_email)
        & Key("SK").begins_with("INVENTORY#")
    )

    return response["Items"]

#Llmar los usuarios registrados mediante el correo principal
def get_invited_users(user_email: str):
    ddb_table = get_db_table()

    response = ddb_table.query(
        KeyConditionExpression=Key("PK").eq(user_email)
        & Key("SK").begins_with("USER#")
    )

    return response["Items"]

#Borrar elementos del inventario
def delete_inventory(user_email: str, inventory_id: str):
    ddb_table = get_db_table()

    response = ddb_table.delete_item(
        Key={
            "PK": user_email,
            "SK": f"INVENTORY#{inventory_id}",
        }
    )

    return response

#Actualizas los elementos del inventario
def update_inventory(
    user_email: str,
    inventory_id: str,
    new_inventory_name: str,
    new_inventory_price: int,
):
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": f"INVENTORY#{inventory_id}",
            "name": new_inventory_name,
            "price": new_inventory_price,
        }
    )

    return response

def delete_pk(user_email: str):
    ddb_table = get_db_table()

    response = ddb_table.query(
        KeyConditionExpression=Key("PK").eq(user_email)
    )
    
    items = response.get("Items", [])

    for item in items:
        ddb_table.delete_item(
            Key={
                "PK": item["PK"],
                "SK": item["SK"]
            }
        )
    
    return response

# print(register_account(
#     user_email="max@gmail.com",
#     user_name="maximiliano",
#     user_address="morelos 109"
# ))

# print(invite_account(
#     user_email="max@gmail.com",
#     invited_user_email="lorena@gmail.com",
#     invited_user_name="noemi"
# ))

# print(register_inventory(
#     user_email="max@gmail.com",
#     inventory_name="Cuchara",
#     inventory_price="20",
# ))

# print(get_inventory(
#     user_email="max@gmail.com"
# ))

# print(get_invited_users(
#     user_email="max@gmail.com"
# ))

# print(delete_inventory(
#     user_email="max@gmail.com",
#     inventory_id="9e8d0021-d021-4dc0-94f6-3383f70001e0"
# ))

# print(update_inventory(
#     user_email="max@gmail.com",
#     inventory_id="c8a4c939-e60f-4db3-b50f-dcf9b2e2a1ca",
#     new_inventory_name="Tenedor",
#     new_inventory_price=50,
# ))

# print(delete_pk (
#     user_email="emi@gmail.com"
# ))