from django.contrib import admin

# Register your models here.
from .models import Author,Genre,Book,BookInstance,Language, Comment,BorrowedBook
class AuthorAdmin(admin.ModelAdmin):
    list_display =('first_name','last_name','date_of_birth')
    fields = ['first_name','last_name', 'date_of_birth']
class InlineBookInstanceAdmin(admin.TabularInline):
    model = BookInstance
class BoookAdmin(admin.ModelAdmin):
    list_display = ('title','author' , 'display_genre')
    search_fields = ('title',)
    list_filter = ('author',)
    inlines = [InlineBookInstanceAdmin]

class BookInstanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
         {'fields':('book','imprint','id')}),
    ('Availability',
     {'fields':('status','due_back') }),)
    list_display = ('book', 'imprint', 'due_back')


admin.site.register(Book,BoookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance,BookInstanceAdmin)
admin.site.register(Language)
admin.site.register(Comment)
admin.site.register(BorrowedBook)

