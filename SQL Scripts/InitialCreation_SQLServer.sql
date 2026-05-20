-- =====================================================
-- Script de Creación de Base de Datos: BibliotecaDigital628
-- Adaptado para SQL Server
-- Fecha de creación: 25 de Abril de 2026
-- =====================================================

-- Crear la base de datos si no existe
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'BibliotecaDigital628')
BEGIN
    CREATE DATABASE BibliotecaDigital628;
END
GO

USE BibliotecaDigital628;
GO

-- 1. Tabla TipoUsuario (Ej: Alumno, Docente, etc.)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TipoUsuario')
BEGIN
    CREATE TABLE TipoUsuario (
        id_tipo_usuario INT IDENTITY(1,1) PRIMARY KEY,
        descripcion VARCHAR(50) NOT NULL
    );
END
GO

-- 2. Tabla Usuario
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Usuario')
BEGIN
    CREATE TABLE Usuario (
        id_usuario INT IDENTITY(1,1) PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        dni VARCHAR(20) UNIQUE NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        telefono VARCHAR(20),
        id_tipo_usuario INT NOT NULL,
        FOREIGN KEY (id_tipo_usuario) REFERENCES TipoUsuario(id_tipo_usuario)
    );
END
GO

-- 3. Tabla Categoria
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Categoria')
BEGIN
    CREATE TABLE Categoria (
        id_categoria INT IDENTITY(1,1) PRIMARY KEY,
        nombre_categoria VARCHAR(100) NOT NULL,
        descripcion NVARCHAR(MAX)
    );
END
GO

-- 4. Tabla Editorial
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Editorial')
BEGIN
    CREATE TABLE Editorial (
        id_editorial INT IDENTITY(1,1) PRIMARY KEY,
        nombre_editorial VARCHAR(150) NOT NULL
    );
END
GO

-- 5. Tabla Libro
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Libro')
BEGIN
    CREATE TABLE Libro (
        id_libro INT IDENTITY(1,1) PRIMARY KEY,
        titulo VARCHAR(200) NOT NULL,
        anio_publicacion INT,
        id_categoria INT,
        FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
    );
END
GO

-- 6. Tabla LibroEditorial (Tabla intermedia para relación muchos a muchos)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'LibroEditorial')
BEGIN
    CREATE TABLE LibroEditorial (
        id_libro_editorial INT IDENTITY(1,1) PRIMARY KEY,
        id_libro INT NOT NULL,
        id_editorial INT NOT NULL,
        FOREIGN KEY (id_libro) REFERENCES Libro(id_libro) ON DELETE CASCADE,
        FOREIGN KEY (id_editorial) REFERENCES Editorial(id_editorial) ON DELETE CASCADE
    );
END
GO

-- 7. Tabla Prestamo
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Prestamo')
BEGIN
    CREATE TABLE Prestamo (
        id_prestamo INT IDENTITY(1,1) PRIMARY KEY,
        id_usuario INT NOT NULL,
        id_libro INT NOT NULL,
        fecha_prestamo DATE NOT NULL,
        fecha_limite_devolucion DATE NOT NULL,
        cantidad INT NOT NULL DEFAULT 1, -- Especifica la cantidad de copias prestadas
        estado_prestamo VARCHAR(20) DEFAULT 'Activo',
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
        FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
    );
END
GO