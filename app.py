from flask import Flask, render_template

app = Flask(__name__)

# Configuración de categorías y colores
categorias_colores = {
    'Libros': '#CC0000',        # rojo oscuro
    'Ropa': '#6B00CC',          # violeta oscuro
    'Antigüedades': '#CCAA00',  # amarillo oscuro/dorado
    'Ferreteria': '#8B5A00',    # cobre oscuro
    'Herreria': '#4D4D4D',      # gris oscuro
    'Camaras': '#000000',       # negro
    'Comida': '#CC7700'         # naranja oscuro
}

# Datos de las ferias con coordenadas exactas
ferias = [
    {
        'nombre': 'Feria de Tristán Narvaja',
        'lat': -34.9015,
        'lng': -56.1785,
        'cuadras': [
            {
                'nombre': 'Inicio - 18 de Julio (media cuadra)',
                'coordenadas': [
                    [-34.90219074248287, -56.176724721855],
                    [-34.902411522128624, -56.177289502325344]
                ],
                'categoria_principal': 'Libros',
                'productos': {
                    'Libros': ['Libros usados', 'Comics', 'Revistas', 'Libros antiguos'],
                    'Antigüedades': ['Vinilos', 'Objetos vintage']
                }
            },
            {
                'nombre': 'Tristán Narvaja completo',
                'coordenadas': [
                    [-34.902411522128624, -56.177289502325344],
                    [-34.896851357852945, -56.18068925224037]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Plantas', 'Flores', 'Especias', 'Frutos secos'],
                    'Ropa': ['Ropa nueva', 'Zapatos'],
                    'Ferreteria': ['Herramientas']
                },
                'negocios': [
                    {
                        'nombre': 'Frutas Don José',
                        'descripcion': 'Frutas frescas de estación, directo del mercado modelo',
                        'especialidad': 'Naranjas, manzanas y frutas exóticas'
                    },
                    {
                        'nombre': 'Verdulería La Abundancia',
                        'descripcion': 'Verduras orgánicas y productos de granja',
                        'especialidad': 'Tomates, lechugas y vegetales orgánicos'
                    },
                    {
                        'nombre': 'Especias del Mundo',
                        'descripcion': 'Especias, hierbas aromáticas y frutos secos',
                        'especialidad': 'Especias importadas, nueces y almendras'
                    }
                ]
            },
            {
                'nombre': 'Tramo 2',
                'coordenadas': [
                    [-34.90238760619995, -56.180080365712584],
                    [-34.9006225908998, -56.175744674746866]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa nueva', 'Zapatos', 'Carteras', 'Accesorios', 'Cinturones', 'Bufandas'],
                    'Antigüedades': ['Joyas vintage']
                }
            },
            {
                'nombre': 'Tramo 3',
                'coordenadas': [
                    [-34.90156106717214, -56.180594769725474],
                    [-34.90029541316459, -56.17731938090875]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Objetos vintage', 'Joyas antiguas', 'Cuadros', 'Porcelanas'],
                    'Libros': ['Libros antiguos'],
                    'Camaras': ['Cámaras vintage', 'Proyectores']
                }
            },
            {
                'nombre': 'Tramo 4',
                'coordenadas': [
                    [-34.90086366839699, -56.18097269920432],
                    [-34.89951190329039, -56.177707808428686]
                ],
                'categoria_principal': 'Ferreteria',
                'productos': {
                    'Ferreteria': ['Herramientas', 'Tornillos', 'Candados', 'Pinturas'],
                    'Herreria': ['Repuestos metálicos', 'Cadenas', 'Rejas'],
                    'Camaras': ['Electrónica usada', 'Celulares', 'Cables']
                }
            }
        ]
    }
]

@app.route('/')
def index():
    return render_template('lobby.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html', ferias=ferias, categorias_colores=categorias_colores)

@app.route('/tristan-narvaja')
def tristan_narvaja():
    # Por ahora redirige al lobby, más adelante tendrá su propia página
    return render_template('lobby.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)