import xml.etree.ElementTree as ET
import json

def get_namespaces(xml_file):
    """Extract all namespaces from the XML file."""
    events = "start", "start-ns"
    ns_map = {}

    try:
        for event, elem in ET.iterparse(xml_file, events):
            if event == "start-ns":
                ns, url = elem
                if ns:
                    ns_map[ns] = url
    except ET.ParseError as e:
        print(f"Error parsing namespaces: {e}")
        ns_map = {'': 'http://camel.apache.org/schema/spring'}  # Fallback to default namespace

    return ns_map

def parse_camel_xml(xml_file):
    namespaces = get_namespaces(xml_file)
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

    routes = []
    for route in root.findall('.//camel:route', namespaces):
        route_data = {
            'from': route.find('camel:from', namespaces).get('uri'),
            'steps': []
        }

        for elem in route:
            step = {}
            if elem.tag.endswith('from'):
                continue
            elif elem.tag.endswith('removeHeaders'):
                step['type'] = 'removeHeaders'
                step['pattern'] = elem.get('pattern')
            elif elem.tag.endswith('process'):
                step['type'] = 'process'
                step['ref'] = elem.get('ref')
            elif elem.tag.endswith('setHeader'):
                step['type'] = 'setHeader'
                step['headerName'] = elem.get('headerName')
                step['constant'] = elem.find('camel:constant', namespaces).text
            elif elem.tag.endswith('log'):
                step['type'] = 'log'
                step['message'] = elem.get('message')
                step['loggingLevel'] = elem.get('loggingLevel')
            elif elem.tag.endswith('to'):
                step['type'] = 'to'
                step['uri'] = elem.get('uri')
            elif elem.tag.endswith('unmarshal'):
                step['type'] = 'unmarshal'
                json_elem = elem.find('camel:json', namespaces)
                if json_elem is not None:
                    step['library'] = json_elem.get('library')
                    step['unmarshalTypeName'] = json_elem.get('unmarshalTypeName')
            
            route_data['steps'].append(step)

        routes.append(route_data)

    return routes

def main():
    xml_file = 'camel-routes.xml'
    routes = parse_camel_xml(xml_file)

    # Convert routes to JSON format
    json_data = json.dumps(routes, indent=2)
    
    # Print or save JSON data
    print(json_data)
    with open('camel-routes.json', 'w') as json_file:
        json.dump(routes, json_file, indent=2)

    print("JSON data has been generated in camel-routes.json")

if __name__ == "__main__":
    main()
