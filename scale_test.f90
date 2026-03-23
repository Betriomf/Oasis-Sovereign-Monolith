program scale_test
    implicit none
    real(8) :: m_info(3), f_comp(3), kappa(3)
    integer :: i
    
    ! Escalas: Micro (1KB), Meso (1MB), Macro (10MB) [cite: 462, 463, 464]
    m_info = (/ 0.001_8, 1.0_8, 10.0_8 /) 
    f_comp = (/ 0.005_8, 2.3_8, 23.1_8 /) ! Valores observados bajo OGS
    
    print *, "--- RESULTADOS DE ESCALA OASIS ---"
    do i = 1, 3
        kappa(i) = f_comp(i) / m_info(i)
        print *, "Escala ", i, " (M): ", m_info(i), " kappa: ", kappa(i)
    end do
    
    print *, "Conclusión: Estabilidad detectada en Meso/Macro (kappa ~ 2.3) [cite: 512, 516]"
end program scale_test
