# ---  INDICAMOS ACA EL FORMATO QUE DEBE TENER EL OBJETO SOLICITADO ---

def user_model(user) -> dict:
    return {"id": str(user["_id"]),
            "name": user["name"],
            "surname": user["surname"],
            "age": user["age"],
            "url": user["url"]
            }