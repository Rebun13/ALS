COMPETICIONES DE CARRERAS CON GAE
=========

Este proyecto consiste en una página web desarrollada mediante **Google Application Engine** (GAE) que muestra el estado
actual de una competición deportiva automovilística. En particular, la información que puede ser consultada es:
- La lista ordenada de los/las deportistas y su puntuación actual.
- La lista de equipos con los pilotos que forman parte de ellos, así como la lista de pilotos que no pertenecen a ningún
  equipo.
- La lista de eventos que componen el campeonato.
Inicialmente, mi intención era poder también escoger entre diferentes competiciones, pero finalmente me he decidido por 
  solo soportar una competición simultáneamente.
  
## Antes de empezar
Para poder arrancar el proyecto será necesario disponer de un equipo en el que estén instalados:
- **Python 2**
- **Pycharm**
- **Google Aplicación Engine**
- **PIL** (Python Imaging Library) o, en su defecto, **Pillow** (versión 6.2.1 o inferior)

Cuando se inicia el servidor, la base de datos (o Datastore) se encuentra completamente vacía. Para insertar datos por 
defecto de todas las entidades, se debe acceder a la siguiente URL:

[localhost:8080/load](http://localhost:8080/load/)

Por el contrario, si se desea acceder a la aplicación sin ningún dato insertado, o si ya se han insertado anteriormente, 
se podrá utilizar la siguiente URL:

[localhost:8080/](http://localhost:8080/)

Solamente los usuarios autenticados como administrador podrán insertar, modificar y eliminar información almacenada en 
la base de datos, a excepción de los datos por defecto, que pueden ser insertados por cualquier usuario mediante el
enlace mencionado anteriormente.

## Entidades
Estas son las entidades que componen el proyecto.

### Driver
La entidad “Driver” representa a los/las deportistas que participan en la competición.

| Atributo | Tipo de dato | Descripción |
| --- | --- | --- |
| Name | Cadena de caracteres | Nombre del/de la deportista. Solo contiene caracteres alfabéticos y “.”. Por ejemplo: _L. Hamilton_ |
| Id | Entero | Dorsal del/de la deportista. Es su identificador. Debe ser mayor que 0. Por ejemplo: _77_ |
| Score | Entero | Puntuación actual del/de la deportista. A mayor puntuación, más alto se encontrará en la clasificación del campeonato. Debe ser mayor o igual que 0. Por ejemplo: _50_ |

Cuando se crea un/a deportista, se deben indicar todos sus atributos. Una vez creado, solo se podrá modificar su puntuación o eliminarlo/a.

### Team
La entidad “Team” representa a los equipos a los cuales pertenecen los deportistas que participan en la competición.

| Atributo | Tipo de dato | Descripción |
| --- | --- | --- |
| Name | Cadena de caracteres | Nombre del equipo. Solo contiene caracteres alfabéticos. Por ejemplo: _Mercedes_ |
| Driver1 | Entero | \[FK\] Id del primer piloto. Puede ser nulo. |
| Driver2 | Entero | \[FK\] Id del segundo piloto. Puede ser nulo. |

Cuando se crea un equipo, se debe indicar su nombre, pero los/las deportistas que lo componen no son necesarios. Una vez
creado, se podrá modificar tanto su nombre como los/las deportistas que contiene. También puede ser eliminado.

### Event
La entidad “Team” representa a los equipos a los cuales pertenecen los/las deportistas que participan en la competición.

| Atributo | Tipo de dato | Descripción |
| --- | --- | --- |
| Name | Cadena de caracteres | Nombre del evento. Por ejemplo: _GP Portugal_ |
| Country | Cadena de caracteres | País donde se celebra el evento. Por ejemplo: _Portugal_ |
| Date  | Fecha | Fecha en la que se celebra el evento, en formato AAAA-MM-DD. Por ejemplo: _2021-05-15_ |
| Image | Blob | Imagen asociada al evento. Es opcional. |

Cuando se crea un equipo, debemos indicar el nombre, el país y la fecha, siendo la imagen opcional. Los eventos no 
pueden ser modificados posteriormente, pero sí eliminados.