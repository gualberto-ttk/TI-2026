nome = input("Digite o nome completo do aluno: ")
matricula = int(input("Digite a matrícula: "))
nota1 = float(input("Digite a primeira nota: "))
nota2 = float(input("Digite a segunda nota: "))


media = (nota1 + nota2) / 2

print("\n--- Relatório do Aluno ---")
print("Nome:", nome)
print("Matrícula:", matricula)
print("Nota 1:", nota1)
print("Nota 2:", nota2)
print("Média:", media)