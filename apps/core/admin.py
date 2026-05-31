from django.contrib import admin
from .models import Suggestion

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    # These are the columns that will show up in the admin list view
    list_display = ('name', 'contact_details', 'created_at')
    
    # A search bar to easily find specific messages
    search_fields = ('name', 'contact_details', 'message')
    
    # A filter sidebar to filter by date
    list_filter = ('created_at',)
    
    # Makes the records read-only to avoid me to edit
    readonly_fields = ('name', 'contact_details', 'message', 'created_at')

    # Prevents adding new suggestions from the admin panel (since users do this)
    def has_add_permission(self, request):
        return False