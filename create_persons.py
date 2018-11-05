import xml.dom.minidom as dom

def create(config, data):
    
    doc = dom.Document()

    persons = doc.createElement("persons")

    for ns, uri in config["persons_namespaces"].items():
        persons.setAttributeNS("", ns, uri)

    doc.appendChild(persons)
    
    for id, obj in data.items():
        
        person = doc.createElement("person")
        person.setAttribute("id", id)
        
        name = doc.createElement("name")
        first_name = doc.createElement("v3:firstname")
        first_name_text = doc.createTextNode(obj["first_name"])
        first_name.appendChild(first_name_text)
        last_name = doc.createElement("v3:lastname")
        last_name_text = doc.createTextNode(obj["surname"])
        last_name.appendChild(last_name_text)
        name.appendChild(first_name)
        name.appendChild(last_name)
        person.appendChild(name)

        names = doc.createElement("names")
        classifiedName = doc.createElement("classifiedName")
        classifiedName.setAttribute("id", "knownas-" + id)
        cnName = doc.createElement("name")
        cnFirst = doc.createElement("v3:firstname")
        cnLast = doc.createElement("v3:lastname")
        cnFirstText = doc.createTextNode(obj["known_as_first"])
        cnLastText = doc.createTextNode(obj["known_as_last"])
        cnFirst.appendChild(cnFirstText)
        cnLast.appendChild(cnLastText)
        cnName.appendChild(cnFirst)
        cnName.appendChild(cnLast)
        tc = doc.createElement("typeClassification")
        tc_text = doc.createTextNode("knownas")
        tc.appendChild(tc_text)
        classifiedName.appendChild(cnName)
        classifiedName.appendChild(tc)
        names.appendChild(classifiedName)
        person.appendChild(names)

        gender = doc.createElement("gender")
        genderText = doc.createTextNode("unknown")
        gender.appendChild(genderText)
        person.appendChild(gender)

        esd = doc.createElement("employeeStartDate")
        esdVal = doc.createTextNode(obj["start_date"])
        esd.appendChild(esdVal)
        person.appendChild(esd)

        # organisaionAssociations is a big job...

        # Turn start date into int for id use:
        start_date_int = obj["start_date"].replace("-","")

        oa = doc.createElement("organisationAssociations")

        soa_id = "-".join([id, obj["dept_code"], start_date_int])
        soa = doc.createElement("staffOrganisationAssociation")
        soa.setAttribute("id", soa_id)
        soa_emails = doc.createElement("emails")
        soa_ce = doc.createElement("v3:classifiedEmail")
        soa_ce_id = "-".join([id, obj["dept_code"], obj["email"]])
        soa_ce.setAttribute("id", soa_ce_id)
        soa_ce_class = doc.createElement("v3:classification")
        soa_ce_class_text = doc.createTextNode("email")
        soa_ce_class.appendChild(soa_ce_class_text)
        soa_ce_val = doc.createElement("v3:value")
        soa_ce_val_text = doc.createTextNode(obj["email"])
        soa_ce_val.appendChild(soa_ce_val_text)
        soa_ce.appendChild(soa_ce_class)
        soa_ce.appendChild(soa_ce_val)
        soa_emails.appendChild(soa_ce)
        soa.appendChild(soa_emails)

        primary = doc.createElement("primaryAssociation")
        primaryText = doc.createTextNode("true")
        primary.appendChild(primaryText)
        soa.appendChild(primary)

        org = doc.createElement("organisation")
        org_id = doc.createElement("v3:source_id")
        org_id_text = doc.createTextNode(obj["dept_code"])
        org_id.appendChild(org_id_text)
        org.appendChild(org_id)
        soa.appendChild(org)

        period = doc.createElement("period")
        p_start = doc.createElement("v3:startDate")
        p_start_text = doc.createTextNode(obj["start_date"])
        p_start.appendChild(p_start_text)
        period.appendChild(p_start)
        soa.appendChild(period)

        staff_type = doc.createElement("staffType")
        staff_type_text = doc.createTextNode("academic")
        staff_type.appendChild(staff_type_text)
        soa.appendChild(staff_type)

        job = doc.createElement("jobDescription")
        job_text = doc.createElement("v3:text")
        job_text_text = doc.createTextNode(obj["role"])
        job_text.appendChild(job_text_text)
        job.appendChild(job_text)
        soa.appendChild(job)

        fte = doc.createElement("fte")
        fte_text = doc.createTextNode(obj["fte"])
        fte.appendChild(fte_text)
        soa.appendChild(fte)

        oa.appendChild(soa)

        person.appendChild(oa)

        user = doc.createElement("user")
        user.setAttribute("id", "user-" + id)
        person.appendChild(user)

        person_ids = doc.createElement("personIds")
        person_ids_id = doc.createElement("v3:id")
        person_ids_id.setAttribute("id", id)
        person_ids_id.setAttribute("type", "employee")
        person_ids_id_text = doc.createTextNode("employee-" + id)
        person_ids_id.appendChild(person_ids_id_text)
        person_ids.appendChild(person_ids_id)
        person.appendChild(person_ids)

        persons.appendChild(person)
    
    with open(config["persons_xml"], "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml())