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
    cuota INT NOT NULL,
    intereses INT NOT NULL,
    vencido BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_vencimiento DATE NOT NULL,
    id_cuenta INT NOT NULL,
    CONSTRAINT fk_cuenta_id
        FOREIGN KEY (id_cuenta)
        REFERENCES Cuenta (id_cuenta)
        ON DELETE CASCADE
); 

CREATE INDEX idx_cedula ON Cuenta (cedula);
CREATE INDEX idx_interacciones ON Interacciones (id_cuenta);
CREATE INDEX idx_movimientos ON Movimientos (id_cuenta);
CREATE INDEX idx_prestamo ON Prestamo (id_cuenta);

