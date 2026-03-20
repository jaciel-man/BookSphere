CREATE DATABASE IF NOT EXISTS BookSphere;
USE BookSphere;


CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono CHAR(10),
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_registro DATE NOT NULL,
    fecha_nacimiento CHAR(8),
    clave VARCHAR(50)
) ENGINE=InnoDB;


CREATE TABLE Libro (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria VARCHAR(50),
    publicacion CHAR(8)
) ENGINE=InnoDB;


CREATE TABLE Compra (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estado ENUM('pendiente', 'pagada', 'cancelada') DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE DetalleCompra (
    id_compra INT NOT NULL,
    id_libro INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    PRIMARY KEY (id_compra, id_libro),
    FOREIGN KEY (id_compra) REFERENCES Compra(id_compra)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Administrador (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,   -- Almacenar hash de la contraseña
    rol ENUM('superadmin', 'admin', 'editor') DEFAULT 'admin',
    ultimo_acceso DATETIME,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


CREATE INDEX idx_compra_usuario ON Compra(id_usuario);
CREATE INDEX idx_detalle_libro ON DetalleCompra(id_libro);
CREATE INDEX idx_administrador_email ON Administrador(email);

ALTER TABLE Usuario ADD COLUMN rol ENUM('usuario', 'admin') DEFAULT 'usuario';

CREATE TABLE Categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO Categoria (nombre) VALUES ('Todos'), ('Ficción'), ('No ficción'), ('Infantil'), ('Revistas'), ('Tesis');

ALTER TABLE Libro ADD COLUMN id_categoria INT;
ALTER TABLE Libro ADD FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria);

INSERT INTO Usuario (nombre, telefono, email, fecha_registro, fecha_nacimiento, clave, rol)
VALUES ('Administrador', '0000000000', 'admin@biblioteca.com', CURDATE(), '20000101', 'admin', 'admin');

