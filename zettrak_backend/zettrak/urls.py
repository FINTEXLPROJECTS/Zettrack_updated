from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("ZetTrak backend is running successfully")


def robots_txt(request):
    content = """User-agent: *
Allow: /
Allow: /about/
Allow: /contact/
Disallow: /dashboard/
Disallow: /employees-page/
Disallow: /attendance-page/
Disallow: /leaves-page/
Disallow: /leave-history-page/
Disallow: /leave-types-page/
Disallow: /leave-balances-page/
Disallow: /companies-page/
Disallow: /roles-page/
Disallow: /users-page/
Disallow: /customer-dashboard/
Disallow: /customer-attendance/
Disallow: /customer-leaves/
Disallow: /customer-leave-history/
Disallow: /admin/
Disallow: /api/

Sitemap: https://yourdomain.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yourdomain.com/about/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://yourdomain.com/contact/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
"""
    return HttpResponse(content, content_type="application/xml")


urlpatterns = [
    path('admin/', admin.site.urls),

    # SEO
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap_xml),

    # Template pages + auth API
    path('', include('accounts.urls')),
    path('api/v1/auth/', include('accounts.urls')),

    # New: Users & Roles API
    path('api/v1/accounts/', include('accounts.api_urls')),

    # Existing API routes (unchanged)
    path('api/v1/employees/', include('employees.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/leaves/', include('leave_management.urls')),

    # New: Companies API
    path('api/v1/companies/', include('companies.urls')),
]
