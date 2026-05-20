-- Crear la base de datos si no existe y usarla
CREATE DATABASE IF NOT EXISTS BibliotecaDigital628;
USE BibliotecaDigital628;

-- 1. Tabla TipoUsuario (Ej: Alumno, Docente, etc.)
CREATE TABLE TipoUsuario (
    id_tipo_usuario INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- 2. Tabla Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    id_tipo_usuario INT NOT NULL,
    FOREIGN KEY (id_tipo_usuario) REFERENCES TipoUsuario(id_tipo_usuario)
);

-- 3. Tabla Categoria
CREATE TABLE Categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- 4. Tabla Editorial
CREATE TABLE Editorial (
    id_editorial INT AUTO_INCREMENT PRIMARY KEY,
    nombre_editorial VARCHAR(150) NOT NULL
);

-- 5. Tabla Libro
CREATE TABLE Libro (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    anio_publicacion INT,
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);

-- 6. Tabla LibroEditorial (Tabla intermedia para relación muchos a muchos)
CREATE TABLE LibroEditorial (
    id_libro_editorial INT AUTO_INCREMENT PRIMARY KEY,
    id_libro INT NOT NULL,
    id_editorial INT NOT NULL,
    FOREIGN KEY (id_libro) REFERENCES Libro(id_libro) ON DELETE CASCADE,
    FOREIGN KEY (id_editorial) REFERENCES Editorial(id_editorial) ON DELETE CASCADE
);

-- 7. Tabla Prestamo
CREATE TABLE Prestamo (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_limite_devolucion DATE NOT NULL,
    cantidad INT NOT NULL DEFAULT 1, -- Especifica la cantidad de copias prestadas
    estado_prestamo VARCHAR(20) DEFAULT 'Activo',
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES Libro(id_libro)
);