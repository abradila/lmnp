import datetime # Import datetime once at the module level
from lmnp_app import create_app, db
from lmnp_app.models.user import User # Import models to make them known to Flask-Migrate
from lmnp_app.models.property import Property
from lmnp_app.models.revenue import Revenue
from lmnp_app.models.expense import Expense
from lmnp_app.models.amortization import Amortization

app = create_app()

# This context processor makes variables available to all templates
@app.context_processor
def inject_now():
    return {"now": datetime.datetime.utcnow}

if __name__ == "__main__":
    # Consider using a proper WSGI server like Gunicorn for production
    app.run(debug=True, host="0.0.0.0") # Listen on all interfaces for accessibility

