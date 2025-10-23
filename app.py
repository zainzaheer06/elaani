# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Add custom Jinja2 filters
@app.template_filter('zfill')
def zfill_filter(value, width):
    return str(value).zfill(width)

@app.template_filter('format_currency_simple')
def format_currency_simple(value):
    return f"{value:,}"

@app.template_filter('format_sar')
def format_sar(value):
    return f"{value:,} ريال"

# Template context processor for customer routes
@app.context_processor
def inject_current_user():
    """Make current_user available in all templates for customer routes"""
    current_user_data = {
        'id': 1,
        'name': 'Omar Al-Rashid',
        'email': 'omar@example.com',
        'phone': '+966-11-555-0123',
        'loyalty_tier': 'Silver',
        'loyalty_points': 850,
        'company': 'Tech Innovations Ltd',
        'total_bookings': 12,
        'total_spent': 75000
    }
    
    user_stats_data = {
        'active_bookings': 3,
        'saved_displays': 12,
        'total_spent': 75000,
        'pending_quotes': 2,
        'completed_events': 15
    }
    
    return dict(current_user=current_user_data, user_stats=user_stats_data)

# Sample data (in production, this would come from a database)
screens_data = [
    {
        'id': 1,
        'name': 'LED Display 65"',
        'type': 'LED',
        'size': '65"',
        'resolution': '4K',
        'status': 'available',
        'location': 'Warehouse A',
        'last_service': '2025-09-10',
        'price_per_day': 1500  # Updated to SAR pricing
    },
    {
        'id': 2,
        'name': 'Mobile LED Truck',
        'type': 'Mobile LED',
        'size': 'Large',
        'resolution': 'P6',
        'status': 'rented',
        'location': 'On Route',
        'last_service': '2025-09-05',
        'price_per_day': 4500,  # Updated to SAR pricing
        'current_client': 'Tech Conference',
        'return_date': '2025-09-25'
    },
    {
        'id': 3,
        'name': 'LCD Video Wall 55"',
        'type': 'LCD Wall',
        'size': '55" (3x3)',
        'resolution': 'Full HD',
        'status': 'maintenance',
        'location': 'Service Center',
        'last_service': '2025-08-30',
        'price_per_day': 2400,  # Updated to SAR pricing
        'issue': 'Calibration needed',
        'expected_return': '2025-09-22'
    },
    {
        'id': 4,
        'name': 'Outdoor LED 85"',
        'type': 'Outdoor LED',
        'size': '85"',
        'resolution': '4K',
        'status': 'available',
        'location': 'Warehouse B',
        'last_service': '2025-09-05',
        'price_per_day': 2250  # Updated to SAR pricing
    }
]

bookings_data = [
    {
        'id': 1,
        'client_name': 'Al-Rajhi School',
        'event_type': 'School Event',
        'screen_id': 1,
        'start_date': '2025-09-23',
        'end_date': '2025-09-25',
        'status': 'confirmed',
        'total_amount': 4500,  # Updated to SAR
        'contact': '+966-12-345-6789'
    },
    {
        'id': 2,
        'client_name': 'Riyadh Events Co.',
        'event_type': 'Wedding',
        'screen_id': 4,
        'start_date': '2025-09-27',
        'end_date': '2025-09-28',
        'status': 'pending',
        'total_amount': 4500,  # Updated to SAR
        'contact': '+966-11-987-6543'
    },
    {
        'id': 3,
        'client_name': 'Tech Conference',
        'event_type': 'Corporate',
        'screen_id': 2,
        'start_date': '2025-09-20',
        'end_date': '2025-09-25',
        'status': 'active',
        'total_amount': 22500,  # Updated to SAR
        'contact': '+966-11-555-0123'
    }
]

clients_data = [
    {
        'id': 1,
        'name': 'Al-Rajhi School',
        'type': 'Educational',
        'contact_person': 'Ahmed Al-Rajhi',
        'phone': '+966-12-345-6789',
        'email': 'ahmed@alrajhi-school.edu.sa',
        'total_bookings': 12,
        'total_spent': 54000  # Updated to SAR
    },
    {
        'id': 2,
        'name': 'Riyadh Events Co.',
        'type': 'Event Planning',
        'contact_person': 'Sarah Mohammed',
        'phone': '+966-11-987-6543',
        'email': 'sarah@riyadh-events.com',
        'total_bookings': 8,
        'total_spent': 72000  # Updated to SAR
    },
    {
        'id': 3,
        'name': 'Tech Conference',
        'type': 'Corporate',
        'contact_person': 'Omar Hassan',
        'phone': '+966-11-555-0123',
        'email': 'omar@techconf.sa',
        'total_bookings': 5,
        'total_spent': 105000  # Updated to SAR
    }
]

@app.route('/')
def dashboard():
    # Calculate dashboard statistics
    total_screens = len(screens_data)
    active_rentals = len([b for b in bookings_data if b['status'] == 'active'])
    monthly_revenue = sum([b['total_amount'] for b in bookings_data if b['status'] in ['confirmed', 'active']])
    active_clients = len(clients_data)
    
    # Recent activity (mock data)
    recent_activity = [
        {
            'type': 'booking',
            'title': 'New booking confirmed',
            'description': 'Al-Rajhi School - 2 hours ago',
            'icon': 'fas fa-check',
            'color': 'green'
        },
        {
            'type': 'delivery',
            'title': 'Delivery completed',
            'description': 'LED Screen 55" - 4 hours ago',
            'icon': 'fas fa-truck',
            'color': 'blue'
        },
        {
            'type': 'payment',
            'title': 'Payment received',
            'description': '135,000 ريال - Wedding Event',
            'icon': 'fas fa-coins',
            'color': 'orange'
        },
        {
            'type': 'client',
            'title': 'New client registered',
            'description': 'Riyadh Events Co.',
            'icon': 'fas fa-user-plus',
            'color': 'purple'
        }
    ]
    
    stats = {
        'total_screens': total_screens,
        'active_rentals': active_rentals,
        'monthly_revenue': monthly_revenue,
        'active_clients': active_clients
    }
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         screens=screens_data[:4], 
                         recent_activity=recent_activity)

@app.route('/inventory')
def screen_inventory():
    return render_template('inventory.html', screens=screens_data)

@app.route('/bookings')
def bookings_rentals():
    return render_template('bookings.html', 
                         bookings=bookings_data, 
                         screens=screens_data,
                         clients=clients_data)

@app.route('/clients')
def clients_crm():
    return render_template('clients.html', clients=clients_data)

@app.route('/analytics')
def analytics_reports():
    return render_template('analytics.html')

@app.route('/marketing')
def marketing():
    return render_template('marketing.html') 

@app.route('/financial')
def financial_billing():
    return render_template('financial.html')

@app.route('/operations')
def operations():
    return render_template('operations.html')

# Mock current user data (in production, this would come from a user session/database)
current_user_data = {
    'id': 1,
    'name': 'Omar Al-Rashid',
    'email': 'omar@example.com',
    'phone': '+966-11-555-0123',
    'loyalty_tier': 'Silver',
    'loyalty_points': 850,
    'company': 'Tech Innovations Ltd',
    'total_bookings': 12,
    'total_spent': 75000
}

@app.route('/dashboard/customer')
def customer_dashboard():
    return render_template('customer/dashboard.html')

@app.route('/dashboard/customer/browse-displays')
def browse_displays():
    return render_template('customer/browser_displays.html', screens=screens_data)

@app.route('/dashboard/customer/bookings')
def customer_bookings():
    # Filter bookings for the current customer (mock filtering)
    customer_bookings = bookings_data  # In real app, filter by customer ID
    return render_template('customer/bookings.html', bookings=customer_bookings, screens=screens_data)

@app.route('/customer/quotes')
def customer_quotes():
    return render_template('customer/quotes.html')

@app.route('/customer/payments')
def customer_payments():
    return render_template('customer/payments.html')

@app.route('/customer/favorites')
def customer_favorites():
    return render_template('customer/favorites.html')

@app.route('/event-planner')
def event_planner():
    return render_template('customer/event_planner.html')

@app.route('/customer/support')
def customer_support():
    return render_template('customer/support.html')

@app.route('/customer/profile')
def customer_profile():
    return render_template('customer/profile.html')

@app.route('/api/screens')
def api_screens():
    return jsonify(screens_data)

@app.route('/api/bookings')
def api_bookings():
    return jsonify(bookings_data)

@app.route('/api/screen/<int:screen_id>')
def api_screen_detail(screen_id):
    screen = next((s for s in screens_data if s['id'] == screen_id), None)
    if screen:
        return jsonify(screen)
    return jsonify({'error': 'Screen not found'}), 404

@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    data = request.json
    new_booking = {
        'id': len(bookings_data) + 1,
        'client_name': data.get('client_name'),
        'event_type': data.get('event_type'),
        'screen_id': int(data.get('screen_id')),
        'start_date': data.get('start_date'),
        'end_date': data.get('end_date'),
        'status': 'pending',
        'total_amount': int(data.get('total_amount', 0)),
        'contact': data.get('contact', '')
    }
    bookings_data.append(new_booking)
    return jsonify({'success': True, 'booking': new_booking})

if __name__ == '__main__':
    app.run(debug=True, port=5900)