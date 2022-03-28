import traceback
import sys
import re
import csv



class estructura(object):
    def videoteca(self): 
        # crea los distintos catalogos
        # relacionados con las peliculas
        with open(self.rutaCatalogo, 'r') as vidioteca:
            vidioteca = csv.reader(vidioteca, delimiter=',')
            for pelicula in vidioteca:
                try:
                    idPelicula = int(pelicula[0])
                    titulo = pelicula[1]
                    #titulo = re.sub('.\((19|20)\d{2}\)', '', titulo)
                    generoPelicula = pelicula[2].split('|')

                    # crear indice de peliculas disponibles
                    if not titulo in self.totalPeliculas:
                        self.totalPeliculas.add(titulo)


                    # diferenciar peliculas por genero y subgnero
                    for subgenero in generoPelicula:
                        # crear identificador de subgenero
                        if not self.directSubgenero.get(subgenero):
                            self.directSubgenero[subgenero] = self.indexadorSubgenero
                            self.indexadorSubgenero += 1

                        # crear catalogo por genero
                        if not self.generos.get(subgenero):
                            self.generos[subgenero] = [titulo]
                        else:
                            self.generos[subgenero].insert(
                                len(self.generos[subgenero]), titulo)
                
                    # crear catalogo detallado
                    self.catalogo[idPelicula] = {'title': titulo,
                                                'categorias': [self.directSubgenero.get(subg) 
                                                for subg in generoPelicula]}

                except:
                    traceback.print_exc(file=sys.stdout)
                    print(f'Ocurrio un problema estructurando: {pelicula}')
                    pass


    def subscriptores(self):
        # crea la lista de usuarios 
        # y el historial de reproduccion
        with open(self.rutaUsers, 'r') as usuarios:
            usuarios = csv.reader(usuarios, delimiter=',')
            for tag in usuarios:
                try:
                    userId = int(tag[0])
                    idPelicula = int(tag[1])
                    etiqueta = tag[2]
                    if not userId in self.subs:
                        self.subs.add(userId)
                    if not self.actividadUsuarios.get(userId):
                        self.actividadUsuarios[userId] = {'historial': [
                                idPelicula], 'etiquetas': [etiqueta]}
                    else:
                        if idPelicula in self.actividadUsuarios[userId].get('historial'):
                                pass
                        else:
                            self.actividadUsuarios[userId].get('historial').insert(
                                len(self.actividadUsuarios[userId]), idPelicula)
                            if etiqueta not in self.actividadUsuarios[userId].get('etiquetas'):
                                self.actividadUsuarios[userId].get('etiquetas').insert(
                                    len(self.actividadUsuarios[userId]), etiqueta)
                except:
                    traceback.print_exc(file=sys.stdout)
                    print(f'Ocurrio un problema estructurando: {tag}')
                    pass


    def subcatEvaluar(self, titulo):
        # determina si la pelicula existe dentro de una
        # categoria
        estructuraPelicula = None
        for idPelicula, elementos in self.catalogo.items():
            if titulo == elementos.get('title'):
                estructuraPelicula = elementos.get('categorias')
                break
        if not estructuraPelicula:
            return f'La pelicula {titulo} no esta en el catalogo'
        return estructuraPelicula


    def local_jaccard(self, set1, set2):
        # dados dos conjuntos retorna la
        # similitud de estos
        set1 = set(set1)
        set2 = set(set2)
        inter = len(set1.intersection(set2))
        union = len(set1.union(set2))
        jc = inter / union
        return jc
