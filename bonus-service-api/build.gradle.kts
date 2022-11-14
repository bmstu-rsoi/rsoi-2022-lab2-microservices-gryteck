plugins {
    kotlin("jvm")
    id("java-library")
}

group = "io.almishev"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(kotlin("stdlib"))
}