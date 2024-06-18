import json
from lxml import etree
from google.colab import files

def add_namespace_to_xml(xml_file, namespace):
    with open(xml_file, 'r') as file:
        content = file.read()

    if 'xmlns:camel' not in content:
        content = content.replace('<camel:routeContext', f'<camel:routeContext xmlns:camel="{namespace}"')

    with open(xml_file, 'w') as file:
        file.write(content)

def get_namespaces(xml_file):
    """Extract all namespaces from the XML file."""
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
    # Define namespaces explicitly
    namespaces = {
        'camel': 'http://camel.apache.org/schema/spring'
    }
    print(f"Namespaces: {namespaces}")  # Debugging: print namespaces

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
            elif tag == 'choice':
                step['type'] = 'choice'
            elif tag == 'when':
                step['type'] = 'when'
            elif tag == 'doCatch':
                step['type'] = 'doCatch'
            elif tag == 'otherwise':
                step['type'] = 'otherwise'
            elif tag == 'strategyRef':
                step['type'] = 'strategyRef'
            elif tag == 'ref':
                step['type'] = 'ref'
            elif tag == 'simple':
                step['type'] = 'simple'
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
                mapped_step['type'] = 'filter'
                mapped_step['pattern'] = step['pattern']
            elif step['type'] == 'setHeader':
                mapped_step['type'] = 'setHeader'
                mapped_step['headerName'] = step['headerName']
                mapped_step['constant'] = step['constant']
            elif step['type'] == 'log':
                mapped_step['type'] = 'log'
                mapped_step['message'] = step['message']
                mapped_step['loggingLevel'] = step['loggingLevel']
            elif step['type'] == 'choice':
                mapped_step['type'] = 'if-else'
            elif step['type'] == 'when':
                mapped_step['type'] = 'if-else'
            elif step['type'] == 'doCatch':
                mapped_step['type'] = 'catch'
            elif step['type'] == 'strategyRef':
                mapped_step['type'] = 'strategyRef'
            elif step['type'] == 'ref':
                mapped_step['type'] = 'endpoint'
            elif step['type'] == 'simple':
                mapped_step['type'] = 'expression'
            elif step['type'] == 'otherwise':
                mapped_step['type'] = 'else'

            spring_boot_route['steps'].append(mapped_step)

        spring_boot_routes.append(spring_boot_route)

    return spring_boot_routes

def main():
    uploaded = files.upload()
    for filename in uploaded.keys():
        xml_file = filename
        add_namespace_to_xml(xml_file, 'http://camel.apache.org/schema/spring')

    routes = parse_camel_xml(xml_file)
    spring_boot_routes = map_to_spring_boot(routes)

    # Print the JSON representation of the Spring Boot routes
    print(json.dumps(spring_boot_routes, indent=4))

if __name__ == "__main__":
    main()
