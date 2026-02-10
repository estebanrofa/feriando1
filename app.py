from flask import Flask, render_template, request

app = Flask(__name__)

categorias_colores = {
    'Libros': '#CC0000',
    'Ropa': '#6B00CC',
    'Antigüedades': '#CCAA00',
    'Ferreteria': '#8B5A00',
    'Herreria': '#4D4D4D',
    'Camaras': '#000000',
    'Comida': '#CC7700'
}

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
        'nombre': 'Feria Calle Salto',
        'barrio': 'Cordón',
        'dia': 'Sábados',
        'lat': -34.909,
        'lng': -56.182,
        'cuadras': [
            {
                'nombre': 'Calle Salto - Recorrido completo',
                'coordenadas': [
                    [-34.91169061803468, -56.181665955354696],
                    [-34.90716234917917, -56.18216673960329]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ropa': ['Ropa usada', 'Accesorios']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Tres Cruces',
        'barrio': 'La Comercial',
        'dia': 'Sábados',
        'lat': -34.889,
        'lng': -56.168,
        'cuadras': [
            {
                'nombre': 'Tres Cruces - Recorrido completo',
                'coordenadas': [
                    [-34.88986640083746, -56.16682645270599],
                    [-34.8891860519139, -56.169361353226115]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos orgánicos'],
                    'Ropa': ['Ropa nueva', 'Zapatos']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Democracia',
        'barrio': 'Villa Muñoz/Retiro',
        'dia': 'Domingos',
        'lat': -34.890,
        'lng': -56.177,
        'cuadras': [
            {
                'nombre': 'Democracia - Recorrido completo',
                'coordenadas': [
                    [-34.89068718380285, -56.17667370807447],
                    [-34.88980637272634, -56.17679857241883]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos de granja'],
                    'Ropa': ['Ropa usada']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Acevedo Díaz',
        'barrio': 'Parque Rodó',
        'dia': 'Martes',
        'lat': -34.906,
        'lng': -56.166,
        'cuadras': [
            {
                'nombre': 'Acevedo Díaz - Recorrido completo',
                'coordenadas': [
                    [-34.90685750900923, -56.166047944787074],
                    [-34.905833784203644, -56.1661575292588]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ropa': ['Ropa', 'Accesorios']
                }
            }
        ]
    },
    {
        'nombre': 'Feria San Salvador',
        'barrio': 'Parque Rodó',
        'dia': 'Miércoles',
        'lat': -34.911,
        'lng': -56.170,
        'cuadras': [
            {
                'nombre': 'San Salvador - Recorrido completo',
                'coordenadas': [
                    [-34.91090280595359, -56.170360333445714],
                    [-34.91081042578227, -56.16868663516422]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos locales'],
                    'Ropa': ['Ropa usada', 'Zapatos']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Isla de Flores',
        'barrio': 'Palermo',
        'dia': 'Jueves',
        'lat': -34.910,
        'lng': -56.177,
        'cuadras': [
            {
                'nombre': 'Isla de Flores - Recorrido completo',
                'coordenadas': [
                    [-34.91048071389207, -56.17705693125584],
                    [-34.91043672499547, -56.17648475403061]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ropa': ['Ropa', 'Calzado']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Martínez Trueba',
        'barrio': 'Palermo',
        'dia': 'Martes',
        'lat': -34.908,
        'lng': -56.183,
        'cuadras': [
            {
                'nombre': 'Martínez Trueba - Recorrido completo',
                'coordenadas': [
                    [-34.90807534389788, -56.18306312419999],
                    [-34.90724257521355, -56.18315193027305]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos de estación'],
                    'Ropa': ['Ropa usada']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Vecinal Juan Paullier',
        'barrio': 'Tres Cruces',
        'dia': 'Martes',
        'lat': -34.9015,
        'lng': -56.1680,
        'cuadras': [
            {
                'nombre': 'Juan Paullier - Mercado y Alimentos',
                'coordenadas': [
                    [-34.90209198741333, -56.1679619550705],
                    [-34.90116368229832, -56.16805851459504]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Pescados', 'Quesos', 'Productos de mercado']
                }
            },
            {
                'nombre': 'Juan Paullier - Ropa y Antigüedades',
                'coordenadas': [
                    [-34.90116368229832, -56.16805851459504],
                    [-34.9001297756249, -56.16814702749253]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Antigüedades': ['Antigüedades']
                }
            },
            {
                'nombre': 'Juan Paullier - Antigüedades',
                'coordenadas': [
                    [-34.9001297756249, -56.16814702749253],
                    [-34.90017157210456, -56.16823822259904]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Julio Herrera y Obes',
        'barrio': 'Centro',
        'dia': 'Viernes',
        'lat': -34.9104,
        'lng': -56.1943,
        'cuadras': [
            {
                'nombre': 'Julio Herrera y Obes - Recorrido completo',
                'coordenadas': [
                    [-34.91078908381817, -56.19426766065802],
                    [-34.909952910158744, -56.19433021672227]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ropa': ['Ropa usada', 'Accesorios']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Acevedo Díaz (Sábados)',
        'barrio': 'Cordón',
        'dia': 'Sábados',
        'lat': -34.8995,
        'lng': -56.1668,
        'cuadras': [
            {
                'nombre': 'Acevedo Díaz - Recorrido completo',
                'coordenadas': [
                    [-34.89995795847101, -56.16678730930974],
                    [-34.8991050295766, -56.16687705192749]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ropa': ['Ropa', 'Calzado']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Guaná',
        'barrio': 'Cordón',
        'dia': 'Viernes',
        'lat': -34.9053,
        'lng': -56.1728,
        'cuadras': [
            {
                'nombre': 'Guaná - Recorrido completo',
                'coordenadas': [
                    [-34.90527733926171, -56.172280018620846],
                    [-34.90533002215996, -56.17335319922175]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos locales'],
                    'Ropa': ['Ropa usada']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Gaboto (Viernes)',
        'barrio': 'Cordón',
        'dia': 'Viernes',
        'lat': -34.9052,
        'lng': -56.1773,
        'cuadras': [
            {
                'nombre': 'Gaboto - Recorrido completo',
                'coordenadas': [
                    [-34.90475811179553, -56.17744792377785],
                    [-34.905612996184374, -56.17720060797018]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ferreteria': ['Herramientas básicas']
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
    feria_tristan = [feria for feria in ferias if feria['nombre'] == 'Feria de Tristán Narvaja'][0]
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
    feria_juan = [feria for feria in ferias if feria['nombre'] == 'Feria Vecinal Juan Paullier'][0]
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
    feria = [f for f in ferias if f['nombre'] == 'Feria Tres Cruces'][0]
    limites_feria = [
        [-34.89050, -56.16650],
        [-34.89050, -56.16970],
        [-34.88880, -56.16970],
        [-34.88880, -56.16650]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/calle-salto')
def calle_salto():
    feria = [f for f in ferias if f['nombre'] == 'Feria Calle Salto'][0]
    limites_feria = [
        [-34.91200, -56.18150],
        [-34.91200, -56.18250],
        [-34.90700, -56.18250],
        [-34.90700, -56.18150]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/democracia')
def democracia():
    feria = [f for f in ferias if f['nombre'] == 'Feria Democracia'][0]
    limites_feria = [
        [-34.89100, -56.17650],
        [-34.89100, -56.17700],
        [-34.88950, -56.17700],
        [-34.88950, -56.17650]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/acevedo-diaz')
def acevedo_diaz():
    feria = [f for f in ferias if f['nombre'] == 'Feria Acevedo Díaz'][0]
    limites_feria = [
        [-34.90720, -56.16590],
        [-34.90720, -56.16630],
        [-34.90550, -56.16630],
        [-34.90550, -56.16590]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/san-salvador')
def san_salvador():
    feria = [f for f in ferias if f['nombre'] == 'Feria San Salvador'][0]
    limites_feria = [
        [-34.91120, -56.16850],
        [-34.91120, -56.17050],
        [-34.91050, -56.17050],
        [-34.91050, -56.16850]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/isla-flores')
def isla_flores():
    feria = [f for f in ferias if f['nombre'] == 'Feria Isla de Flores'][0]
    limites_feria = [
        [-34.91080, -56.17630],
        [-34.91080, -56.17720],
        [-34.91010, -56.17720],
        [-34.91010, -56.17630]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/martinez-trueba')
def martinez_trueba():
    feria = [f for f in ferias if f['nombre'] == 'Feria Martínez Trueba'][0]
    limites_feria = [
        [-34.90840, -56.18290],
        [-34.90840, -56.18330],
        [-34.90700, -56.18330],
        [-34.90700, -56.18290]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/julio-herrera')
def julio_herrera():
    feria = [f for f in ferias if f['nombre'] == 'Feria Julio Herrera y Obes'][0]
    limites_feria = [
        [-34.91100, -56.19400],
        [-34.91100, -56.19460],
        [-34.90970, -56.19460],
        [-34.90970, -56.19400]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/acevedo-diaz-sabados')
def acevedo_diaz_sabados():
    feria = [f for f in ferias if f['nombre'] == 'Feria Acevedo Díaz (Sábados)'][0]
    limites_feria = [
        [-34.90020, -56.16650],
        [-34.90020, -56.16710],
        [-34.89890, -56.16710],
        [-34.89890, -56.16650]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/guana')
def guana():
    feria = [f for f in ferias if f['nombre'] == 'Feria Guaná'][0]
    limites_feria = [
        [-34.90560, -56.17200],
        [-34.90560, -56.17360],
        [-34.90500, -56.17360],
        [-34.90500, -56.17200]
    ]
    return render_template('feria_generica.html', 
                         feria=feria, 
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/gaboto-viernes')
def gaboto_viernes():
    feria = [f for f in ferias if f['nombre'] == 'Feria Gaboto (Viernes)'][0]
    limites_feria = [
        [-34.90580, -56.17700],
        [-34.90580, -56.17770],
        [-34.90450, -56.17770],
        [-34.90450, -56.17700]
    ]
    return render_template('feria_generica.html',
                         feria=feria,
                         categorias_colores=categorias_colores,
                         limites_feria=limites_feria)

@app.route('/registro')
def registro():
    tipo = request.args.get('tipo', 'visitante')
    declarado = request.args.get('declarado', '')
    return render_template('registro.html', tipo=tipo, declarado=declarado)

@app.route('/login')
def login():
    return render_template('registro.html', tipo='login', dgi='')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)