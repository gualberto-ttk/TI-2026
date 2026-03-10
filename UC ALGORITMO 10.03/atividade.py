paciente = {}

paciente["nome"] = input ("Qua o seu nome:")
paciente["idade"] = int(input("Quantos anos você tem: "))
paciente[ "peso"] = float(input("Digite seu peso(kg): "))
paciente["altura"] = float(input("Digite sua altura(m): "))

imc = paciente["peso"] / (paciente["altura"] ** 2)

paciente["imc"] = imc

print("\n Dados")
print("Nome: ", paciente ["nome"])
print("Idade: ", paciente["idade"])
print("Peso: ", paciente["peso"])
print("Altura: ", paciente["altura"])
print("IMC: ", round(paciente["altura"], 2))