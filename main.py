import os.path
import pickle
from clase import *


def punto_1(tf, bf):
    if os.path.exists(tf):
        if os.path.exists(bf):
            print("Advertencia: Se creará un archivo nuevo y se perderán los registros viejos")
            print("Ingrese 1 para continuar o 0 para cancelar la operación")
            respuesta = int(input("Ingrese su opción: "))
            if respuesta == 1:
                print("Se eliminó el archivo de registros ya existente...")
            else:
                print("Operación cancelada.")
                return main()

        print("Creando el archivo de registros...")
        mt = open(tf, "rt")
        ln = mt.readline()
        ln = mt.readline()

        mb = open(bf, "wb")
        while True:
            ln = mt.readline()

            # control de eof...
            if ln == "":
                break

            tokens = ln.split(",")
            cod = int(tokens[0])
            pat = tokens[1]
            tipo = int(tokens[2])
            pago = int(tokens[3])
            cab = int(tokens[4])
            dis = int(tokens[5])
            tik = Ticket(cod, pat, tipo, pago, cab, dis)
            pickle.dump(tik, mb)

        mt.close()
        mb.close()
        print("Listo...")
    else:
        print("El archivo", tf, "no existe...")
    return main()


def punto_2(bf):
    cod, pat, tipo, pago, cab, dis = cargar_ticket_teclado()
    tik = Ticket(cod, pat, tipo, pago, cab, dis)
    with open(bf, "ab") as mb:
        pickle.dump(tik, mb)
    print("Ticket cargado con éxito.")


def cargar_ticket_teclado():
    cod = int(input("Ingrese el código del ticket: "))
    while cod <= 0:
        print("El código ingresado debe ser mayor a 0")
        cod = int(input("Ingrese el código del ticket: "))

    pat = input("Ingrese la patente: ")

    tipo = int(input("Ingrese el tipo de vehiculo (0: motocicleta, 1: automóvil, 2: camión): "))
    while tipo not in [0, 1, 2]:
        print("Digito erróneo, ingrese los indicados")
        tipo = int(input("Ingrese el tipo de vehiculo (0: motocicleta, 1: automóvil, 2: camión): "))

    pago = int(input("Ingrese la forma de pago (1: manual, 2 telepeaje): "))
    while pago not in [1, 2]:
        print("Digito erróneo, ingrese los indicados")
        pago = int(input("Ingrese la forma de pago (1: manual, 2 telepeaje): "))

    cab = int(input("Ingrese país de la cabina (0: Argentina - 1: Bolivia - 2: Brasil - 3: Paraguay - 4: "
                    "Uruguay): "))
    while cab not in [0, 1, 2, 3, 4]:
        print("Digito erróneo, ingrese los indicados")
        cab = int(input("Ingrese país de la cabina (0: Argentina - 1: Bolivia - 2: Brasil - 3: Paraguay - 4: "
                        "Uruguay): "))

    dis = int(input("Ingrese los kilómetros recorridos desde la cabina anterior (0 si es la primera cabina): "))
    while dis < 0:
        print("El kilometraje ingresado debe ser mayor o igual a 0")
        dis = int(input("Ingrese los kilómetros recorridos desde la cabina anterior (0 si es la primera "
                        "cabina): "))
    return cod, pat, tipo, pago, cab, dis


def identificar_pais(pat):
    lp = len(pat)

    if lp < 6 or lp > 7:
        return 'Otro'

    if lp == 6:
        if pat[0:4].isalpha() and pat[4:6].isdigit():
            return 5
        else:
            return 6

    if pat[0:2].isalpha() and pat[2:5].isdigit() and pat[5:7].isalpha():
        return 0

    if pat[0:2].isalpha() and pat[2:7].isdigit():
        return 1

    if pat[0:3].isalpha() and pat[3].isdigit() and pat[4].isalpha() and pat[5:7].isdigit():
        return 2

    if pat[0:4].isalpha() and pat[4:7].isdigit():
        return 3

    if pat[0:3].isalpha() and pat[3:7].isdigit():
        return 4

    return 6


def punto_3(bf):
    nombres_paises = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay", "Chile", "Otro",)
    if os.path.exists(bf):
        mb = open(bf, "rb")
        t = os.path.getsize(bf)
        print("Listado de tickets...")
        while mb.tell() < t:
            r = pickle.load(mb)
            pais = identificar_pais(r.patente)
            print(r, " | PAIS DE LA PATENTE:", nombres_paises[pais])
        mb.close()
        print("Listo...")
    else:
        print("El archivo", bf, "no existe...")
    print()


def punto_4(bf):
    cont = 0
    if os.path.exists(bf):
        p = input('Ingrese la petente que desea buscar: ')
        mb = open(bf, "rb")
        t = os.path.getsize(bf)
        while mb.tell() < t:
            r = pickle.load(mb)
            if r.patente == p:
                print(r)
                cont += 1
        print()
        print('Total de patente encontradas: ', cont)
        mb.close()
    else:
        print("El archivo", bf, "no existe...")
    print()


def punto_5(bf):
    if os.path.exists(bf):
        c = int(input('Ingrese el código de ticket que desea buscar: '))
        mb = open(bf, "rb")
        t = os.path.getsize(bf)
        registro_encontrado = False

        while mb.tell() < t:
            r = pickle.load(mb)
            if r.codigo == c:
                print("Registro encontrado:")
                print(r)
                registro_encontrado = True
                break

        mb.close()

        if not registro_encontrado:
            print("No se encontró un registro con el código de ticket:", c)

    else:
        print("El archivo", bf, "no existe.")
    print()


def punto_6(bf):
    if os.path.exists(bf):
        contador_combinaciones = [[0] * 5 for _ in range(3)]  # Matriz de conteo
        mb = open(bf, "rb")
        t = os.path.getsize(bf)

        while mb.tell() < t:
            r = pickle.load(mb)
            contador_combinaciones[r.tipo_vehiculo][r.pais_cabina] += 1

        mb.close()

        nombres_paises = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay", "Chile", "Otro")

        # Mostrar la cantidad de vehículos por combinación
        for tipo in range(3):
            for pais in range(5):
                cantidad = contador_combinaciones[tipo][pais]
                if cantidad > 0:
                    print(f"Tipo de Vehículo: {tipo}, País de Cabina: {nombres_paises[pais]}, Cantidad: {cantidad}")

    else:
        print("El archivo", bf, "no existe.")
    print()


def main():
    print("1. Crear archivo binario")
    print("2. Cargar por teclado un ticket")
    print("3. Mostrar todos los datos de todos los registros")
    print("4. Mostrar registros filtrando por patente")
    print("5. Buscar si existe registro filtrando por código de ticket")
    print("6. Mostrar cantidad de vehículos de cada combinación posible entre tipo de vehículo y país de cabina")
    print("7. Mostrar cantidad total de vehículos contados por cada tipo de vehículo posible")
    print("8. Calcular y mostrar distancia promedio desde la última cabina recorrida entre todos los vehículos")
    op = int(input('Ingrese opción: '))
    csv = "peajes-tp4.csv"
    binario = "tickets.dat"
    if op == 1:
        punto_1(csv, binario)
    if op == 2:
        punto_2(binario)
    if op == 3:
        punto_3(binario)
    if op == 4:
        punto_4(binario)
    if op == 5:
        punto_5(binario)
    if op == 6:
        punto_6(binario)
    if op == 7:
        pass
    if op == 8:
        pass


if __name__ == "__main__":
    main()
