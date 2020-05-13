Pento Facturas

El proyecto se encuentra realizado en Laravel Back y front jquery. La base de datos es mysql alojada en https://www.freemysqlhosting.net/ estructurada en tres tablas: facturas, empresas y detalle factura. 


Las tablas y la data se generó a partir de un script en python 3.8.2, donde se toma una carpeta dte-files con xml, donde cada xml es una factura con la estructura indicada en la solicitud. Dicha carpeta debe estar en el mismo directorio del script de python. Para ejecutar el script se necesita tener instalada además la librería mysql.


Dada que la data se encuentra alojada en un servidor gratuito y se estableció la configuración de conexión tanto en el script de python con en el archivo .env de laravel, no se necesita agregar manualmente ningún script de bd.


Para ejecutar el proyecto de forma local, se debe tener instalado PHP 7.2.3. Para la creación del proyecto se utilizó composer. Para ejecutar de forma local el proyecto, basta con abrir la consola ingresar al directorio del proyecto, y ejecutar >>php artisan serve.


Cuando se revisa http://localhost:8000/ se podrá ver el listado de resultado.
La información se extrae de la tabla facturas, que tiene el monto total (suma de los ítem) y se ordena de mayor a menor respecto a la emisión que es una marca de tiempo. Además se incluye otra información relevante de la factura. Igualmente se permite, reordenar por otras columnas, y la información se encuentra paginada, si es que se tratara de mucha información.



