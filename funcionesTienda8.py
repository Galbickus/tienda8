import sqlite3
import os       # Obtiene la ruta del directorio donde se encuentra el script

directorio_actual = os.path.dirname(os.path.abspath(__file__))  # Define la ruta relativa a la base de datos
ruta_db = os.path.join(directorio_actual, "inventario8.db")  # Conecta a la base de datos usando la ruta relativa
conexion = sqlite3.connect(ruta_db)

#CREAR LA BASE DATOS Y LA TABLA DE PRODUCTOS.
def inicializar_bbdd():
    conexion= sqlite3.connect(ruta_db)
    cursor= conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Código TEXT UNIQUE,
            Nombre TEXT NOT NULL,
            Descripción TEXT,
            Cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            Precio REAL NOT NULL CHECK(precio > 0),
            Categoria TEXT
        )
    ''')

    conexion.commit()
    conexion.close()
    
# inicializar_bbdd()
# una vez creada la bbdd borramos el llamado a la función inicializar

#CREACIÓN DEL MENÚ DE OPCIONES.
def mostrar_menu():
    """\nMuestra el menú principal."""
    print("\nMenú para la Gestión de Productos:\n")
    print("1. Registro: Alta de productos nuevos.")
    print("2. Búsqueda: Consulta de datos de un producto específico.")
    print("3. Actualización: Modificar los datos de un producto.")
    print("4. Eliminación: Dar de baja productos.")
    print("5. Listado: Listado completo de los productos en la base de datos.")
    print("6. Reporte de Bajo Stock: Lista de productos con cantidad bajo mínimo.")
    print("7. Salir.\n")

# FUNCION REGISTRAR PRODUCTOS (opcion 1)
def registrar_producto():
    print("\n --- Registro de Producto Nuevo ---")

    nombre= input("Nombre del producto:").strip()
    descripcion= input("Descripción del producto:").strip()

    while True:    
        try:
            precio= float(input("Precio del producto:"))
            if precio > 0:
                break
            else:
                print("Entrada inválida. Debe ingresar un número decimal mayor a 0.")
        except ValueError:
            print("Entrada inválida. Debe ingresar un valor numérico decimal mayor a 0.")

    while True:
        try:
            cantidad= int(input(f"Cantidad en stock de {nombre}:"))
            if cantidad >= 0:
                break
            else:
                print("Entrada inválida. El stock no puede ser negativo.")
        except ValueError:
            print("Entrada inválida. Debe ingresar un valor numérico entero mayor a 0.")

    categoria= input("Categoría del producto:").strip()

    conexion= sqlite3.connect(ruta_db)
    cursor= conexion.cursor()

    try:
        cursor.execute('''
            INSERT INTO productos (Código, Nombre, Descripción, Cantidad, Precio, Categoria)
            
            VALUES (NULL, ?, ?, ?, ?, ?)''',
            (nombre, descripcion, cantidad, precio, categoria)
        )

        id_producto= cursor.lastrowid
        codigo= f"PROD{id_producto}"

        cursor.execute('''
        UPDATE productos SET Código = ? WHERE id = ?''',
        (codigo, id_producto))

        conexion.commit()
        print(f"Producto registrado con éxito. Código asignado: {codigo}")

    except sqlite3.IntegrityError:
        print("Error. No se pudo registrar el producto.")

    finally:
        conexion.close()

# FUNCION BUSCAR UN PRODUCTO POR CODIGO (opcion2)
def buscar_producto():
    print("\n --- Busqueda de Producto ---")
    codigo= input("Ingrese el código del producto que desea buscar: ").strip()
    
    conexion= sqlite3.connect(ruta_db)
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE Código= ?",(codigo,))
    producto= cursor.fetchone()
    
    conexion.close()
    
    if producto:
        _, codigo, nombre, descripcion, cantidad, precio, categoria =producto
        print(f"\nProducto encontrado con el código: {codigo}")
        print(f"Nombre      :   {nombre}")
        print(f"Descripcion :   {descripcion}")
        print(f"Cantidad    :   {cantidad}")
        print(f"Precio      :   $ {precio}")
        print(f"Categoría   :   {categoria}")
    else:
        print(f"No se encontró el producto registrado bajo el código: {codigo}")

# FUNCION LISTAR PRODUCTOS(opcion 5)
def listar_productos():
    print("\n --- LISTA DE PRODUCTOS ---")
    conexion= sqlite3.connect(ruta_db)
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos= cursor.fetchall()
    conexion.close()
    
    if not productos:
        print("El inventario está vacío.")
    else:
        for _, codigo, nombre, descripcion, cantidad, precio, categoria in productos:
            print(f"\nCódigo:           {codigo}")
            print(f"Nombre:         {nombre}")
            print(f"Descripcion:    {descripcion}")
            print(f"Cantidad:       {cantidad}")
            print(f"Precio:         $ {precio}")
            print(f"Categoría:      {categoria}")
            print("\n ------\n")       

#FUNCION PARA ACTUALIZAR UN PRODUCTO (opcion 3)
def actualizar_producto():
    print("\n --- Actualización de Producto ---")
    
    codigo = input("Ingrese el código del producto a actualizar: ").strip()

    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE Código = ?", (codigo,))
    producto = cursor.fetchone()

    if not producto:
        print(f"No se encontró ningún producto con el código: {codigo}")
        conexion.close()
        return

    _, codigo, nombre, descripcion, cantidad, precio, categoria = producto

    print("\nProducto encontrado. Deje el campo vacío si no desea modificarlo.")
    
    nuevo_nombre = input(f"Nombre actual ({nombre}): ").strip() or nombre
    nueva_descripcion = input(f"Descripción actual ({descripcion}): ").strip() or descripcion

    while True:
        try:
            nueva_cantidad = input(f"Cantidad actual ({cantidad}): ").strip()
            nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else cantidad
            if nueva_cantidad >= 0:
                break
            else:
                print("La cantidad no puede ser negativa.")
        except ValueError:
            print("Debe ingresar un valor numérico entero.")

    while True:
        try:
            nuevo_precio = input(f"Precio actual (${precio}): ").strip()
            nuevo_precio = float(nuevo_precio) if nuevo_precio else precio
            if nuevo_precio > 0:
                break
            else:
                print("El precio debe ser mayor a 0.")
        except ValueError:
            print("Debe ingresar un valor numérico decimal.")

    nueva_categoria = input(f"Categoría actual ({categoria}): ").strip() or categoria

    # Actualizar en la base de datos
    try:
        cursor.execute('''
            UPDATE productos
            SET Nombre = ?, Descripción = ?, Cantidad = ?, Precio = ?, Categoria = ?
            WHERE Código = ?''',
            (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, codigo)
        )

        conexion.commit()
        print("Producto actualizado con éxito.")

    except sqlite3.Error as e:
        print(f"Error al actualizar el producto: {e}")

    finally:
        conexion.close()

# FUNCION PARA ELIMINAR UN PRODUCTO (opción 4)
def eliminar_producto():
    print("\n --- Eliminación de Producto ---\n")
    
    codigo = input("Ingrese el código del producto a eliminar: ").strip()

    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    # Verificar si el producto existe
    cursor.execute("SELECT * FROM productos WHERE Código = ?", (codigo,))
    producto = cursor.fetchone()

    if not producto:
        print(f"No se encontró ningún producto con el código: {codigo}")
        conexion.close()
        return

    # Confirmación antes de eliminar
    confirmacion = input(f"¿Está seguro de que desea eliminar el producto con código {codigo}? (s/n): ").strip().lower()
    if confirmacion != 's':
        print("Operación cancelada.")
        conexion.close()
        return

    try:
        cursor.execute("DELETE FROM productos WHERE Código = ?", (codigo,))
        conexion.commit()
        print("Producto eliminado con éxito.\n")

    except sqlite3.Error as e:
        print(f"Error al eliminar el producto: {e}")

    finally:
        conexion.close()

# FUNCION DE REPORTE DE BAJO STOCK (opcion 6)
def reporte_bajo_stock():
    print("\n --- Reporte de Bajo Stock ---")
    
    while True:
        try:
            limite = int(input("Ingrese el límite de stock para el reporte: "))
            if limite >= 0:
                break
            print("El límite de stock no puede ser negativo. Inténtelo de nuevo.")
        except ValueError:
            print("Entrada inválida. Debe ser un número entero.")

    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos WHERE Cantidad <= ?", (limite,))
    productos = cursor.fetchall()

    conexion.close()

    if not productos:
        print("\nNo hay productos con stock igual o inferior al límite especificado.")
    else:
        print(f"\nProductos con stock igual o inferior a {limite}:")
        for _, codigo, nombre, descripcion, cantidad, precio, categoria in productos:
            print(f"\nCódigo: {codigo}")
            print(f"  Nombre      : {nombre}")
            print(f"  Descripción : {descripcion}")
            print(f"  Cantidad    : {cantidad}")
            print(f"  Precio      : ${precio:.2f}")
            print(f"  Categoría   : {categoria}")
            print("-" * 50)
