from django.contrib import admin
from .models import Question, Response, CheckupSubmission

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type')


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    readonly_fields = ('question', 'answer')
    can_delete = False
    show_change_link = False


@admin.register(CheckupSubmission)
class CheckupSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'response_count')
    list_filter = ('user',)
    search_fields = ('user__username',)
    readonly_fields = ('user', 'created_at')
    inlines = [ResponseInline]

    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = "Number of Responses"
