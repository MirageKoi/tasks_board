from django.contrib import admin
from . models import CardModel


# class TaskAdmin(admin.ModelAdmin):
#     model = CardModel
#     list_display = ('status',)
#     search_fields = ('status',)

#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return CardModel.objects.all()
#         else:
#             return CardModel.objects.filter(status__status='Done')

#     def has_change_permission(self, request, obj=None):
#         if obj is not None and obj.status.status != 'Done':
#             return request.user.has_perm('cards.change_task_status')
#         else:
#             return super().has_change_permission(request, obj=obj)

# admin.site.register(CardModel, TaskAdmin)