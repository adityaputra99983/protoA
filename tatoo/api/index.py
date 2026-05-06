import os
import sys

# Add project root to sys.path
# api/index.py -> BASE_DIR is the folder containing 'tatoo', 'tedapp', etc.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tatoo.settings')

# Export WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    app = application
    
    # Run migrations automatically for in-memory DB or first-time setup
    # This is helpful for Vercel demo deployments
    from django.core.management import call_command
    try:
        # Check if we are on Vercel and using in-memory DB
        from django.conf import settings
        if settings.DATABASES['default']['NAME'] == ':memory:':
            print("Running migrations for in-memory database...")
            call_command('migrate', interactive=False)
            # Optional: load sample data if you have a command for it
            try:
                call_command('add_sample_data', interactive=False)
            except:
                pass
    except Exception as migration_error:
        print(f"Migration error: {migration_error}")

except Exception as e:
    print(f"Error loading Django: {e}")
    def app(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [f"Django startup error: {e}".encode('utf-8')]