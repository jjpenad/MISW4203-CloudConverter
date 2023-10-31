# MISW4203-CloudConverter

## Requisitos
* Tener Docker instalado (Docker Desktop)
* Tener Postman instalado
* Saber usar la línea de comandos del sistema operativo
* Conocimientos en Git
* Conocimientos en Postman y API REST

## Instalación
* Clonar este repositorio en un directorio local
* Acceder a la carpeta de este repositorio y luego a la carpeta `/app`
* Si en la carpeta `/app` no existen las carpetas `/output` y `/uploads`, créelas en este directorio
* Copie el video que desea convertir a la carpeta `/uploads` (El video convertido al nuevo formato se creará automáticamente en la carpeta `/output`)
* **IMPORTANTE**: Debe tener Docker instalado en su máquina y tener creadas las carpetas de los pasos anteriores, antes de realizar el siguiente paso.
* Abrir una terminal en esta ruta (`/app`) y ejecutar el comando `docker-compose up`
* Abrir Postman y hacer las peticiones a los endpoints.

## Postman
* La configuración del <ins>ambiente</ins> de Postman para está aplicación se encuenta con el nombre: `Video converver - localhost.postman_environment.json` en la carpeta raíz del repositorio. Impórtela para poder hacer uso correcto de la colección.
* La configuración de la <ins>colección</ins> de Postman para esta aplicación se encuentra con el nombre: `Video converter - Team 7.postman_collection.json` en la carpeta raíz del repositorio. Impórtela para poder probar los endpoints más fácil y cómodamente. (Recuerde importar la configuración del ambiente del paso anterior)

## Endpoints
Para ver la documentación completa sobre los distintos endpoints de esta aplicación, es necesario que importe la configuración de la colección de Postman del paso anterior.

## Despliegue:
Actualmente, nuestra aplicación se encuentra desplegada en GCP en la siguiente [URL](34.29.108.46:5000)
