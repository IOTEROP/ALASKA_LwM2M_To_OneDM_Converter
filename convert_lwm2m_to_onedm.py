#!/usr/bin/env python
#
# Copyright (c) IoTerop.
# All rights reserved.
#

import argparse
import collections
import json
import os
import urllib.parse
import urllib.request

import xmltodict

OMA_REGISTRY_URL = "http://www.openmobilealliance.org/api"


def uniformize_name(name):
    name = name.replace(" ", "_")  # Replace the whitespace
    name = name.replace("/", "")  # Remove '/'
    name = name.replace("(", "")  # Remove '('
    name = name.replace(")", "")  # Remove ')'

    return name


def get_lwm2m_object_metadata(object_id):
    # Generate the URL
    queries = urllib.parse.urlencode({"ObjectID": object_id, "ObjectVersion": "1.0"})
    url = "{:s}/lwm2m/v1/Object?{:s}".format(OMA_REGISTRY_URL, queries)

    url_request = urllib.request.Request(url)
    url_request.add_header("User-Agent", "curl/7.76.1")  # To mimic a curl request

    with urllib.request.urlopen(url_request) as url_reader:
        response = json.loads(url_reader.read().decode("utf-8"))

        if response is None or len(response) == 0:
            print("No definition was received from the registry")
            return None

        first_definition = response[0]
        if "ObjectLink" not in first_definition:
            print("No object definition provided for the object")
            return None

        return first_definition["ObjectLink"]


def get_lwm2m_object_definition(object_id):
    xml_object_url = get_lwm2m_object_metadata(object_id)
    if xml_object_url is None:
        print("No object metadata has been retrieved")
        return None

    url_request = urllib.request.Request(xml_object_url)
    url_request.add_header("User-Agent", "curl/7.76.1")  # To mimic a curl request

    with urllib.request.urlopen(url_request) as url_reader:
        response = url_reader.read().decode("utf-8")

        json_response = xmltodict.parse(response)
        if "LWM2M" not in json_response and "Object" not in json_response["LWM2M"]:
            print("Received response is not valid")
            return None

        return json_response["LWM2M"]["Object"]


def print_output(json_content, filename=None):
    if filename is not None:
        with open(filename, "w") as f:
            content = json.dumps(json_content, indent=2)
            f.write(content)

        print("The JSON has been saved under the name: {:s}".format(filename))
    else:
        content = json.dumps(json_content, separators=(",", ":"), indent=2)

        print(content)


def convert_lwm2m_object_to_onedm(lwm2m_object_id, number_of_instance):
    lwm2m_object_definition = get_lwm2m_object_definition(lwm2m_object_id)

    if "Name" not in lwm2m_object_definition \
            or "Resources" not in lwm2m_object_definition \
            or "Item" not in lwm2m_object_definition["Resources"]:
        print("Received object definition is not valid")
        return None

    things = []

    for object_instance_id in range(number_of_instance):
        thing_identifier = uniformize_name(lwm2m_object_definition["Name"])
        thing_properties = []
        thing_actions = []

        if object_instance_id > 0:
            # Add a number for each new instance at the end of the name
            thing_identifier = "{:s}_{:d}".format(thing_identifier, object_instance_id + 1)

        for resource in lwm2m_object_definition["Resources"]["Item"]:
            if "@ID" not in resource \
                    or "Name" not in resource \
                    or "Operations" not in resource:
                print("Object resource definition is not valid")
                continue

            resource_id = int(resource["@ID"])
            resource_name = uniformize_name(resource["Name"])
            resource_operations = resource["Operations"]

            resource = {
                "id": resource_name,
                "name": resource_name,
                "mapping": {
                    "protocol": "LWM2M",
                    "protocolPath": "/{:d}/{:d}/{:d}".format(lwm2m_object_id, object_instance_id, resource_id)
                }
            }

            if "E" in resource_operations:
                resource["mapping"]["operation"] = "LWM2M_EXECUTE"
                resource["mapping"]["defaultValue"] = ""

                for thing_action in thing_actions:
                    if thing_action["name"] == resource["name"]:
                        # Append 'Bis' since the name of this resource is already in used
                        resource["name"] = "{:s}_Bis".format(resource["name"])
                        break

                thing_actions.append(resource)
            else:
                for thing_property in thing_properties:
                    if thing_property["name"] == resource["name"]:
                        # Append 'Bis' since the name of this resource is already in used
                        resource["name"] = "{:s}_Bis".format(resource["name"])
                        break

                thing_properties.append(resource)

        things.append({
            "id": thing_identifier,
            "name": thing_identifier,
            "properties": thing_properties,
            "actions": thing_actions
        })

    return things


def get_output(base_file, onedm_thing):
    if base_file is None:
        return onedm_thing

    if not os.path.isfile(base_file):
        print("Base file does not exist")
        return None

    with open(base_file, "r") as f:
        content = f.read()
        json_content = json.loads(content)

        if not isinstance(json_content, dict):
            print("Bad JSON content file")
            return None

        if "templates" not in json_content \
           or len(json_content["templates"]) != 1:
            print("'.templates' is not present or badly formatted")
            return None

        template = json_content["templates"][0]
        if not isinstance(template, dict):
            print("'.templates[0]' is badly formatted")
            return None

        if "mappings" not in template \
           or not isinstance(template["mappings"], dict):
            print("'.templates[0].mappings' is badly formatted")
            return None

        if "things" not in template["mappings"] \
           or not isinstance(template["mappings"]["things"], list) \
           or len(template["mappings"]["things"]) != 0:
            print("'.templates[0].mappings.things' is not present or badly formatted")
            return None

        template["mappings"]["things"].append(onedm_thing)

        return json_content


def convert_lwm2m_objects(lwm2m_objects, base_file, output_file):
    onedm_definitions = []
    lwm2m_objects_counter = collections.Counter(lwm2m_objects)
    for lwm2m_object_id in lwm2m_objects_counter.keys():
        lwm2m_object_definition = convert_lwm2m_object_to_onedm(lwm2m_object_id, lwm2m_objects_counter[lwm2m_object_id])

        # Add the new objects
        onedm_definitions = onedm_definitions + lwm2m_object_definition

    onedm_lwm2m_thing = {
        "id": "DeviceMapping",
        "name": "LwM2M Objects",
        "things": onedm_definitions
    }

    output = get_output(base_file, onedm_lwm2m_thing)
    if output is None:
        print("Cannot generate the output")
        return

    print_output(output, filename=output_file)


if __name__ == "__main__":
    # Initialize the arguments parser
    parser = argparse.ArgumentParser(description="Alaska LwM2M Objects to OneDM Objects converter")
    parser.add_argument("-i", "--id", nargs="+", help="Identifiers of the LwM2M objects", type=int, required=True)
    parser.add_argument("-b", "--base", help="Base file", type=str)
    parser.add_argument("-o", "--output", help="Output file", type=str)
    args = parser.parse_args()

    convert_lwm2m_objects(args.id, args.base, args.output)
