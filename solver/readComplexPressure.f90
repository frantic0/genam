
FUNCTION readComplexPressure( model, node, coord ) RESULT(load)
  USE DefUtils
  IMPLICIT None

  ! INTERFACE 
  ! SUBROUTINE ReadPressureFromFile( filename, x, y, z, p ) 
  !     real*8 :: x, y, z
  !     real*8 :: p 
  !     character (len = 40) :: filename
  ! END SUBROUTINE ReadPressureFromFile
  ! END INTERFACE
  
  
  TYPE(Model_t) :: model
  INTEGER :: node 
  REAL(KIND=dp) :: load, coord(3)
  REAL(KIND=dp) :: Pressure

  
  INTEGER :: m, n, col = 4
  INTEGER :: i, k, j
  real, dimension(100) :: x, y, z, wavelength

  ! real, dimension(100) :: p, q
  REAL(KIND=dp) :: min_diff, euclidean_distance, diff_coord_x, diff_coord_y, p, q
  
  real, dimension (:,:), allocatable :: darray    



  ! filename = "entities-pressure-in.dat"
  
  open( unit = 1, file = "entities-pressure-in.dat" )
  ! open( unit = 1, file = "entities-pressure-in.dat", status='old', action='read' )
  ! open( unit = 2, file = "node-ids.dat" )

  ! read first line with transducer array configuration to set EOL in the data read cycle
  read(1,*) m, n
  print *, m, n 

  ! allocate memory for multi-dimensional array
  allocate ( darray( m*n, col ) )     

  print *, node,',', Coord(1),',', Coord(2),',', Coord(3),','

  do I=1,n*m,1
    read(1,*) darray(I,:)
    print*, "darray(",I,") = ", darray(I,:)           
  enddo
  
  min_diff = 2147483647
  do k = 1, m*n            
    do j = 1, col                          
      print*, "darray(",k,",",j,") = ", darray(k,j)           
    end do
      
    diff_coord_x = ABS( Coord(1) - darray(k,1) )   
    diff_coord_y = ABS( Coord(2) - darray(k,2) ) 
    euclidean_distance = SQRT( diff_coord_x*diff_coord_x + diff_coord_y*diff_coord_y )   
      
    IF ( min_diff > euclidean_distance ) THEN  
      min_diff = euclidean_distance
      p = darray(k,3)
    END IF
    ! print*, "min_diff - ",min_diff ," - ",diff_coord_x,",",diff_coord_y,") = ", p          
  end do    
  
  close(1)
  deallocate (darray) 
  
  print*, "pressure = ", p           
  Pressure = p
  
  ! CALL ReadPressureFromFile( filename, Coord(1), Coord(2), Coord(3), Pressure)
  load = Pressure
  

END FUNCTION readComplexPressure

SUBROUTINE  ReadPressureFromFile( filename, x, y, z, p ) 
  IMPLICIT NONE
  
  real*8 :: x, y, z
  real*8 :: p1, p2 
  real*8 :: p

  integer :: i = 42
  real*8 :: pi = 3.14
  complex :: w
  character (len = 40) :: filename


  w = cmplx(i, pi)

  p = complex(p1, p2)

  print *, filename, z, cmplx(x)


  ! any number in the range 9-99 and it indicates the file, you may choose any number but every open file in the program must have a unique number
  ! open ( unit = i, file = filename )
  
  ! do i=1,100  
  !   read(1,*) x(i), y(i), z(i), p1(i), p2(i)   
  ! end do  
 
 close(1)


END SUBROUTINE ReadPressureFromFile


! FUNCTION readComplexPressure( model, n, coord ) RESULT(load)
!     USE DefUtils
!     IMPLICIT None
!     TYPE(Model_t) :: model
!     INTEGER :: n
!     REAL(KIND=dp) :: load, coord(3)
!     REAL(KIND=dp) :: Pressure
!     character (len = 40) :: filename  
! 
!     filename = "entities-pressure-in.txt"
! 
!     CALL ReadPressureFromFile( filename, Coord(1), Coord(2), Coord(3), Pressure)
!     load = Pressure
!     
! END FUNCTION readComplexPressure