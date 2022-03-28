from estructura import estructura
import random

class recomendador(estructura):
    def __init__(self, rutaCatalogo, rutaUsers):
        self.rutaCatalogo = rutaCatalogo
        self.rutaUsers = rutaUsers
        self.catalogo = {}
        self.indexadorSubgenero = 1
        self.directSubgenero = {}
        self.generos = {}
        self.subs = set()
        self.actividadUsuarios = {}
        self.etiquetaUsuario = {}
        self.totalPeliculas = set()
        
        # instacia de catalogo y videoteca
        self.videoteca()
        self.subscriptores()

        self.pivoteReco = [{i[0]: i[1].get('categorias')}
                        for i in self.catalogo.items()]



    # recomendacion simple: de todo los generenos que
    # el usuario ha visto se toma la subcategoria de mayor
    # frecuencia y se toma una pelicula al azar del genero
    # se revisa si ya la vio, en ese caso se toma
    # otra hasta que se sugiere una que no ha vist

    def recomendacion_simple(self, titulo: str) -> dict:
        if titulo in self.totalPeliculas:
            for genero, peliculas in self.generos.items():
                if titulo in peliculas:
                    recomendaciones = random.choices(peliculas, k=3)
            return recomendaciones
        raise Exception(
            f'El titulo {titulo} no esta disponible en el catalogo')


    def recomendacion_jaccard(self, titulo):
        recomendaciones = {}
        estructuraPelicula = self.subcatEvaluar(titulo)
        for pelicula in self.pivoteReco:
            comparacion = list(pelicula.values())[0]
            coeficiente = self.local_jaccard(estructuraPelicula, comparacion)
            idRecomendacion = list(pelicula.keys())[0]

            if not recomendaciones or len(recomendaciones) < 3:
                recomendaciones[coeficiente] = idRecomendacion

            elif coeficiente > max(recomendaciones):
                del recomendaciones[max(recomendaciones)]
                recomendaciones[coeficiente] = idRecomendacion

            elif coeficiente < max(recomendaciones) and coeficiente > min(recomendaciones):
                del recomendaciones[min(recomendaciones)]
                recomendaciones[coeficiente] = idRecomendacion

        resultado = list(recomendaciones.values())

        for num, idPelicula in enumerate(resultado):
            resultado[num] = self.catalogo[idPelicula].get('title')
        try:
            resultado.index(titulo)
            print('entro')
            resultado[resultado.index(
                titulo)] = random.choice(self.recomendacion_simple(titulo))
        except:
            pass
        return resultado

    def recomendaciones(self, entrada):
        if isinstance(entrada,list):
            for pelicula in entrada:
                listaJaccard = self.recomendacion_jaccard(pelicula)
                listaSimple = self.recomendacion_simple(pelicula)
                print(f'Porque viste "{pelicula}" te sugerimos:\n')
                for sugerencia in listaJaccard:
                    print(f'{sugerencia}')

                print(f'\n Tambien podria gustarte:\n')
                for sugerencia in listaSimple:
                    print(f'{sugerencia}')
                print('-------------')

        if isinstance(entrada,str):
            listaJaccard = self.recomendacion_jaccard(entrada)
            listaSimple = self.recomendacion_simple(entrada)
            print(f'Porque viste "{entrada}" te sugerimos:\n')
            for sugerencia in listaJaccard:
                print(f'{sugerencia}')

            print(f'\n Tambien podria gustarte:\n')
            for sugerencia in listaSimple:
                print(f'{sugerencia}')
