#!/bin/bash

echo "Iniciando despliegue en puerto 8888"

# Parar contenedores antiguos si existen
sudo docker compose down

# Levantar la nueva infraestructura en segundo plano
sudo docker compose up -d --build

echo "Web activa"
echo "Acceso local: http://192.168.1.51:8888"
echo "Acceso DuckDNS: http://polkayan.duckdns.org:8888"
echo "anel Nginx: http://192.168.1.51:81"

