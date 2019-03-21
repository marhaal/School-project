from django.contrib import admin
from .models import Post, Loan, Comment, Comment2, Community, Trade_request, Trade_loan, Profile, Report, Contact

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Loan)
admin.site.register(Comment2)
admin.site.register(Community)
admin.site.register(Report)
admin.site.register(Trade_request)
admin.site.register(Trade_loan)
admin.site.register(Profile)
admin.site.register(Contact)
