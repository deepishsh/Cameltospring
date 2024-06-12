import xml.etree.ElementTree as ET

NAMESPACE = {'camel': 'http://camel.apache.org/schema/spring'}

def parse_camel_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    routes = []
    for route in root.findall('.//camel:route', NAMESPACE):
        route_data = {
            'from': route.find('camel:from', NAMESPACE).get('uri'),
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
                step['constant'] = elem.find('camel:constant', NAMESPACE).text
            elif elem.tag.endswith('log'):
                step['type'] = 'log'
                step['message'] = elem.get('message')
                step['loggingLevel'] = elem.get('loggingLevel')
            elif elem.tag.endswith('to'):
                step['type'] = 'to'
                step['uri'] = elem.get('uri')
            elif elem.tag.endswith('unmarshal'):
                step['type'] = 'unmarshal'
                json_elem = elem.find('camel:json', NAMESPACE)
                if json_elem is not None:
                    step['library'] = json_elem.get('library')
                    step['unmarshalTypeName'] = json_elem.get('unmarshalTypeName')
            route_data['steps'].append(step)
        
        routes.append(route_data)
    
    return routes

def generate_java_dsl(routes):
    java_code = "import org.apache.camel.builder.RouteBuilder;\n"
    java_code += "import org.apache.camel.model.dataformat.JsonLibrary;\n"
    java_code += "import org.springframework.stereotype.Component;\n\n"
    java_code += "@Component\n"
    java_code += "public class CamelRoutes extends RouteBuilder {\n\n"
    java_code += "    @Override\n"
    java_code += "    public void configure() throws Exception {\n"

    for route in routes:
        java_code += f"        from(\"{route['from']}\")\n"
        
        for step in route['steps']:
            if step['type'] == 'removeHeaders':
                java_code += f"            .removeHeaders(\"{step['pattern']}\")\n"
            elif step['type'] == 'process':
                java_code += f"            .process(\"{step['ref']}\")\n"
            elif step['type'] == 'setHeader':
                java_code += f"            .setHeader(\"{step['headerName']}\", constant(\"{step['constant']}\"))\n"
            elif step['type'] == 'log':
                java_code += f"            .log(\"{step['loggingLevel']}\", \"{step['message']}\")\n"
            elif step['type'] == 'to':
                java_code += f"            .to(\"{step['uri']}\")\n"
            elif step['type'] == 'unmarshal':
                java_code += f"            .unmarshal().json(JsonLibrary.{step['library']}, {step['unmarshalTypeName']}.class)\n"
        
        java_code += "            ;\n\n"

    java_code += "    }\n"
    java_code += "}\n"

    return java_code

def main():
    xml_file = 'camel-routes.xml'
    routes = parse_camel_xml(xml_file)
    java_dsl = generate_java_dsl(routes)

    with open('CamelRoutes.java', 'w') as file:
        file.write(java_dsl)

    print("Java DSL code has been generated in CamelRoutes.java")

if __name__ == "__main__":
    main()
