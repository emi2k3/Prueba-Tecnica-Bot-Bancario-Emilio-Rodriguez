INSERT INTO Cuenta (nombre_completo, cedula, email, direccion, telefono, saldo, pin)
VALUES
    ('Juan Pérez López', '12345678', 'juan.perez@example.com', 'Calle Falsa 123', '598-1234', 95000, crypt('1234', gen_salt('bf'))),
    ('María González Ruiz', '87654321', 'maria.gonzalez@example.com', 'Avenida Siempre Viva 742', '598-2143', 48000, crypt('5678', gen_salt('bf'))),
    ('Carlos Ramírez Soto', '11223344', 'carlos.ramirez@example.com', 'Boulevard de los Sueños 101','598-4321', 120000, crypt('9012', gen_salt('bf')));

-- CUENTA 1: dos préstamos
INSERT INTO Prestamo (monto_original, tasa_interes, cuota_mensual, plazo_meses, fecha_otorgamiento, id_cuenta)
VALUES
    (100000, 27.00, 5284, 24, '2024-01-15', 1),
    (50000, 28.00, 2150, 12, '2025-03-01', 1);

-- CUENTA 2: un préstamo, una cuota atrasada
INSERT INTO Prestamo (monto_original, tasa_interes, cuota_mensual, plazo_meses, fecha_otorgamiento, id_cuenta)
VALUES
    (50000, 25.00, 2529, 24, '2024-09-01', 2);

INSERT INTO Cuota_Prestamo (id_prestamo, numero_cuota, monto_cuota, fecha_vencimiento, pagada, fecha_pago)
VALUES
(1, 1, 5284, '2024-02-15', TRUE, '2024-02-14'),
(1, 2, 5284, '2024-03-15', TRUE, '2024-03-14'),
(1, 3, 5284, '2024-04-15', TRUE, '2024-04-14'),
(1, 4, 5284, '2024-05-15', TRUE, '2024-05-14'),
(1, 5, 5284, '2024-06-15', TRUE, '2024-06-14'),
(1, 6, 5284, '2024-07-15', TRUE, '2024-07-14'),
(1, 7, 5284, '2024-08-15', TRUE, '2024-08-14'),
(1, 8, 5284, '2024-09-15', TRUE, '2024-09-14'),
(1, 9, 5284, '2024-10-15', TRUE, '2024-10-14'),
(1,10, 5284, '2024-11-15', TRUE, '2024-11-14'),
(1,11, 5284, '2024-12-15', TRUE, '2024-12-14'),
(1,12, 5284, '2025-01-15', TRUE, '2025-01-14'),
(1,13, 5284, '2025-02-15', TRUE, '2025-02-14'),
(1,14, 5284, '2025-03-15', TRUE, '2025-03-14'),
(1,15, 5284, '2025-04-15', TRUE, '2025-04-14'),
(1,16, 5284, '2025-05-15', TRUE, '2025-05-14'),
(1,17, 5284, '2025-06-15', TRUE, '2025-06-14'),
(1,18, 5284, '2025-07-15', TRUE, '2025-07-14'),
(1,19, 5284, '2025-08-15', TRUE, '2025-08-14'),
(1,20, 5284, '2025-09-15', TRUE, '2025-09-14'),
(1,21, 5284, '2025-10-15', FALSE, NULL),  
(1,22, 5284, '2025-11-15', FALSE, NULL),
(1,23, 5284, '2025-12-15', FALSE, NULL),
(1,24, 5284, '2026-01-15', FALSE, NULL);

INSERT INTO Cuota_Prestamo (id_prestamo, numero_cuota, monto_cuota, fecha_vencimiento, pagada, fecha_pago)
VALUES
(2, 1, 2150, '2025-04-01', TRUE, '2025-04-01'),
(2, 2, 2150, '2025-05-01', TRUE, '2025-05-01'),
(2, 3, 2150, '2025-06-01', TRUE, '2025-06-01'),
(2, 4, 2150, '2025-07-01', TRUE, '2025-07-01'),
(2, 5, 2150, '2025-08-01', TRUE, '2025-08-01'),
(2, 6, 2150, '2025-09-01', TRUE, '2025-09-01'),
(2, 7, 2150, '2025-10-01', FALSE, NULL); -- Única cuota atrasada (vencida 5 días)

-- CUENTA 2 (María González): cuotas para préstamo 3
INSERT INTO Cuota_Prestamo (id_prestamo, numero_cuota, monto_cuota, fecha_vencimiento, pagada, fecha_pago)
VALUES
(3, 1, 2529, '2024-10-01', TRUE, '2024-10-01'),
(3, 2, 2529, '2024-11-01', TRUE, '2024-11-01'),
(3, 3, 2529, '2024-12-01', TRUE, '2024-12-01'),
(3, 4, 2529, '2025-01-01', TRUE, '2025-01-01'),
(3, 5, 2529, '2025-02-01', TRUE, '2025-02-01'),
(3, 6, 2529, '2025-03-01', TRUE, '2025-03-01'),
(3, 7, 2529, '2025-04-01', TRUE, '2025-04-01'),
(3, 8, 2529, '2025-05-01', TRUE, '2025-05-01'),
(3, 9, 2529, '2025-06-01', TRUE, '2025-06-01'),
(3, 10, 2529, '2025-07-01', TRUE, '2025-07-01'),
(3, 11, 2529, '2025-08-01', TRUE, '2025-08-01'),
(3, 12, 2529, '2025-09-01', TRUE, '2025-09-01'),
(3, 13, 2529, '2025-10-01', FALSE, NULL), -- Cuota vencida (morosa)
(3, 14, 2529, '2025-11-01', FALSE, NULL),
(3, 15, 2529, '2025-12-01', FALSE, NULL),
(3, 16, 2529, '2026-01-01', FALSE, NULL),
(3, 17, 2529, '2026-02-01', FALSE, NULL),
(3, 18, 2529, '2026-03-01', FALSE, NULL),
(3, 19, 2529, '2026-04-01', FALSE, NULL),
(3, 20, 2529, '2026-05-01', FALSE, NULL),
(3, 21, 2529, '2026-06-01', FALSE, NULL),
(3, 22, 2529, '2026-07-01', FALSE, NULL),
(3, 23, 2529, '2026-08-01', FALSE, NULL),
(3, 24, 2529, '2026-09-01', FALSE, NULL);

-- Movimientos

INSERT INTO Movimientos (importe, concepto, fecha_operacion, saldo_restante, id_cuenta)
VALUES
    (-5284, 'Pago cuota préstamo #1', '2025-10-04', 89716, 1),
    (-2150, 'Pago cuota préstamo #2', '2025-10-04', 87566, 1),
    (7434, 'Bono por desempeño', '2025-10-05', 95000, 1);

INSERT INTO Movimientos (importe, concepto, fecha_operacion, saldo_restante, id_cuenta)
VALUES
    (-8000, 'Pago servicios', '2025-10-03', 40000, 2),
    (-5000, 'Retiro ATM', '2025-10-04', 35000, 2),
    (13000, 'Freelance', '2025-10-05', 48000, 2);

INSERT INTO Movimientos (importe, concepto, fecha_operacion, saldo_restante, id_cuenta)
VALUES
    (-15000, 'Compra electrodoméstico', '2025-10-02', 105000, 3),
    (-10000, 'Inversión plazo fijo', '2025-10-03', 95000, 3),
    (25000, 'Vencimiento inversión', '2025-10-04', 120000, 3);