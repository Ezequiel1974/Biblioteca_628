-- Biblioteca Digital EETP N.º 628
-- Script generado desde schema.dbml

CREATE DATABASE IF NOT EXISTS BibliotecaDigital628
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE BibliotecaDigital628;

-- ============================================
-- 1- Tabla tipo_usuario
-- ============================================
CREATE TABLE IF NOT EXISTS tipo_usuario (
  id_tipo_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 2- Tabla orientacion
-- ============================================
CREATE TABLE IF NOT EXISTS orientacion (
  id_orientacion INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 3- Tabla curso
-- ============================================
CREATE TABLE IF NOT EXISTS curso (
  id_curso INT AUTO_INCREMENT PRIMARY KEY,
  descripcion VARCHAR(10) NOT NULL,
  anio TINYINT NOT NULL,
  division CHAR(1) NOT NULL,
  turno VARCHAR(10) NOT NULL,
  id_orientacion INT NOT NULL,
  UNIQUE INDEX ux_curso_anio_division (anio, division),
  CONSTRAINT fk_curso_orientacion FOREIGN KEY (id_orientacion) 
    REFERENCES orientacion(id_orientacion) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 4- Tabla usuario
-- ============================================
CREATE TABLE IF NOT EXISTS usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  dni VARCHAR(15) NOT NULL UNIQUE,
  telefono VARCHAR(20),
  email VARCHAR(100),
  fecha_alta TIMESTAMP NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  id_tipo_usuario INT NOT NULL,
  id_curso INT,
  CONSTRAINT fk_usuario_tipo_usuario FOREIGN KEY (id_tipo_usuario) 
    REFERENCES tipo_usuario(id_tipo_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_usuario_curso FOREIGN KEY (id_curso) 
    REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 5- Tabla editorial
-- ============================================
CREATE TABLE IF NOT EXISTS editorial (
  id_editorial INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 6- Tabla autor
-- ============================================
CREATE TABLE IF NOT EXISTS autor (
  id_autor INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 7- Tabla categoria
-- ============================================
CREATE TABLE IF NOT EXISTS categoria (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 8- Tabla libro
-- ============================================
CREATE TABLE IF NOT EXISTS libro (
  id_libro INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  anio_publicacion YEAR,
  stock_total INT NOT NULL,
  id_editorial INT NOT NULL,
  CONSTRAINT fk_libro_editorial FOREIGN KEY (id_editorial) 
    REFERENCES editorial(id_editorial) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 9- Tabla libro_autor
-- ============================================
CREATE TABLE IF NOT EXISTS libro_autor (
  id_libro INT NOT NULL,
  id_autor INT NOT NULL,
  PRIMARY KEY (id_libro, id_autor),
  CONSTRAINT fk_libro_autor_libro FOREIGN KEY (id_libro) 
    REFERENCES libro(id_libro) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_libro_autor_autor FOREIGN KEY (id_autor) 
    REFERENCES autor(id_autor) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 10- Tabla libro_categoria
-- ============================================
CREATE TABLE IF NOT EXISTS libro_categoria (
  id_libro INT NOT NULL,
  id_categoria INT NOT NULL,
  PRIMARY KEY (id_libro, id_categoria),
  CONSTRAINT fk_libro_categoria_libro FOREIGN KEY (id_libro) 
    REFERENCES libro(id_libro) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_libro_categoria_categoria FOREIGN KEY (id_categoria) 
    REFERENCES categoria(id_categoria) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 11- Tabla tipo_prestamo
-- ============================================
CREATE TABLE IF NOT EXISTS tipo_prestamo (
  id_tipo_prestamo INT AUTO_INCREMENT PRIMARY KEY,
  descripcion_prestamo VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 12- Tabla prestamo
-- ============================================
CREATE TABLE IF NOT EXISTS prestamo (
  id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
  fecha_prestamo DATE NOT NULL,
  fecha_devolucion DATE NOT NULL,
  cantidad INT NOT NULL,
  observaciones VARCHAR(255),
  id_tipo_prestamo INT NOT NULL,
  id_solicitante INT NOT NULL,
  id_responsable INT NOT NULL,
  id_libro INT NOT NULL,
  id_curso INT,
  CONSTRAINT fk_prestamo_tipo_prestamo FOREIGN KEY (id_tipo_prestamo) 
    REFERENCES tipo_prestamo(id_tipo_prestamo) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_prestamo_solicitante FOREIGN KEY (id_solicitante) 
    REFERENCES usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_prestamo_responsable FOREIGN KEY (id_responsable) 
    REFERENCES usuario(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_prestamo_libro FOREIGN KEY (id_libro) 
    REFERENCES libro(id_libro) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_prestamo_curso FOREIGN KEY (id_curso) 
    REFERENCES curso(id_curso) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
