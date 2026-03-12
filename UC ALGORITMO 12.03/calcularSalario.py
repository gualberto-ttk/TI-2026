def calcular_ganho(vh, hd, dm=22):
   
    extra = (50 * dm) if hd > 8 else 0
    return (vh * hd * dm) + extra

v = float(input("Valor/hora: "))
h = int(input("Horas/dia: "))

print(f"Total: R$ {calcular_ganho(v, h):.2f}")