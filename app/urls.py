from django.urls import path 
from . import views 

app_name = 'app' 
urlpatterns = [
    path('', views.index, name='index'), 
    path('inicio/', views.inicio, name='inicio'),
    path('inicioPost',views.inicioPost, name='inicioPost'),
    path('salir',views.salir, name='salir'),
    path('inicioError/', views.inicioError, name='inicioError'),
    path('menuDecano/', views.menuDecano, name='menuDecano'),
    path('agregarEstudiante/', views.agregarEstudiante, name='agregarEstudiante'),
    path('registroPost/',views.registroPost,name='registroPost'),
    path('agregarEstudianteError/', views.agregarEstudianteError, name='agregarEstudianteError'),
    path('crearVotacion/', views.crearVotacion, name='crearVotacion'),
    path('votacionPost/', views.votacionPost, name='votacionPost'),
    path('listaDeEstudiantes/', views.listaDeEstudiantes, name='listaDeEstudiantes'),
    path('listaDeVotaciones/', views.listaDeVotaciones, name='listaDeVotaciones'),
    path('editarVotaciones/<int:id_votacion>', views.editarVotaciones, name='editarVotaciones'),
    path('editarVotacionesPost/<int:id_votacion>/', views.editarVotacionesPost, name='editarVotacionesPost'),
    path('vistaVotacionFacultad/', views.vistaVotacionFacultad, name='vistaVotacionFacultad'),
    path('vistaVotacionFacultadPost/<int:id_votacion>/', views.vistaVotacionFacultadPost, name='vistaVotacionFacultadPost'),
    path('vistaVotacionSemestre/', views.vistaVotacionSemestre, name='vistaVotacionSemestre'),
    path('vistaVotacionSemestrePost/<int:id_votacion>/', views.vistaVotacionSemestrePost, name='vistaVotacionSemestrePost'),
    path('postulacionEstudiante2/', views.postulacionEstudiante2, name='postulacionEstudiante2'),
    # estudiante
    path('detallesHistorico/<int:id_voto>/',views.detallesHistorico, name='detallesHistorico'),
    path('detallesResultado/<int:id_votacion>/',views.detallesResultado, name='detallesResultado'),
    path('detallesResultadosFacultad/',views.detallesResultadosFacultad, name='detallesResultadosFacultad'),
    path('historicoVotaciones/',views.historicoVotaciones, name='historicoVotaciones'),
    path('listaResultados/',views.listaResultados, name='listaResultados'),
    path('listaVotacionesEstudiantes/',views.listaVotacionesEstudiantes, name='listaVotacionesEstudiantes'),
    path('postularme/',views.postularme, name='postularme'),
    path('menuEstudiante/',views.menuEstudiante, name='menuEstudiante'),
    path('postulacionExitosa/',views.postulacionExitosa, name='postulacionExitosa'),
    path('postulacion/<int:id_votacion>/',views.postulacion, name='postulacion'),
    path('postulacionPost/<int:id_votacion>/',views.postulacionPost, name='postulacionPost'),
    path('votacionExitosa/',views.votacionExitosa, name='votacionExitosa'),
    path('votacionExitosaPost/<int:id_candidato>/<int:id_votacion>/',views.votacionExitosaPost, name='votacionExitosaPost'),
    path('votarCandidato/',views.votarCandidato, name='votarCandidato'),
    path('votarCandidatoPost/<int:id_votacion>/',views.votarCandidatoPost, name='votarCandidatoPost'),
    path('YaEstaPostulado/',views.YaEstaPostulado, name='YaEstaPostulado'),

]