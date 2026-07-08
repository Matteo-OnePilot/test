from django.urls import path

from vulnapp import views

urlpatterns = [
    path("search", views.search_users),
    path("ping", views.ping_host),
    path("run", views.run_command),
    path("file", views.read_file),
    path("profile", views.render_profile),
    path("import", views.import_config),
    path("goto", views.go_to),
    path("token", views.generate_token),
    path("login", views.login_view),
    path("upload", views.extract_upload),
    path("template", views.render_template),
    path("eval", views.eval_expression),
]
