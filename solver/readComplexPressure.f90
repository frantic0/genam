
FUNCTION readRealPressure( model, node, coord ) RESULT(load)
  USE DefUtils
  IMPLICIT None
  
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
  
  open( unit = 1, file = "entities-pressure-in.dat" )

  ! read first line with transducer array configuration to set EOL in the data read cycle
  read(1,*) m, n
  ! print *, m, n 

  ! allocate memory for multi-dimensional array
  allocate ( darray( m*n, col ) )     

  ! print *, node,',', Coord(1),',', Coord(2),',', Coord(3),','

  do I=1,n*m,1
    read(1,*) darray(I,:)
    ! print*, "darray(",I,") = ", darray(I,:)           
  enddo
  
  min_diff = 2147483647
  do k = 1, m*n            
    do j = 1, col                          
      ! print*, "darray(",k,",",j,") = ", darray(k,j)           
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
  
  ! print*, "real pressure = ", p           
  Pressure = p
  
  ! CALL ReadPressureFromFile( filename, Coord(1), Coord(2), Coord(3), Pressure)
  load = Pressure
  

END FUNCTION readRealPressure




FUNCTION readImaginaryPressure( model, node, coord ) RESULT(load)
  USE DefUtils
  IMPLICIT None
  
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

  open( unit = 1, file = "entities-pressure-in.dat" )


  ! read first line with transducer array configuration to set EOL in the data read cycle
  read(1,*) m, n
  ! print *, m, n 

  ! allocate memory for multi-dimensional array
  allocate ( darray( m*n, col ) )     

  ! print *, node,',', Coord(1),',', Coord(2),',', Coord(3),','

  do I=1,n*m,1
    read(1,*) darray(I,:)
    ! print*, "darray(",I,") = ", darray(I,:)           
  enddo
  
  min_diff = 2147483647
  do k = 1, m*n            
    ! do j = 1, col                          
      ! print*, "darray(",k,",",j,") = ", darray(k,j)           
    ! end do
      
    diff_coord_x = ABS( Coord(1) - darray(k,1) )   
    diff_coord_y = ABS( Coord(2) - darray(k,2) ) 
    euclidean_distance = SQRT( diff_coord_x*diff_coord_x + diff_coord_y*diff_coord_y )   
      
    IF ( min_diff > euclidean_distance ) THEN  
      min_diff = euclidean_distance
      p = darray(k,4)
    END IF
    ! print*, "min_diff - ",min_diff ," - ",diff_coord_x,",",diff_coord_y,") = ", p          
  end do    
  
  close(1)
  deallocate (darray) 
  
  ! print*, "imaginary pressure = ", p           
  Pressure = p
  
  load = Pressure
  

END FUNCTION readImaginaryPressure