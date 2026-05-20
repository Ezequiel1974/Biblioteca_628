# =====================================================
# BibliotecaDigital628 - CRUD Minimal
# Fecha de creación: 25 de Abril de 2026
# =====================================================

from mysql.connector import connect, Error
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MySql!186932',
    'database': 'BibliotecaDigital628'
}

class Database:
    """Clase para manejar la conexión a la base de datos."""
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos."""
        return connect(**DB_CONFIG)
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Ejecuta una consulta y opcionalmente obtiene resultados."""
        try:
            with Database.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query, params or ())
                    if fetch:
                        return cursor.fetchall()
                    conn.commit()
                    return cursor.lastrowid
        except Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None


class TipoUsuarioCRUD:
    """CRUD para la tabla TipoUsuario."""
    
    @staticmethod
    def create(descripcion):
        query = "INSERT INTO TipoUsuario (descripcion) VALUES (%s)"
        return Database.execute_query(query, (descripcion,))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM TipoUsuario"
        return Database.execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(id_tipo_usuario):
        query = "SELECT * FROM TipoUsuario WHERE id_tipo_usuario = %s"
        return Database.execute_query(query, (id_tipo_usuario,), fetch=True)
    
    @staticmethod
    def update(id_tipo_usuario, descripcion):
        query = "UPDATE TipoUsuario SET descripcion = %s WHERE id_tipo_usuario = %s"
        return Database.execute_query(query, (descripcion, id_tipo_usuario))
    
    @staticmethod
    def delete(id_tipo_usuario):
        query = "DELETE FROM TipoUsuario WHERE id_tipo_usuario = %s"
        return Database.execute_query(query, (id_tipo_usuario,))


class UsuarioCRUD:
    """CRUD para la tabla Usuario."""
    
    @staticmethod
    def create(nombre, apellido, dni, email, telefono, id_tipo_usuario):
        query = """INSERT INTO Usuario 
                   (nombre, apellido, dni, email, telefono, id_tipo_usuario) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        return Database.execute_query(query, (nombre, apellido, dni, email, telefono, id_tipo_usuario))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM Usuario"
        return Database.execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(id_usuario):
        query = "SELECT * FROM Usuario WHERE id_usuario = %s"
        return Database.execute_query(query, (id_usuario,), fetch=True)

    @staticmethod
    def get_by_dni(dni):
        query = "SELECT * FROM Usuario WHERE dni = %s"
        result = Database.execute_query(query, (dni,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def create_if_not_exists(nombre, apellido, dni, email, telefono, id_tipo_usuario):
        existing = UsuarioCRUD.get_by_dni(dni)
        if existing:
            return existing['id_usuario'], existing
        user_id = UsuarioCRUD.create(nombre, apellido, dni, email, telefono, id_tipo_usuario)
        user = UsuarioCRUD.get_by_id(user_id)
        return user_id, user[0] if user else None

    @staticmethod
    def update(id_usuario, nombre, apellido, dni, email, telefono, id_tipo_usuario):
        query = """UPDATE Usuario SET 
                   nombre = %s, apellido = %s, dni = %s, 
                   email = %s, telefono = %s, id_tipo_usuario = %s 
                   WHERE id_usuario = %s"""
        return Database.execute_query(query, (nombre, apellido, dni, email, telefono, id_tipo_usuario, id_usuario))
    
    @staticmethod
    def delete(id_usuario):
        query = "DELETE FROM Usuario WHERE id_usuario = %s"
        return Database.execute_query(query, (id_usuario,))


class CategoriaCRUD:
    """CRUD para la tabla Categoria."""
    
    @staticmethod
    def create(nombre_categoria, descripcion=None):
        query = "INSERT INTO Categoria (nombre_categoria, descripcion) VALUES (%s, %s)"
        return Database.execute_query(query, (nombre_categoria, descripcion))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM Categoria"
        return Database.execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(id_categoria):
        query = "SELECT * FROM Categoria WHERE id_categoria = %s"
        return Database.execute_query(query, (id_categoria,), fetch=True)
    
    @staticmethod
    def update(id_categoria, nombre_categoria, descripcion=None):
        query = "UPDATE Categoria SET nombre_categoria = %s, descripcion = %s WHERE id_categoria = %s"
        return Database.execute_query(query, (nombre_categoria, descripcion, id_categoria))
    
    @staticmethod
    def delete(id_categoria):
        query = "DELETE FROM Categoria WHERE id_categoria = %s"
        return Database.execute_query(query, (id_categoria,))


class EditorialCRUD:
    """CRUD para la tabla Editorial."""
    
    @staticmethod
    def create(nombre_editorial):
        query = "INSERT INTO Editorial (nombre_editorial) VALUES (%s)"
        return Database.execute_query(query, (nombre_editorial,))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM Editorial"
        return Database.execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(id_editorial):
        query = "SELECT * FROM Editorial WHERE id_editorial = %s"
        return Database.execute_query(query, (id_editorial,), fetch=True)
    
    @staticmethod
    def update(id_editorial, nombre_editorial):
        query = "UPDATE Editorial SET nombre_editorial = %s WHERE id_editorial = %s"
        return Database.execute_query(query, (nombre_editorial, id_editorial))
    
    @staticmethod
    def delete(id_editorial):
        query = "DELETE FROM Editorial WHERE id_editorial = %s"
        return Database.execute_query(query, (id_editorial,))


class LibroCRUD:
    """CRUD para la tabla Libro."""
    
    @staticmethod
    def create(titulo, anio_publicacion=None, id_categoria=None):
        query = "INSERT INTO Libro (titulo, anio_publicacion, id_categoria) VALUES (%s, %s, %s)"
        return Database.execute_query(query, (titulo, anio_publicacion, id_categoria))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM Libro"
        return Database.execute_query(query, fetch=True)
    
    @staticmethod
    def get_all_with_category():
        query = """SELECT L.*, C.nombre_categoria AS categoria_nombre
                   FROM Libro L
                   LEFT JOIN Categoria C ON L.id_categoria = C.id_categoria"""
        return Database.execute_query(query, fetch=True)

    @staticmethod
    def get_by_id(id_libro):
        query = "SELECT * FROM Libro WHERE id_libro = %s"
        return Database.execute_query(query, (id_libro,), fetch=True)
    
    @staticmethod
    def update(id_libro, titulo, anio_publicacion=None, id_categoria=None):
        query = "UPDATE Libro SET titulo = %s, anio_publicacion = %s, id_categoria = %s WHERE id_libro = %s"
        return Database.execute_query(query, (titulo, anio_publicacion, id_categoria, id_libro))
    
    @staticmethod
    def delete(id_libro):
        query = "DELETE FROM Libro WHERE id_libro = %s"
        return Database.execute_query(query, (id_libro,))


class PrestamoCRUD:
    """CRUD para la tabla Prestamo."""
    
    @staticmethod
    def create(id_usuario, id_libro, fecha_prestamo, fecha_limite_devolucion, cantidad=1):
        query = """INSERT INTO Prestamo 
                   (id_usuario, id_libro, fecha_prestamo, fecha_limite_devolucion, cantidad) 
                   VALUES (%s, %s, %s, %s, %s)"""
        return Database.execute_query(query, (id_usuario, id_libro, fecha_prestamo, fecha_limite_devolucion, cantidad))
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM Prestamo"
        return Database.execute_query(query, fetch=True)

    @staticmethod
    def get_all_with_details():
        query = """SELECT P.*, U.nombre AS usuario_nombre, U.apellido AS usuario_apellido,
                   U.dni AS usuario_dni, L.titulo AS libro_titulo
                   FROM Prestamo P
                   JOIN Usuario U ON P.id_usuario = U.id_usuario
                   JOIN Libro L ON P.id_libro = L.id_libro"""
        return Database.execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(id_prestamo):
        query = "SELECT * FROM Prestamo WHERE id_prestamo = %s"
        return Database.execute_query(query, (id_prestamo,), fetch=True)
    
    @staticmethod
    def update(id_prestamo, id_usuario, id_libro, fecha_prestamo, fecha_limite_devolucion, cantidad=1, estado_prestamo='Activo'):
        query = """UPDATE Prestamo SET 
                   id_usuario = %s, id_libro = %s, fecha_prestamo = %s, 
                   fecha_limite_devolucion = %s, cantidad = %s, estado_prestamo = %s 
                   WHERE id_prestamo = %s"""
        return Database.execute_query(query, (id_usuario, id_libro, fecha_prestamo, fecha_limite_devolucion, cantidad, estado_prestamo, id_prestamo))
    
    @staticmethod
    def delete(id_prestamo):
        query = "DELETE FROM Prestamo WHERE id_prestamo = %s"
        return Database.execute_query(query, (id_prestamo,))


# =====================================================
# Ejemplo de uso
# =====================================================
if __name__ == "__main__":
    # Ejemplo: Crear un tipo de usuario
    print("=== Ejemplo de uso del CRUD ===\n")
    
    # Crear tipo de usuario
    tipo_id = TipoUsuarioCRUD.create("Alumno")
    print(f"Tipo de usuario creado con ID: {tipo_id}")
    
    # Obtener todos los tipos de usuario
    tipos = TipoUsuarioCRUD.get_all()
    print(f"Tipos de usuario: {tipos}")
    
    # Crear categoría
    cat_id = CategoriaCRUD.create("Ciencia Ficción", "Libros de ciencia ficción")
    print(f"Categoría creada con ID: {cat_id}")
    
    # Crear editorial
    edit_id = EditorialCRUD.create("Planeta")
    print(f"Editorial creada con ID: {edit_id}")
    
    # Crear libro
    libro_id = LibroCRUD.create("Dune", 1965, cat_id)
    print(f"Libro creado con ID: {libro_id}")
    
    # Crear usuario
    usuario_id = UsuarioCRUD.create("Juan", "Pérez", "12345678", "juan@email.com", "555-1234", tipo_id)
    print(f"Usuario creado con ID: {usuario_id}")
    
    # Crear préstamo
    prestamo_id = PrestamoCRUD.create(usuario_id, libro_id, "2026-04-25", "2026-05-25", 1)
    print(f"Préstamo creado con ID: {prestamo_id}")
    
    print("\n=== Operaciones completadas ===")