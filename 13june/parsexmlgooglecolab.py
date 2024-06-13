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
            route_data['steps'].append(step)

        routes.append(route_data)

    return routes

def main():
    uploaded = files.upload()
    for filename in uploaded.keys():
        xml_file = filename
        add_namespace_to_xml(xml_file, 'http://camel.apache.org/schema/spring')

    routes = parse_camel_xml(xml_file)
    
    # Print the JSON representation of the routes
    print(json.dumps(routes, indent=4))

if __name__ == "__main__":
    main()
