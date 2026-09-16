"""Calculadora de terminal com operações extras e histórico da sessão."""

import math


OPERACOES = {
    "1": ("Adição (+)", "+"),
    "2": ("Subtração (-)", "-"),
    "3": ("Multiplicação (*)", "*"),
    "4": ("Divisão (/)", "/"),
    "5": ("Potência (base elevada ao expoente)", "^"),
    "6": ("Raiz quadrada", "√"),
    "7": ("Porcentagem (X% de um valor)", "% de"),
    "8": ("Resto da divisão (%)", "%"),
}


def formatar_numero(numero):
    """Exibe os números usando vírgula como separador decimal."""
    return format(numero, ".12g").replace(".", ",")


def ler_numero(mensagem):
    """Repete a pergunta até receber um número real finito."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            numero = float(entrada)
            if not math.isfinite(numero):
                raise ValueError
            return numero
        except ValueError:
            print("Erro: digite um número válido e finito (ex.: 10 ou 2,5).")


def calcular(opcao, num1, num2=None):
    """Calcula uma operação sem depender do terminal."""
    if opcao not in OPERACOES:
        raise ValueError("Opção de operação inválida.")

    if not math.isfinite(num1):
        raise ValueError("Os números devem ser finitos.")

    if opcao != "6":
        if num2 is None:
            raise ValueError("Esta operação precisa de dois números.")
        if not math.isfinite(num2):
            raise ValueError("Os números devem ser finitos.")

    if opcao in ("4", "8") and num2 == 0:
        raise ValueError("Não é possível dividir por zero.")

    if opcao == "6" and num1 < 0:
        raise ValueError("A raiz quadrada de um número negativo não é real.")

    if opcao == "5":
        if num1 == 0 and num2 < 0:
            raise ValueError("Zero não pode ser elevado a um expoente negativo.")
        if num1 < 0 and not float(num2).is_integer():
            raise ValueError("Uma base negativa exige um expoente inteiro.")

    try:
        if opcao == "1":
            resultado = num1 + num2
        elif opcao == "2":
            resultado = num1 - num2
        elif opcao == "3":
            resultado = num1 * num2
        elif opcao == "4":
            resultado = num1 / num2
        elif opcao == "5":
            resultado = math.pow(num1, num2)
        elif opcao == "6":
            resultado = math.sqrt(num1)
        elif opcao == "7":
            resultado = (num1 / 100) * num2
        else:
            resultado = num1 % num2
    except OverflowError:
        raise ValueError("O resultado excede o limite numérico da calculadora.") from None

    if not math.isfinite(resultado):
        raise ValueError("O resultado excede o limite numérico da calculadora.")

    return resultado


def exibir_menu():
    print("\n=== CALCULADORA ===")
    for opcao, (descricao, _) in OPERACOES.items():
        print(f"{opcao} - {descricao}")
    print("9 - Ver histórico")
    print("10 - Limpar histórico")
    print("0 - Sair")


def calculadora():
    """Executa o menu até o usuário escolher sair."""
    historico = []
    print("Use ponto ou vírgula nos decimais, sem separadores de milhar.")

    try:
        while True:
            exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                print("Calculadora encerrada.")
                return

            if opcao == "9":
                print("\n=== HISTÓRICO DA SESSÃO ===")
                if historico:
                    for indice, registro in enumerate(historico, start=1):
                        print(f"{indice}. {registro}")
                else:
                    print("Nenhum cálculo realizado.")
                continue

            if opcao == "10":
                historico.clear()
                print("Histórico limpo.")
                continue

            if opcao not in OPERACOES:
                print("Opção inválida! Escolha uma das opções do menu.")
                continue

            if opcao == "6":
                num1 = ler_numero("Digite o número para calcular a raiz: ")
                num2 = None
            elif opcao == "7":
                num1 = ler_numero("Digite a porcentagem (ex.: 15 para 15%): ")
                num2 = ler_numero("Digite o valor base: ")
            elif opcao == "5":
                num1 = ler_numero("Digite a base: ")
                num2 = ler_numero("Digite o expoente: ")
            else:
                num1 = ler_numero("Digite o primeiro número: ")
                num2 = ler_numero("Digite o segundo número: ")

            try:
                resultado = calcular(opcao, num1, num2)
            except ValueError as erro:
                print(f"Erro: {erro}")
                continue

            if opcao == "6":
                expressao = f"√({formatar_numero(num1)})"
            else:
                operador = OPERACOES[opcao][1]
                expressao = (
                    f"{formatar_numero(num1)} {operador} "
                    f"{formatar_numero(num2)}"
                )

            registro = f"{expressao} = {formatar_numero(resultado)}"
            historico.append(registro)
            print(f"\nResultado: {registro}")

    except (KeyboardInterrupt, EOFError):
        print("\nCalculadora encerrada.")


if __name__ == "__main__":
    calculadora()