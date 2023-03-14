FROM archlinux:latest

RUN pacman -Syu && \
    pacman -S jre-openjdk-headless && \
    archlinux-java set java-19-openjdk && \
    mkdir /app/

COPY ./app.jar /app/app.jar

WORKDIR /app/

ENTRYPOINT [ "java", "-jar", "app.jar" ]
