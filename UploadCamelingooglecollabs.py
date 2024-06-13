# Step 1: Upload the file
from google.colab import files
uploaded = files.upload()

# Step 2: Verify the file is uploaded
!ls /content

# Step 3: Script to parse and generate Java DSL
import xml.etree.ElementTree as ET
import os

def preprocess_xml(xml_file, processed_file):
    """Preprocess the XML file to ensure all prefixes are correctly bound."""
    with open(xml_file, 'r') as file:
        content = file.read()
    
    # Add a default namespace declaration if missing
    if 'xmlns:camel' not in content:
        content = content.replace('<routes', '<routes xmlns:camel="http://camel.apache.org/schema/spring"', 1)
    
    with open(processed_file, 'w') as file:
        file.write(content)

def parse_camel_xml(xml_file):
    processed_file = 'processed_camel_routes.xml'
    preprocess_xml(xml_file, processed_file)
    
    namespaces = {'camel': 'http://camel.apache.org/schema/spring'}
    print(f"Namespaces: {namespaces}")  # Debugging: print namespaces
    
    try:
        tree = ET.parse(processed_file)
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
            tag = elem.tag.split('}', 1)[-1]  # Remove namespace

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
                step['constant'] = elem.find('camel:constant', namespaces).text
            elif tag == 'log':
                step['type'] = 'log'
                step['message'] = elem.get('message')
                step['loggingLevel'] = elem.get('loggingLevel')
            elif tag == 'to':
                step['type'] = 'to'
                step['uri'] = elem.get('uri')
            elif tag == 'unmarshal':
                step['type'] = 'unmarshal'
                json_elem = elem.find('camel:json', namespaces)
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
    xml_file = '/content/camel-routes.xml'  # Specified path to the XML file
    routes = parse_camel_xml(xml_file)
    java_dsl = generate_java_dsl(routes)

    output_dir = 'output'  # Directory where the generated Java file will be stored
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    java_file_path = os.path.join(output_dir, 'CamelRoutes.java')

    with open(java_file_path, 'w') as file:
        file.write(java_dsl)

    print(f"Java DSL code has been generated in {java_file_path}")

if __name__ == "__main__":
    main()
