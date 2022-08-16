
SUBROUTINE  ReadPressureFromFile( filename, x, y, z, p ) 
    IMPLICIT NONE
    
    real*8 :: x, y, z
    real*8 :: p1, p2 
    complex*16 :: p

    integer :: i = 42
    real*8 :: pi = 3.14
    complex :: w
    character (len = 40) :: filename


    w = cmplx(i, pi)

    p = complex(p1, p2)

    print *, filename, z, cmplx(x)


    ! any number in the range 9-99 and it indicates the file, you may choose any number but every open file in the program must have a unique number
    open ( unit = i, file = filename )
    
    do i=1,100  
      read(1,*) x(i), y(i), z(i), p1(i), p2(i)   
    end do  
   
   close(1)


END SUBROUTINE ReadPressureFromFile


FUNCTION acousticPressure( model, n, coord ) RESULT(load)
    USE DefUtils
    IMPLICIT None
    TYPE(Model_t) :: model
    INTEGER :: n
    REAL(KIND=dp) :: load, coord(3)
    COMPLEX(KIND=dp) :: Pressure
    character (len = 40) :: filename  

    filename = "entities-pressure-in.txt"

    CALL ReadPressureFromFile( filename, Coord(1), Coord(2), Coord(3), Pressure)
    load = Pressure
END FUNCTION acousticPressure