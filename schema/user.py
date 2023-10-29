def individual_serial(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]

    }


def list_serial(users) -> list:
    return [individual_serial(user) for user in users]