from django.contrib import admin
from django.db.models import Count
from .models import Category, Tag, Article, UserProfile, SubscriptionPlan, Comment, NewsletterSubscription

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'submitted_at', 'published_at', 'views_count', 'is_premium', 'read_time_minutes')
    list_filter = ('status', 'category', 'is_premium')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_articles', 'reject_articles']

    def approve_articles(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, "Selected articles have been approved and published.")
    approve_articles.short_description = "Approve selected articles"

    def reject_articles(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, "Selected articles have been rejected and returned to draft.")
    reject_articles.short_description = "Reject selected articles"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(author=request.user)
        return qs

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected comments have been approved.")
    approve_comments.short_description = "Approve selected comments"

class DSMAdminSite(admin.AdminSite):
    site_header = "DSM Times Admin"
    site_title = "DSM Times Admin Portal"
    index_title = "Welcome to DSM Times Admin Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Analytics
        total_articles = Article.objects.count()
        pending_articles = Article.objects.filter(status='pending').count()
        published_articles = Article.objects.filter(status='published').count()
        total_users = User.objects.count()
        total_subscribers = UserProfile.objects.filter(is_subscriber=True).count()
        total_comments = Comment.objects.count()
        approved_comments = Comment.objects.filter(is_approved=True).count()
        total_newsletter_subs = NewsletterSubscription.objects.count()
        top_articles = Article.objects.filter(status='published').order_by('-views_count')[:5]
        top_authors = User.objects.annotate(article_count=Count('articles')).order_by('-article_count')[:5]
        
        extra_context.update({
            'total_articles': total_articles,
            'pending_articles': pending_articles,
            'published_articles': published_articles,
            'total_users': total_users,
            'total_subscribers': total_subscribers,
            'total_comments': total_comments,
            'approved_comments': approved_comments,
            'total_newsletter_subs': total_newsletter_subs,
            'top_articles': top_articles,
            'top_authors': top_authors,
        })
        return super().index(request, extra_context)

admin_site = DSMAdminSite(name='dsm_admin')
admin.site = admin_site

admin_site.register(Category)
admin_site.register(Tag)
admin_site.register(Article, ArticleAdmin)
admin_site.register(UserProfile)
admin_site.register(SubscriptionPlan)
admin_site.register(Comment, CommentAdmin)
admin_site.register(NewsletterSubscription)