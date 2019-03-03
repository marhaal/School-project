from django.contrib import admin
from .models import Post, Loan
from .models import Comment, Comment2
from .models import Community

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Loan)
admin.site.register(Comment2)
admin.site.register(Community)
