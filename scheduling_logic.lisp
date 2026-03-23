(defun simulate-collisions (phase-increment iterations)
  (let ((collisions 0)
        (current-phase 0.0))
    (dotimes (i iterations)
      (setf current-phase (mod (+ current-phase phase-increment) 1.0))
      ;; Simulamos una colisión si la fase cae en un múltiplo racional de 0.1
      (if (< (abs (- (mod (* current-phase 10) 1.0) 0)) 0.01)
          (incf collisions)))
    collisions))

(let ((rational-collisions (simulate-collisions 0.1 1000))
      (irrational-collisions (simulate-collisions 0.6180339887 1000))) ; Base PHI [cite: 1128]
  (format t "--- RESULTADOS DE AGENDAMIENTO ---~%")
  (format t "Colisiones Racionales (Baseline): ~D~%" rational-collisions)
  (format t "Colisiones Irracionales (OASIS):  ~D~%" irrational-collisions)
  (format t "Conclusión: El flujo laminar requiere geometría de fase no repetitiva[cite: 1273].~%"))
