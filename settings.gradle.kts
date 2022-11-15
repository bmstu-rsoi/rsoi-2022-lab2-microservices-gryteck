rootProject.name = "rsoi-2022-lab2-microservices-gryteck"

// Common
include("common")

// Api
include("bonus-service-api")
include("ticket-service-api")
include("flight-service-api")
include("user-service-api")

// Service
include("config-server")
include("gateway")
include("ticket-service")
include("user-service")
include("bonus-service")
include("flight-service")