# Apéndice A: Operadores en Espacios de Hilbert Restringidos

## A.1 Proyector de Fibonacci
Sea $\mathcal{H}_{2^N}$ el espacio de Hilbert binario estándar. Definimos el operador proyector $\hat{P}_{\Phi}$ tal que:
205\hat{P}_{\Phi} |s\rangle = 0 \text{ si } s \text{ contiene la subsecuencia '11'}205

## A.2 Hamiltoniano de Información
El operador de energía para el borrado de información en Oasis se define como:
205\hat{H}_{Oasis} = -k_B T \ln(\hat{P}_{\Phi} \rho)205
donde $\rho$ es la matriz de densidad. Este operador tiene autovalores proporcionales a $\ln \phi$, validando la reducción del 30.6% de la disipación térmica.
