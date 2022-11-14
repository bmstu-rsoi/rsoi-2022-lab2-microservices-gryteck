FROM openjdk:11

COPY *.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java" ,"-Xmx512m", "-Xms512m", "-jar","/app.jar"]