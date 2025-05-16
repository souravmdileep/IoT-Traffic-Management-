(define (problem traffic-problem)
  (:domain traffic-light)

  (:objects
    car1 - vehicle
    amb1 - emergency
    car2 - vehicle
    car3 - vehicle
    seg1 - segment
    seg2 - segment
    seg3 - segment
    seg4 - segment
    seg5 - segment
    sig1 - signal
    sig2 - signal
    sig3 - signal
    sig4 - signal
    red green yellow
  )

  (:init
    (at car1 seg1)
    (signal_status sig1 red)
    (at amb1 seg4)
    (signal_status sig2 red)
    (at car2 seg5)
    (signal_status sig3 red)
    (at car3 seg3)
    (signal_status sig4 red)
    (intersection seg2)
    (connected seg1 seg2)
    (connected seg2 seg3)
    (connected seg4 seg2)
    (connected seg5 seg2)
    (signal_between sig1 seg1 seg2)
    (signal_between sig2 seg2 seg3)
    (signal_between sig3 seg5 seg2)
    (signal_between sig4 seg3 seg2)
  )

  (:goal (and
    (at car1 seg2)
    (at amb1 seg3)
    (at car2 seg5)
    (at car3 seg1)
  ))
)
