import csv
import json
from time import strptime

def get(config):

    # Read in the CSV data:
    with open(config["csv_source"], "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Create starting data, including root UON info from config:
    py_data = {
        "areas": config["uon_data"],
        "depts": {},
        "persons": {},
        "alerts": []
    }

    # Take the data line by line:
    for d in data:
        if not (d["Area"] in py_data["areas"]):
            py_data["areas"][d["Area"]] = {
                "name": d["Area(T)"],
                "parent": config["uon_id"],
                "type": "faculty",
                "start_date": config["start_date"]
            }
        if not (d["Department"] in py_data["depts"]):
            py_data["depts"][d["Department"]] = {
                "name": d["Department(T)"],
                "parent": d["Area"],
                "type": "department",
                "start_date": config["start_date"]
            }
        # Flag to determine whether or not to include a staff member:
        process_staff = True
        if (d["ResID"] in py_data["persons"]):
            # If we have a duplicate staff entry, only process the data if
            # the "Main position" value is other than 0:
            if(d["Main position"] == "0"):
                process_staff = False
            # Log the duplicate in the alerts section of the data output:
            py_data["alerts"].append("Duplicate person entry: %(id)s (%(name)s)" % {
                "id": d["ResID"],
                "name": d["Known As"]
            })
        # Only process if data is wanted:
        if (process_staff):
            start_date = convert_date(d['Start Date'], config["start_date"])
            # Split known-as value into first / last names
            # As per the data supplied, the first name comes before the
            # first space, so maxsplit=1 puts the rest of the string into
            # the surname value:
            [aka_first, aka_last] = d["Known As"].split(" ", maxsplit=1)
            py_data["persons"][d["ResID"]] = {
                "first_name": d["First name"],
                "surname": d["Surname"],
                "known_as_first": aka_first,
                "known_as_last": aka_last,
                "email": d["E-mail"].lower(),
                "role": d["Position(T)"],
                "start_date": start_date,
                "area_code": d["Area"],
                "area": d["Area(T)"],
                "dept_code": d["Department"],
                "dept": d["Department(T)"],
                "fte": d["FTE"]
            }
    # Write JSON output of data for verification / checking
    with open(config["json_source"], 'w') as f:
        f.write(json.dumps(py_data, indent=4))

    # Return data as Python object:
    return(py_data)

def convert_date(date, default):
    # Convert UON format (31/01/2018) to Pure format (2018-01-31):
    date_parts = date.split("/")
    date_parts.reverse()
    new_date = "-".join(date_parts)
    # Also clamp any dates earlier than the default start date:
    if (strptime(new_date, "%Y-%m-%d") < strptime(default, "%Y-%m-%d")):
        return(default)
    else:
        return(new_date)