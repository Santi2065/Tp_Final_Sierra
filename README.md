# Trabajo Práctico Final - Pensamiento Computacional
https://udesa-pc.github.io/tps/tpf/

# Nota

Es posible proponer otro proyecto como trabajo final. En ese caso, se debe escribir una consigna de estilo similar a esta y presentarla a los docentes de la práctica. Ellos determinarán si la propuesta es o no viable. Procuren decidir esto a la brevedad, para maximizar el tiempo disponible para el desarrollo del trabajo.
Introducción

En 1927 Franz R. fue al Himalaya, dijo haber llegado a la cima del mítico monte K3 y declaró haber plantado una bandera allí, pero nadie le creyó. Recientemente se descubrió la ubicación del K3, que durante décadas había permanecido oculto por una inusual capa de nubes a su alrededor. Tal es el revuelo del descubrimiento del monte K3 que el gobierno de Nepal ha decidido organizar una competencia. El primer equipo que llegue a la cima del monte y saque una foto de la bandera que plantó Franz R., será el ganador.

Sigue habiendo una gran cantidad de nubes en la zona, por lo que cada escalador debe ser guíado por un equipo de apoyo que le indique la dirección a seguir. Para abaratar costos, todos los equipos comparten el mismo canal de radio asi que solo se puede comandar al equipo de escaladores cada 1 minuto (iteración). En todo momento se puede conocer la posición de todos los escaladores de todos los equipos.

Ustedes deciden participar de la competencia, conformando un equipo de 4 escaladores.

# Reglas de la competencia

    Los equipos de escaladores están compuestos por 4 personas.
    Cada escalador puede llevar:
        Un localizador GPS que le permite saber su posición (x,y,z).
        Una brújula, que le permite orientarse a un escalador.
        Inclinómetro, dispositivo que provee la compañía de bebidas energizantes Blue Cow que le permite saber la inclinación del punto donde está parado.
    Los escaladores estuvieron entrenando todos juntos por lo que todos se mueven como máximo a 50 m/min.
    El campamento base está localizado en (x,y) = (14000, 14000), y todos los escaladores partirán de ahí al mismo tiempo.
    La base del monte K3 es inusualmente circular con centro en (x,y) = (0,0) y con un radio de 23000 m. Los locales han creado una autopista de circunvalación por lo que cualquier escalador que se salga será atropellado por una horda incontenible de bueyes y eliminado de la competencia ¡Cuidado!
    El equipo del escalador que llegue a la cima del monte K3 y saque una foto de la bandera que plantó Franz R. será el ganador.

# Comunicación

Las comunicaciones por radio se hacen a través de un servidor conectado a una antena de alta ganancia en el campamento base. El servidor empieza en un estado inicial en el que espera que se registren los equipos de escaladores que participarán de la competencia. En un momento determinado, termina la inscripción de equipos y comienza el evento. En ese instante, el servidor comienza a recibir las direcciones y velocidades de los equipos de apoyo. El servidor es capaz de recibir indicaciones una vez por minuto, pero el equipo de apoyo puede pedir información sobre el estado de los escaladores en cualquier momento.

Las direcciones se comunican como un ángulo en radianes, donde 0 rad es hacia el eje X positivo, y el ángulo crece en sentido antihorario. Y las velocidades deben ser siempre positivas y menores o iguales a 50 m/min.

Si por alguna razón, el equipo de apoyo no manda las direcciones de sus escaladores a tiempo, el servidor asume que el equipo de apoyo se ha retirado de la competencia y elimina a sus escaladores de la competencia.
Requerimientos
Equipo de apoyo

La competencia provee el código del servidor, donde puede consultar las funciones que tiene y su documentación en sus docstrings. Los programadores del servidor, también les proveen a los equipos un programa cliente que se encarga de comunicarse con el servidor. Puede obtener los archivos del servidor y del cliente en el siguiente link.

Importante: Por ninguna razón deberían modificar el código del servidor y cliente que se les provee.

Su tarea consiste en crear un programa informático en el lenguaje Python que le indique a los escaladores de su equipo en qué dirección avanzar en la próxima iteración. Tenga en consideración que, si bien los 4 pertenecen a un mismo equipo, cada escalador es una entidad independiente. Como consecuencia, cada uno puede tomar una estrategia distinta para encarar la escalada. El objetivo es, como se imaginarán, llegar a la cima del monte antes que los otros equipos. Tenga en cuenta que una misma montaña puede tener muchos picos, nos interesa encontrar el más alto de estos.

Las estrategias propuestas deben permitir enviar indicaciones secuenciales a los escaladores de forma automática, es decir, no se requiere que se envíe de forma manual el comando de avance en una dirección determinada. La idea es que las indicaciones a los escaladores se generen en función de una estrategia de avance diseñada con algún criterio, en conjunto con información tomada del servidor. Se ponderarán favorablemente estrategias basadas en algún tipo de lógica, pero son aceptables técnicas basadas netamente en el azar, sin uso de datos del servidor. Las indicaciones generadas por la estrategias propuestas se deben comunicar al servidor mediante el cliente provisto, siguiendo el formato descripto anteriormente.
Dashboard

Durante la competencia, los inversores de su equipo desean ver el progreso de sus escaladores. Para esto, deben crear un dashboard, que se actualice en tiempo real, con al menos 5 visualizaciones distintas. Como ejemplos, se proponen:

    La altura máxima alcanzada de cada equipo a lo largo del tiempo.
    La altura promedio de cada equipo a lo largo del tiempo.
    La altura de cada escalador de su equipo a lo largo del tiempo.
    Distancia recorrida por cada escalador de su equipo a lo largo del tiempo.
    Velocidades de los escaladores en cada iteración.
    La posición (x,y,z) de todos los escaladores en todo momento (3D).
    La trayectoria (x,y,z) de sus escaladores (3D).
    Un leaderboard de los mejores 10 escaladores cada iteración.
    Un mapa de calor de la cantidad de escaladores en cada sector de la montaña.
    La altura promedio que se vio de cada sector de la montaña explorada hasta el momento.
    Lista scrolleable y ordenada de los escaladores con sus alturas.
    Lista scrolleable y ordenada de los escaladores que van llegando a la cima.
    Otras que propongan durante el desarrollo del trabajo, y que deben comunicar a los docentes para verificar su viabilidad.

Los dashboards tienen que ser interactivos, es decir, que el usuario pueda interactuar con ellos. Por ejemplo, que se pueda elegir los escaladores de qué equipos seguir, si se quiere seguir a un escalador en específico, tener en cuenta solo los escaladores a partir de cierta altura, etc.

Para esto puede utilizar cualquiera de las siguientes librerías:

    Tkinter
    Matplotlib (Especialmente animations)
    Bokeh
    PyGame
    Panel
    Datashader
    Otras, que deben ser informadas a los docentes durante el desarrollo del trabajo.

Si deciden usar Tkinter, les dejamos un código mínimo para que puedan tener la información de los escaladores en tiempo real.

# Argumentos por línea de comando

Deben poder agregar argumentos por línea de comando a su programa. Como mínimo, deben poder pasar la IP y puerto con el que deben conectarse. Por ejemplo, el cliente debe poder ejecutarse de forma similar a la siguiente:

    python tpf_NOMBRE_DE_GRUPO_cliente.py --ip 127.0.0.1:8000

Siendo 127.0.0.1 la dirección IP y 8000 el puerto que se usarán para comunicarse con el servidor. Pueden agregar otros argumentos que consideren necesarios en todos los programas que creen.

# Entrega

El trabajo se realizará en grupos de hasta 4 personas. Los grupos deben estar inscritos en el campus de la materia. Recomendamos que el nombre de grupo que elijan sea corto.

Se debe realizar la entrega de los archivos de Python generados a través de la tarea creada en el campus de la materia. En la misma (y en el calendario) se encuentra la fecha de entrega.

    Los archivos deben llamarse tpf_NOMBRE_DE_GRUPO_X.py. Por ejemplo, si el grupo llama ‘LINAR’, los archivos que creen deberán tener el nombre: tpf_linar_{nombre_representativo}.py

Se recuerda a los estudiantes que las entregas deben ser un producto original de cada estudiante, por lo que se les pide revisar la sección 6 del programa de la materia y el Código de Honor y Ética.

# Evaluación

Para aprobar, es fundamental que el código se ejecute correctamente sin lanzar excepciones al hacerlo; cumpliendo con los requerimientos de la consigna. Además se evaluará la calidad del código, la calidad de los comentarios y la calidad de la documentación. Se espera que usen Programación Orientada a Objetos (POO) y que usen los conceptos vistos en clase debidamente. Cualquier cosa extra que se agregue será tenida en cuenta para la nota final.

