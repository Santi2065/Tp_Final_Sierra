# Trabajo Práctico Final - Pensamiento Computacional
https://udesa-pc.github.io/tps/tpf/

# Introducción

El objetivo de este trabajo es participar en una competencia para llegar a la cima del monte K3 y sacar una foto de la bandera que plantó Franz R. Los equipos están compuestos por 4 escaladores y deben ser guiados por un equipo de apoyo que les indica la dirección a seguir.
Reglas de la competencia

    Los equipos están compuestos por 4 escaladores.
    Cada escalador puede llevar un localizador GPS, una brújula y un inclinómetro.
    Todos los escaladores se mueven a una velocidad máxima de 50 m/min.
    El campamento base está localizado en (x,y) = (14000, 14000) y todos los escaladores partirán de ahí al mismo tiempo.
    La base del monte K3 es circular con centro en (x,y) = (0,0) y radio de 23000 m.
    El equipo del escalador que llegue a la cima del monte K3 y saque una foto de la bandera que plantó Franz R. será el ganador.

# Comunicación

Las comunicaciones por radio se hacen a través de un servidor conectado a una antena de alta ganancia en el campamento base. El servidor empieza en un estado inicial en el que espera que se registren los equipos de escaladores que participarán de la competencia. En un momento determinado, termina la inscripción de equipos y comienza el evento. En ese instante, el servidor comienza a recibir las direcciones y velocidades de los equipos de apoyo. El servidor es capaz de recibir indicaciones una vez por minuto, pero el equipo de apoyo puede pedir información sobre el estado de los escaladores en cualquier momento.
