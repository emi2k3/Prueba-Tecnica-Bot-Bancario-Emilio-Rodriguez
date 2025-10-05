CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

--Veo después si queda muy dificil saber cual es el tipo de consulta o si los datos no sirven
CREATE TYPE tipo_enum AS ENUM ('Consulta', 'Movimiento', 'Prestamo');

CREATE TABLE IF NOT EXISTS Cuenta(
    id_cuenta SERIAL PRIMARY KEY,
    nombre_completo TEXT NOT NULL,
    cedula TEXT UNIQUE NOT NULL,
    email CITEXT NOT NULL UNIQUE,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL,
    saldo INT NOT NULL,
    pin TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Interacciones(
    id_interaccion SERIAL PRIMARY KEY,
    fecha_hora TIMESTAMP NOT NULL,
    tipo tipo_enum NOT NULL DEFAULT 'Consulta',
    id_cuenta INT NOT NULL,
    CONSTRAINT fk_cuenta_id
        FOREIGN KEY (id_cuenta)
        REFERENCES Cuenta (id_cuenta)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movimientos(
    id_movimiento SERIAL PRIMARY KEY,
    importe INT NOT NULL,
    concepto TEXT NOT NULL DEFAULT 'Sin concepto',
    fecha_operacion TIMESTAMP NOT NULL,
    saldo_restante INT NOT NULL,
    id_cuenta INT NOT NULL,
    CONSTRAINT fk_cuenta_id
        FOREIGN KEY (id_cuenta)
        REFERENCES Cuenta (id_cuenta)
        ON DELETE CASCADE


);

CREATE TABLE IF NOT EXISTS Prestamo(
    id_prestamo SERIAL PRIMARY KEY,
    monto_original INT NOT NULL,
    tasa_interes DECIMAL(5,2) NOT NULL,
    cuota_mensual INT NOT NULL,
    plazo_meses INT NOT NULL,
    fecha_otorgamiento DATE NOT NULL DEFAULT CURRENT_DATE,
    id_cuenta INT NOT NULL,
    CONSTRAINT fk_cuenta_id
        FOREIGN KEY (id_cuenta)
        REFERENCES Cuenta (id_cuenta)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Cuota_Prestamo(
    id_cuota SERIAL PRIMARY KEY,
    id_prestamo INT NOT NULL,
    numero_cuota INT NOT NULL,
    monto_cuota INT NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    pagada BOOLEAN DEFAULT FALSE,
    fecha_pago DATE,
    CONSTRAINT fk_prestamo
        FOREIGN KEY (id_prestamo)
        REFERENCES Prestamo (id_prestamo)
        ON DELETE CASCADE
);

CREATE INDEX idx_cuota_prestamo ON Cuota_Prestamo (id_prestamo);
CREATE INDEX idx_pin ON Cuenta (pin);
CREATE INDEX idx_interacciones ON Interacciones (id_cuenta);
CREATE INDEX idx_movimientos ON Movimientos (id_cuenta);
CREATE INDEX idx_prestamo ON Prestamo (id_cuenta);


