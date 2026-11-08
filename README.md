# Proyecto 4: calculadora gráfica modular

Python 3.10 o posterior y Tkinter. El programa usa únicamente la biblioteca estándar.

## Ejecutar desde esta carpeta

```bash
python3 calculadora.py
```

En Linux se puede abrir la carpeta con:

```bash
cd ~/Documentos/MAD/VIS/PRO4
python3 calculadora.py
```

En Windows, desde la carpeta descargada: `py calculadora.py`.
Si Python no incluye Tkinter, hay que instalar el paquete Tkinter correspondiente a la distribución; en Debian/Ubuntu se llama `python3-tk`.

## Uso

1. Introducir un primo p (2 a 1000000000).
2. Escribir la expresión sin el sufijo `(mod p)`. Usar `^` para potencia y `*` para multiplicación.
3. Pulsar `=` o Enter. El resultado y el procedimiento aparecen debajo.
4. Para los ejemplos de la tarea, elegir uno y pulsar **Cargar ejemplo**, después `=`.

Resultados de los cinco ejemplos: **13, 10, 30, 25 y 37**.
La división es modular, no decimal. No está definida si el denominador se reduce a cero.

## Convenciones

- Potencia antes que signos unarios; luego multiplicación/división y suma/resta.
- `2^3^2` significa `2^(3^2)`; `-2^2` significa `-(2^2)`.
- Los exponentes se calculan como enteros, sin reducirlos módulo p.
- Dentro de un exponente, las divisiones deben ser exactas y las potencias internas deben tener exponente no negativo.
- Se admite exponente negativo cuando la base tiene inverso. `0^0` se define como 1.
- Hasta 500 caracteres, 200 elementos y 100 cifras por entero.
- Exponentes y pasos enteros intermedios: entre -1000000 y 1000000.
  Una potencia interna del exponente admite hasta 1000 y una cota adicional de tamaño para evitar cálculos excesivos.

## Pruebas

```bash
python3 -m unittest discover -s tests -v
```

La prueba de interfaz requiere una sesión gráfica. Para Linux sin escritorio y con Xvfb instalado:

```bash
xvfb-run -a python3 -m unittest discover -s tests -v
```

## Documentación y entrega

- `calculadora.py`: código completo, se puede ejecutar sin otros archivos del proyecto.
- `documentacion/informe.tex`: fuente del informe.
- `documentacion/informe.pdf`: PDF compilado.
- `documentacion/capturas/`: capturas reales necesarias para recompilar el TEX.
- `documentacion/pruebas.txt`: registro de las seis pruebas.

Para recompilar, conservar las imágenes junto al TEX:

```bash
cd documentacion
pdflatex informe.tex
pdflatex informe.tex
```

El informe documenta la asistencia de un LLM y la validación matemática y funcional posterior.
