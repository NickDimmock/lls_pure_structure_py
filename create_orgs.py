import xml.dom.minidom as dom

def create(config, data):

    doc = dom.Document()

    orgs = doc.createElement("organisations")

    for ns, uri in config['org_namespaces'].items():
        orgs.setAttributeNS("", ns, uri)

    doc.appendChild(orgs)

    # Iterate through our organisational data set:
    for id, obj in data.items():

        org = doc.createElement("organisation")

        org_id = doc.createElement("organisationId")
        id_text = doc.createTextNode(id)
        org_id.appendChild(id_text)
        org.appendChild(org_id)

        org_type = doc.createElement("type")
        type_text = doc.createTextNode(obj["type"])
        org_type.appendChild(type_text)
        org.appendChild(org_type)

        name = doc.createElement("name")
        nameText = doc.createElement("v3:text")
        nameTextVal = doc.createTextNode(obj["name"])

        name.appendChild(nameText)
        nameText.appendChild(nameTextVal)
        org.appendChild(name)

        start_date = doc.createElement("startDate")
        start_date_text = doc.createTextNode(obj["start_date"])
        start_date.appendChild(start_date_text)
        org.appendChild(start_date)

        vis = doc.createElement("visibility")
        visText = doc.createTextNode("Public")
        vis.appendChild(visText)
        org.appendChild(vis)

        # UON won't have a parent, so we need to check before creating:
        if "parent" in obj:
            parent = doc.createElement("parentOrganisationId")
            parent_text = doc.createTextNode(obj["parent"])
            parent.appendChild(parent_text)
            org.appendChild(parent)

        orgs.appendChild(org)

    #root_xml.appendChild(orgs)

    with open(config["org_xml"], "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml())
