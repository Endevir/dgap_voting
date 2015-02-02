from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from polls.models import Poll, Choice, UserProfile
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

class ChoiceInline(admin.TabularInline):
    model = Choice
    exclude = ('votes',)
    extra = 1

class PollAdmin(admin.ModelAdmin):
	# button generating pdf and html
	def name_with_button(self, obj):
		return mark_safe(obj.name + '  <input type="button", value="pdf", onclick="location.href=\'' + Site.objects.all()[0].domain + 'polls/' + str(obj.id) + '/create_advert/\'">')
	name_with_button.short_description = 'Название опроса'
	
	exclude = ('voted_users',)
	inlines = [ChoiceInline,]
	list_display=['name_with_button']

admin.site.register(Poll, PollAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

#TODO нормальное отображение профиля юзера в админке, разобраться, нужно ли показывать права доступа и группы 

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

