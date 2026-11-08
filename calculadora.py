#!/usr/bin/env python3
"""Calculadora gráfica de Z_p. Python 3.10+, tkinter, sin paquetes externos.
Ejecutar: python3 calculadora.py
"""
import re
from math import isqrt
import tkinter as tk
from tkinter import ttk

EJEMPLOS = [
    ('(7^3 + 4 * 5) * 2', 23, 13),
    ('((15 + 7) * 3 - 2^4) / 5', 29, 10),
    ('(3^4 * 2 + 7) / (11 - 5^2)', 31, 30),
    ('(8 * (13 + 5^2) - 3^3) / (2^4 + 1)', 37, 25),
    ('((6^2 * 3 + 7) / (2^3 - 5)) * (11 + 4^3) - 9', 41, 37),
]


def es_primo(p):
    if isinstance(p, bool) or not isinstance(p, int) or p < 2:
        return False
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    return all(p % d for d in range(3, isqrt(p) + 1, 2))


class Analizador:
    """Convierte los símbolos permitidos en un árbol, sin usar eval ni exec."""
    def __init__(self, texto):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError('Escribe una expresión.')
        if len(texto) > 500:
            raise ValueError('La expresión admite hasta 500 caracteres.')
        if re.search(r'[^0-9\s+*/^()\-]', texto):
            raise ValueError('Usa solo enteros, +, -, *, /, ^ y paréntesis.')
        self.tokens = re.findall(r'\d+|[^\s]', texto)
        if len(self.tokens) > 200:
            raise ValueError('La expresión tiene demasiados elementos (máximo 200).')
        self.i = 0

    def ver(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else ''

    def tomar(self):
        t = self.ver()
        self.i += 1
        return t

    def analizar(self):
        arbol = self.suma()
        if self.ver():
            raise ValueError(f'Elemento inesperado: {self.ver()}. Usa * para multiplicar.')
        return arbol

    def suma(self):
        nodo = self.producto()
        while self.ver() in ('+', '-'):
            nodo = (self.tomar(), nodo, self.producto())
        return nodo

    def producto(self):
        nodo = self.signo()
        while self.ver() in ('*', '/'):
            nodo = (self.tomar(), nodo, self.signo())
        return nodo

    def signo(self):
        if self.ver() in ('+', '-'):
            return ('u' + self.tomar(), self.signo())
        return self.potencia()

    def potencia(self):
        nodo = self.atomo()
        if self.ver() == '^':
            self.tomar()
            nodo = ('^', nodo, self.signo())
        return nodo

    def atomo(self):
        t = self.tomar()
        if t.isdigit():
            if len(t) > 100:
                raise ValueError('Cada entero admite hasta 100 cifras.')
            return ('n', int(t))
        if t == '(':
            nodo = self.suma()
            if self.tomar() != ')':
                raise ValueError('Falta cerrar un paréntesis.')
            return nodo
        raise ValueError('Falta un número o hay un operador/paréntesis mal colocado.')


def entero(nodo):
    """Evalúa exponentes como enteros, sin reducirlos módulo p."""
    op = nodo[0]
    if op == 'n':
        r = nodo[1]
    elif op in ('u+', 'u-'):
        r = entero(nodo[1]) * (-1 if op == 'u-' else 1)
    else:
        a, b = entero(nodo[1]), entero(nodo[2])
        if op == '+': r = a + b
        elif op == '-': r = a - b
        elif op == '*': r = a * b
        elif op == '/':
            if b == 0 or a % b:
                raise ValueError('El exponente debe ser entero; su división debe ser exacta.')
            r = a // b
        else:
            if b < 0:
                raise ValueError('Dentro del exponente no se admiten potencias negativas.')
            if b > 1000 or (abs(a) > 1 and b * max(1, abs(a).bit_length() - 1) > 24):
                raise ValueError('El cálculo del exponente excede el límite permitido.')
            r = a ** b
    if abs(r) > 1_000_000:
        raise ValueError('Los exponentes y sus pasos intermedios deben estar entre -1000000 y 1000000.')
    return r


def calcular(expresion, p):
    """Retorna (representante entre 0 y p-1, lista de pasos)."""
    if isinstance(p, bool) or not isinstance(p, int) or not 2 <= p <= 1_000_000_000:
        raise ValueError('p debe ser un entero primo entre 2 y 1000000000.')
    if not es_primo(p):
        raise ValueError('p no es primo. Prueba con 2, 3, 5, 23, 29, 31, 37 o 41.')
    arbol = Analizador(expresion).analizar()
    pasos = []

    def evaluar(nodo):
        op = nodo[0]
        if op == 'n':
            return nodo[1] % p
        a = evaluar(nodo[1])
        if op in ('u+', 'u-'):
            r = a if op == 'u+' else (-a) % p
            pasos.append(f'{op[1]}({a}) ≡ {r} (mod {p})')
            return r
        if op == '^':
            b = entero(nodo[2])
            if a == 0 and b < 0:
                raise ValueError('No existe una potencia negativa de 0 módulo p.')
            r = pow(a, b, p)
            pasos.append(f'{a}^{b} ≡ {r} (mod {p})')
            return r
        b = evaluar(nodo[2])
        if op == '+': r = (a + b) % p
        elif op == '-': r = (a - b) % p
        elif op == '*': r = (a * b) % p
        else:
            if b == 0:
                raise ValueError(f'División no definida: el denominador es 0 módulo {p}.')
            inv = pow(b, -1, p)
            r = (a * inv) % p
            pasos.append(f'Inverso de {b}: {inv}, porque {b} × {inv} ≡ 1 (mod {p})')
        pasos.append(f'{a} {op} {b} ≡ {r} (mod {p})')
        return r

    resultado = evaluar(arbol)
    return resultado, pasos


class Calculadora:
    """Ventana, teclado, ejemplos, cálculo y mensajes de validación."""
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title('Proyecto 4 · Calculadora modular')
        ventana.geometry('850x730')
        ventana.minsize(760, 690)
        estilo = ttk.Style(ventana)
        estilo.theme_use('clam')
        estilo.configure('TButton', padding=7)
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill='both', expand=True)
        ttk.Label(marco, text='Calculadora de aritmética modular', font=('Sans', 18, 'bold')).pack(anchor='w')
        ttk.Label(marco, text='Escribe la expresión y el módulo primo p. La división utiliza el inverso modular.').pack(anchor='w', pady=(6, 12))
        fila = ttk.Frame(marco); fila.pack(fill='x')
        ttk.Label(fila, text='Primo p:').pack(side='left')
        self.modulo = tk.StringVar(value='23')
        ttk.Entry(fila, textvariable=self.modulo, width=12).pack(side='left', padx=8)
        self.ejemplo = ttk.Combobox(fila, values=[f'Ejemplo {i}' for i in range(1, 6)], state='readonly', width=15)
        self.ejemplo.current(0); self.ejemplo.pack(side='left', padx=12)
        ttk.Button(fila, text='Cargar ejemplo', command=self.cargar).pack(side='left')
        ttk.Label(marco, text='Expresión (sin escribir «mod p»):').pack(anchor='w', pady=(12, 4))
        self.expresion = tk.StringVar(value=EJEMPLOS[0][0])
        self.entrada = ttk.Entry(marco, textvariable=self.expresion, font=('Monospace', 12))
        self.entrada.pack(fill='x'); self.entrada.bind('<Return>', lambda _: self.resolver())
        teclado = ttk.Frame(marco); teclado.pack(fill='x', pady=10)
        for fila_n, teclas in enumerate([['7','8','9','+','('], ['4','5','6','-',')'], ['1','2','3','*','^'], ['0','/','←','Limpiar','=']]):
            for col, tecla in enumerate(teclas):
                cmd = self.resolver if tecla == '=' else self.limpiar if tecla == 'Limpiar' else lambda t=tecla: self.insertar(t)
                ttk.Button(teclado, text=tecla, command=cmd).grid(row=fila_n, column=col, sticky='ew', padx=3, pady=3)
        for col in range(5): teclado.columnconfigure(col, weight=1)
        self.resultado = tk.StringVar(value='Pulsa = o Enter para calcular.')
        self.etiqueta = ttk.Label(marco, textvariable=self.resultado, font=('Sans', 13, 'bold'), wraplength=790)
        self.etiqueta.pack(anchor='w', pady=7)
        ttk.Label(marco, text='Procedimiento:').pack(anchor='w')
        zona = ttk.Frame(marco); zona.pack(fill='both', expand=True, pady=5)
        self.pasos = tk.Text(zona, height=8, wrap='word', font=('Monospace', 11), state='disabled')
        barra = ttk.Scrollbar(zona, command=self.pasos.yview)
        self.pasos.configure(yscrollcommand=barra.set)
        barra.pack(side='right', fill='y'); self.pasos.pack(fill='both', expand=True)
        ttk.Label(marco, text='^ es potencia · exponentes enteros · 0^0 se define como 1 · usa * para multiplicar').pack(anchor='w')
        self.entrada.focus_set()

    def texto_pasos(self, texto):
        self.pasos.configure(state='normal'); self.pasos.delete('1.0', 'end')
        self.pasos.insert('1.0', texto); self.pasos.configure(state='disabled')

    def cargar(self):
        expresion, p, _ = EJEMPLOS[self.ejemplo.current()]
        self.expresion.set(expresion); self.modulo.set(str(p))
        self.resultado.set('Ejemplo cargado. Pulsa = para calcular.'); self.texto_pasos('')

    def insertar(self, tecla):
        self.entrada.focus_set()
        if tecla == '←':
            if self.entrada.selection_present(): self.entrada.delete('sel.first', 'sel.last')
            else:
                i = self.entrada.index('insert')
                if i: self.entrada.delete(i - 1, i)
        else:
            if self.entrada.selection_present(): self.entrada.delete('sel.first', 'sel.last')
            self.entrada.insert('insert', tecla)

    def limpiar(self):
        self.expresion.set(''); self.resultado.set('Escribe una nueva expresión.')
        self.texto_pasos(''); self.entrada.focus_set()

    def resolver(self):
        self.texto_pasos('')
        try:
            try: p = int(self.modulo.get())
            except ValueError: raise ValueError('Escribe un número entero para p.') from None
            resultado, pasos = calcular(self.expresion.get(), p)
            self.resultado.set(f'Resultado: {resultado} (mod {p})')
            self.etiqueta.configure(foreground='#174822')
            self.texto_pasos('\n'.join(pasos) or f'El entero se reduce a {resultado} módulo {p}.')
        except (ValueError, RecursionError) as error:
            mensaje = str(error) if isinstance(error, ValueError) else 'La expresión tiene demasiados niveles de paréntesis.'
            self.resultado.set('Error: ' + mensaje); self.etiqueta.configure(foreground='#9b1c1c')


def main():
    raiz = tk.Tk()
    Calculadora(raiz)
    raiz.mainloop()


if __name__ == '__main__':
    main()
