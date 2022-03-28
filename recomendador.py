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


    def recomendacion_simple(self, titulo: str) -> dict:
        # data una pelicula, regresa la sugerencia 
        # de otras tres peliculas del mismo genero 
        if titulo in self.totalPeliculas:
            for genero, peliculas in self.generos.items():
                if titulo in peliculas:
                    recomendaciones = random.choices(peliculas, k=3)
            return recomendaciones
        raise Exception(
            f'El titulo {titulo} no esta disponible en el catalogo')


    def recomendacion_jaccard(self, titulo):
        # data una pelicula, regresa las tres peliculas
        # mas similares a esta de acuerdo a los subgeneros
        # de la pelicula dada
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

        # convertir id de pelicula a titulo
        for num, idPelicula in enumerate(resultado):
            resultado[num] = self.catalogo[idPelicula].get('title')
        try:
            # ajuste cuando la pelicula se suguiere a si misma
            resultado.index(titulo)
            print('entro')
            resultado[resultado.index(
                titulo)] = random.choice(self.recomendacion_simple(titulo))
        except:
            pass
        return resultado


    def recomendaciones(self, entrada):
        # imprime la lista de recomendaciones dada
        # una pelicula o lista de estas
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
