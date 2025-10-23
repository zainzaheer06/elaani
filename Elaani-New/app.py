from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Mock data for prototype
mock_screens = [
    {
        'id': 1,
        'title': 'King Fahd Road LED Billboard',
        'location': 'King Fahd Road, Riyadh',
        'type': 'LED Billboard',
        'size': '6m x 3m',
        'price_per_hour': 250,
        'price_per_day': 5000,
        'owner': 'Digital Media Co.',
        'rating': 4.8,
        'image': '/static/images/screen1.jpg',
        'available': True,
        'features': ['4K Resolution', 'Weather Resistant', 'High Traffic Area']
    },
    {
        'id': 2,
        'title': 'Riyadh Mall Indoor Screen',
        'location': 'Al Nakheel Mall, Riyadh',
        'type': 'Indoor LED',
        'size': '3m x 2m',
        'price_per_hour': 180,
        'price_per_day': 3600,
        'owner': 'Mall Advertising LLC',
        'rating': 4.6,
        'image': '/static/images/screen2.jpg',
        'available': True,
        'features': ['HD Display', 'Shopping Center Location', 'Family Audience']
    },
    {
        'id': 3,
        'title': 'Olaya Street Digital Display',
        'location': 'Olaya Street, Business District',
        'type': 'Digital Display',
        'size': '4m x 2.5m',
        'price_per_hour': 200,
        'price_per_day': 4200,
        'owner': 'Urban Screens KSA',
        'rating': 4.9,
        'image': '/static/images/screen3.jpg',
        'available': False,
        'features': ['Ultra HD', 'Business District', 'Premium Location']
    }
]

mock_bookings = [
    {
        'id': 1,
        'screen_title': 'King Fahd Road LED Billboard',
        'start_date': '2025-09-25',
        'end_date': '2025-09-27',
        'total_cost': 15000,
        'status': 'confirmed',
        'campaign_name': 'New Restaurant Launch'
    },
    {
        'id': 2,
        'screen_title': 'Riyadh Mall Indoor Screen',
        'start_date': '2025-10-01',
        'end_date': '2025-10-03',
        'total_cost': 10800,
        'status': 'pending',
        'campaign_name': 'Fashion Week Promotion'
    }
]

# Routes
@app.route('/')
def index():
    featured_screens = mock_screens[:2]
    return render_template('index.html', screens=featured_screens)

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

@app.route('/choose-role')
def choose_role():
    return render_template('auth/choose_role.html')

# Advertiser Routes
@app.route('/advertiser/dashboard')
def advertiser_dashboard():
    return render_template('advertiser/dashboard.html', bookings=mock_bookings)

@app.route('/advertiser/browse')
def browse_screens():
    return render_template('advertiser/browse_screens.html', screens=mock_screens)

@app.route('/advertiser/screen/<int:screen_id>')
def screen_details(screen_id):
    screen = next((s for s in mock_screens if s['id'] == screen_id), None)
    if not screen:
        flash('Screen not found', 'error')
        return redirect(url_for('browse_screens'))
    return render_template('advertiser/screen_details.html', screen=screen)

@app.route('/advertiser/book/<int:screen_id>')
def book_screen(screen_id):
    screen = next((s for s in mock_screens if s['id'] == screen_id), None)
    if not screen:
        flash('Screen not found', 'error')
        return redirect(url_for('browse_screens'))
    return render_template('advertiser/booking.html', screen=screen)

# Vendor Routes
@app.route('/vendor/dashboard')
def vendor_dashboard():
    return render_template('vendor/dashboard.html', screens=mock_screens[:2])

@app.route('/vendor/list-screen')
def list_screen():
    return render_template('vendor/list_screen.html')

@app.route('/vendor/manage-screens')
def manage_screens():
    return render_template('vendor/manage_screens.html', screens=mock_screens)

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    stats = {
        'total_screens': len(mock_screens),
        'active_bookings': len([b for b in mock_bookings if b['status'] == 'confirmed']),
        'pending_approvals': 3,
        'total_revenue': 125000
    }
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/pending-approvals')
def pending_approvals():
    return render_template('admin/pending_approvals.html', screens=mock_screens)

# API Routes for AJAX
@app.route('/api/screens')
def api_screens():
    return jsonify(mock_screens)

@app.route('/api/book', methods=['POST'])
def api_book():
    data = request.get_json()
    # Mock booking process
    return jsonify({'success': True, 'booking_id': 12345})

if __name__ == '__main__':
    app.run(debug=True)