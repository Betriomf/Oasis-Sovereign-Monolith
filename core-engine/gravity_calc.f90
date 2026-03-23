program gravity_calc
    implicit none
    real(8) :: kappa_vp, m_info, f_comp, variance_reduction
    
    ! Entrada de constantes vitales reales [cite: 7]
    m_info = 18.0_8  ! Masa Informacional (Usado: 18G) [cite: 34]
    f_comp = 41.4_8  ! Fuerza Computacional medida [cite: 52]
    
    ! Cálculo del Acoplamiento Verlinde-Panzano
    kappa_vp = f_comp / m_info
    
    ! Métrica de mejora estadística calculada en Sección 5.2 [cite: 480]
    variance_reduction = 30.6_8 
    
    print *, "=========================================="
    print *, "   OASIS GRAVITY CALCULATOR (FORTRAN 90)"
    print *, "=========================================="
    print *, "Masa Informacional (bits*chi): ", m_info
    print *, "Acoplamiento (kappa_VP):       ", kappa_vp
    print *, "Reducción de Varianza:         ", variance_reduction, "%"
    
    if (abs(kappa_vp - 2.3) <= 0.17) then
        print *, "ESTADO: FLUJO LAMINAR PURO DETECTADO [cite: 7, 121]"
    else
        print *, "ESTADO: TURBULENCIA DETECTADA"
    end if
end program gravity_calc
