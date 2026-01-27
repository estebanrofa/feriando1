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
        'barrio': 'Cordón',
        'dia': 'Domingos',
        'lat': -34.9015,
        'lng': -56.1785,
        'cuadras': [
            {
                'nombre': 'Tristán Narvaja - Desde 18 de Julio hasta La Paz',
                'coordenadas': [
                    [-34.90199079826579, -56.176362633705146],
                    [-34.9023251619308, -56.17727458477021],
                    [-34.901502448887946, -56.1778485774994],
                    [-34.90076771957824, -56.17830991744996],
                    [-34.89996698913292, -56.17877125740051],
                    [-34.899245445121835, -56.17921650409699],
                    [-34.898215914033884, -56.17982268333436],
                    [-34.89755155165228, -56.1802089214325],
                    [-34.89688278409271, -56.180643439292915],
                    [-34.896781588527176, -56.180407404899604],
                    [-34.89897266463721, -56.18674278259278]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Plantas', 'Flores', 'Especias', 'Frutos secos'],
                    'Ropa': ['Ropa nueva', 'Zapatos', 'Accesorios'],
                    'Libros': ['Libros usados', 'Comics', 'Revistas']
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
                    }
                ]
            },
            {
                'nombre': 'Av. Uruguay',
                'coordenadas': [
                    [-34.89974260722322, -56.178229451179504],
                    [-34.89996258949352, -56.17878198623658],
                    [-34.900288162172274, -56.17956519126893]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa nueva', 'Ropa usada', 'Zapatos', 'Carteras', 'Accesorios'],
                    'Antigüedades': ['Joyas vintage', 'Relojes']
                }
            },
            {
                'nombre': 'Pdu (Propios y Desarrollo Urbano)',
                'coordenadas': [
                    [-34.89871308236705, -56.17822408676148],
                    [-34.89921904705001, -56.179146766662605],
                    [-34.89984379914075, -56.18029475212098],
                    [-34.90028376255009, -56.18134617805482]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Objetos vintage', 'Cuadros', 'Porcelanas', 'Muebles antiguos'],
                    'Libros': ['Libros antiguos', 'Mapas'],
                    'Camaras': ['Cámaras vintage', 'Equipos fotográficos']
                }
            },
            {
                'nombre': 'Magallanes',
                'coordenadas': [
                    [-34.89911785436277, -56.18204355239869],
                    [-34.89842270122825, -56.18244588375092],
                    [-34.897696743889895, -56.182891130447395],
                    [-34.89719516961729, -56.183164715766914],
                    [-34.89672439097846, -56.183481216430664]
                ],
                'categoria_principal': 'Ferreteria',
                'productos': {
                    'Ferreteria': ['Herramientas', 'Tornillos', 'Candados', 'Pinturas', 'Cerraduras'],
                    'Herreria': ['Repuestos metálicos', 'Cadenas', 'Rejas']
                }
            },
            {
                'nombre': 'Minas',
                'coordenadas': [
                    [-34.90063133197708, -56.18228495121003],
                    [-34.89944783005727, -56.182907223701484],
                    [-34.898739480601485, -56.18333101272584],
                    [-34.89798272784974, -56.18376016616822],
                    [-34.89713357256563, -56.18428587913514]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa deportiva', 'Zapatos', 'Mochilas', 'Gorras'],
                    'Comida': ['Snacks', 'Bebidas']
                }
            },
            {
                'nombre': 'Gaboto',
                'coordenadas': [
                    [-34.90045534764091, -56.18001580238343],
                    [-34.899870197011765, -56.180353760719306],
                    [-34.89932903895997, -56.180675625801086],
                    [-34.898985863713776, -56.180874109268196],
                    [-34.89869548353938, -56.18104577064515],
                    [-34.89805752349036, -56.18151247501374],
                    [-34.897375560717144, -56.18195772171021],
                    [-34.896807987382374, -56.18233859539033],
                    [-34.89631080751797, -56.18268728256226]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Verduras', 'Frutas', 'Plantas', 'Flores', 'Especias'],
                    'Ferreteria': ['Herramientas básicas']
                }
            },
            {
                'nombre': '9 de Abril',
                'coordenadas': [
                    [-34.89718637004131, -56.183170080184944],
                    [-34.896807987382374, -56.18232250213624]
                ],
                'categoria_principal': 'Libros',
                'productos': {
                    'Libros': ['Libros usados', 'Comics', 'Revistas', 'Libros técnicos'],
                    'Antigüedades': ['Vinilos', 'Revistas antiguas']
                }
            },
            {
                'nombre': 'Damasceno',
                'coordenadas': [
                    [-34.89873068119095, -56.18597567081452],
                    [-34.89906065844092, -56.18578791618348]
                ],
                'categoria_principal': 'Camaras',
                'productos': {
                    'Camaras': ['Cámaras', 'Celulares', 'Cables', 'Electrónica usada'],
                    'Ferreteria': ['Herramientas electrónicas']
                }
            },
            {
                'nombre': 'Galicia',
                'coordenadas': [
                    [-34.898743880306405, -56.18334710597993],
                    [-34.89842270122825, -56.18244051933289],
                    [-34.898066322973, -56.18151783943177],
                    [-34.89778913881656, -56.18082582950593],
                    [-34.89756475095721, -56.18021965026856]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Objetos vintage', 'Joyas antiguas', 'Cuadros', 'Artículos de colección'],
                    'Libros': ['Libros antiguos']
                }
            },
            {
                'nombre': 'Cerro Largo',
                'coordenadas': [
                    [-34.89945662939097, -56.18292331695557],
                    [-34.89910465530741, -56.18203282356263],
                    [-34.89870428295369, -56.18105649948121],
                    [-34.89846229871672, -56.180402040481574],
                    [-34.89823351296432, -56.17981195449829],
                    [-34.89785073537661, -56.178862452507026]
                ],
                'categoria_principal': 'Herreria',
                'productos': {
                    'Herreria': ['Repuestos metálicos', 'Cadenas', 'Rejas', 'Herrajes'],
                    'Ferreteria': ['Tornillos', 'Clavos', 'Herramientas'],
                    'Camaras': ['Electrónica', 'Cables']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Vecinal Juan Paullier',
        'barrio': 'Tres Cruces',
        'lat': -34.9015,
        'lng': -56.1680,
        'cuadras': [
            {
                'nombre': 'Juan Paullier - Tramo completo',
                'coordenadas': [
                    [-34.90207878883594, -56.16795659065247],
                    [-34.9011724814482, -56.16802096366883],
                    [-34.90049494414942, -56.16809606552125],
                    [-34.900219968001814, -56.168133616447456]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos orgánicos'],
                    'Ropa': ['Ropa usada', 'Accesorios']
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
    # Filtrar solo la feria de Tristán Narvaja
    feria_tristan = [feria for feria in ferias if feria['nombre'] == 'Feria de Tristán Narvaja'][0]
    
    # Límites del área de la feria (polígono delimitador)
    limites_feria = [
        [-34.90539596455646, -56.18953227996827],
        [-34.90346022842819, -56.168932914733894],
        [-34.89173925162138, -56.17343902587891],
        [-34.89367526399983, -56.19000434875489],
        [-34.90520239299701, -56.1895376443863]
    ]
    
    return render_template('tristan_narvaja.html', 
                         feria=feria_tristan, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/juan-paullier')
def juan_paullier():
    # Filtrar solo la feria de Juan Paullier
    feria_juan = [feria for feria in ferias if feria['nombre'] == 'Feria Vecinal Juan Paullier'][0]
    
    # Límites del área de la feria
    limites_feria = [
        [-34.90250, -56.16750],
        [-34.90250, -56.16850],
        [-34.90000, -56.16850],
        [-34.90000, -56.16750]
    ]
    
    return render_template('juan_paullier.html', 
                         feria=feria_juan, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/tres-cruces')
def tres_cruces():
    # Por ahora redirige al lobby, más adelante tendrá su propia página
    return render_template('lobby.html')

@app.route('/calle-salto')
def calle_salto():
    # Por ahora redirige al lobby, más adelante tendrá su propia página
    return render_template('lobby.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)