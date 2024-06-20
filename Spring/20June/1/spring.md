Sure! I'll guide you step by step on how to achieve this transformation from a Camel XML file to a Spring Boot application with a controller and service class. We'll focus on creating an `EndpointInformation` class and a logging service to set headers.

### Step 1: Set Up Your Spring Boot Project

1. **Create a new Spring Boot project** using Spring Initializr (https://start.spring.io/). Include dependencies for `Spring Web` and `Spring Boot DevTools`.

2. **Download the project** and import it into your favorite IDE (e.g., IntelliJ, Eclipse).

### Step 2: Define the `EndpointInformation` Model

Create a new class `EndpointInformation` in the `model` package.

```java
package com.example.demo.model;

public class EndpointInformation {
    private String endpoint;
    private String method;
    private String description;

    // Constructors
    public EndpointInformation() {}

    public EndpointInformation(String endpoint, String method, String description) {
        this.endpoint = endpoint;
        this.method = method;
        this.description = description;
    }

    // Getters and Setters
    public String getEndpoint() {
        return endpoint;
    }

    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
```

### Step 3: Create the Logging Service

Create a new class `LoggingService` in the `service` package.

```java
package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;

@Service
public class LoggingService {
    private static final Logger logger = LoggerFactory.getLogger(LoggingService.class);

    public void logRequest(HttpServletRequest request) {
        logger.info("Request URL: " + request.getRequestURL());
        logger.info("Request Method: " + request.getMethod());
        logger.info("Request Headers: " + request.getHeaderNames());
    }

    public void setHeaders(HttpServletRequest request) {
        // Example of setting headers (you might need to adapt this to your needs)
        request.setAttribute("Custom-Header", "HeaderValue");
    }
}
```

### Step 4: Create the Controller

Create a new class `EndpointController` in the `controller` package.

```java
package com.example.demo.controller;

import com.example.demo.model.EndpointInformation;
import com.example.demo.service.LoggingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api")
public class EndpointController {

    @Autowired
    private LoggingService loggingService;

    @GetMapping("/endpoints")
    public List<EndpointInformation> getAllEndpoints(HttpServletRequest request) {
        loggingService.logRequest(request);
        loggingService.setHeaders(request);

        return Arrays.asList(
            new EndpointInformation("/api/endpoints", "GET", "Get all endpoints"),
            new EndpointInformation("/api/endpoint", "POST", "Create an endpoint")
        );
    }

    @PostMapping("/endpoint")
    public EndpointInformation createEndpoint(@RequestBody EndpointInformation endpointInformation, HttpServletRequest request) {
        loggingService.logRequest(request);
        loggingService.setHeaders(request);
        return endpointInformation;
    }
}
```

### Step 5: Convert Camel XML to Spring Boot Code

To automate the conversion from Camel XML to Spring Boot code, you can write a Python script that parses the Camel XML and generates the corresponding Spring Boot code. This script would need to read the XML, extract relevant information, and then use templates to generate the Java classes.

Here is a basic example of a Python script that can help with the conversion:

#### Python Script

```python
import xml.etree.ElementTree as ET

def parse_camel_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    routes = []
    for route in root.findall('.//route'):
        endpoint = route.find('.//to').attrib['uri']
        method = route.attrib['id']
        description = route.attrib.get('description', '')

        routes.append({
            'endpoint': endpoint,
            'method': method,
            'description': description
        })

    return routes

def generate_spring_boot_code(routes):
    controller_code = """
package com.example.demo.controller;

import com.example.demo.model.EndpointInformation;
import com.example.demo.service.LoggingService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api")
public class EndpointController {

    @Autowired
    private LoggingService loggingService;

    @GetMapping("/endpoints")
    public List<EndpointInformation> getAllEndpoints(HttpServletRequest request) {
        loggingService.logRequest(request);
        loggingService.setHeaders(request);

        return Arrays.asList(
            {endpoints}
        );
    }

    @PostMapping("/endpoint")
    public EndpointInformation createEndpoint(@RequestBody EndpointInformation endpointInformation, HttpServletRequest request) {
        loggingService.logRequest(request);
        loggingService.setHeaders(request);
        return endpointInformation;
    }
}
"""

    endpoint_code = ",\n            ".join(
        [f'new EndpointInformation("{route["endpoint"]}", "GET", "{route["description"]}")' for route in routes])

    controller_code = controller_code.format(endpoints=endpoint_code)

    with open('EndpointController.java', 'w') as f:
        f.write(controller_code)

if __name__ == '__main__':
    camel_routes = parse_camel_xml('camel-routes.xml')
    generate_spring_boot_code(camel_routes)
```

This script parses the Camel XML to extract the routes and generates a basic Spring Boot controller class. You can customize and expand this script as needed to handle more complex cases and additional details from your Camel XML.

### Step 6: Running Your Spring Boot Application

1. **Compile and run your Spring Boot application** using your IDE or command line:
   ```sh
   ./mvnw spring-boot:run
   ```

2. **Test the endpoints** using tools like Postman or curl.

### Step 7: Further Customization

You can further customize your application by adding more services, refining the logging logic, and handling more complex XML structures as needed.

This step-by-step guide should help you get started with converting Camel XML routes to a Spring Boot application with a controller and service class.
