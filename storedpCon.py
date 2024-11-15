import pyodbc

def conectar_a_sql_server():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-8EBRJ06;'  
            'DATABASE=DB_BIBLIOTECA;'  
            'Trusted_Connection=yes;' 
        )
        print("Conexión establecida exitosamente")
        return conexion
    except Exception as e:
        print(f"Fallo en la conexión: {e}")
        return None

def insertar_prestamo(conexion):
    codigo_usuario = input("Ingresa el código del usuario: ")
    codigo_ejemplar = input("Ingresa el código del ejemplar: ")
    fecha_prestamo = input("Ingresa la fecha de préstamo (AAAA-MM-DD): ")
    fecha_devolucion = input("Ingresa la fecha de devolución (AAAA-MM-DD): ")
    cursor = conexion.cursor()
    cursor.execute("EXEC BIBLIOTECA.sp_InsertarPrestamo ?, ?, ?, ?", 
                   codigo_usuario, codigo_ejemplar, fecha_prestamo, fecha_devolucion)
    conexion.commit()
    print("Préstamo insertado exitosamente")
    cursor.close()

def consultar_libros(conexion):
    titulo = input("Ingresa el título del libro a buscar (deja en blanco para todos los libros): ")
    cursor = conexion.cursor()
    cursor.execute("EXEC BIBLIOTECA.sp_ConsultarLibros @TITULO = ?", titulo)
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)
    cursor.close()

def actualizar_autor(conexion):
    codigo = input("Ingresa el código del autor: ")
    nombre = input("Ingresa el nuevo nombre del autor: ")
    cursor = conexion.cursor()
    cursor.execute("EXEC BIBLIOTECA.sp_ActualizarAutor ?, ?", codigo, nombre)
    conexion.commit()
    print("Autor actualizado exitosamente")
    cursor.close()


def borrar_estudiante(conexion):
    codigo_usuario = input("Ingresa el código del usuario a eliminar: ")
    cursor = conexion.cursor()
    cursor.execute("EXEC BIBLIOTECA.sp_BorrarEstudiante ?", codigo_usuario)
    conexion.commit()
    print("Estudiante eliminado exitosamente")
    cursor.close()

def main():
    conexion = conectar_a_sql_server()
    if not conexion:
        return

    acciones = {
        '1': lambda: insertar_prestamo(conexion),
        '2': lambda: consultar_libros(conexion),
        '3': lambda: actualizar_autor(conexion),
        '4': lambda: borrar_estudiante(conexion)
    }

    while True:
        print("\nMenú:")
        print("1. Insertar un préstamo")
        print("2. Buscar libros")
        print("3. Actualizar la información de un autor")
        print("4. Eliminar un estudiante")
        print("5. Salir")

        eleccion = input("Elige una opción: ")
        if eleccion == '5':
            print("Saliendo del programa.")
            break
        elif eleccion in acciones:
            try:
                acciones[eleccion]()
            except Exception as e:
                print(f"Ocurrió un error: {e}")
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == '__main__':
    main()
