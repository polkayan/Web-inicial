# Panel de Acceso Web

Este repositorio contiene el código de un panel de acceso web. El sistema está estructurado mediante contenedores para separar los servicios de forma ordenada y mantener la seguridad del entorno.

## Componentes del Sistema

* **Frontend:** Interfaz de usuario construida con HTML y CSS.
* **Backend:** Servidor en Python. Se encarga de recibir las peticiones y aplicar cifrado AES a la información confidencial antes de almacenarla.
* **Base de Datos:** PostgreSQL (versión Alpine) para guardar la información de los usuarios.
* **Proxy:** Nginx Proxy Manager, utilizado para recibir y dirigir el tráfico entrante de forma segura.



## Pruebas de Seguridad y Rendimiento
Se han realizado auditorías de carga y seguridad para garantizar la estabilidad del servicio:

* **Protección SQL Injection:** Validado el uso de consultas parametrizadas que neutralizan intentos de inyección de código malicioso en los formularios.
* **Stress Testing (DoS):**
    * **500 Peticiones:** Éxito del 100% sin pérdida de datos.
    * **2,000 Peticiones:** Éxito del 100%, manteniendo la integridad de la base de datos.
    * **10,000 Peticiones:** Identificado el punto de saturación en ~7,700 peticiones concurrentes, demostrando una alta resiliencia en entornos de desarrollo.



## Configuración de Red

Los componentes se comunican a través de una red interna de Docker. Para el acceso desde el exterior, el sistema expone únicamente el puerto 8888. Esta configuración técnica se utiliza para evitar los conflictos habituales con el puerto 80 que suelen estar bloqueados o reservados por los routers.

## Instrucciones de Despliegue

Para poner en marcha el proyecto, es necesario tener instalados Docker y Docker Compose en el servidor.

1. Clonar el repositorio en el servidor.
2. Configurar la clave de cifrado AES en el entorno. (Nota: por motivos de seguridad, los archivos con claves están excluidos del control de versiones mediante `.gitignore`).
3. Iniciar los contenedores ejecutando el siguiente comando:
   ```bash
   sudo docker compose up -d




Desarrollado por Rayan Dahmani.

