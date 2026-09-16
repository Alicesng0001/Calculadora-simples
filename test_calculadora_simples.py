"""Testes da calculadora. Execute: python -B -m unittest -v."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import calculadora_simples as c


class TestCalculadora(unittest.TestCase):
    def test_operacoes(self):
        casos = [
            ("1", 2, 3, 5),
            ("2", 2, 3, -1),
            ("3", 2, 3, 6),
            ("4", 7, 2, 3.5),
            ("5", 2, 3, 8),
            ("5", -2, 3, -8),
            ("6", 9, None, 3),
            ("7", 15, 200, 30),
            ("8", 7, 3, 1),
        ]
        for opcao, num1, num2, esperado in casos:
            with self.subTest(opcao=opcao, num1=num1):
                self.assertAlmostEqual(c.calcular(opcao, num1, num2), esperado)

    def test_erros(self):
        casos = [
            ("4", 1, 0),
            ("8", 1, 0),
            ("6", -1, None),
            ("5", 0, -1),
            ("5", -2, 0.5),
            ("5", 10, 1000),
            ("3", 1e308, 1e308),
            ("1", float("nan"), 1),
            ("1", 1, float("inf")),
            ("1", 1, None),
            ("99", 1, 2),
        ]
        for argumentos in casos:
            with self.subTest(argumentos=argumentos):
                with self.assertRaises(ValueError):
                    c.calcular(*argumentos)

    def test_entrada_invalida_e_virgula(self):
        with patch("builtins.input", side_effect=["abc", "nan", "inf", " 2,5 "]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(c.ler_numero("Número: "), 2.5)

    def test_menu_e_historico(self):
        entradas = [
            "99",
            "1", "2,5", "3",
            "9",
            "10",
            "9",
            "4", "1", "0",
            "6", "9",
            "7", "15", "200",
            "0",
        ]
        saida = io.StringIO()
        with patch("builtins.input", side_effect=entradas):
            with redirect_stdout(saida):
                c.calculadora()

        texto = saida.getvalue()
        self.assertIn("Opção inválida!", texto)
        self.assertIn("Resultado: 2,5 + 3 = 5,5", texto)
        self.assertIn("1. 2,5 + 3 = 5,5", texto)
        self.assertIn("Histórico limpo.", texto)
        self.assertIn("Nenhum cálculo realizado.", texto)
        self.assertIn("Erro: Não é possível dividir por zero.", texto)
        self.assertIn("Resultado: √(9) = 3", texto)
        self.assertIn("Resultado: 15 % de 200 = 30", texto)
        self.assertIn("Calculadora encerrada.", texto)

    def test_interrupcao(self):
        for erro in (EOFError, KeyboardInterrupt):
            with self.subTest(erro=erro):
                saida = io.StringIO()
                with patch("builtins.input", side_effect=erro):
                    with redirect_stdout(saida):
                        c.calculadora()
                self.assertIn("Calculadora encerrada.", saida.getvalue())

    def test_formatacao(self):
        self.assertEqual(c.formatar_numero(2.5), "2,5")
        self.assertEqual(c.formatar_numero(3.0), "3")


if __name__ == "__main__":
    unittest.main()