
import funcionesTienda8


#PROGRAMA PRINCIPAL
if __name__ == "__main__":
    funcionesTienda8.inicializar_bbdd()
    

    while True:
        funcionesTienda8.mostrar_menu()

        try:
            opcion= int(input("Seleccione una opción (1-7):"))

            if opcion == 7:
                print("Saliendo del sistema. ¡Hasta pronto!")
                break
            elif opcion == 1:
                funcionesTienda8.registrar_producto()
            elif opcion == 2:
                funcionesTienda8.buscar_producto()
            elif opcion == 3:
                funcionesTienda8.actualizar_producto()
            elif opcion == 4:
                funcionesTienda8.eliminar_producto()
            elif opcion == 5:
                funcionesTienda8.listar_productos()
            elif opcion == 6:
                funcionesTienda8.reporte_bajo_stock()
            else:
                print("Opción no váida. Por favor, seleccione entre 1 y 7.")
        except ValueError: 
            print("Opción no válida. Por favor, ingrese un valor numérico.\n")