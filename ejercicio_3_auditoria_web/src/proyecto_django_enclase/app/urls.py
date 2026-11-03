from django.urls import path
from .views import HomeView,PanelSustentabilidadView,TestPytestWebRunnerView

urlpatterns = [
    path('', HomeView.as_view()),
    #path('cursos/', CursosView.as_view()),
    path('sustentabilidad/', PanelSustentabilidadView.as_view()),
    path('testing/', TestPytestWebRunnerView.as_view()),
    
    
]
