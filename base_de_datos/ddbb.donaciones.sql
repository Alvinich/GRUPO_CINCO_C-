CREATE DATABASE donaciones;
USE donaciones;
CREATE TABLE donante (
    id_donante INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pais VARCHAR(50),
    tipo ENUM('local','internacional') NOT NULL
);

CREATE TABLE programa (
    id_programa INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    aldea VARCHAR(100)
);

CREATE TABLE metodo_pago (
    id_metodo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,      -- QR, billetera móvil, tarjeta, transferencia
    pasarela VARCHAR(50)
);

CREATE TABLE compromiso (
    id_compromiso INT PRIMARY KEY AUTO_INCREMENT,
    id_donante INT NOT NULL,
    id_programa INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    frecuencia ENUM('unico','mensual','anual') NOT NULL,
    fecha_inicio DATE NOT NULL,
    estado ENUM('activo','pausado','cancelado') DEFAULT 'activo',
    FOREIGN KEY (id_donante) REFERENCES donante(id_donante),
    FOREIGN KEY (id_programa) REFERENCES programa(id_programa)
);

CREATE TABLE pago (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    id_compromiso INT NOT NULL,
    id_metodo INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL,
    estado ENUM('pendiente','exitoso','fallido') DEFAULT 'pendiente',
    referencia_pasarela VARCHAR(100) UNIQUE,
    conciliado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_compromiso) REFERENCES compromiso(id_compromiso),
    FOREIGN KEY (id_metodo) REFERENCES metodo_pago(id_metodo)
);

CREATE TABLE reporte (
    id_reporte INT PRIMARY KEY AUTO_INCREMENT,
    id_programa INT NOT NULL,
    id_donante INT NOT NULL,
    fecha DATE NOT NULL,
    contenido TEXT,
    FOREIGN KEY (id_programa) REFERENCES programa(id_programa),
    FOREIGN KEY (id_donante) REFERENCES donante(id_donante)
);
INSERT INTO donante (nombre , email ,pais , tipo ) 
VALUES ('Ruben','Ruben@gmail.com' , 'Australia', 'internacional');
SELECT * FROM donante;
