from django.contrib import admin
from .models import AI_Agent, TaskPipeline, Escalation,  SalesFunnelStageInstruction

# Register your models here.
admin.site.register(AI_Agent)
admin.site.register(TaskPipeline)
admin.site.register(Escalation)
admin.site.register( SalesFunnelStageInstruction)
