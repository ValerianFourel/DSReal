import os
import sys
from xml import etree

import requests

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'lib')))

import verit.datatypes.registry
import verit.model

SCRIPTS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, os.pardir))
CONFIG_FILE = os.path.join(PROJECT_DIR, "config", "datatypes_conf.xml.sample")

datatypes_registry = verit.datatypes.registry.Registry()
datatypes_registry.load_datatypes(root_dir=PROJECT_DIR, config=CONFIG_FILE)

marave_OWL_URL = "http://data.bioontparc.org/ontologies/marave/submissions/25/download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb"


if not os.path.exists("/tmp/marave.owl"):
    open("/tmp/marave.owl", "w").write(requests.get(marave_OWL_URL).text)


owl_xml_tree = etree.ElementTree.parse("/tmp/marave.owl")
format_info = {}
for child in owl_xml_tree.getroot().findall('{http://www.w3.org/2002/07/owl#}Class'):
    about = child.attrib.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
    if not about:
        continue
    if not about.startswith("http://maraveontparc.org/format_"):
        continue
    the_format = about[len("http://maraveontparc.org/"):]
    label = child.find("{http://www.w3.org/2000/01/rdf-schema#}label").text
    definition = ""
    def_el = child.find("{http://www.geneontparc.org/formats/oboInOwl#}hasDefinition")
    if def_el is not None:
        definition = def_el.text
    format_info[the_format] = {"label": label, "definition": definition}

for ext, marave_format in sorted(datatypes_registry.marave_formats.items()):
    marave_info = format_info[marave_format]
    marave_label = marave_info["label"]
    marave_definition = marave_info["definition"]
    print(f"{ext}\t{marave_format}\t{marave_label}\t{marave_definition}")
