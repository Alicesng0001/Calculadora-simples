# Calculadora-simples
def calculadora():
    print("Escolha a operação:")
    print("1 - Adição (+)")
    print("2 - Subtração (-)")
    print("3 - Multiplicação (*)")
    print("4 - Divisão (/)")

    opcao = input("Digite o número da operação desejada: ")

    if opcao not in ["1", "2", "3", "4"]:
        print("Opção inválida!")
        return

    try:
        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))
    except ValueError:
        print("Erro: você deve digitar números válidos!")
        return

    if opcao == "1":
        resultado = num1 + num2
        operador = "+"
    elif opcao == "2":
        resultado = num1 - num2
        operador = "-"
    elif opcao == "3":
        resultado = num1 * num2
        operador = "*"
    elif opcao == "4":
        if num2 == 0:
            print("Erro: divisão por zero!")
            return
        resultado = num1 / num2
        operador = "/"

    print(f"\n{num1} {operador} {num2} = {resultado}")

calculadora()
