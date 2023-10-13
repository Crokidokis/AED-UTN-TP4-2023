import os.path
import pickle
from clase import *


def validacion_bf_existe(bf):
    if os.path.exists(bf):
        return True
    else:
        print("El archivo ", bf, "no existe, porfavor cree uno.")
        return False


def punto_1(tf, bf):
    if os.path.exists(tf):
        if os.path.exists(bf):
            print("Advertencia: Se creará un archivo nuevo y se perderán los registros viejos")
            print("Ingrese 1 para continuar o 0 para cancelar la operación")
            respuesta = int(input("Ingrese su opción: "))
            if respuesta == 1:
                print("Se eliminó el archivo de registros ya existente...")
            elif respuesta == 0:
                print("Operación cancelada.")
                return main()
            while respuesta != 1 and respuesta != 0:
                print("Opcion inválida, ingrese una correcta.")
                respuesta = int(input("Ingrese su opción: "))

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

    if lp == 7:
        if pat[0:2].isalpha() and pat[2:5].isdigit() and pat[5:7].isalpha():
            return 0
        elif pat[0:2].isalpha() and pat[2:7].isdigit():
            return 1
        elif pat[0:3].isalpha() and pat[3].isdigit() and pat[4].isalpha() and pat[5:7].isdigit():
            return 2
        elif pat[0:4].isalpha() and pat[4:7].isdigit():
            return 3
        elif pat[0:3].isalpha() and pat[3:7].isdigit():
            return 4
        else:
            return 6
    elif lp == 6:
        if pat[0:4].isalpha() and pat[4:6].isdigit():
            return 5
        else:
            return 6
    else:
        return 6


def punto_3(bf):
    nombres_paises = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay", "Chile", "Otro",)
    if validacion_bf_existe(bf):
        mb = open(bf, "rb")
        t = os.path.getsize(bf)
        print("Listado de tickets...")
        while mb.tell() < t:
            r = pickle.load(mb)
            pais = identificar_pais(r.patente)
            print(r, " | PAIS DE LA PATENTE:", nombres_paises[pais])
        mb.close()
        print("Listo...")


def punto_4(bf):
    cont = 0
    if validacion_bf_existe(bf):
        p = input('Ingrese la patente que desea buscar: ')
        mb = open(bf, "rb")
        t = os.path.getsize(bf)
        while mb.tell() < t:
            r = pickle.load(mb)
            if r.patente == p:
                print('REGISTRO ENCONTRADO:')
                print('=' * 150)
                print(r)
                print('=' * 150)
                cont += 1
        print()
        if cont == 0:
            print('No se encontró ningun registro con esa patente')

        else:
            print('Total de patente encontradas: ', cont)

        print()
        mb.close()


def punto_5(bf):
    if validacion_bf_existe(bf):
        c = int(input('Ingrese el código de ticket que desea buscar: '))
        mb = open(bf, "rb")
        t = os.path.getsize(bf)
        registro_encontrado = False

        while mb.tell() < t:
            r = pickle.load(mb)
            if r.codigo == c:
                print("REGISTRO ENCONTRADO:")
                print('=' * 150)
                print(r)
                print('=' * 150)
                print()
                registro_encontrado = True
                break

        mb.close()

        if not registro_encontrado:
            print('=' * 150)
            print("No se encontró un registro con el código de ticket:", c)
            print('=' * 150)
            print()


def punto_6(bf):
    if validacion_bf_existe(bf):
        contador_combinaciones = [[0] * 5 for f in range(3)]
        mb = open(bf, "rb")
        t = os.path.getsize(bf)

        while mb.tell() < t:
            r = pickle.load(mb)
            tipo = r.tipo
            pais = r.pais_cabina
            contador_combinaciones[tipo][pais] += 1

        mb.close()

        nombres_paises = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay")

        for tipo in range(3):
            for pais in range(5):
                cantidad = contador_combinaciones[tipo][pais]
                print('=' * 200)
                if cantidad > 0:
                    print(f"Tipo de Vehículo: {tipo}, País de Cabina: {nombres_paises[pais]}, Cantidad: {cantidad}")
                print('=' * 200)
                print()

        return contador_combinaciones


def punto_7(m):
    c = 3
    f = 5
    cont_filas = [0] * c
    for i in range(c):
        for j in range(f):
            cont_filas[i] += m[i][j]

    cont_cols = [0] * f
    for c in range(len(m[0])):
        for f in range(len(m)):
            cont_cols[c] += m[f][c]

    return cont_filas, cont_cols


def display(f, c):
    tipo = 'Motocicleta', 'Automovil', 'Camión'
    nombres_paises = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay", "Chile", "Otro")
    print()
    print('=' * 100)
    for i in range(len(f)):
        print(f'Cantidad de vehículos del tipo {tipo[i]}: ', f[i])
    print('=' * 100)
    for j in range(len(c)):
        print(f'Cantidad de vehículos que pasaron por la cabina de {nombres_paises[j]}: ', c[j])
    print('=' * 100)
    print()


def punto_8(bf):
    if validacion_bf_existe(bf):
        nombres_paises = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay", "Chile", "Otro",)
        mb = open(bf, 'rb')
        t = os.path.getsize(bf)
        cont = acum = 0
        while mb.tell() < t:
            r = pickle.load(mb)
            acum += r.km_recorridos
            cont += 1
        promedio = acum / cont if cont > 0 else 0
        mb.close()
        vector_mayor_promedio = arreglo_may_prome(bf, promedio)
        print('=' * 200)
        for i in range(len(vector_mayor_promedio)):
            pais = identificar_pais(vector_mayor_promedio[i].patente)
            print(vector_mayor_promedio[i], " | PAIS DE LA PATENTE:", nombres_paises[pais])
        print('=' * 200)
        print('El promedio es: ', promedio, 'km')
        print('=' * 200)
        print()


def arreglo_may_prome(bf, prom):
    v = []
    mb = open(bf, 'rb')
    t = os.path.getsize(bf)
    while mb.tell() < t:
        r = pickle.load(mb)
        if r.km_recorridos > prom:
            v.append(r)
    mb.close()
    return shell_sort(v)


def shell_sort(v):
    n = len(v)
    h = 1
    while h <= n // 9:
        h = 3 * h + 1
    while h > 0:
        for j in range(h, n):
            y = v[j].km_recorridos
            k = j - h
            while k >= 0 and y < v[k].km_recorridos:
                v[k + h].km_recorridos = v[k].km_recorridos
                k -= h
            v[k + h].km_recorridos = y
        h //= 3
    return v


def main():
    op = -1
    m = 0
    while op != 9:
        print("1. Crear archivo binario")
        print("2. Cargar por teclado un ticket")
        print("3. Mostrar todos los datos de todos los registros")
        print("4. Mostrar registros filtrando por patente")
        print("5. Buscar si existe registro filtrando por código de ticket")
        print("6. Mostrar cantidad de vehículos de cada combinación posible entre tipo de vehículo y país de cabina")
        print("7. Mostrar cantidad total de vehículos contados por cada tipo de vehículo posible")
        print("8. Calcular y mostrar distancia promedio desde la última cabina recorrida entre todos los vehículos")
        print("9. Salir del programa")
        op = int(input('Ingrese opción: '))
        csv = "peajes-tp4.csv"
        binario = "tickets.dat"
        if op == 1:
            punto_1(csv, binario)
        elif op == 2:
            punto_2(binario)
        elif op == 3:
            punto_3(binario)
        elif op == 4:
            punto_4(binario)
        elif op == 5:
            punto_5(binario)
        elif op == 6:
            m = punto_6(binario)
        elif op == 7:
            if m == 0 or m is None:
                print('Primero debe crear la matriz de conteo')
            else:
                tot_filas, tot_cols = punto_7(m)
                display(tot_filas, tot_cols)
        elif op == 8:
            punto_8(binario)
        elif op == 9:
            print()
            print('=' * 50)
            print('Usted ha salido con éxito')
            print('=' * 50)
        else:
            print("Ingrese una opción correcta.")


if __name__ == "__main__":
    main()
