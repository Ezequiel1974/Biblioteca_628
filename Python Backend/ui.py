from datetime import date, timedelta

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from crud import (
    CategoriaCRUD,
    EditorialCRUD,
    LibroCRUD,
    PrestamoCRUD,
    TipoUsuarioCRUD,
    UsuarioCRUD,
)


class BibliotecaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biblioteca Digital - CRUD")
        self.resize(1200, 760)

        tabs = QTabWidget()
        tabs.addTab(self.create_libros_tab(), "Libros")
        tabs.addTab(self.create_prestamos_tab(), "Préstamos")
        tabs.addTab(self.create_usuarios_tab(), "Usuarios")
        tabs.addTab(self.create_categorias_tab(), "Categorías")
        tabs.addTab(self.create_config_tab(), "Configuración")

        self.setCentralWidget(tabs)

    def create_libros_tab(self):
        widget = QWidget()
        main_layout = QHBoxLayout(widget)

        self.libro_table = QTableWidget(0, 4)
        self.libro_table.setHorizontalHeaderLabels(["ID", "Título", "Año", "Categoría"])
        self.libro_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.libro_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.libro_table.cellClicked.connect(self.on_libro_selected)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Libros existentes"))
        left_layout.addWidget(self.libro_table)

        form = QGroupBox("Datos del Libro")
        form_layout = QHBoxLayout(form)

        self.libro_title_input = QLineEdit()
        self.libro_year_input = QSpinBox()
        self.libro_year_input.setRange(1000, date.today().year + 5)
        self.libro_category_combo = QComboBox()
        self.libro_category_combo.addItem("(Ninguna)", None)

        form_layout.addWidget(QLabel("Título:"))
        form_layout.addWidget(self.libro_title_input)
        form_layout.addWidget(QLabel("Año:"))
        form_layout.addWidget(self.libro_year_input)
        form_layout.addWidget(QLabel("Categoría:"))
        form_layout.addWidget(self.libro_category_combo)

        buttons = QHBoxLayout()
        self.libro_new_btn = QPushButton("Nuevo")
        self.libro_save_btn = QPushButton("Guardar")
        self.libro_delete_btn = QPushButton("Eliminar")
        self.libro_refresh_btn = QPushButton("Refrescar")
        self.libro_new_btn.clicked.connect(self.clear_libro_form)
        self.libro_save_btn.clicked.connect(self.save_libro)
        self.libro_delete_btn.clicked.connect(self.delete_libro)
        self.libro_refresh_btn.clicked.connect(self.load_libros)

        buttons.addWidget(self.libro_new_btn)
        buttons.addWidget(self.libro_save_btn)
        buttons.addWidget(self.libro_delete_btn)
        buttons.addWidget(self.libro_refresh_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Formulario de libro"))
        right_layout.addWidget(form)
        right_layout.addLayout(buttons)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.selected_libro_id = None
        self.load_categoria_options()
        self.load_libros()
        return widget

    def create_usuarios_tab(self):
        widget = QWidget()
        main_layout = QHBoxLayout(widget)

        self.usuario_table = QTableWidget(0, 7)
        self.usuario_table.setHorizontalHeaderLabels([
            "ID",
            "Nombre",
            "Apellido",
            "DNI",
            "Email",
            "Teléfono",
            "Tipo de Usuario",
        ])
        self.usuario_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.usuario_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.usuario_table.cellClicked.connect(self.on_usuario_selected)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Usuarios existentes"))
        left_layout.addWidget(self.usuario_table)

        form = QGroupBox("Datos del Usuario")
        form_layout = QHBoxLayout(form)

        self.usuario_nombre_input = QLineEdit()
        self.usuario_apellido_input = QLineEdit()
        self.usuario_dni_input = QLineEdit()
        self.usuario_email_input = QLineEdit()
        self.usuario_telefono_input = QLineEdit()
        self.usuario_tipo_combo = QComboBox()

        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.usuario_nombre_input)
        form_layout.addWidget(QLabel("Apellido:"))
        form_layout.addWidget(self.usuario_apellido_input)
        form_layout.addWidget(QLabel("DNI:"))
        form_layout.addWidget(self.usuario_dni_input)
        form_layout.addWidget(QLabel("Email:"))
        form_layout.addWidget(self.usuario_email_input)
        form_layout.addWidget(QLabel("Teléfono:"))
        form_layout.addWidget(self.usuario_telefono_input)
        form_layout.addWidget(QLabel("Tipo:"))
        form_layout.addWidget(self.usuario_tipo_combo)

        buttons = QHBoxLayout()
        self.usuario_new_btn = QPushButton("Nuevo")
        self.usuario_save_btn = QPushButton("Guardar")
        self.usuario_delete_btn = QPushButton("Eliminar")
        self.usuario_refresh_btn = QPushButton("Refrescar")
        self.usuario_new_btn.clicked.connect(self.clear_usuario_form)
        self.usuario_save_btn.clicked.connect(self.save_usuario)
        self.usuario_delete_btn.clicked.connect(self.delete_usuario)
        self.usuario_refresh_btn.clicked.connect(self.load_usuarios)

        buttons.addWidget(self.usuario_new_btn)
        buttons.addWidget(self.usuario_save_btn)
        buttons.addWidget(self.usuario_delete_btn)
        buttons.addWidget(self.usuario_refresh_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Formulario de usuario"))
        right_layout.addWidget(form)
        right_layout.addLayout(buttons)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.selected_usuario_id = None
        self.load_tipo_usuario_options()
        self.load_usuarios()
        return widget

    def create_prestamos_tab(self):
        widget = QWidget()
        main_layout = QHBoxLayout(widget)

        self.prestamo_table = QTableWidget(0, 8)
        self.prestamo_table.setHorizontalHeaderLabels([
            "ID",
            "Usuario",
            "DNI",
            "Libro",
            "Fecha Prestamo",
            "Fecha Límite",
            "Cantidad",
            "Estado",
        ])
        self.prestamo_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.prestamo_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.prestamo_table.cellClicked.connect(self.on_prestamo_selected)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Préstamos existentes"))
        left_layout.addWidget(self.prestamo_table)

        form = QGroupBox("Préstamo")
        form_layout = QVBoxLayout(form)

        row1 = QHBoxLayout()
        self.prestamo_dni_input = QLineEdit()
        self.prestamo_nombre_input = QLineEdit()
        self.prestamo_apellido_input = QLineEdit()
        self.prestamo_email_input = QLineEdit()
        self.prestamo_telefono_input = QLineEdit()
        self.prestamo_tipo_combo = QComboBox()

        row1.addWidget(QLabel("DNI:"))
        row1.addWidget(self.prestamo_dni_input)
        row1.addWidget(QLabel("Nombre:"))
        row1.addWidget(self.prestamo_nombre_input)
        row1.addWidget(QLabel("Apellido:"))
        row1.addWidget(self.prestamo_apellido_input)
        row1.addWidget(QLabel("Email:"))
        row1.addWidget(self.prestamo_email_input)
        row1.addWidget(QLabel("Teléfono:"))
        row1.addWidget(self.prestamo_telefono_input)
        row1.addWidget(QLabel("Tipo:"))
        row1.addWidget(self.prestamo_tipo_combo)

        row2 = QHBoxLayout()
        self.prestamo_libro_combo = QComboBox()
        self.prestamo_fecha_input = QDateEdit()
        self.prestamo_fecha_input.setCalendarPopup(True)
        self.prestamo_fecha_input.setDate(QDate.currentDate())
        self.prestamo_limite_input = QDateEdit()
        self.prestamo_limite_input.setCalendarPopup(True)
        self.prestamo_limite_input.setDate(QDate.currentDate().addDays(7))
        self.prestamo_cantidad_input = QSpinBox()
        self.prestamo_cantidad_input.setRange(1, 10)

        row2.addWidget(QLabel("Libro:"))
        row2.addWidget(self.prestamo_libro_combo)
        row2.addWidget(QLabel("Fecha préstamo:"))
        row2.addWidget(self.prestamo_fecha_input)
        row2.addWidget(QLabel("Fecha límite:"))
        row2.addWidget(self.prestamo_limite_input)
        row2.addWidget(QLabel("Cantidad:"))
        row2.addWidget(self.prestamo_cantidad_input)

        form_layout.addLayout(row1)
        form_layout.addLayout(row2)

        buttons = QHBoxLayout()
        self.prestamo_new_btn = QPushButton("Nuevo")
        self.prestamo_save_btn = QPushButton("Guardar")
        self.prestamo_delete_btn = QPushButton("Eliminar")
        self.prestamo_refresh_btn = QPushButton("Refrescar")
        self.prestamo_new_btn.clicked.connect(self.clear_prestamo_form)
        self.prestamo_save_btn.clicked.connect(self.save_prestamo)
        self.prestamo_delete_btn.clicked.connect(self.delete_prestamo)
        self.prestamo_refresh_btn.clicked.connect(self.load_prestamos)

        buttons.addWidget(self.prestamo_new_btn)
        buttons.addWidget(self.prestamo_save_btn)
        buttons.addWidget(self.prestamo_delete_btn)
        buttons.addWidget(self.prestamo_refresh_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Formulario de préstamo"))
        right_layout.addWidget(form)
        right_layout.addLayout(buttons)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.selected_prestamo_id = None
        self.load_tipo_usuario_options(prestamos=True)
        self.load_libro_options()
        self.load_prestamos()
        return widget

    def create_config_tab(self):
        widget = QWidget()
        main_layout = QHBoxLayout(widget)

        self.tipo_table = QTableWidget(0, 2)
        self.tipo_table.setHorizontalHeaderLabels(["ID", "Descripción"])
        self.tipo_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.tipo_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tipo_table.cellClicked.connect(self.on_tipo_selected)

        self.editorial_table = QTableWidget(0, 2)
        self.editorial_table.setHorizontalHeaderLabels(["ID", "Editorial"])
        self.editorial_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.editorial_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.editorial_table.cellClicked.connect(self.on_editorial_selected)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Tipos de Usuario"))
        left_layout.addWidget(self.tipo_table)
        left_layout.addWidget(QLabel("Editoriales"))
        left_layout.addWidget(self.editorial_table)

        tipo_form = QGroupBox("Tipo de Usuario")
        tipo_layout = QHBoxLayout(tipo_form)
        self.tipo_descripcion_input = QLineEdit()
        tipo_layout.addWidget(QLabel("Descripción:"))
        tipo_layout.addWidget(self.tipo_descripcion_input)
        tipo_buttons = QHBoxLayout()
        self.tipo_save_btn = QPushButton("Guardar")
        self.tipo_delete_btn = QPushButton("Eliminar")
        self.tipo_refresh_btn = QPushButton("Refrescar")
        self.tipo_save_btn.clicked.connect(self.save_tipo)
        self.tipo_delete_btn.clicked.connect(self.delete_tipo)
        self.tipo_refresh_btn.clicked.connect(self.load_tipos)
        tipo_buttons.addWidget(self.tipo_save_btn)
        tipo_buttons.addWidget(self.tipo_delete_btn)
        tipo_buttons.addWidget(self.tipo_refresh_btn)

        editorial_form = QGroupBox("Editorial")
        editorial_layout = QHBoxLayout(editorial_form)
        self.editorial_nombre_input = QLineEdit()
        editorial_layout.addWidget(QLabel("Nombre:"))
        editorial_layout.addWidget(self.editorial_nombre_input)
        editorial_buttons = QHBoxLayout()
        self.editorial_save_btn = QPushButton("Guardar")
        self.editorial_delete_btn = QPushButton("Eliminar")
        self.editorial_refresh_btn = QPushButton("Refrescar")
        self.editorial_save_btn.clicked.connect(self.save_editorial)
        self.editorial_delete_btn.clicked.connect(self.delete_editorial)
        self.editorial_refresh_btn.clicked.connect(self.load_editoriales)
        editorial_buttons.addWidget(self.editorial_save_btn)
        editorial_buttons.addWidget(self.editorial_delete_btn)
        editorial_buttons.addWidget(self.editorial_refresh_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(tipo_form)
        right_layout.addLayout(tipo_buttons)
        right_layout.addWidget(editorial_form)
        right_layout.addLayout(editorial_buttons)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.selected_tipo_id = None
        self.selected_editorial_id = None
        self.load_tipos()
        self.load_editoriales()
        return widget

    def create_categorias_tab(self):
        widget = QWidget()
        main_layout = QHBoxLayout(widget)

        self.categoria_table = QTableWidget(0, 3)
        self.categoria_table.setHorizontalHeaderLabels(["ID", "Categoría", "Descripción"])
        self.categoria_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.categoria_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.categoria_table.cellClicked.connect(self.on_categoria_selected)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Categorías existentes"))
        left_layout.addWidget(self.categoria_table)

        categoria_form = QGroupBox("Categoría")
        categoria_layout = QHBoxLayout(categoria_form)
        self.categoria_nombre_input = QLineEdit()
        self.categoria_descripcion_input = QLineEdit()
        categoria_layout.addWidget(QLabel("Nombre:"))
        categoria_layout.addWidget(self.categoria_nombre_input)
        categoria_layout.addWidget(QLabel("Descripción:"))
        categoria_layout.addWidget(self.categoria_descripcion_input)

        categoria_buttons = QHBoxLayout()
        self.categoria_save_btn = QPushButton("Guardar")
        self.categoria_delete_btn = QPushButton("Eliminar")
        self.categoria_refresh_btn = QPushButton("Refrescar")
        self.categoria_save_btn.clicked.connect(self.save_categoria)
        self.categoria_delete_btn.clicked.connect(self.delete_categoria)
        self.categoria_refresh_btn.clicked.connect(self.load_categorias)
        categoria_buttons.addWidget(self.categoria_save_btn)
        categoria_buttons.addWidget(self.categoria_delete_btn)
        categoria_buttons.addWidget(self.categoria_refresh_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Formulario de categoría"))
        right_layout.addWidget(categoria_form)
        right_layout.addLayout(categoria_buttons)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 2)

        self.selected_categoria_id = None
        self.load_categorias()
        return widget

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.exec()

    def load_categoria_options(self):
        self.libro_category_combo.clear()
        self.libro_category_combo.addItem("(Ninguna)", None)
        categorias = CategoriaCRUD.get_all() or []
        for categoria in categorias:
            self.libro_category_combo.addItem(categoria.get("nombre_categoria"), categoria.get("id_categoria"))

    def load_tipo_usuario_options(self, prestamos=False):
        combo = self.prestamo_tipo_combo if prestamos else self.usuario_tipo_combo
        combo.clear()
        tipos = TipoUsuarioCRUD.get_all() or []
        for tipo in tipos:
            combo.addItem(tipo.get("descripcion"), tipo.get("id_tipo_usuario"))

    def load_libro_options(self):
        self.prestamo_libro_combo.clear()
        libros = LibroCRUD.get_all() or []
        for libro in libros:
            self.prestamo_libro_combo.addItem(libro.get("titulo"), libro.get("id_libro"))

    def load_libros(self):
        libros = LibroCRUD.get_all_with_category() or []
        self.libro_table.setRowCount(0)
        for libro in libros:
            row = self.libro_table.rowCount()
            self.libro_table.insertRow(row)
            self.libro_table.setItem(row, 0, QTableWidgetItem(str(libro.get("id_libro"))))
            self.libro_table.setItem(row, 1, QTableWidgetItem(libro.get("titulo", "")))
            self.libro_table.setItem(row, 2, QTableWidgetItem(str(libro.get("anio_publicacion") or "")))
            self.libro_table.setItem(row, 3, QTableWidgetItem(str(libro.get("categoria_nombre") or "")))

    def on_libro_selected(self, row, _column):
        self.selected_libro_id = int(self.libro_table.item(row, 0).text())
        self.libro_title_input.setText(self.libro_table.item(row, 1).text())
        year_text = self.libro_table.item(row, 2).text()
        self.libro_year_input.setValue(int(year_text) if year_text else date.today().year)
        categoria_text = self.libro_table.item(row, 3).text()
        index = self.libro_category_combo.findText(categoria_text)
        self.libro_category_combo.setCurrentIndex(index if index >= 0 else 0)

    def clear_libro_form(self):
        self.selected_libro_id = None
        self.libro_title_input.clear()
        self.libro_year_input.setValue(date.today().year)
        self.libro_category_combo.setCurrentIndex(0)

    def save_libro(self):
        titulo = self.libro_title_input.text().strip()
        anio = self.libro_year_input.value()
        id_categoria = self.libro_category_combo.currentData()
        if not titulo:
            self.show_message("Validación", "El título es obligatorio.")
            return
        if self.selected_libro_id:
            LibroCRUD.update(self.selected_libro_id, titulo, anio, id_categoria)
            self.show_message("Libro actualizado", "El libro se actualizó correctamente.")
        else:
            LibroCRUD.create(titulo, anio, id_categoria)
            self.show_message("Libro creado", "El libro se creó correctamente.")
        self.load_libros()
        self.load_libro_options()

    def delete_libro(self):
        if not self.selected_libro_id:
            self.show_message("Eliminar libro", "Seleccione un libro para eliminar.")
            return
        LibroCRUD.delete(self.selected_libro_id)
        self.show_message("Libro eliminado", "El libro se eliminó correctamente.")
        self.clear_libro_form()
        self.load_libros()
        self.load_libro_options()

    def load_usuarios(self):
        usuarios = UsuarioCRUD.get_all() or []
        self.usuario_table.setRowCount(0)
        for usuario in usuarios:
            row = self.usuario_table.rowCount()
            self.usuario_table.insertRow(row)
            self.usuario_table.setItem(row, 0, QTableWidgetItem(str(usuario.get("id_usuario"))))
            self.usuario_table.setItem(row, 1, QTableWidgetItem(usuario.get("nombre", "")))
            self.usuario_table.setItem(row, 2, QTableWidgetItem(usuario.get("apellido", "")))
            self.usuario_table.setItem(row, 3, QTableWidgetItem(usuario.get("dni", "")))
            self.usuario_table.setItem(row, 4, QTableWidgetItem(usuario.get("email", "")))
            self.usuario_table.setItem(row, 5, QTableWidgetItem(usuario.get("telefono", "")))
            self.usuario_table.setItem(row, 6, QTableWidgetItem(str(usuario.get("id_tipo_usuario", ""))))

    def on_usuario_selected(self, row, _column):
        self.selected_usuario_id = int(self.usuario_table.item(row, 0).text())
        self.usuario_nombre_input.setText(self.usuario_table.item(row, 1).text())
        self.usuario_apellido_input.setText(self.usuario_table.item(row, 2).text())
        self.usuario_dni_input.setText(self.usuario_table.item(row, 3).text())
        self.usuario_email_input.setText(self.usuario_table.item(row, 4).text())
        self.usuario_telefono_input.setText(self.usuario_table.item(row, 5).text())
        tipo_id = int(self.usuario_table.item(row, 6).text()) if self.usuario_table.item(row, 6).text() else None
        index = self.usuario_tipo_combo.findData(tipo_id)
        self.usuario_tipo_combo.setCurrentIndex(index if index >= 0 else 0)

    def clear_usuario_form(self):
        self.selected_usuario_id = None
        self.usuario_nombre_input.clear()
        self.usuario_apellido_input.clear()
        self.usuario_dni_input.clear()
        self.usuario_email_input.clear()
        self.usuario_telefono_input.clear()
        self.usuario_tipo_combo.setCurrentIndex(0)

    def save_usuario(self):
        nombre = self.usuario_nombre_input.text().strip()
        apellido = self.usuario_apellido_input.text().strip()
        dni = self.usuario_dni_input.text().strip()
        email = self.usuario_email_input.text().strip()
        telefono = self.usuario_telefono_input.text().strip()
        tipo_usuario_id = self.usuario_tipo_combo.currentData()

        if not nombre or not apellido or not dni or not email:
            self.show_message("Validación", "Complete nombre, apellido, DNI y email.")
            return
        if self.selected_usuario_id:
            UsuarioCRUD.update(self.selected_usuario_id, nombre, apellido, dni, email, telefono, tipo_usuario_id)
            self.show_message("Usuario actualizado", "El usuario se actualizó correctamente.")
        else:
            UsuarioCRUD.create(nombre, apellido, dni, email, telefono, tipo_usuario_id)
            self.show_message("Usuario creado", "El usuario se creó correctamente.")
        self.load_usuarios()

    def delete_usuario(self):
        if not self.selected_usuario_id:
            self.show_message("Eliminar usuario", "Seleccione un usuario para eliminar.")
            return
        UsuarioCRUD.delete(self.selected_usuario_id)
        self.show_message("Usuario eliminado", "El usuario se eliminó correctamente.")
        self.clear_usuario_form()
        self.load_usuarios()

    def load_prestamos(self):
        prestamos = PrestamoCRUD.get_all_with_details() or []
        self.prestamo_table.setRowCount(0)
        for prestamo in prestamos:
            row = self.prestamo_table.rowCount()
            self.prestamo_table.insertRow(row)
            self.prestamo_table.setItem(row, 0, QTableWidgetItem(str(prestamo.get("id_prestamo"))))
            usuario = f"{prestamo.get('usuario_nombre', '')} {prestamo.get('usuario_apellido', '')}".strip()
            self.prestamo_table.setItem(row, 1, QTableWidgetItem(usuario))
            self.prestamo_table.setItem(row, 2, QTableWidgetItem(prestamo.get("usuario_dni", "")))
            self.prestamo_table.setItem(row, 3, QTableWidgetItem(prestamo.get("libro_titulo", "")))
            self.prestamo_table.setItem(row, 4, QTableWidgetItem(str(prestamo.get("fecha_prestamo", ""))))
            self.prestamo_table.setItem(row, 5, QTableWidgetItem(str(prestamo.get("fecha_limite_devolucion", ""))))
            self.prestamo_table.setItem(row, 6, QTableWidgetItem(str(prestamo.get("cantidad", ""))))
            self.prestamo_table.setItem(row, 7, QTableWidgetItem(str(prestamo.get("estado_prestamo", ""))))

    def on_prestamo_selected(self, row, _column):
        self.selected_prestamo_id = int(self.prestamo_table.item(row, 0).text())
        self.prestamo_dni_input.setText(self.prestamo_table.item(row, 2).text())
        self.prestamo_libro_combo.setCurrentIndex(self.prestamo_libro_combo.findText(self.prestamo_table.item(row, 3).text()))
        fecha = self.prestamo_table.item(row, 4).text()
        limite = self.prestamo_table.item(row, 5).text()
        if fecha:
            self.prestamo_fecha_input.setDate(QDate.fromString(fecha, "yyyy-MM-dd"))
        if limite:
            self.prestamo_limite_input.setDate(QDate.fromString(limite, "yyyy-MM-dd"))
        self.prestamo_cantidad_input.setValue(int(self.prestamo_table.item(row, 6).text()))

    def clear_prestamo_form(self):
        self.selected_prestamo_id = None
        self.prestamo_dni_input.clear()
        self.prestamo_nombre_input.clear()
        self.prestamo_apellido_input.clear()
        self.prestamo_email_input.clear()
        self.prestamo_telefono_input.clear()
        self.prestamo_tipo_combo.setCurrentIndex(0)
        self.prestamo_libro_combo.setCurrentIndex(0)
        self.prestamo_fecha_input.setDate(QDate.currentDate())
        self.prestamo_limite_input.setDate(QDate.currentDate().addDays(7))
        self.prestamo_cantidad_input.setValue(1)

    def save_prestamo(self):
        dni = self.prestamo_dni_input.text().strip()
        if not dni:
            self.show_message("Validación", "DNI del usuario es obligatorio.")
            return

        usuario = UsuarioCRUD.get_by_dni(dni)
        if usuario:
            usuario_id = usuario.get("id_usuario")
        else:
            nombre = self.prestamo_nombre_input.text().strip()
            apellido = self.prestamo_apellido_input.text().strip()
            email = self.prestamo_email_input.text().strip()
            telefono = self.prestamo_telefono_input.text().strip()
            tipo_usuario_id = self.prestamo_tipo_combo.currentData()
            if not nombre or not apellido or not email:
                self.show_message(
                    "Validación",
                    "Complete nombre, apellido y email para crear un nuevo usuario."
                )
                return
            usuario_id, usuario = UsuarioCRUD.create_if_not_exists(
                nombre,
                apellido,
                dni,
                email,
                telefono,
                tipo_usuario_id,
            )
            if not usuario_id:
                self.show_message("Error", "No se pudo crear el usuario automáticamente.", QMessageBox.Critical)
                return

        libro_id = self.prestamo_libro_combo.currentData()
        fecha_prestamo = self.prestamo_fecha_input.date().toString("yyyy-MM-dd")
        fecha_limite = self.prestamo_limite_input.date().toString("yyyy-MM-dd")
        cantidad = self.prestamo_cantidad_input.value()

        if self.selected_prestamo_id:
            PrestamoCRUD.update(
                self.selected_prestamo_id,
                usuario_id,
                libro_id,
                fecha_prestamo,
                fecha_limite,
                cantidad,
            )
            self.show_message("Préstamo actualizado", "El préstamo se actualizó correctamente.")
        else:
            PrestamoCRUD.create(usuario_id, libro_id, fecha_prestamo, fecha_limite, cantidad)
            self.show_message("Préstamo creado", "El préstamo se creó correctamente.")

        self.load_prestamos()
        self.load_usuarios()

    def delete_prestamo(self):
        if not self.selected_prestamo_id:
            self.show_message("Eliminar préstamo", "Seleccione un préstamo para eliminar.")
            return
        PrestamoCRUD.delete(self.selected_prestamo_id)
        self.show_message("Préstamo eliminado", "El préstamo se eliminó correctamente.")
        self.clear_prestamo_form()
        self.load_prestamos()

    def load_tipos(self):
        tipos = TipoUsuarioCRUD.get_all() or []
        self.tipo_table.setRowCount(0)
        for tipo in tipos:
            row = self.tipo_table.rowCount()
            self.tipo_table.insertRow(row)
            self.tipo_table.setItem(row, 0, QTableWidgetItem(str(tipo.get("id_tipo_usuario"))))
            self.tipo_table.setItem(row, 1, QTableWidgetItem(tipo.get("descripcion", "")))

    def on_tipo_selected(self, row, _column):
        self.selected_tipo_id = int(self.tipo_table.item(row, 0).text())
        self.tipo_descripcion_input.setText(self.tipo_table.item(row, 1).text())

    def save_tipo(self):
        descripcion = self.tipo_descripcion_input.text().strip()
        if not descripcion:
            self.show_message("Validación", "La descripción es obligatoria.")
            return
        if self.selected_tipo_id:
            TipoUsuarioCRUD.update(self.selected_tipo_id, descripcion)
            self.show_message("Tipo usuario actualizado", "El tipo de usuario se actualizó correctamente.")
        else:
            TipoUsuarioCRUD.create(descripcion)
            self.show_message("Tipo usuario creado", "El tipo de usuario se creó correctamente.")
        self.load_tipos()
        self.load_tipo_usuario_options()

    def delete_tipo(self):
        if not self.selected_tipo_id:
            self.show_message("Eliminar tipo usuario", "Seleccione un tipo de usuario para eliminar.")
            return
        TipoUsuarioCRUD.delete(self.selected_tipo_id)
        self.show_message("Tipo usuario eliminado", "El tipo de usuario se eliminó correctamente.")
        self.selected_tipo_id = None
        self.tipo_descripcion_input.clear()
        self.load_tipos()
        self.load_tipo_usuario_options()

    def load_categorias(self):
        categorias = CategoriaCRUD.get_all() or []
        self.categoria_table.setRowCount(0)
        for categoria in categorias:
            row = self.categoria_table.rowCount()
            self.categoria_table.insertRow(row)
            self.categoria_table.setItem(row, 0, QTableWidgetItem(str(categoria.get("id_categoria"))))
            self.categoria_table.setItem(row, 1, QTableWidgetItem(categoria.get("nombre_categoria", "")))
            self.categoria_table.setItem(row, 2, QTableWidgetItem(categoria.get("descripcion", "")))

    def on_categoria_selected(self, row, _column):
        self.selected_categoria_id = int(self.categoria_table.item(row, 0).text())
        self.categoria_nombre_input.setText(self.categoria_table.item(row, 1).text())
        self.categoria_descripcion_input.setText(self.categoria_table.item(row, 2).text())

    def save_categoria(self):
        nombre = self.categoria_nombre_input.text().strip()
        descripcion = self.categoria_descripcion_input.text().strip()
        if not nombre:
            self.show_message("Validación", "El nombre de categoría es obligatorio.")
            return
        if self.selected_categoria_id:
            CategoriaCRUD.update(self.selected_categoria_id, nombre, descripcion)
            self.show_message("Categoría actualizada", "La categoría se actualizó correctamente.")
        else:
            CategoriaCRUD.create(nombre, descripcion)
            self.show_message("Categoría creada", "La categoría se creó correctamente.")
        self.load_categorias()
        self.load_categoria_options()

    def delete_categoria(self):
        if not self.selected_categoria_id:
            self.show_message("Eliminar categoría", "Seleccione una categoría para eliminar.")
            return
        CategoriaCRUD.delete(self.selected_categoria_id)
        self.show_message("Categoría eliminada", "La categoría se eliminó correctamente.")
        self.selected_categoria_id = None
        self.categoria_nombre_input.clear()
        self.categoria_descripcion_input.clear()
        self.load_categorias()
        self.load_categoria_options()

    def load_editoriales(self):
        editoriales = EditorialCRUD.get_all() or []
        self.editorial_table.setRowCount(0)
        for editorial in editoriales:
            row = self.editorial_table.rowCount()
            self.editorial_table.insertRow(row)
            self.editorial_table.setItem(row, 0, QTableWidgetItem(str(editorial.get("id_editorial"))))
            self.editorial_table.setItem(row, 1, QTableWidgetItem(editorial.get("nombre_editorial", "")))

    def on_editorial_selected(self, row, _column):
        self.selected_editorial_id = int(self.editorial_table.item(row, 0).text())
        self.editorial_nombre_input.setText(self.editorial_table.item(row, 1).text())

    def save_editorial(self):
        nombre = self.editorial_nombre_input.text().strip()
        if not nombre:
            self.show_message("Validación", "El nombre de editorial es obligatorio.")
            return
        if self.selected_editorial_id:
            EditorialCRUD.update(self.selected_editorial_id, nombre)
            self.show_message("Editorial actualizada", "La editorial se actualizó correctamente.")
        else:
            EditorialCRUD.create(nombre)
            self.show_message("Editorial creada", "La editorial se creó correctamente.")
        self.load_editoriales()

    def delete_editorial(self):
        if not self.selected_editorial_id:
            self.show_message("Eliminar editorial", "Seleccione una editorial para eliminar.")
            return
        EditorialCRUD.delete(self.selected_editorial_id)
        self.show_message("Editorial eliminada", "La editorial se eliminó correctamente.")
        self.selected_editorial_id = None
        self.editorial_nombre_input.clear()
        self.load_editoriales()


if __name__ == "__main__":
    app = QApplication([])
    ventana = BibliotecaApp()
    ventana.show()
    app.exec()
