FROM archlinux:latest

RUN pacman -Syu --noconfirm && \
    pacman -S jre-openjdk-headless --noconfirm && \
    archlinux-java set java-19-openjdk && \
    mkdir /app/

COPY ./target/user_control-1.0.0.jar /app/app.jar

WORKDIR /app/

ENTRYPOINT [ "java", "-jar", "app.jar" ]
