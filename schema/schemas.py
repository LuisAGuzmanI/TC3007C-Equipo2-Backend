def individual_serial(item) -> dict:
    item["id"]: str(item,["_id"])
    item.pop("_id")
    keys = list(item.keys())
    return {key: item[key] for key in keys}

# def individual_serial(user) -> dict:
#     return {
#         "id": str(user["_id"]),
#         "name": user["name"],
#         "email": user["email"],
#     }

def list_serial(items) -> list:
    return (individual_serial(item) for item in items)