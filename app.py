import os
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for, jsonify

# Cargar variables de entorno (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Sentry para error tracking (opcional)
try:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_dsn = os.environ.get('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.1,  # 10% de requests para performance
            profiles_sample_rate=0.1,
        )
except ImportError:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# ============================================
# USUARIOS DE PRUEBA (SOLO PARA DESARROLLO LOCAL)
# ============================================
USUARIOS_PRUEBA = {
    'usuario1234': {
        'password': 'HA436276',
        'nombre': 'Usuario de Prueba',
        'tipo': 'visitante'
    },
    'usuarioferiante': {
        'password': 'HA436276',
        'nombre': 'Feriante de Prueba',
        'tipo': 'vendedor'
    }
}

# Compresion gzip (opcional)
try:
    from flask_compress import Compress
    Compress(app)
except ImportError:
    pass

# Configuracion para produccion
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache 1 año para assets

categorias_colores = {
    'Libros': '#CC0000',
    'Ropa': '#6B00CC',
    'Antigüedades': '#CCAA00',
    'Ferreteria': '#8B5A00',
    'Herreria': '#4D4D4D',
    'Camaras': '#000000',
    'Comida': '#CC7700',
    'Plantas': '#228B22',
    'Quesos y pescado': '#1E90FF',
    'Pollo y carnes': '#DC143C',
    'Frutas y verduras': '#32CD32',
    'Quesos': '#F0E68C',
    'Herramientas': '#5D4E37',
    'Artesanías': '#E07020'
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
                'nombre': 'Tristán Narvaja - Plantas y Mascotas',
                'coordenadas': [
                    [-34.902025994505166, -56.176394820213325],
                    [-34.90233836046859, -56.17724776268006]
                ],
                'categoria_principal': 'Plantas',
                'productos': {
                    'Plantas': ['Plantas'],
                    'Mascotas': ['Artículos para mascotas']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Ropa, Joyería, Limpieza y Verduras',
                'coordenadas': [
                    [-34.90233836046859, -56.17724776268006],
                    [-34.901524446670116, -56.17783784866334]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa nueva'],
                    'Antigüedades': ['Joyería'],
                    'Limpieza': ['Artículos de limpieza'],
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Ropa, Verduras, Quesos y Pescados',
                'coordenadas': [
                    [-34.901524446670116, -56.17783784866334],
                    [-34.900745721593374, -56.1782991886139]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Frutas y verduras': ['Verduras', 'Frutas'],
                    'Quesos y pescado': ['Quesos', 'Pescados']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Ropa, Verduras, Huevos y Tecnología',
                'coordenadas': [
                    [-34.900745721593374, -56.1782991886139],
                    [-34.89996258949352, -56.17877662181855]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Frutas y verduras': ['Verduras', 'Frutas'],
                    'Huevos': ['Huevos'],
                    'Camaras': ['Tecnología']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Artesanías y Libros',
                'coordenadas': [
                    [-34.89965461415012, -56.17807924747468],
                    [-34.89996698913292, -56.17877125740051]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Artesanías de madera', 'Artesanías de metal'],
                    'Libros': ['Libros']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Puestos de Comida',
                'coordenadas': [
                    [-34.89996698913292, -56.17877125740051],
                    [-34.90025736481198, -56.17951154708863]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Puestos de comida']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Ropa, Frutos secos y Plantas',
                'coordenadas': [
                    [-34.89996699, -56.17877126],
                    [-34.89927184, -56.17922187]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Frutas y verduras': ['Frutos secos'],
                    'Plantas': ['Plantas']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Libros',
                'coordenadas': [
                    [-34.89927184, -56.17922187],
                    [-34.89885827, -56.17850840]
                ],
                'categoria_principal': 'Libros',
                'productos': {
                    'Libros': ['Libros']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Antigüedades, Bronce, Ropa Vintage y Plantas',
                'coordenadas': [
                    [-34.89927184, -56.17922187],
                    [-34.89986140, -56.18034303]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades', 'Artículos de bronce', 'Ropa vintage'],
                    'Plantas': ['Plantas']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Ropa Vintage y Antigüedades',
                'coordenadas': [
                    [-34.89986140, -56.18034303],
                    [-34.90023977, -56.18013918]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa vintage'],
                    'Antigüedades': ['Antigüedades']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Antigüedades y Artículos de mercado',
                'coordenadas': [
                    [-34.89988780, -56.18033767],
                    [-34.90028816, -56.18135154]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades', 'Artículos de mercado']
                }
            },
            {
                'nombre': 'Tristán Narvaja - Recorrido principal (continuación)',
                'coordenadas': [
                    [-34.89927184, -56.17922187],
                    [-34.898215914033884, -56.17982268333436],
                    [-34.89755155165228, -56.1802089214325]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras'],
                    'Ropa': ['Ropa'],
                    'Libros': ['Libros usados']
                }
            },
            {
                'nombre': 'Magallanes - Tramo 1',
                'coordenadas': [
                    [-34.89911785436277, -56.18204355239869],
                    [-34.89842270122825, -56.18244588375092],
                    [-34.89769894, -56.18288845]
                ],
                'categoria_principal': 'Ferreteria',
                'productos': {
                    'Ferreteria': ['Herramientas', 'Tornillos', 'Candados', 'Pinturas', 'Cerraduras'],
                    'Herreria': ['Repuestos metálicos', 'Cadenas', 'Rejas']
                }
            },
            {
                'nombre': 'Magallanes - Ropa y Herramientas',
                'coordenadas': [
                    [-34.89769894, -56.18288845],
                    [-34.89719517, -56.18318349]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Herramientas': ['Herramientas']
                }
            },
            {
                'nombre': 'Magallanes - Ropa, Antigüedades y Herramientas',
                'coordenadas': [
                    [-34.89719517, -56.18318349],
                    [-34.89670679, -56.18348122]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Antigüedades': ['Antigüedades'],
                    'Herramientas': ['Herramientas']
                }
            },
            {
                'nombre': '9 de Abril - Ropa y Antigüedades',
                'coordenadas': [
                    [-34.89719517, -56.18318349],
                    [-34.89681679, -56.18235737]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Antigüedades': ['Antigüedades']
                }
            },
            {
                'nombre': '9 de Abril - Ropa, Antigüedades y Tecnología',
                'coordenadas': [
                    [-34.89681679, -56.18235737],
                    [-34.89636581, -56.18263900]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Antigüedades': ['Antigüedades'],
                    'Camaras': ['Tecnología']
                }
            },
            {
                'nombre': 'Gaboto - Ropa y Antigüedades',
                'coordenadas': [
                    [-34.89681679, -56.18235737],
                    [-34.89737336, -56.18195772]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Antigüedades': ['Antigüedades']
                }
            },
            {
                'nombre': 'Galicia - Antigüedades y Artesanías',
                'coordenadas': [
                    [-34.89769894, -56.18288845],
                    [-34.89737336, -56.18195772]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades'],
                    'Artesanías': ['Artesanías']
                }
            },
            {
                'nombre': 'Galicia - Artículos de mercado y Herramientas',
                'coordenadas': [
                    [-34.89737336, -56.18195772],
                    [-34.89682999, -56.18056029]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Artículos de mercado'],
                    'Herramientas': ['Herramientas']
                }
            },
            {
                'nombre': 'Galicia - Ropa y Artesanías',
                'coordenadas': [
                    [-34.89686518, -56.18063271],
                    [-34.89754935, -56.18022770]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Artesanías': ['Artesanías']
                }
            },
            {
                'nombre': 'Galicia - Antigüedades y Herrería',
                'coordenadas': [
                    [-34.89754935, -56.18022770],
                    [-34.89822911, -56.17981732]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades'],
                    'Herreria': ['Herrería']
                }
            },
            {
                'nombre': 'Minas - Tramo 1',
                'coordenadas': [
                    [-34.90063133197708, -56.18228495121003],
                    [-34.89944783005727, -56.182907223701484]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa deportiva', 'Zapatos', 'Mochilas', 'Gorras'],
                    'Frutas y verduras': ['Snacks', 'Bebidas']
                }
            },
            {
                'nombre': 'Minas - Ropa, Antigüedades y Juguetes',
                'coordenadas': [
                    [-34.89873948, -56.18334711],
                    [-34.89797833, -56.18378699]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa', 'Ropa de Construcción', 'Jeans Levis'],
                    'Antigüedades': ['Antigüedades', 'Juguetes Vintage'],
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Minas - Ropa y Artículos de mercado',
                'coordenadas': [
                    [-34.89797833, -56.18378699],
                    [-34.89834351, -56.18482232]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa', 'Ropa de Segunda Mano'],
                    'Antigüedades': ['Artículos de mercado']
                }
            },
            {
                'nombre': 'Minas - Ropa',
                'coordenadas': [
                    [-34.89797393, -56.18377894],
                    [-34.89714457, -56.18428856]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa']
                }
            },
            {
                'nombre': 'Galicia - Frutas y Verduras',
                'coordenadas': [
                    [-34.89796733, -56.18378699],
                    [-34.89769894, -56.18288845]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'La Paz - Antigüedades y Herramientas',
                'coordenadas': [
                    [-34.89834351, -56.18482232],
                    [-34.89873948, -56.18597567]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades'],
                    'Herramientas': ['Herramientas']
                }
            },
            {
                'nombre': 'La Paz - Antigüedades y Carteras',
                'coordenadas': [
                    [-34.89873948, -56.18597567],
                    [-34.89859209, -56.18605614]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades'],
                    'Ropa': ['Carteras de mujer']
                }
            },
            {
                'nombre': 'La Paz - Verduras, Antigüedades y Varios',
                'coordenadas': [
                    [-34.89873948, -56.18597567],
                    [-34.89884507, -56.18630290]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Verduras', 'Frutas'],
                    'Antigüedades': ['Antigüedades'],
                    'Ferreteria': ['Artículos de cocina', 'Artículos de pesca'],
                    'Comida': ['Huevos']
                }
            },
            {
                'nombre': 'Damasceno - Ropa y Herramientas',
                'coordenadas': [
                    [-34.89873948, -56.18597567],
                    [-34.89908046, -56.18577987]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Herramientas': ['Herramientas']
                }
            },
            {
                'nombre': 'Gaboto - Ropa Vintage, Antigüedades y Artesanías',
                'coordenadas': [
                    [-34.89988780, -56.18033767],
                    [-34.89872628, -56.18104041]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Ropa': ['Ropa Vintage'],
                    'Antigüedades': ['Antigüedades', 'Lentes'],
                    'Artesanías': ['Artesanías', 'Cuchillos artesanales'],
                    'Herramientas': ['Herramientas']
                }
            },
            {
                'nombre': 'Gaboto',
                'coordenadas': [
                    [-34.89872628, -56.18104041],
                    [-34.89805752349036, -56.18151247501374],
                    [-34.897375560717144, -56.18195772171021]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Verduras', 'Frutas', 'Plantas', 'Flores', 'Especias'],
                    'Ferreteria': ['Herramientas básicas']
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
                'nombre': 'Cerro Largo - Antigüedades, Camisetas y Herrería',
                'coordenadas': [
                    [-34.89870428, -56.18105114],
                    [-34.89822471, -56.17983341]
                ],
                'categoria_principal': 'Antigüedades',
                'productos': {
                    'Antigüedades': ['Antigüedades'],
                    'Ropa': ['Camisetas de fútbol'],
                    'Herreria': ['Herrería']
                }
            },
            {
                'nombre': 'Cerro Largo - Ropa, Antigüedades y Varios',
                'coordenadas': [
                    [-34.89822471, -56.17983341],
                    [-34.89788153, -56.17890000]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Ropa': ['Ropa'],
                    'Antigüedades': ['Antigüedades', 'CDs'],
                    'Plantas': ['Plantas'],
                    'Comida': ['Arepas']
                }
            },
            {
                'nombre': 'Cerro Largo - Verduras, Frutas y Huevos',
                'coordenadas': [
                    [-34.89870868, -56.18104577],
                    [-34.89911345, -56.18203819]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Verduras', 'Frutas'],
                    'Antigüedades': ['Artículos de mercado'],
                    'Comida': ['Huevos']
                }
            },
            {
                'nombre': 'Cerro Largo - Verduras, Herramientas y Calzado',
                'coordenadas': [
                    [-34.89911345, -56.18205428],
                    [-34.89944343, -56.18291795]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Verduras', 'Frutas'],
                    'Herramientas': ['Herramientas'],
                    'Ropa': ['Calzado Deportivo'],
                    'Comida': ['Pastas']
                }
            },
            {
                'nombre': 'Cerro Largo - Comida y Antigüedades',
                'coordenadas': [
                    [-34.89944343, -56.18291795],
                    [-34.89982180, -56.18393719]
                ],
                'categoria_principal': 'Comida',
                'productos': {
                    'Comida': ['Comida', 'Huevos'],
                    'Antigüedades': ['Antigüedades']
                }
            },
            {
                'nombre': 'Minas - Jardinería, Herrería y Artesanías',
                'coordenadas': [
                    [-34.89943463, -56.18292868],
                    [-34.89873948, -56.18334711]
                ],
                'categoria_principal': 'Plantas',
                'productos': {
                    'Plantas': ['Jardinería', 'Plantas'],
                    'Ferreteria': ['Artículos de Cocina', 'Cerrajería'],
                    'Herreria': ['Herrería'],
                    'Artesanías': ['Inciensos', 'Cuchillos Artesanales', 'Artículos para Mascotas']
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
                'nombre': 'Calle Salto - Cuadra 1',
                'coordenadas': [
                    [-34.91221027251413, -56.18162244558335],
                    [-34.91171758490295, -56.181668043136604]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Calle Salto - Cuadra 2',
                'coordenadas': [
                    [-34.91171758490295, -56.181668043136604],
                    [-34.910809184368276, -56.181767284870155]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Calle Salto - Cuadra 3',
                'coordenadas': [
                    [-34.910809184368276, -56.181767284870155],
                    [-34.90994036573643, -56.181855797767646]
                ],
                'categoria_principal': 'Quesos',
                'productos': {
                    'Quesos': ['Quesos']
                }
            },
            {
                'nombre': 'Calle Salto - Cuadra 4',
                'coordenadas': [
                    [-34.90994036573643, -56.181855797767646],
                    [-34.909007750188735, -56.1819550395012]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Calle Salto - Cuadra 5',
                'coordenadas': [
                    [-34.909007750188735, -56.1819550395012],
                    [-34.90807072484237, -56.18208646774292]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Calle Salto - Cuadra 6',
                'coordenadas': [
                    [-34.90807072484237, -56.18208646774292],
                    [-34.90714468693991, -56.182166934013374]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos orgánicos'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos de granja'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos frescos'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos locales'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos frescos'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos de estación'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Pescados', 'Quesos', 'Productos de mercado']
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ropa': ['Ropa usada', 'Accesorios']
                }
            }
        ]
    },
    {
        'nombre': 'Feria Acevedo Díaz (Sábados)',
        'barrio': 'Cordón',
        'dia': 'Sábados',
        'lat': -34.901,
        'lng': -56.1666,
        'cuadras': [
            {
                'nombre': 'Acevedo Díaz - Plantas',
                'coordenadas': [
                    [-34.902025994505166, -56.166438460350044],
                    [-34.90202159497606, -56.16655111312866]
                ],
                'categoria_principal': 'Plantas',
                'productos': {
                    'Plantas': ['Plantas']
                }
            },
            {
                'nombre': 'Acevedo Díaz - Comida variada',
                'coordenadas': [
                    [-34.90202159497606, -56.16655111312866],
                    [-34.901075690747724, -56.166663765907295]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras'],
                    'Quesos y pescado': ['Pescado', 'Quesos'],
                    'Pollo y carnes': ['Pollo']
                }
            },
            {
                'nombre': 'Acevedo Díaz - Frutas y Verduras',
                'coordenadas': [
                    [-34.901075690747724, -56.166663765907295],
                    [-34.90001538515072, -56.16677641868592]
                ],
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras']
                }
            },
            {
                'nombre': 'Acevedo Díaz - Varios',
                'coordenadas': [
                    [-34.90001538515072, -56.16677641868592],
                    [-34.89913985278364, -56.16688907146454]
                ],
                'categoria_principal': 'Ropa',
                'productos': {
                    'Limpieza': ['Artículos de limpieza', 'Papel higiénico'],
                    'Ropa': ['Ropa'],
                    'Mascotas': ['Artículos para mascotas']
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos locales'],
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
                'categoria_principal': 'Frutas y verduras',
                'productos': {
                    'Frutas y verduras': ['Frutas', 'Verduras', 'Productos frescos'],
                    'Ferreteria': ['Herramientas básicas']
                }
            }
        ]
    }
]

@app.route('/')
def index():
    ga_id = os.environ.get('GA_MEASUREMENT_ID', '')
    return render_template('lobby.html', ga_id=ga_id)

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
        [-34.91250, -56.18140],
        [-34.91250, -56.18240],
        [-34.90680, -56.18240],
        [-34.90680, -56.18140]
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
        [-34.90230, -56.16620],
        [-34.90230, -56.16710],
        [-34.89880, -56.16710],
        [-34.89880, -56.16620]
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

# ============================================
# RUTAS DE AUTENTICACIÓN (PRUEBAS LOCALES)
# ============================================
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if username in USUARIOS_PRUEBA and password == USUARIOS_PRUEBA[username]['password']:
        usuario = USUARIOS_PRUEBA[username]
        session['logged_in'] = True
        session['username'] = username
        session['nombre'] = usuario['nombre']
        session['tipo'] = usuario['tipo']
        return jsonify({
            'success': True,
            'mensaje': 'Login exitoso',
            'nombre': usuario['nombre'],
            'tipo': usuario['tipo']
        })
    else:
        return jsonify({'success': False, 'mensaje': 'Usuario o contraseña incorrectos'}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'mensaje': 'Sesión cerrada'})

@app.route('/api/sesion')
def api_sesion():
    if session.get('logged_in'):
        return jsonify({
            'logged_in': True,
            'username': session.get('username'),
            'nombre': session.get('nombre'),
            'tipo': session.get('tipo', 'visitante')
        })
    return jsonify({'logged_in': False})

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

# SEO: Servir robots.txt y sitemap.xml desde la raiz
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

# PWA: Servir manifest.json desde la raiz (opcional, algunos navegadores lo buscan ahi)
@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)