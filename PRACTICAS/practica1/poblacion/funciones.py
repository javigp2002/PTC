## Escribe a cadena el formato html
import os


def html_start(title):
    html = """ <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>""" + title + """"</title>
    <link rel="stylesheet" href="./ayudas/estilo.css">
  </head>
  <body>
"""
    return html

# Escribe a cadena el formato final del html
def html_end():
    html = """ </body> </html> """
    return html

#cambiar el nombre de un archivo y devolver el path
