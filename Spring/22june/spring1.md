Let's add a model class `EndpointInformation` to represent the endpoint data. This class will be used in the controller and service layers for handling endpoint-related information.

### Updated Project Structure

```
project-root/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           └── demo/
│   │   │               ├── controller/
│   │   │               │   └── EndpointInformationController.java
│   │   │               ├── model/
│   │   │               │   └── EndpointInformation.java
│   │   │               ├── service/
│   │   │               │   ├── EndpointInformationService.java
│   │   │               │   ├── LoggingService.java
│   │   │               │   └── HeaderService.java
│   │   │               └── DemoApplication.java
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/
│               └── example/
│                   └── demo/
│                       └── controller/
│                           └── EndpointInformationControllerTest.java
├── pom.xml
└── camel-routes.xml
```

### Model Class

#### EndpointInformation.java

```java
package com.example.demo.model;

public class EndpointInformation {

    private String fromUri;
    private String toUri;
    private String processRef;
    private String headerName;
    private String headerValue;
    private String logMessage;
    private String loggingLevel;

    // Getters and Setters

    public String getFromUri() {
        return fromUri;
    }

    public void setFromUri(String fromUri) {
        this.fromUri = fromUri;
    }

    public String getToUri() {
        return toUri;
    }

    public void setToUri(String toUri) {
        this.toUri = toUri;
    }

    public String getProcessRef() {
        return processRef;
    }

    public void setProcessRef(String processRef) {
        this.processRef = processRef;
    }

    public String getHeaderName() {
        return headerName;
    }

    public void setHeaderName(String headerName) {
        this.headerName = headerName;
    }

    public String getHeaderValue() {
        return headerValue;
    }

    public void setHeaderValue(String headerValue) {
        this.headerValue = headerValue;
    }

    public String getLogMessage() {
        return logMessage;
    }

    public void setLogMessage(String logMessage) {
        this.logMessage = logMessage;
    }

    public String getLoggingLevel() {
        return loggingLevel;
    }

    public void setLoggingLevel(String loggingLevel) {
        this.loggingLevel = loggingLevel;
    }
}
```

### Updated Service Classes

#### EndpointInformationService.java

```java
package com.example.demo.service;

import com.example.demo.model.EndpointInformation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

@Service
public class EndpointInformationService {

    @Autowired
    private LoggingService loggingService;

    @Autowired
    private HeaderService headerService;

    public List<EndpointInformation> fetchEndpoints() {
        // Implement logic to fetch endpoints
        return null;
    }

    public EndpointInformation createEndpoint(EndpointInformation endpointInformation) {
        // Implement logic to create endpoint
        return null;
    }

    public void logRequest(HttpServletRequest request) {
        loggingService.logRequest(request);
    }

    public void setHeaders(HttpServletRequest request) {
        headerService.setHeaders(request);
    }
}
```

#### LoggingService.java

```java
package com.example.demo.service;

import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;

@Service
public class LoggingService {

    public void logRequest(HttpServletRequest request) {
        // Implement logging logic for incoming requests
    }
}
```

#### HeaderService.java

```java
package com.example.demo.service;

import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;

@Service
public class HeaderService {

    public void setHeaders(HttpServletRequest request) {
        // Implement logic to set headers for outgoing requests
    }
}
```

### Updated Controller Class

#### EndpointInformationController.java

```java
package com.example.demo.controller;

import com.example.demo.model.EndpointInformation;
import com.example.demo.service.EndpointInformationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

@RestController
@RequestMapping("/api")
public class EndpointInformationController {

    @Autowired
    private EndpointInformationService endpointInformationService;

    @GetMapping("/endpoints")
    public List<EndpointInformation> getAllEndpoints(HttpServletRequest request) {
        endpointInformationService.logRequest(request);
        endpointInformationService.setHeaders(request);

        // Implement logic to fetch endpoint information
        List<EndpointInformation> endpoints = endpointInformationService.fetchEndpoints();

        return endpoints;
    }

    @PostMapping("/endpoint")
    public EndpointInformation createEndpoint(@RequestBody EndpointInformation endpointInformation, HttpServletRequest request) {
        endpointInformationService.logRequest(request);
        endpointInformationService.setHeaders(request);
        
        // Implement logic to create endpoint
        return endpointInformationService.createEndpoint(endpointInformation);
    }
}
```

### Main Application Class

#### DemoApplication.java

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

### Dependencies in pom.xml

Make sure you have the necessary dependencies in your `pom.xml` for Spring Boot:

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### Conclusion

This setup should provide a basic Spring Boot project structure with a controller, service classes, and a model class. The `EndpointInformationService` class integrates with `LoggingService` and `HeaderService` to handle logging and header setting functionalities, respectively. You can further extend and customize these components based on your specific business logic and requirements derived from the Camel XML routes.
