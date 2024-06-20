import json
from lxml import etree

def add_namespace_to_xml(xml_file, namespace):
    with open(xml_file, 'r') as file:
        content = file.read()

    if 'xmlns:camel' not in content:
        content = content.replace('<camel:routeContext', f'<camel:routeContext xmlns:camel="{namespace}"')

    with open(xml_file, 'w') as file:
        file.write(content)

def get_namespaces(xml_file):
    events = ("start", "start-ns")
    ns_map = {}

    try:
        for event, elem in etree.iterparse(xml_file, events):
            if event == "start-ns":
                ns, url = elem
                ns_map[ns] = url
    except etree.XMLSyntaxError as e:
        print(f"Error parsing namespaces: {e}")
        ns_map = {'': 'http://camel.apache.org/schema/spring'}  # Fallback to default namespace

    return ns_map

def parse_camel_xml(xml_file):
    namespaces = {
        'camel': 'http://camel.apache.org/schema/spring'
    }
    print(f"Namespaces: {namespaces}")

    try:
        tree = etree.parse(xml_file)
        root = tree.getroot()
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return []

    routes = []
    for route in root.findall('.//camel:route', namespaces=namespaces):
        route_data = {
            'from': route.find('camel:from', namespaces=namespaces).get('uri'),
            'steps': []
        }

        for elem in route:
            step = {}
            tag = etree.QName(elem).localname  # Remove namespace
            if tag == 'from':
                continue
            elif tag == 'removeHeaders':
                step['type'] = 'removeHeaders'
                step['pattern'] = elem.get('pattern')
            elif tag == 'process':
                step['type'] = 'process'
                step['ref'] = elem.get('ref')
            elif tag == 'setHeader':
                step['type'] = 'setHeader'
                step['headerName'] = elem.get('headerName')
                step['constant'] = elem.find('camel:constant', namespaces=namespaces).text
            elif tag == 'log':
                step['type'] = 'log'
                step['message'] = elem.get('message')
                step['loggingLevel'] = elem.get('loggingLevel')
            elif tag == 'to':
                step['type'] = 'to'
                step['uri'] = elem.get('uri')
            elif tag == 'unmarshal':
                step['type'] = 'unmarshal'
                json_elem = elem.find('camel:json', namespaces=namespaces)
                if json_elem is not None:
                    step['library'] = json_elem.get('library')
                    step['unmarshalTypeName'] = json_elem.get('unmarshalTypeName')
            route_data['steps'].append(step)

        routes.append(route_data)

    return routes

def map_to_spring_boot(routes):
    spring_boot_routes = []

    for route in routes:
        spring_boot_route = {
            'endpoint': route['from'],
            'steps': []
        }

        for step in route['steps']:
            mapped_step = {}

            if step['type'] == 'to':
                mapped_step['uri'] = step['uri']
            elif step['type'] == 'unmarshal':
                mapped_step['Jaxb2Marshaller'] = {
                    'library': step['library'],
                    'unmarshalTypeName': step['unmarshalTypeName']
                }
            elif step['type'] == 'process':
                mapped_step['annotations'] = ['@Autowired']
                mapped_step['customBean'] = step['ref']
            elif step['type'] == 'removeHeaders':
                mapped_step['type'] = 'removeHeaders'
                mapped_step['pattern'] = step['pattern']
            elif step['type'] == 'setHeader':
                mapped_step['type'] = 'setHeader'
                mapped_step['headerName'] = step['headerName']
                mapped_step['constant'] = step['constant']
            elif step['type'] == 'log':
                mapped_step['type'] = 'log'
                mapped_step['message'] = step['message']
                mapped_step['loggingLevel'] = step['loggingLevel']

            spring_boot_route['steps'].append(mapped_step)

        spring_boot_routes.append(spring_boot_route)

    return spring_boot_routes

def generate_spring_boot_code(routes):
    controller_template = """
package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import com.example.demo.service.EndpointInformationService;

@RestController
@RequestMapping("/api")
public class EndpointInformationController {

    @Autowired
    private EndpointInformationService endpointInformationService;

    @PostMapping("{endpoint}")
    public void processRequest(@PathVariable String endpoint) {
        endpointInformationService.process(endpoint);
    }
}
"""

    service_template = """
package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class EndpointInformationService {

    @Autowired
    public void process(String endpoint) {
        // Implement the logic to handle the route steps here
    }
}
"""

    with open('EndpointInformationController.java', 'w') as file:
        file.write(controller_template)

    with open('EndpointInformationService.java', 'w') as file:
        file.write(service_template)

def main():
    xml_file = input("Enter the path to your Camel XML file: ")
    add_namespace_to_xml(xml_file, 'http://camel.apache.org/schema/spring')

    routes = parse_camel_xml(xml_file)
    spring_boot_routes = map_to_spring_boot(routes)

    # Print the JSON representation of the Spring Boot routes
    print(json.dumps(spring_boot_routes, indent=4))

    # Generate Spring Boot code
    generate_spring_boot_code(spring_boot_routes)

if __name__ == "__main__":
    main()
