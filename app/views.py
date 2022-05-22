from ast import Break
from datetime import date, datetime,time
# from msilib.schema import RadioButton
from multiprocessing import context
from tkinter import E
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from app.models import Decano, Facultad, Estudiante, EstadoVotacion, TipoVotacion, Votacion,Candidato, Voto
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    return HttpResponse("Hola")

def inicio(request):
    return render (request, 'app/inicio.html')

def inicioPost(request):
    # recuperar datos
    u= request.POST['username']
    p= request.POST['password']
    #autentificacion de datos
    usuario= authenticate(username=u, password=p)
    
    if usuario is None:
        return render (request, 'app/inicioError.html')
    else:
        # inicia sesion
        login(request, usuario)
        t=request.user.is_superuser
        print(t)
        if t == True:
            return redirect('app:menuDecano')
        else:
            return redirect('app:menuEstudiante')

def inicioError(request):
    return render (request, 'app/inicioError.html')

def salir(request):
    # cierra la sesion
    logout(request)
    return redirect('app:inicio')

@login_required
def menuDecano(request):
    return render (request, 'app/menuDecano.html')

@login_required
def agregarEstudiante(request):
    try:
    # retorna la facultad del decano
        id_usuario=request.user.id
        facultad=Decano.objects.get(user_id=id_usuario)
        contexto={
            'Facultad':facultad
        }
        return render (request,'app/agregarEstudiante.html',contexto)
    except:
        veri=True
        return render (request, 'app/agregarEstudiante.html')
        
def registroPost(request):
    #VALIDACION DE LOS DATOS
    try:
    # saca datos
        nombre=request.POST['nombres']
        apellidos=request.POST['apellidos']
        semestre=request.POST['semestre']
        email=request.POST['email']
        documento=request.POST['documento']
        
        # se obtiene el id de la facultad del estudiante
        id_usuario=request.user.id
        facultad=Decano.objects.get(user_id=id_usuario)
        #crea usuario
        usuario=User()
        usuario.first_name=nombre
        usuario.last_name=apellidos
        usuario.username=email
        usuario.email=email
        usuario.set_password(documento)
        usuario.save()

        estudiante=Estudiante()

        estudiante.semestreActual=semestre
        estudiante.user_id=usuario.id
        estudiante.facultad_id=facultad.id
        estudiante.documento=documento
        estudiante.save()

        return redirect('app:listaDeEstudiantes')
    except:
        veri=True
        return redirect('app:listaDeEstudiantes')

@login_required
def agregarEstudianteError(request):
    return render (request, 'app/agregarEstudianteError.html')

@login_required
def crearVotacion(request):
    try:
        # retorna la facultad del decano
        id_usuario=request.user.id
        Facultad=Decano.objects.get(user_id=id_usuario)
        Tipo=TipoVotacion.objects.all()
        # siempre debe estar en estado postulacion
        Estado=EstadoVotacion.objects.get(id=1)
        # estado de la votacion
        contexto={
            'Facultad':Facultad,
            'tipo':Tipo,
            'estado':Estado  
        }
        return render (request,'app/crearVotacion.html',contexto)
    except:
        veri=True
        return render (request, 'app/crearVotacion.html')

def votacionPost(request):
    
    # try:
    # saca datos
        Nombre=request.POST['nombre']
        FechaInicio=request.POST['fechaInicio']
        FechaFin=request.POST['fechaFin']
        Tipo=request.POST['tipo']
        # el estado es postulacion
       
        #id de la facultad del decano (facultad.id)
        id_usuario=request.user.id
        facultad=Decano.objects.get(user_id=id_usuario)

        # crea votacion
        votacion=Votacion()
        # siempre queda en estado Postulacion
        estado=EstadoVotacion.objects.get(id=1)
        votacion.nombre=Nombre
        votacion.estado_id=estado.id
        votacion.facultad_id=facultad.id
        votacion.fechaInicio=FechaInicio
        votacion.fechaFinal=FechaFin
        votacion.tipo_id= Tipo
        votacion.save()

        return redirect('app:listaDeVotaciones')
    # except:
    #     veri=True
    #     return redirect('app:listaDeVotaciones')

@login_required
def listaDeEstudiantes(request):  
    try:
        # id del la facultad del decano
        id_usuario=request.user.id
        facultad_decano=Decano.objects.get(user_id=id_usuario)
        
        lista=Estudiante.objects.filter(facultad_id=facultad_decano.id)
        
        contexto={
            'Estudiantes':lista
        }
        return render (request, 'app/listaDeEstudiantes.html',contexto)
    except:
        veri= True
        return render(request, 'app/listaDeEstudiantes.html')


@login_required
def listaDeVotaciones(request):
    try:
        # id del la facultad del decano
        id_usuario=request.user.id
        facultad_decano=Decano.objects.get(user_id=id_usuario)
        
        v=Votacion.objects.filter(facultad_id=facultad_decano.id)
        contexto={
            'votaciones':v,
        }
        return render (request, 'app/listaDeVotaciones.html',contexto)
    except:
        veri= True
        return render(request, 'app/listaDeVotaciones.html')
    
@login_required
def editarVotaciones(request, id_votacion):
    votacion=Votacion.objects.get(id=id_votacion)
    facultad=Facultad.objects.get(id=votacion.facultad_id)

    if votacion.estado_id == 1:
        estado=EstadoVotacion.objects.filter(Q(id=1) | Q(id=2))
    elif votacion.estado_id == 2:
        estado=EstadoVotacion.objects.filter(Q(id=2) | Q(id=3))
    else:
        estado=EstadoVotacion.objects.filter(Q(id=3) | Q(id=4))

    contexto={
        'id':votacion.id,
        'estado':estado,
        'f':facultad,
        'v':votacion
    }
    return render (request, 'app/editarVotaciones.html',contexto)

@login_required
def editarVotacionesPost(request, id_votacion):
    votacion=Votacion.objects.get(id=id_votacion)
    Estado=request.POST['estado']
    votacion.estado_id=Estado
    votacion.save()

    return redirect('app:listaDeVotaciones')

@login_required
def vistaVotacionFacultad(request):
    return render (request, 'app/vistaVotacionFacultad.html')

@login_required
def vistaVotacionFacultadPost(request, id_votacion):
    votacion=Votacion.objects.get(id=id_votacion)
    # Revisar si existe otra forma de llamarlo
    facultad=Facultad.objects.get(id=votacion.facultad_id)
    tipo=TipoVotacion.objects.get(id=votacion.tipo_id)
    estado=EstadoVotacion.objects.get(id=votacion.estado_id)
    contexto={
        'v':votacion,
        'f':facultad,
        't':tipo,
        'e':estado
    }
    return render (request, 'app/vistaVotacionFacultad.html',contexto)

@login_required
def vistaVotacionSemestre(request):
    return render (request, 'app/vistaVotacionSemestre.html')

@login_required
def vistaVotacionSemestrePost(request, id_votacion):
    votacion=Votacion.objects.get(id=id_votacion)
    # Revisar si existe otra forma de llamarlo
    facultad=Facultad.objects.get(id=votacion.facultad_id)

    contexto={
        'votaciones':votacion,
        'f':facultad,
    }
    return render (request, 'app/vistaVotacionSemestre.html',contexto)

@login_required
def postulacionEstudiante2(request):
    return render (request, 'app/postulacionEstudiante2.html')

# PARTE DE ESTUDIANTES
@login_required
def detallesHistorico(request, id_voto):
    id_usuario=request.user.id
    id_votante = Estudiante.objects.get(user_id=id_usuario).id
    v = Votacion.objects.filter(id=id_voto)
    c = Candidato.objects.filter(Votacion_id=id_voto)
    v1 = Voto.objects.filter(Q(votacion_id=id_voto) & Q(votante_id=id_votante))
    contexto={
            'Votacion':v,
            'Candidato':c,
            'Voto':v1,
        }
    return render (request, 'app/detallesHistorico.html',contexto)

@login_required
def detallesResultado(request, id_votacion):
    v = Votacion.objects.filter(id=id_votacion)
    c = Candidato.objects.filter(Votacion_id=id_votacion)
    cVoto = Voto.objects.filter(votacion_id=id_votacion)
    print(cVoto.count())
    contexto={
        'Candidatos':c,
        'Votacion':v,
        'Votos':cVoto.count(),
    }
    return render (request, 'app/detallesResultado.html',contexto)

@login_required
def detallesResultadosFacultad (request):
    return render (request, 'app/detallesResultadosFacultad.html')

@login_required
def historicoVotaciones(request):
    id_usuario=request.user.id
    id_votante = Estudiante.objects.get(user_id=id_usuario)
    v = Votacion.objects.filter(Q(facultad_id=id_votante.facultad_id) & (Q(estado_id=2) | Q(estado_id=3)))
    print(v)
    contexto={
            'Estudiante':id_votante,
            'Votacion':v,
        }
    return render (request, 'app/historicoVotaciones.html',contexto)

@login_required
def listaResultados(request):
    id_usuario=request.user.id
    e=Estudiante.objects.get(user_id=id_usuario)
    v=Votacion.objects.filter(facultad_id=e.facultad_id)
    contexto={
            'estudiante':e,
            'votaciones':v,
    }
    return render (request, 'app/listaResultados.html',contexto)

@login_required
def listaVotacionesEstudiantes(request):
    # id del la facultad del estudiante
        id_usuario=request.user.id
        facultad_estudiante=Estudiante.objects.get(user_id=id_usuario)
        v=Votacion.objects.filter(Q(facultad_id=facultad_estudiante.facultad_id) & Q(estado_id=2))
        i = Voto.objects.filter(Q(votante_id=facultad_estudiante.id))
        if not i:
            i = 1
        else:
            i = 2
        contexto={
            'votaciones':v,
            'voto':i,
        }
        return render (request, 'app/listaVotacionesEstudiantes.html',contexto)

@login_required
def votarCandidato(request):
    return render (request, 'app/votarCandidato.html')

@login_required
def votarCandidatoPost(request, id_votacion):
    votacion=Votacion.objects.get(id=id_votacion)
    facultad=Facultad.objects.get(id=votacion.facultad_id)
    candidato=Candidato.objects.filter(Votacion_id=id_votacion)
    usuario=[]
    id_usuario=request.user.id
    facultad_estudiante=Estudiante.objects.get(user_id=id_usuario)
    print(facultad_estudiante.id)
    i = Voto.objects.filter(Q(votacion_id=id_votacion) & Q(votante_id=facultad_estudiante.id))
    v=Votacion.objects.filter(Q(facultad_id=facultad_estudiante.facultad_id) & Q(estado_id=2))
    if not i:
        i = 1
    else:
        i = 2
    for c in candidato:
        estudiante=Estudiante.objects.filter(id=c.estudiante_id)
        for e in estudiante:
            usuario.extend(User.objects.filter(id=e.user_id))
    contexto={
        'v':votacion,   
        'f':facultad,
        'candidato':candidato,
        'usuario':usuario,
        'voto':i,
        'usuarioID':facultad_estudiante.id,
    }

    return render (request, 'app/votarCandidato.html', contexto)

@login_required
def votacionExitosa(request):
    return render (request, 'app/votacionExitosa.html')

def votacionExitosaPost(request, id_candidato, id_votacion):
    id_usuario=request.user.id
    estudiante=Estudiante.objects.get(user_id=id_usuario)
    voto=Voto()
    voto.candidato_id=id_candidato
    voto.votante_id=estudiante.id
    voto.FechaHora=datetime.today()
    voto.votacion_id=id_votacion
    voto.save()
    return redirect ('app:votacionExitosa')
 

@login_required
def postularme(request):
    # id del la facultad del estudiante
        id_usuario=request.user.id
        facultad_estudiante=Estudiante.objects.get(user_id=id_usuario)
        votacion=Votacion.objects.filter(Q(facultad_id=facultad_estudiante.facultad_id) & Q(estado_id=1))
        contexto={
            'votaciones':votacion,
        }
        
        return render (request, 'app/postularme.html',contexto)

@login_required
def postulacion(request,id_votacion):
    votacion=Votacion.objects.get(id=id_votacion)
    facultad=Facultad.objects.get(id=votacion.facultad_id)
    contexto={
        'v':votacion,
        'f':facultad,
    }
    return render (request, 'app/postulacion.html',contexto)

@login_required
def postulacionPost(request,id_votacion):
    try:
        id_usuario=request.user.id
        estudiante=Estudiante.objects.get(user_id=id_usuario)
        candidato=Candidato.objects.get(Q(Votacion_id=id_votacion) & Q(estudiante_id=estudiante.id))
        return redirect ('app:YaEstaPostulado')

    except:
        id_usuario=request.user.id
        estudiante=Estudiante.objects.get(user_id=id_usuario)
        candidato=Candidato.objects.filter(Q(Votacion_id=id_votacion) & Q(estudiante_id=estudiante.id))
        id_usuario=request.user.id
        p=request.POST['propuesta']
        candidato=Candidato()
        candidato.propuesta=p
        candidato.semestre=estudiante.semestreActual
        candidato.Votacion_id=id_votacion
        candidato.estudiante_id=estudiante.id
        candidato.save()
        veri=True
        return redirect ('app:postulacionExitosa')

@login_required
def YaEstaPostulado(request):
    return render (request,'app/YaEstaPostulado.html')

@login_required
def menuEstudiante(request):
    return render (request, 'app/menuEstudiante.html')

@login_required
def postulacionExitosa(request):
    return render (request, 'app/postulacionExitosa.html')


    
