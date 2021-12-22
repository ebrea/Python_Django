from django.db import models
from django.contrib.auth.models import User    # para usar o User importar modos do django
from datetime import datetime, timedelta

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100, verbose_name='Compromisso')
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data e Hora')
    data_criacao = models.DateTimeField(auto_now=True, verbose_name='Momento do Agendamento')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # se apagar o usuário, apaga tudo dele

    class Meta:
        db_table = 'evento'

    def __str__(self):                  # retorna o titulo do evento agendado
        return self.titulo              # troca "Evento object(1)" por "Dentista"


    def dataEvento(self):               # função para formatar a data padrão Brasil
        return self.data_evento.strftime('%d/%m/%Y  %H:%M')


    def mostraData(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')


    def passados(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False

