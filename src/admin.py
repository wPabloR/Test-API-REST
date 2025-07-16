import os
from flask_admin import Admin
from models import db, User, Airport, Flight, Book
from flask_admin.contrib.sqla import ModelView

class FlightModel(ModelView):
    form_columns = ['flight_number', 'departure_date', 'arrive_date', 'capacity', 'airport']
    form_widget_args = {
        'departure_date': {
            'type': 'date'
        },
        'arrive_date': {
            'type': 'date'
        }
    }

class BookModel(ModelView):
    form_columns = ['seat', 'booking_date', 'user', 'flight']
    form_widget_args = {
        'booking_date': {
            'type': 'date'
        }
    }



def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(FlightModel(Flight, db.session))
    admin.add_view(ModelView(Airport, db.session))
    admin.add_view(BookModel(Book, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))