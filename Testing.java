import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class CamelToSpringBootConverter {

    public static void main(String[] args) {
        String camelXmlPath = "/content/camel-routes.xml";
        String projectName = "SpringBootProject";

        // Step 1: Parse Camel XML
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.parse(new File(camelXmlPath));

            // Step 2: Generate Spring Boot Project Structure
            generateProjectStructure(projectName);

            // Step 3: Generate Controller Class
            generateControllerClass(document);

            // Step 4: Generate Service Class (if needed)
            generateServiceClass();
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void generateProjectStructure(String projectName) throws IOException {
        // Create main project directory
        Path projectDir = Paths.get(System.getProperty("user.dir"), projectName);
        Files.createDirectories(projectDir);

        // Create standard Spring Boot project structure
        Path srcMainJava = projectDir.resolve("src/main/java/com/example/demo");
        Files.createDirectories(srcMainJava);
    }

    private static void generateControllerClass(Document document) throws IOException {
        NodeList routes = document.getElementsByTagName("route");

        // Example Template for Controller class
        StringBuilder controllerClass = new StringBuilder();
        controllerClass.append("package com.example.demo;\n\n");
        controllerClass.append("import org.springframework.web.bind.annotation.*;\n\n");
        controllerClass.append("@RestController\n");
        controllerClass.append("public class EndpointInformation {\n\n");

        // Generate endpoint mappings based on Camel XML routes
        for (int i = 0; i < routes.getLength(); i++) {
            Element route = (Element) routes.item(i);
            String endpoint = route.getAttribute("uri");

            // Extract endpoint method name from Camel route definition
            String methodName = extractMethodNameFromUri(endpoint);

            // Generate method for each endpoint
            controllerClass.append("    @RequestMapping(\"").append(endpoint).append("\")\n");
            controllerClass.append("    public String ").append(methodName).append("() {\n");
            controllerClass.append("        // Implement route logic here\n");
            controllerClass.append("        return \"").append(endpoint).append(" handled!\";\n");
            controllerClass.append("    }\n\n");
        }

        controllerClass.append("}\n");

        // Write controller class to file
        Path controllerFilePath = Paths.get(System.getProperty("user.dir"), "SpringBootProject", "src/main/java/com/example/demo/EndpointInformation.java");
        Files.write(controllerFilePath, controllerClass.toString().getBytes());
    }

    private static void generateServiceClass() throws IOException {
        // Example Template for Service class (if needed)
        String serviceClass = "package com.example.demo;\n\n";
        serviceClass += "@Service\n";
        serviceClass += "public class ServiceClass {\n\n";
        serviceClass += "    // Service methods here\n\n";
        serviceClass += "}\n";

        // Write service class to file
        Path serviceFilePath = Paths.get(System.getProperty("user.dir"), "SpringBootProject", "src/main/java/com/example/demo/ServiceClass.java");
        Files.write(serviceFilePath, serviceClass.getBytes());
    }

    private static String extractMethodNameFromUri(String uri) {
        // Simplified method to extract method name from URI
        // You might need more sophisticated logic based on your Camel route structure
        return uri.replaceAll("/", "").replaceAll("\\{\\w+\\}", "");
    }
}
