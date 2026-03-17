import datetime

def create_invoice(client_name, amount_eur):
    invoice_id = f"OASIS-{datetime.datetime.now().strftime('%Y%m%d')}-001"
    date = datetime.date.today().strftime("%d/%m/%Y")
    
    content = f"""
============================================================
           🏛️ OASIS SOVEREIGN MONOLITH - INVOICE
============================================================
ID FACTURA: {invoice_id}
FECHA: {date}
EMISOR: Mariano Panzano Caballé (Barcelona, España)
IBAN: ES36 0182 1756 1802 0152 9233
------------------------------------------------------------
CLIENTE: {client_name}
CONCEPTO: Licencia Comercial ODSC v1.0
DETALLE: Optimización de Eficiencia Landauer (+30.6%)
         Inhibición de Telemetría Profunda
         Topología de Perelman (Coherencia 0.00005294)
------------------------------------------------------------
TOTAL: {amount_eur} EUR
------------------------------------------------------------
MOTIVO DEL VALOR:
El cliente paga por el ahorro energético real y la 
eliminación de singularidades en su infraestructura.
============================================================
Factura generada bajo la Jurisdicción Euler-Fibonacci.
"""
    with open(f"INVOICE_{invoice_id}.txt", "w") as f:
        f.write(content)
    print(f"✅ Factura {invoice_id} generada con éxito para {client_name}")

# Simulación de cobro de licencia comercial
create_invoice("CORPORATE_CLIENT_001", 1000)
