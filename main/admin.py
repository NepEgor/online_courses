from django.contrib import admin
from main.models import Course, Subscription


class CourseAdmin(admin.ModelAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Course, CourseAdmin)
