(define (domain traffic-light)
  (:requirements :typing)

  (:types
    vehicle segment signal - object
    emergency - vehicle)

  (:predicates
    (at ?v - vehicle ?s - segment)
    (free ?s - segment)
    (connected ?s1 ?s2 - segment)
    (signal_between ?sig - signal ?s1 ?s2 - segment)
    (signal_status ?sig - signal ?st)          ; untyped symbol
    (emergency_vehicle ?v - vehicle)
    (intersection ?s - segment)                ; allows multi-occupancy
  )

  (:action change-signal
    :parameters (?sig - signal ?current ?new)
    :precondition (signal_status ?sig ?current)
    :effect (and
              (not (signal_status ?sig ?current))
              (signal_status ?sig ?new))
  )

  (:action move-vehicle
    :parameters (?v - vehicle ?s1 ?s2 - segment)
    :precondition (and
      (at ?v ?s1)
      (connected ?s1 ?s2)
      (or (intersection ?s2) (free ?s2))
    )
    :effect (and
      (not (at ?v ?s1))
      (at ?v ?s2)
      (free ?s1)
      (when (not (intersection ?s2)) (not (free ?s2)))
    )
  )

  (:action mark-emergency
    :parameters (?v - vehicle)
    :precondition (not (emergency_vehicle ?v))
    :effect (emergency_vehicle ?v))
)
