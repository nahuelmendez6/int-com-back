from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from django.utils import timezone

from authentication.models import Provider, Customer
from postulations.models import Postulation
from petitions.models import Petition
from grades.models import GradeProvider, GradeCustomer
from notifications.models import Notification
from chat.models import Conversation, Message
try:
    from offers.models import Offer
except ImportError:
    Offer = None


class DashboardAPIView(APIView):
    """
    API para obtener datos del dashboard según el rol del usuario.
    Proporciona un resumen general de actividad, estadísticas y notificaciones.
    """
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Obtiene datos del dashboard según el rol del usuario autenticado.
        
        Returns:
            Response: Datos del dashboard personalizados por rol.
        """
        provider = getattr(request.user, 'provider', None)
        customer = getattr(request.user, 'customer', None)

        if provider:
            return self._get_provider_dashboard(request, provider)
        elif customer:
            return self._get_customer_dashboard(request, customer)
        else:
            return Response(
                {"detail": "Usuario sin rol válido."},
                status=status.HTTP_403_FORBIDDEN
            )

    def _get_provider_dashboard(self, request, provider):
        """Dashboard para proveedores"""
        # Estadísticas de postulaciones
        postulations = Postulation.objects.filter(
            id_provider=provider.id_provider,
            is_deleted=False
        )
        
        # IDs de estados según la base de datos:
        # 1: Pendiente
        # 2: Aprobada
        # 3: Rechazada
        # 4: Ganadora

        total_postulations = postulations.count()
        approved_count = postulations.filter(id_state_id=2).count()
        pending_count = postulations.filter(id_state_id=1).count()
        winner_count = postulations.filter(id_state_id=4).count()

        # Calificaciones
        provider_grades = GradeProvider.objects.filter(provider=request.user, is_visible=True)
        avg_rating = provider_grades.aggregate(avg=Avg('rating'))['avg'] or 0
        total_reviews = provider_grades.count()

        # Peticiones activas (para postular)
        active_petitions = Petition.objects.filter(
            is_deleted=False,
            date_until__gte=timezone.now().date()
        ).count()

        # Mensajes no leídos
        unread_messages = Message.objects.filter(
            conversation__participants=request.user,
            read=False
        ).exclude(sender=request.user).count()

        # Notificaciones no leídas
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        # Postulaciones recientes (últimas 5)
        recent_postulations = postulations.order_by('-date_create')[:5].values(
            'id_postulation', 'id_petition', 'id_state__name', 'date_create', 'winner'
        )

        # Ofertas activas
        active_offers = 0
        if Offer:
            active_offers = Offer.objects.filter(
                id_provider=provider.id_provider,
                is_deleted=False
            ).count()

        return Response({
            'role': 'provider',
            'summary': {
                'postulations': {
                    'total': total_postulations,
                    'approved': approved_count,
                    'pending': pending_count,
                    'winners': winner_count,
                },
                'ratings': {
                    'average': round(float(avg_rating), 2),
                    'total_reviews': total_reviews,
                },
                'opportunities': {
                    'active_petitions': active_petitions,
                    'active_offers': active_offers,
                },
                'communications': {
                    'unread_messages': unread_messages,
                    'unread_notifications': unread_notifications,
                }
            },
            'recent_postulations': list(recent_postulations),
        }, status=status.HTTP_200_OK)

    def _get_customer_dashboard(self, request, customer):
        """Dashboard para clientes"""
        # Peticiones del cliente
        petitions = Petition.objects.filter(
            id_customer=customer.id_customer,
            is_deleted=False
        )

        total_petitions = petitions.count()
        active_petitions = petitions.filter(
            date_until__gte=timezone.now().date()
        ).count()

        # Postulaciones recibidas
        all_postulations = Postulation.objects.filter(
            id_petition__in=petitions.values_list('id_petition', flat=True),
            is_deleted=False
        )
        total_postulations_received = all_postulations.count()

        # Calificaciones dadas
        customer_grades = GradeCustomer.objects.filter(customer=request.user, is_visible=True)
        total_grades_given = customer_grades.count()

        # Mensajes no leídos
        unread_messages = Message.objects.filter(
            conversation__participants=request.user,
            read=False
        ).exclude(sender=request.user).count()

        # Notificaciones no leídas
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        # Peticiones recientes (últimas 5)
        recent_petitions = petitions.order_by('-date_create')[:5].values(
            'id_petition', 'description', 'id_state__name', 'date_create', 'date_until'
        )

        # Postulaciones pendientes de revisión (ID 1: Pendiente)
        pending_review = all_postulations.filter(id_state_id=1).count()

        return Response({
            'role': 'customer',
            'summary': {
                'petitions': {
                    'total': total_petitions,
                    'active': active_petitions,
                    'pending_review': pending_review,
                },
                'postulations': {
                    'total_received': total_postulations_received,
                },
                'ratings': {
                    'total_given': total_grades_given,
                },
                'communications': {
                    'unread_messages': unread_messages,
                    'unread_notifications': unread_notifications,
                }
            },
            'recent_petitions': list(recent_petitions),
        }, status=status.HTTP_200_OK)

