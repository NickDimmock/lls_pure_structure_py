import xml.etree.ElementTree as ET
import xml.dom.minidom

def create(config, data):
    
    #doc = dom.Document()

    persons = ET.Element("persons")


    for ns, uri in config["persons_namespaces"].items():
        persons.set(ns, uri)
    
    for id, obj in data.items():
        
        person = ET.SubElement(persons, "person")
        person.set("id", id)
        
        name = ET.SubElement(person, "name")
        first_name = ET.SubElement(name, "v3:firstname")
        first_name.text = obj["first_name"]
        last_name = ET.SubElement(name, "v3:lastname")
        last_name.text = obj["surname"]

        names = ET.SubElement(person, "names")
        classified_name = ET.SubElement(names, "classifiedName")
        classified_name.set("id", f"knownas-{id}")
        cn_name = ET.SubElement(classified_name, "name")
        cn_first = ET.SubElement(cn_name,"v3:firstname")
        cn_first.text =obj["known_as_first"]
        cn_last = ET.SubElement(cn_name,"v3:lastname")
        cn_last.text = obj["known_as_last"]

        tc = ET.SubElement(classified_name, "typeClassification")
        tc.text = "knownas"
        
        titles = ET.SubElement(person, "titles")
        title = ET.SubElement(titles, "title")
        title.set("id", f"title-{id}")
        title_type = ET.SubElement(title, "typeClassification")
        title_type.text = "designation"
        title_value = ET.SubElement(title, "value")
        title_value_text = ET.SubElement(title_value, "v3:text")
        title_value_text.set("lang", "en")
        title_value_text.set("country", "GB")
        title_value_text.text = obj["title"]

        gender = ET.SubElement(person, "gender")
        gender.text = "unknown"

        emp_start = ET.SubElement(person, "employeeStartDate")
        emp_start.text = obj["uni_start_date"]
        
        org_assoc = ET.SubElement(person, "organisationAssociations")
        soa_id = "-".join([id, obj["dept_code"], obj["div_start_date"]])
        soa = ET.SubElement(org_assoc, "staffOrganisationAssociation")
        soa.set("id", soa_id)
        
        soa_emails = ET.SubElement(soa, "emails")
        soa_email = ET.SubElement(soa_emails, "v3:classifiedEmail")
        soa_email_id = "-".join([id, obj["dept_code"], obj["email"]])
        soa_email.set("id", soa_email_id)
        soa_email_class = ET.SubElement(soa_email, "v3:classification")
        soa_email_class.text = "email"
        soa_email_val = ET.SubElement(soa_email, "v3:value")
        soa_email_val.text = obj["email"]

        primary = ET.SubElement(soa, "primaryAssociation")
        primary.text = "true"

        org = ET.SubElement(soa, "organisation")
        org_id = ET.SubElement(org, "v3:source_id")
        org_id.text = obj["dept_code"]

        period = ET.SubElement(soa, "period")
        p_start = ET.SubElement(period, "v3:startDate")
        p_start.text = obj["div_start_date"]

        staff_type = ET.SubElement(soa, "staffType")
        staff_type.text = "academic"

        job = ET.SubElement(soa, "jobDescription")
        job_text = ET.SubElement(job, "v3:text")
        job_text.text = obj["role"]

        fte = ET.SubElement(soa, "fte")
        fte.text = obj["fte"]

        user = ET.SubElement(person, "user")
        user.set("id", f"user-{id}")

        person_ids = ET.SubElement(person, "personIds")
        person_id = ET.SubElement(person_ids, "v3:id")
        person_id.set("id", id)
        person_id.set("type", "employee")
        person_id.text = f"employee-{id}"

    # Create XML string, then use minidom to generate a readable version
    xml_string = ET.tostring(persons, encoding="unicode")
    new_xml = xml.dom.minidom.parseString(xml_string)
    
    with open(config["persons_xml"], "w", encoding="utf-8") as f:
        f.write(new_xml.toprettyxml())
