; REGLAS JUGADOR 1

(defrule Regla1
    (declare (salience 90))
    (contador ?c)
    =>
    (printout t "Soy el jugador 1, probando regla con salience 90")
)

(defrule Regla2
    (declare (salience 70))
    =>
    (printout t "Soy el jugador 1 con regla 70")
)

(defrule Regla4
    (declare (salience 20))
    =>
    (printout t "Soy el jugador 1 y pruebo la regla 20")
)

