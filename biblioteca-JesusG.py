
from datetime import datetime, timedelta

# Listas 
registros = []
prestamos = []
multas = []


# regresar al menu
def volver_menu():
    while True:
        try:
            respuesta = int(input("\nDesea volver al menu principal? 1. Si / 2. No: "))

            if respuesta == 1:
                return
            elif respuesta == 2:
                print("Puede seleccionar 1 para regresar al menu.")
            else:
                print("Ingrese solamente 1 o 2.")

        except ValueError:
            print("Error: ingrese solamente numeros.")


opcion = 0

while opcion != 7:

    print("\n========== BIBLIOTECA DEL BARRIO ==========")
    print("1. Registrar usuario y libro")
    print("2. Consultar registros")
    print("3. Prestar libro")
    print("4. Devolver libro")
    print("5. Consultar prestamos")
    print("6. Consultar multas")
    print("7. Salir")

    try:
        opcion = int(input("Seleccione una opcion del 1 al 7: "))

        # OPCION 1: REGISTRAR USUARIO Y LIBRO
        if opcion == 1:
            print("\n========== REGISTRAR USUARIO Y LIBRO ==========")

            nombre = input("Ingrese el nombre del usuario: ")
            libro = input("Ingrese el nombre del libro: ")

            if nombre == "" or libro == "":
                print("Error: el nombre y el libro no pueden estar vacios.")

            else:
                cantidad = 0

                for registro in registros:
                    if registro["usuario"].lower() == nombre.lower():
                        cantidad += 1

                if cantidad >= 3:
                    print("Este usuario ya tiene 3 libros registrados.")

                else:
                    nuevo_registro = {
                        "usuario": nombre,
                        "libro": libro
                    }

                    registros.append(nuevo_registro)
                    print("Usuario y libro registrados correctamente.")

        # OPCION 2: CONSULTAR REGISTROS
        elif opcion == 2:
            print("\n========== CONSULTAR REGISTROS ==========")

            if len(registros) == 0:
                print("Aun no hay usuarios ni libros registrados.")
                volver_menu()

            else:
                for registro in registros:
                    print("\nUsuario:", registro["usuario"])
                    print("Libro:", registro["libro"])
                    print("------------------------------")

        # OPCION 3: PRESTAR LIBRO
        elif opcion == 3:
            print("\n========== PRESTAR LIBRO ==========")

            disponibles = []

            for registro in registros:
                ocupado = False

                for prestamo in prestamos:
                    if (prestamo["registro"] is registro and
                            prestamo["fecha_devolucion"] == ""):
                        ocupado = True

                if ocupado == False:
                    disponibles.append(registro)

            if len(disponibles) == 0:
                print("Aun no hay libros disponibles para prestar.")
                volver_menu()

            else:
                for i in range(len(disponibles)):
                    print(i + 1, ".", disponibles[i]["usuario"],
                          "-", disponibles[i]["libro"])

                try:
                    numero = int(input("Seleccione el numero del registro: "))

                    if numero >= 1 and numero <= len(disponibles):
                        registro = disponibles[numero - 1]

                        fecha_texto = input(
                            "Ingrese la fecha del prestamo (DD/MM/AAAA): "
                        )

                        try:
                            fecha = datetime.strptime(fecha_texto, "%d/%m/%Y")
                            fecha_limite = fecha + timedelta(days=8)

                            nuevo_prestamo = {
                                "registro": registro,
                                "usuario": registro["usuario"],
                                "libro": registro["libro"],
                                "fecha_prestamo": fecha.strftime("%d/%m/%Y"),
                                "fecha_limite": fecha_limite.strftime("%d/%m/%Y"),
                                "fecha_devolucion": ""
                            }

                            prestamos.append(nuevo_prestamo)

                            print("\nPrestamo registrado correctamente.")
                            print("Usuario:", registro["usuario"])
                            print("Libro:", registro["libro"])
                            print("Fecha del prestamo:",
                                  nuevo_prestamo["fecha_prestamo"])
                            print("Fecha limite:",
                                  nuevo_prestamo["fecha_limite"])

                        except ValueError:
                            print("Error: ingrese una fecha valida en formato DD/MM/AAAA.")

                    else:
                        print("Error: el numero seleccionado no existe.")

                except ValueError:
                    print("Error: debe ingresar solamente numeros.")

        # OPCION 4: DEVOLVER LIBRO
        elif opcion == 4:
            print("\n========== DEVOLVER LIBRO ==========")

            pendientes = []

            for prestamo in prestamos:
                if prestamo["fecha_devolucion"] == "":
                    pendientes.append(prestamo)

            if len(pendientes) == 0:
                print("Aun no hay prestamos pendientes de devolucion.")
                volver_menu()

            else:
                for i in range(len(pendientes)):
                    print(i + 1, ".", pendientes[i]["usuario"],
                          "-", pendientes[i]["libro"])

                try:
                    numero = int(input(
                        "Seleccione el prestamo que desea devolver: "
                    ))

                    if numero >= 1 and numero <= len(pendientes):
                        prestamo = pendientes[numero - 1]

                        fecha_texto = input(
                            "Ingrese la fecha de devolucion (DD/MM/AAAA): "
                        )

                        try:
                            fecha_devolucion = datetime.strptime(
                                fecha_texto, "%d/%m/%Y"
                            )

                            fecha_limite = datetime.strptime(
                                prestamo["fecha_limite"], "%d/%m/%Y"
                            )

                            fecha_prestamo = datetime.strptime(
                                prestamo["fecha_prestamo"], "%d/%m/%Y"
                            )

                            if fecha_devolucion < fecha_prestamo:
                                print("Error: la devolucion no puede ser anterior al prestamo.")

                            else:
                                prestamo["fecha_devolucion"] = fecha_devolucion.strftime(
                                    "%d/%m/%Y"
                                )

                                dias_retraso = (
                                    fecha_devolucion - fecha_limite
                                ).days

                                if dias_retraso > 0:
                                    valor_multa = dias_retraso * 5000

                                    nueva_multa = {
                                        "usuario": prestamo["usuario"],
                                        "libro": prestamo["libro"],
                                        "dias": dias_retraso,
                                        "valor": valor_multa
                                    }

                                    multas.append(nueva_multa)

                                    print("Dias de retraso:", dias_retraso)
                                    print("Multa: $", valor_multa)

                                else:
                                    print("Libro devuelto a tiempo. No tiene multa.")

                                print("Devolucion registrada correctamente.")

                        except ValueError:
                            print("Error: ingrese una fecha valida en formato DD/MM/AAAA.")

                    else:
                        print("Error: el numero seleccionado no existe.")

                except ValueError:
                    print("Error: debe ingresar solamente numeros.")

        # OPCION 5: CONSULTAR PRESTAMOS
        elif opcion == 5:
            print("\n========== CONSULTAR PRESTAMOS ==========")

            if len(prestamos) == 0:
                print("Aun no hay prestamos registrados.")
                volver_menu()

            else:
                for prestamo in prestamos:
                    print("\nUsuario:", prestamo["usuario"])
                    print("Libro:", prestamo["libro"])
                    print("Fecha de prestamo:", prestamo["fecha_prestamo"])
                    print("Fecha limite de devolucion:", prestamo["fecha_limite"])

                    if prestamo["fecha_devolucion"] != "":
                        print("Fecha de devolucion:",
                              prestamo["fecha_devolucion"])

                    print("------------------------------")

        # OPCION 6: CONSULTAR MULTAS
        elif opcion == 6:
            print("\n========== CONSULTAR MULTAS ==========")

            if len(multas) == 0:
                print("Aun no hay multas registradas.")
                volver_menu()

            else:
                total_multas = 0

                for multa in multas:
                    print("\nUsuario:", multa["usuario"])
                    print("Libro:", multa["libro"])
                    print("Dias de retraso:", multa["dias"])
                    print("Multa: $", multa["valor"])
                    print("------------------------------")

                    total_multas += multa["valor"]

                print("Total de multas: $", total_multas)

        # OPCION 7: SALIR
        elif opcion == 7:
            print("\nGracias por utilizar la Biblioteca del Barrio.")
            print("Programa finalizado correctamente.")

        else:
            print("Opcion incorrecta. Ingrese un numero del 1 al 7.")

    except ValueError:
        print("Error: debe ingresar solamente numeros.")
