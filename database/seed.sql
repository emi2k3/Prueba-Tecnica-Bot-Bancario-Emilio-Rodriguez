INSERT INTO Cuenta (nombre_completo, cedula, email, direccion, telefono, saldo, pin)
VALUES
    ('Juan Pérez López', '12345678', 'juan.perez@example.com', 'Calle Falsa 123', '598-1234', 95000, crypt('1234', gen_salt('bf'))),
    ('María González Ruiz', '87654321', 'maria.gonzalez@example.com', 'Avenida Siempre Viva 742', '598-2143', 48000, crypt('5678', gen_salt('bf'))),
    ('Carlos Ramírez Soto', '11223344', 'carlos.ramirez@example.com', 'Boulevard de los Sueños 101','598-4321', 120000, crypt('9012', gen_salt('bf')));

-- Movimientos
INSERT INTO Movimientos (importe, concepto, fecha_operacion, saldo_restante, id_cuenta)
VALUES
    (50000, 'Depósito inicial', '2024-09-29', 50000, 1),
    (-5000, 'Retiro ATM', '2024-10-01', 45000, 1),
    (50000, 'Cobro de sueldo', '2024-10-03', 95000, 1),
    (100000, 'Transferencia recibida', '2024-09-24', 100000, 2),
    (-52000, 'Pago cuotas préstamo', '2024-10-02', 48000, 2),
    (120000, 'Depósito inicial', '2024-09-04', 120000, 3);

-- Interacciones
INSERT INTO Interacciones (fecha_hora, tipo, id_cuenta)
VALUES
    ('2024-10-03 10:30:00', 'Consulta', 1),  
    ('2024-10-03 14:20:00', 'Movimiento', 1),
    ('2024-10-01 09:15:00', 'Prestamo', 2),
    ('2024-10-04 11:00:00', 'Consulta', 3);

-- Préstamos
INSERT INTO Prestamo (monto_original, tasa_interes, cuota_mensual, plazo_meses, fecha_otorgamiento, id_cuenta)
VALUES
    (100000, 27.00, 5284, 24, '2024-01-15', 1),
    (50000, 22.00, 2529, 24, '2024-06-01', 2),
    (150000, 28.00, 8212, 36, '2024-03-10', 3);

INSERT INTO Cuota_Prestamo (id_prestamo, numero_cuota, monto_cuota, fecha_vencimiento, pagada, fecha_pago) VALUES
(1, 1, 5284, '2024-02-15', TRUE, '2024-02-14'),
(1, 2, 5284, '2024-03-15', TRUE, '2024-03-14'),
(1, 3, 5284, '2024-04-15', TRUE, '2024-04-14'),
(1, 4, 5284, '2024-05-15', TRUE, '2024-05-14'),
(1, 5, 5284, '2024-06-15', TRUE, '2024-06-14'),
(1, 6, 5284, '2024-07-15', TRUE, '2024-07-14'),
(1, 7, 5284, '2024-08-15', TRUE, '2024-08-14'),
(1, 8, 5284, '2024-09-15', TRUE, '2024-09-14'),
(1, 9, 5284, '2024-10-15', FALSE, NULL),  
(1, 10, 5284, '2024-11-15', FALSE, NULL),
(1, 11, 5284, '2024-12-15', FALSE, NULL),
(1, 12, 5284, '2025-01-15', FALSE, NULL),
(1, 13, 5284, '2025-02-15', FALSE, NULL),
(1, 14, 5284, '2025-03-15', FALSE, NULL),
(1, 15, 5284, '2025-04-15', FALSE, NULL),
(1, 16, 5284, '2025-05-15', FALSE, NULL),
(1, 17, 5284, '2025-06-15', FALSE, NULL),
(1, 18, 5284, '2025-07-15', FALSE, NULL),
(1, 19, 5284, '2025-08-15', FALSE, NULL),
(1, 20, 5284, '2025-09-15', FALSE, NULL),
(1, 21, 5284, '2025-10-15', FALSE, NULL),
(1, 22, 5284, '2025-11-15', FALSE, NULL),
(1, 23, 5284, '2025-12-15', FALSE, NULL),
(1, 24, 5284, '2026-01-15', FALSE, NULL);

INSERT INTO Cuota_Prestamo (id_prestamo, numero_cuota, monto_cuota, fecha_vencimiento, pagada, fecha_pago) VALUES
(2, 1, 2529, '2024-07-01', TRUE, '2024-06-30'),
(2, 2, 2529, '2024-08-01', TRUE, '2024-07-31'),
(2, 3, 2529, '2024-09-01', TRUE, '2024-08-31'),
(2, 4, 2529, '2024-10-01', FALSE, NULL),  -- VENCIDA (3 días de mora)
(2, 5, 2529, '2024-11-01', FALSE, NULL),
(2, 6, 2529, '2024-12-01', FALSE, NULL),
(2, 7, 2529, '2025-01-01', FALSE, NULL),
(2, 8, 2529, '2025-02-01', FALSE, NULL),
(2, 9, 2529, '2025-03-01', FALSE, NULL),
(2, 10, 2529, '2025-04-01', FALSE, NULL),
(2, 11, 2529, '2025-05-01', FALSE, NULL),
(2, 12, 2529, '2025-06-01', FALSE, NULL),
(2, 13, 2529, '2025-07-01', FALSE, NULL),
(2, 14, 2529, '2025-08-01', FALSE, NULL),
(2, 15, 2529, '2025-09-01', FALSE, NULL),
(2, 16, 2529, '2025-10-01', FALSE, NULL),
(2, 17, 2529, '2025-11-01', FALSE, NULL),
(2, 18, 2529, '2025-12-01', FALSE, NULL),
(2, 19, 2529, '2026-01-01', FALSE, NULL),
(2, 20, 2529, '2026-02-01', FALSE, NULL),
(2, 21, 2529, '2026-03-01', FALSE, NULL),
(2, 22, 2529, '2026-04-01', FALSE, NULL),
(2, 23, 2529, '2026-05-01', FALSE, NULL),
(2, 24, 2529, '2026-06-01', FALSE, NULL);

INSERT INTO Cuota_Prestamo (id_prestamo, numero_cuota, monto_cuota, fecha_vencimiento, pagada, fecha_pago) VALUES
(3, 1, 8212, '2024-04-10', TRUE, '2024-04-09'),
(3, 2, 8212, '2024-05-10', TRUE, '2024-05-09'),
(3, 3, 8212, '2024-06-10', TRUE, '2024-06-09'),
(3, 4, 8212, '2024-07-10', TRUE, '2024-07-09'),
(3, 5, 8212, '2024-08-10', TRUE, '2024-08-09'),
(3, 6, 8212, '2024-09-10', TRUE, '2024-09-09'),
(3, 7, 8212, '2024-10-10', FALSE, NULL),  -- Próxima a vencer (6 días)
(3, 8, 8212, '2024-11-10', FALSE, NULL),
(3, 9, 8212, '2024-12-10', FALSE, NULL),
(3, 10, 8212, '2025-01-10', FALSE, NULL),
(3, 11, 8212, '2025-02-10', FALSE, NULL),
(3, 12, 8212, '2025-03-10', FALSE, NULL),
(3, 13, 8212, '2025-04-10', FALSE, NULL),
(3, 14, 8212, '2025-05-10', FALSE, NULL),
(3, 15, 8212, '2025-06-10', FALSE, NULL),
(3, 16, 8212, '2025-07-10', FALSE, NULL),
(3, 17, 8212, '2025-08-10', FALSE, NULL),
(3, 18, 8212, '2025-09-10', FALSE, NULL),
(3, 19, 8212, '2025-10-10', FALSE, NULL),
(3, 20, 8212, '2025-11-10', FALSE, NULL),
(3, 21, 8212, '2025-12-10', FALSE, NULL),
(3, 22, 8212, '2026-01-10', FALSE, NULL),
(3, 23, 8212, '2026-02-10', FALSE, NULL),
(3, 24, 8212, '2026-03-10', FALSE, NULL),
(3, 25, 8212, '2026-04-10', FALSE, NULL),
(3, 26, 8212, '2026-05-10', FALSE, NULL),
(3, 27, 8212, '2026-06-10', FALSE, NULL),
(3, 28, 8212, '2026-07-10', FALSE, NULL),
(3, 29, 8212, '2026-08-10', FALSE, NULL),
(3, 30, 8212, '2026-09-10', FALSE, NULL),
(3, 31, 8212, '2026-10-10', FALSE, NULL),
(3, 32, 8212, '2026-11-10', FALSE, NULL),
(3, 33, 8212, '2026-12-10', FALSE, NULL),
(3, 34, 8212, '2027-01-10', FALSE, NULL),
(3, 35, 8212, '2027-02-10', FALSE, NULL),
(3, 36, 8212, '2027-03-10', FALSE, NULL);