import matplotlib.pyplot as plt
import locale
import os
import urllib.request

import numpy as np
from bs4 import BeautifulSoup
import certifi
import ssl
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years_csv, write_cleaned_csv, \
    write_html, DIRECTORIO_FICHEROS
import csv

