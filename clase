class Ticket:
    def __init__(self, codigo, patente, tipo, forma_de_pago, pais_cabina, km_recorridos ):
        self.codigo = codigo
        self.patente = patente
        self.tipo = tipo
        self.forma_de_pago = forma_de_pago
        self.pais_cabina = pais_cabina
        self.km_recorridos = km_recorridos

    def __str__(self):
        tipos_vehiculo = ("Motocicleta", "Automóvil", "Camión")
        formas_pago = ("Manual", "Telepeaje")
        cabinas = ("Argentina", "Bolivia", "Brasil", "Paraguay", "Uruguay")

        cad = 'Código: {:<15} | Patente: {:<10} | Tipo: {:<15} | Forma pago: {:<10} | Cabina: {:<15} | Distancia:' \
              ' {:>5}km'
        cad = cad.format(self.codigo, self.patente, tipos_vehiculo[self.tipo], formas_pago[self.forma_de_pago - 1],
                         cabinas[self.pais_cabina], self.km_recorridos)
        return cad
