FROM alpine

RUN apk update
RUN apk add openjdk21-jre
RUN apk add wget
RUN apk add bash
RUN apk add unzip

WORKDIR /data

RUN wget https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/496/downloads/paper-1.20.4-496.jar
RUN wget https://github.com/Cubxity/UnifiedMetrics/releases/download/v0.3.8/unifiedmetrics-platform-bukkit-0.3.8.jar

RUN mkdir plugins
RUN mv unifiedmetrics-platform-bukkit-0.3.8.jar plugins/unifiedmetrics-platform-bukkit-0.3.8.jar

COPY driver.yml plugins/unifiedmetrics/driver/prometheus.yml
COPY start.sh .

COPY server.properties .
COPY bukkit.yml .

COPY data.zip .
RUN unzip data.zip

WORKDIR /data/cache
COPY mojang_1.20.4.jar .

EXPOSE 25565/tcp
EXPOSE 25565/udp
EXPOSE 9100

WORKDIR /data
CMD ["bash", "./start.sh"]
