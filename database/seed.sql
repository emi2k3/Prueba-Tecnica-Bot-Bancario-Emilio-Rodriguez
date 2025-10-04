INSERT INTO Cuenta (nombre_completo, cedula, email, direccion, telefono,saldo, pin)
VALUES 
    ('Juan Pérez López', '12345678', 'juan.perez@example.com', 'Calle Falsa 123, Ciudad Ejemplo', '598-1234',20000, crypt('1234', gen_salt('bf'))),
    ('María González Ruiz', '87654321', 'maria.gonzalez@example.com', 'Avenida Siempre Viva 742, Otra Ciudad', '598-2143', 15000, crypt('5678', gen_salt('bf'))),
    ('Carlos Ramírez Soto', '11223344', 'carlos.ramirez@example.com', 'Boulevard de los Sueños 101, Pueblo Nuevo','598-4321',40000,  crypt('9012', gen_salt('bf')));

INSERT INTO Interacciones (fecha_hora, tipo, id_cuenta)
VALUES 
    (CURRENT_TIMESTAMP - INTERVAL '1 day', 'Consulta', 1),  
    (CURRENT_TIMESTAMP - INTERVAL '2 hours', 'Movimiento', 1), 
    (CURRENT_TIMESTAMP - INTERVAL '3 days', 'Prestamo', 2), 
    (CURRENT_TIMESTAMP, 'Consulta', 3); 

INSERT INTO Movimientos (importe, concepto, fecha_operacion, saldo_restante, id_cuenta)
VALUES 
    (5000, 'Depósito inicial', CURRENT_TIMESTAMP - INTERVAL '5 days', 5000, 1),  -- Depósito 
    (-2000, 'Retiro ATM', CURRENT_TIMESTAMP - INTERVAL '1 day', 3000, 1),  -- Retiro 
    (10000, 'Transferencia recibida', CURRENT_TIMESTAMP - INTERVAL '10 days', 10000, 2),  -- Depósito 
    (-1500, 'Pago servicios', CURRENT_TIMESTAMP - INTERVAL '2 days', 8500, 2);  -- Gasto 

INSERT INTO Prestamo (cuota, intereses, vencido, fecha_vencimiento, id_cuenta)
VALUES 
    (4500, 600, FALSE, '2025-12-01', 1),  --  no vencido
    (3000, 400, TRUE, '2025-09-15', 2),  -- vencido
    (2000, 300, FALSE, '2026-01-10', 3);  --  no vencido