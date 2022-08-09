
SUBROUTINE  GetPressureFromFile( x, y, z, p ) 
    IMPLICIT NONE
    
    real :: x, y, z
    real :: p1, p2 
    complex :: p

    p = complex(p1, p2)

END SUBROUTINE GetPressureFromFile


FUNCTION acousticPressure( model, n, coord ) RESULT(load)
    USE DefUtils
    IMPLICIT None
    TYPE(Model_t) :: model
    INTEGER :: n
    REAL(KIND=dp) :: load,coord(3),Pressure

    CALL GetPressureFromFile(Coord(1),Coord(2),Coord(3),Pressure)
    load = Pressure
END FUNCTION acousticPressure