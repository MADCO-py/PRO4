import tkinter as tk
import unittest
import calculadora as c

class PruebasGUI(unittest.TestCase):
    def test_interaccion_real(self):
        raiz=tk.Tk()
        try:
            app=c.Calculadora(raiz);raiz.update()
            for i,(_,p,esperado) in enumerate(c.EJEMPLOS):
                app.ejemplo.current(i);app.cargar();app.resolver();raiz.update()
                self.assertEqual(app.resultado.get(),f'Resultado: {esperado} (mod {p})')
            app.modulo.set('9');app.resolver()
            self.assertIn('no es primo',app.resultado.get())
            app.modulo.set('7');app.expresion.set('1/7');app.resolver()
            self.assertIn('División no definida',app.resultado.get())
            app.limpiar();self.assertEqual(app.expresion.get(),'')
            app.insertar('2');app.insertar('+');app.insertar('3');app.resolver()
            self.assertEqual(app.resultado.get(),'Resultado: 5 (mod 7)')
        finally:raiz.destroy()

if __name__=='__main__':unittest.main()
