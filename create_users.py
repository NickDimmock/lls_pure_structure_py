import xml.dom.minidom as dom

def create(config, data):
    
    user_doc = dom.Document()

    users = user_doc.createElement("users")

    for ns, uri in config["users_namespaces"].items():
        users.setAttributeNS("", ns, uri)

    user_doc.appendChild(users)
    
    for id, obj in data.items():

        user = user_doc.createElement("user")
        user.setAttribute("id", f"user-{id}")

        user_username = user_doc.createElement("userName")
        user_username_val = user_doc.createTextNode(id)
        user_username.appendChild(user_username_val)
        user.appendChild(user_username)
        
        user_email = user_doc.createElement("email")
        user_email_val = user_doc.createTextNode(obj["email"])
        user_email.appendChild(user_email_val)
        user.appendChild(user_email)

        user_name = user_doc.createElement("name")
        user_name_first = user_doc.createElement("v3:firstname")
        user_name_last = user_doc.createElement("v3:lastname")
        user_name_first_val = user_doc.createTextNode(obj["first_name"])
        user_name_last_val = user_doc.createTextNode(obj["surname"])
        user_name_first.appendChild(user_name_first_val)
        user_name_last.appendChild(user_name_last_val)
        user_name.appendChild(user_name_first)
        user_name.appendChild(user_name_last)
        user.appendChild(user_name)

        users.appendChild(user)

    # Users file needs declaration attributes we can't set using minidom.
    # (standalone = "yes")
    # So we'll just write the header out manually and then add the users data.
    with open(config["users_xml"], "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        f.write(users.toprettyxml())
    