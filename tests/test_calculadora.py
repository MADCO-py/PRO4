import unittest
from fractions import Fraction
import calculadora as c

class Pruebas(unittest.TestCase):
    def test_ejemplos(self):
        for expresion, p, esperado in c.EJEMPLOS:
            with self.subTest(p=p): self.assertEqual(c.calcular(expresion, p)[0], esperado)

    def test_operaciones_en_varios_primos(self):
        for p in [2,3,5,7,11,23,29,31,37,41,97]:
            for a in range(-3, p + 1):
                for b in range(-2, 5):
                    for op, esperado in [('+',(a+b)%p),('-',(a-b)%p),('*',(a*b)%p)]:
                        self.assertEqual(c.calcular(f'({a}){op}({b})',p)[0],esperado)
                    if b%p:
                        inv=next(i for i in range(1,p) if (b*i)%p==1)
                        self.assertEqual(c.calcular(f'({a})/({b})',p)[0],a*inv%p)
                    else:
                        with self.assertRaises(ValueError):c.calcular(f'({a})/({b})',p)
                for e in range(7):self.assertEqual(c.calcular(f'({a})^{e}',p)[0],a**e%p)

    def test_precedencia_y_exponentes(self):
        for exp,p,r in [('2^3^2',23,pow(2,9,23)),('-2^2',7,3),('(-2)^2',7,4),
                        ('2^-1',7,4),('2^(3+4)',5,3),('2^(8/2)',7,2),
                        ('0^0',5,1),('2^(-3)',7,1),('2+3*4',11,3)]:
            self.assertEqual(c.calcular(exp,p)[0],r)
        for exp in ['2^(1/2)','0^-1','2^1000001']:
            with self.assertRaises(ValueError):c.calcular(exp,7)

    def test_ejemplos_con_oraculo_racional(self):
        valores=[Fraction((7**3+4*5)*2),Fraction((15+7)*3-2**4,5),
                 Fraction(3**4*2+7,11-5**2),Fraction(8*(13+5**2)-3**3,2**4+1),
                 Fraction(6**2*3+7,2**3-5)*(11+4**3)-9]
        for (exp,p,_),valor in zip(c.EJEMPLOS,valores):
            inv=next(i for i in range(1,p) if valor.denominator*i%p==1)
            self.assertEqual(c.calcular(exp,p)[0],valor.numerator*inv%p)

    def test_entradas_invalidas(self):
        for exp in ['', '2**3','2(3)','(2+3','2+3)','2//3','2.5','a+1','__import__(1)','2 3']:
            with self.subTest(exp=exp),self.assertRaises(ValueError):c.calcular(exp,7)
        for p in [0,1,4,9,25,-7,True,1_000_000_001]:
            with self.assertRaises(ValueError):c.calcular('2+3',p)
        with self.assertRaises(ValueError):c.calcular('1/(3-3)',7)
        with self.assertRaises(ValueError):c.calcular('1/7',7)

if __name__=='__main__':unittest.main()
