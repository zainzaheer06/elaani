# app.py - Pure Signage Main Flask Application
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from flask_babel import Babel, gettext
from datetime import datetime, timedelta
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            static_folder=os.path.join(basedir, 'static'),
            static_url_path='/static')
app.secret_key = 'Pure Signage-bilingual-2025'

app.config['BABEL_DEFAULT_LOCALE'] = 'ar'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

def get_locale():
    return session.get('lang', 'ar')

babel = Babel()
babel.init_app(app, locale_selector=get_locale)


# ─── Jinja filters ─────────────────────────────────────────────
@app.template_filter('zfill')
def zfill_filter(value, width):
    return str(value).zfill(width)

@app.template_filter('format_currency_simple')
def format_currency_simple(value):
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return value

@app.template_filter('format_egp')
def format_egp(value):
    """Format an integer as Saudi Riyals, e.g. 600000 -> '600,000 SAR'."""
    if value in (None, '', 0):
        return ''
    try:
        return f"{int(value):,} SAR"
    except (TypeError, ValueError):
        return value

@app.template_filter('format_sar')
def format_sar(value):
    """Format an integer as Saudi Riyals, e.g. 600000 -> '600,000 SAR'."""
    if value in (None, '', 0):
        return ''
    try:
        return f"{int(value):,} SAR"
    except (TypeError, ValueError):
        return value


# ─── Template globals ──────────────────────────────────────────
@app.context_processor
def inject_current_user():
    current_user_data = {
        'id': 1,
        'name': 'Nour El-Masry',
        'email': 'nour@example.com',
        'phone': '+20-100-555-0123',
        'loyalty_tier': 'Silver',
        'loyalty_points': 850,
        'company': 'Tech Innovations Ltd',
        'total_bookings': 12,
        'total_spent': 750000,
    }

    user_stats_data = {
        'active_bookings': 3,
        'saved_displays': 12,
        'total_spent': 750000,
        'pending_quotes': 2,
        'completed_events': 15,
    }

    return dict(current_user=current_user_data, user_stats=user_stats_data, _=gettext)


# ─── Screen catalogue (Yafta Map quotation 2026-01-13) ─────────
def _screen(_id, district, address, image, price, vat, total, type_, size, sides,
            lat, lng, **kwargs):
    """Build a single screen record. Unset detail fields stay blank — the user fills them in per-screen."""
    return {
        # core
        'id': _id,
        'district': district,
        'address': address,
        'name': f"{district} — {address}" if district else address,
        'image': image,
        'lat': lat,
        'lng': lng,

        # pricing (EGP, monthly)
        'rental_fee': price,
        'vat': vat,
        'total': total,

        # screen specs
        'type': type_,
        'size': size,
        'sides': sides,
        'quantity': kwargs.get('quantity', 1),

        # detail-page fields (blank by default; user fills per-screen)
        'gps': kwargs.get('gps', ''),
        'description': kwargs.get('description', ''),
        'est_traffic': kwargs.get('est_traffic', ''),
        'est_eyeballs': kwargs.get('est_eyeballs', ''),
        'media_type': kwargs.get('media_type', 'LED'),
        'panel_size': kwargs.get('panel_size', size),
        'availability': kwargs.get('availability', 'IMMEDIATE'),
        'rate_card': kwargs.get('rate_card', ''),
        'promotion_rate': price,
        'content_mgmt': kwargs.get('content_mgmt', ''),
        'content_pixel': kwargs.get('content_pixel', ''),
        'duration_per_ad': kwargs.get('duration_per_ad', ''),
        'no_advertiser': kwargs.get('no_advertiser', ''),
        'no_slots': kwargs.get('no_slots', ''),
        'duration_per_loop': kwargs.get('duration_per_loop', ''),
        'no_loop_per_hour': kwargs.get('no_loop_per_hour', ''),
        'no_exposures_per_day': kwargs.get('no_exposures_per_day', ''),
        'screening_hours': kwargs.get('screening_hours', ''),
        'content_format': kwargs.get('content_format', ''),
        'timeline': kwargs.get('timeline', ''),

        # backward-compat (existing templates: bookings/inventory/map)
        'status': kwargs.get('status', 'available'),
        'location': f"{district}, {address}" if district else address,
        'price_per_day': round(price / 30) if price else 0,
        'last_service': '2026-01-13',
        'resolution': kwargs.get('resolution', 'HD'),
    }


screens_data = [
    # ─── Ring Road ───────────────────────────────────────────────
    _screen(1, 'Ring Road', 'In Front Of Mercedes Show Room', 'Ring Road.PNG',
            600000, 84000, 684000, 'Digital screen 6 sec / 1 min', '5H × 50W (3×6)', 10, 30.0083, 31.3033),
    _screen(2, 'Ring Road', 'In Front Of Mercedes Show Room (Another Face)', 'Another Ring Road in front of mercidies showroom.PNG',
            600000, 84000, 684000, 'Digital screen 6 sec / 1 min', '5H × 50W (3×6)', 10, 30.0083, 31.3033),
    _screen(3, 'Ring Road', 'Carrefour - Ring Road', 'Carrefour –Ring road.PNG',
            350000, 49000, 399000, 'LED Screen 10 sec / 2 min', '38 × 5 (3×6)', 10, 29.9762, 31.3194,
            description='2 Faces : Screen, 8 Faces : 3×6 Units'),
    _screen(4, 'Ring Road', 'Carrefour - Ring Road (Another Face)', 'Carrefour –Ring road another face.PNG',
            350000, 49000, 399000, 'LED Screen 10 sec / 2 min', '38 × 5 (3×6)', 10, 29.9762, 31.3194),
    _screen(5, 'Ring Road', 'At Sokhna Bridge', 'At SokhnaBridge Ring road.PNG',
            250000, 35000, 285000, 'LED Screen 7 sec / 60 sec', '8 × 16', 1, 30.0700, 31.4100),
    _screen(6, 'Ring Road', 'At Ketamaya', 'ADDRESS At Ketamaya- ringroad.PNG',
            250000, 35000, 285000, 'LED Screen 7 sec / 60 sec', '8 × 24', 1, 30.0900, 31.4500),
    _screen(7, 'Ring Road', 'JW Marriott Hotel', 'JW Marriott Hotel ring road.PNG',
            250000, 35000, 285000, 'LED Screen 7 sec / 60 sec', '8 × 24', 1, 30.0703, 31.4090),
    _screen(8, 'Ring Road', 'JW Marriott Hotel', 'JW Marriott Hotel.PNG',
            300000, 42000, 342000, 'LED Screen 10 sec / 3 min', '8 × 16', 2, 30.0703, 31.4090,
            quantity=2),

    # ─── October Bridge ─────────────────────────────────────────
    _screen(9, 'October Bridge', 'Lebanon Square', 'Lebanon Square.PNG',
            250000, 35000, 285000, 'LED Screen 10 sec / 2 min', '11.52 × 4.8', 2, 30.0635, 31.2027),
    _screen(10, '6th of October', '6th of October', '6th of October.PNG',
            350000, 49000, 399000, 'LED Screen 7 sec / 70 sec', '12 × 20', 1, 29.9602, 30.9265),
    _screen(11, '6th of October', 'Al Sharabeya', 'Al Sharabeya.PNG',
            150000, 21000, 171000, 'LED Screen 7 sec / 70 sec', '11 × 12', 1, 30.0820, 31.2700),
    _screen(12, 'October Bridge', '6th of October Bridge Exit Towards Nasr City', '6th of October Bridge Exit Towards Nasr City.PNG',
            150000, 21000, 171000, 'LED Screen 15 sec / 3 min', '14 × 7', 1, 30.0723, 31.2456),
    _screen(13, 'October Bridge', '6th of October Bridge Egypt Station', '6th of October Bridge Egypt station.PNG',
            250000, 35000, 285000, 'LED Screen 10 sec / 2 min', '35 × 10', 1, 30.0723, 31.2456),

    # ─── Salah Salem ────────────────────────────────────────────
    _screen(14, 'Salah Salem', 'Al-Sikka Al Bidaa', 'Al –SikkaAl Bidaa.PNG',
            270000, 37800, 307800, 'LED Screen 7 sec / 2 min', '7 × 30', 2, 30.0626, 31.2868),
    _screen(15, 'Salah Salem', 'Oroba Road', 'Salah Salem Led Screen 10 sec 2 min.PNG',
            350000, 49000, 399000, 'LED Screen 7 sec / 2 min', '7 × 30', 2, 30.0908, 31.3260),
    _screen(16, 'Salah Salem', 'Salah Salem', 'Salah Salem.PNG',
            150000, 21000, 171000, 'LED Screen 10 sec / 2 min', '26 × 5 / 22 × 5', 2, 30.0626, 31.2868),

    # ─── Al Thawra Road / Heliopolis ────────────────────────────
    _screen(17, 'Heliopolis', 'El Thawra Street', 'Heliopolis-El Thawra st.PNG',
            270000, 37800, 307800, 'Digital screen 10 sec / 100 sec', '5 × 20', 1, 30.0808, 31.3225),
    _screen(18, 'Heliopolis', 'Kilo 4.5 Sheraton Street', 'st kilo 4.5 Sheraton.PNG',
            270000, 37800, 307800, 'Digital screen 10 sec / 100 sec', '5 × 20', 1, 30.1000, 31.3650),
    _screen(19, 'Heliopolis', 'El Thawra Street (Multi-face)', 'El Thawrast.PNG',
            350000, 49000, 399000, 'Digital screen 7 sec / 60 sec', '7 × 62 (Face 2) / 3×6 (Face 8)', 5, 30.0808, 31.3225),

    # ─── Nasr City ──────────────────────────────────────────────
    _screen(20, 'Nasr City', 'Abbas El-Akkad', 'Abbas El-Akkad.PNG',
            150000, 21000, 171000, 'Digital screen 10 sec / 100 sec', '5W × 20H', 1, 30.0617, 31.3296),
    _screen(21, 'Nasr City', 'El-Nasr Street', 'El-Nasr Street.PNG',
            250000, 35000, 285000, 'Digital screen 7 sec / 60 sec', '7.5W × 36H', 2, 30.0626, 31.3460),

    # ─── Zamalek ────────────────────────────────────────────────
    _screen(22, 'Zamalek', 'Al Zamalik', 'Al Zamalik.PNG',
            150000, 21000, 171000, 'LED Screen 12 sec / 2.5 min', '15 × 6', 1, 30.0626, 31.2197),
    _screen(23, 'Zamalek', '26th of July Street', '(26TH of July Street)  - Zamalek.PNG',
            70000, 9800, 79800, 'LED Screen 10 sec / 100 sec', '4 × 6', 1, 30.0635, 31.2197),

    # ─── Mehwar / Zayed / 6th October Axis ──────────────────────
    _screen(24, 'Mehwar', 'Mehwar Road (Mohandessin)', 'Mehwar Road (Mohandessin).PNG',
            150000, 21000, 171000, 'LED Screen 15 sec / 2.5 min', '20 × 5', 2, 30.0500, 31.2050),
    _screen(25, 'Mehwar', 'Al Mehwar (Zayed - October)', 'Al Mehwar (Zayed-October ).PNG',
            300000, 42000, 342000, 'LED Screen 8 sec / 1.5 min', '30 × 9', 2, 30.0184, 30.9750),
    _screen(26, 'Zayed', 'Zayed City / Alex Desert Road', 'ZayedCity-Alex Desert Road.PNG',
            450000, 63000, 513000, 'LED Screen 7 sec / 70 sec', '6 × 50 / 3×5', 5, 30.0245, 30.9742),
    _screen(27, 'Mehwar', 'Al Mehwar (Mall of Egypt area)', 'Al Mehwar (Zayed-October ).PNG',
            250000, 35000, 285000, 'LED Screen 8 sec / 1.5 min', '30 × 9', 2, 30.0184, 30.9750),
    _screen(28, 'Zayed', 'Zayed City (Hyper One)', 'Zayed city (hyper one).PNG',
            250000, 35000, 285000, 'Uni-pole 10 sec / 100 sec', '7 × 15 / 6 × 3', 3, 30.0298, 30.9876),
    _screen(29, 'Zayed', 'Capital Business Park', 'Capital Business Park.PNG',
            250000, 35000, 285000, 'Uni-pole 10 sec / 100 sec', '9 × 18', 1, 30.0010, 31.0070),
    _screen(30, 'Zayed', 'Galleria 40', 'Galleria 40.PNG',
            250000, 35000, 285000, 'Uni-pole 10 sec / 100 sec', '9 × 18', 1, 30.0066, 30.9966),
    _screen(31, 'Dahshour', 'North Dahshour Road', 'NORTHDahshourRoad.PNG',
            250000, 35000, 285000, 'Uni-pole 10 sec / 100 sec', '9 × 18', 1, 29.9990, 31.0250),
    _screen(32, 'Dahshour', 'South Dahshour', 'South DahshourDahshour.PNG',
            250000, 35000, 285000, 'Uni-pole 10 sec / 100 sec', '9 × 18', 1, 29.7900, 31.2050),
    _screen(33, 'Palm Hills', 'Palm Hills - El Khamayel', 'Palm Hills – El Khamayel.PNG',
            100000, 14000, 114000, 'Uni-pole 10 sec / 100 sec', '12 × 5', 1, 30.0081, 30.9700),
    _screen(34, 'Zayed', 'Hyper - Zayed', 'HYPER -Zayed.PNG',
            300000, 42000, 342000, 'LED Screen 10 sec / 2 min', '25 × 5', 2, 30.0298, 30.9876),
    _screen(35, 'Palm Hills', 'Izar Mall - Palm Hills', 'Izar Mall – Palm Hills.PNG',
            150000, 21000, 171000, 'LED Screen 10 sec / 2 min', '26 × 10', 1, 30.0070, 30.9700),
    _screen(36, 'Zayed', 'Dorra Square', 'DorraSquare.PNG',
            350000, 49000, 399000, 'LED Screen 10 sec / 2 min', '7 × 5 / 3×6 (Face 8)', 9, 30.0150, 30.9900),
    _screen(37, 'Zayed', 'Arkan', 'Arkan.PNG',
            60000, 8400, 68400, 'LED Screen 10 sec / 2 min', '7 × 5', 1, 30.0224, 31.0001),
    _screen(38, 'Dahshour', 'North Dahshour Axis', 'North DahshourAxis.PNG',
            300000, 42000, 342000, 'LED Screen 10 sec / 2 min', '3 × 6 / 10 × 20', 6, 29.9990, 31.0250,
            quantity=6),
    _screen(39, 'Giza', 'Grand Museum Area', 'Grand Museum Area.PNG',
            350000, 49000, 399000, 'LED Screen 10 sec / 2 min', '8 × 16', 1, 29.9928, 31.1342),

    # ─── Maadi ──────────────────────────────────────────────────
    _screen(40, 'Maadi', 'Maadi Corniche', 'MaadiCorniche.PNG',
            180000, 25200, 205200, 'Digital screen 7 sec / 3 min', '25W × 5H', 1, 29.9603, 31.2569),

    # ─── Downtown ───────────────────────────────────────────────
    _screen(41, 'Downtown', 'Abdelmonem Riyadh', 'AbdelmonemRiyadh.PNG',
            150000, 21000, 171000, 'Digital screen 10 sec / 100 sec', '4 × 17', 1, 30.0561, 31.2275),

    # ─── Mohandessin ───────────────────────────────────────────
    _screen(42, 'Mohandessin', 'Gameat El Dewal', 'Gameat El Dewal.PNG',
            120000, 16800, 136800, 'LED Screen 10 sec / 2 min', '14 × 4', 1, 30.0578, 31.2025),
    _screen(43, 'Mohandessin', 'Gameat El Dewal (Larger)', 'Gameat El Dewal 2.PNG',
            300000, 42000, 342000, 'LED Screen 10 sec / 2 min', '6 × 14', 2, 30.0578, 31.2025),
    _screen(44, 'Mohandessin', 'AL-Batal Ahmed Abdel Aziz', 'AL-BatalAhmed Abdel Aziz.PNG',
            120000, 16800, 136800, 'LED Screen 10 sec / 2 min', '10 × 4', 1, 30.0581, 31.2025),
    _screen(45, 'Mohandessin', 'In Front of Tersana Club', 'In front of Zamalek Club.PNG',
            175000, 24500, 199500, 'LED Screen 10 sec / 100 sec', '5 × 12', 2, 30.0651, 31.2027),
    _screen(46, 'Mohandessin', 'In Front of Zamalek Club', 'In front of Zamalek Club.PNG',
            175000, 24500, 199500, 'LED Screen 10 sec / 100 sec', '5 × 8', 1, 30.0635, 31.2197),
    _screen(47, 'Mohandessin', 'Lebanon Square (Mohandessin)', '(lebanon square)- Al-Mohandeseen.PNG',
            80000, 11200, 91200, 'LED Screen 10 sec / 100 sec', '4 × 7', 2, 30.0635, 31.2027),
    _screen(48, 'Mohandessin', 'Doki', 'Al-Mohandeseen-Doki.PNG',
            60000, 8400, 68400, 'LED Screen 10 sec / 100 sec', '3 × 7', 1, 30.0379, 31.2069),
    _screen(49, 'Mohandessin', 'Doki (2 sides)', 'Doki-Al-Mohandeseen.PNG',
            60000, 8400, 68400, 'LED Screen 10 sec / 100 sec', '4 × 7', 2, 30.0379, 31.2069),
    _screen(50, 'Giza', 'Mourad Street', 'Mourad St -Giza.PNG',
            30000, 4200, 34200, 'LED Screen 10 sec / 100 sec', '3 × 5', 1, 30.0144, 31.2089),

    # ─── Suez Road / Heliopolis ─────────────────────────────────
    _screen(51, 'Suez Road', 'Almaza City Center (Suez Road)', 'Heliopolis-El Thawra st.PNG',
            300000, 42000, 342000, 'LED Screen 10 sec / 2 min', '20 × 5 / 3 × 6', 6, 30.0987, 31.3475),
    _screen(52, 'Heliopolis', 'Al Rehab Inter', 'Al Rehab Inter- Heliopolis.PNG',
            250000, 35000, 285000, 'Digital screen 7 sec / 60 sec', '8 × 16 (Face 1) / 8 × 8 (Face 1)', 2, 30.0625, 31.4925),

    # ─── Al Mosher Road ─────────────────────────────────────────
    _screen(53, 'Al Mosher', 'Coming from Nasr City to Village & Al 90 St', 'Coming from Nasr City to Village & Al 90 St.PNG',
            375000, 52500, 427500, 'Digital screen 7 sec / 60 sec', '7 × 30', 2, 30.0220, 31.4750),
    _screen(54, 'Al Mosher', 'Nasr City to Olympic Village & Ring Road / 90 St', 'Coming from Nasr City to the Olympic Village & Ring Road and Al 90 St.,.PNG',
            250000, 35000, 285000, 'Digital screen 10 sec / 2 min', '5 × 20', 1, 30.0220, 31.4720),
    _screen(55, 'Al Mosher', 'Al Mosher', 'Al Mosher.PNG',
            350000, 49000, 399000, 'Digital screen 10 sec / 2 min', '5 × 20 / 3 × 6', 4, 30.0220, 31.4750),

    # ─── New Cairo ──────────────────────────────────────────────
    _screen(56, 'New Cairo', 'Downtown Mall - New Cairo', 'Downtown Mall  -New Cairo.PNG',
            250000, 35000, 285000, 'LED Screen 15 sec / 2.5 min', '75 × 6', 1, 30.0301, 31.4738),
    _screen(57, 'New Cairo', 'North 90th Street', 'North 90’st-new cairo.PNG',
            500000, 70000, 570000, 'LED Screen 15 sec / 2 min', '5H × 18W', 1, 30.0260, 31.4990),
    _screen(58, 'New Cairo', 'In Front of Downtown', 'IN  front of Downtown  - New Cairo.PNG',
            250000, 35000, 285000, 'LED Screen 15 sec / 2 min', '8H × 24W', 1, 30.0301, 31.4738),
    _screen(59, 'New Cairo', 'North 90th St Exit (Downtown ↔ Cairo Festival)', 'North 90’s Street Exit BetweenDowntown & Cairo Festival.PNG',
            250000, 35000, 285000, 'LED Screen 15 sec / 2 min', '8H × 18W', 1, 30.0287, 31.4072),
    _screen(60, 'New Cairo', 'One Mall (Beside Waterway 1, Mohamed Naguib St)', 'One Mall Beside Waterway 1Mohamed Naguib street.PNG',
            250000, 35000, 285000, 'LED Screen 15 sec / 2 min', '8H × 16W', 1, 30.0207, 31.4738),
    _screen(61, 'New Cairo', 'S Street - The Ark', 'S ST the Ark.PNG',
            260000, 36400, 296400, 'LED Screen 15 sec / 2 min', '8H × 16W', 1, 30.0290, 31.4990),
    _screen(62, 'New Cairo', 'North 90th St "Water Way 2"', 'North 90th St. “Water Way 2”.PNG',
            350000, 49000, 399000, 'Digital screen 10 sec / 2.5 min', '5H × 25W (2 face) / 3H × 6W (4 face)', 6, 30.0207, 31.4738),
    _screen(63, 'New Cairo', 'Jumia', 'Jumia.PNG',
            300000, 42000, 342000, 'Digital screen 10 sec / 2.5 min', '8H × 17W / 3H × 6W (4 face)', 5, 30.0265, 31.4955),
    _screen(64, 'New Cairo', 'Dusit Hotel', 'Dusit Hotel.PNG',
            300000, 42000, 342000, 'LED Screen 10 sec / 2 min', '8H × 24W / 8 × 16', 1, 30.0306, 31.4711),
    _screen(65, 'New Cairo', 'Dusit Hotel (Another Face)', 'Dusit Hotel.PNG',
            550000, 77000, 627000, 'LED Screen 10 sec / 2 min', '8H × 24W / 8 × 16', 2, 30.0306, 31.4711),
    _screen(66, 'New Cairo', 'One Golden Square (Jibouty Sq.)', 'One golden square (Jibouty sq.).PNG',
            250000, 35000, 285000, 'LED Screen 15 sec / 2 min', '8H × 16W', 1, 30.0263, 31.4752),
    _screen(67, 'New Cairo', 'Katamya - Gamal Abdelnaser Axis', 'KATAMYA –Gamal AbdelnaserAxis.PNG',
            250000, 35000, 285000, 'LED Screen 15 sec / 2 min', '8H × 16W', 1, 29.9853, 31.4290),
    _screen(68, 'New Cairo', 'Entrance Between Downtown & Cairo Festival', 'Entrance Between Downtown & Cairo Festival.PNG',
            150000, 21000, 192000, 'LED Screen 10 sec / 2 min', '3H × 6W', 4, 30.0287, 31.4072,
            quantity=4),
    _screen(69, 'New Cairo', 'Al Rehab Entrance Gate 1', 'AL Rehab Entrance Gate 1.PNG',
            150000, 21000, 171000, 'LED Screen 15 sec / 2 min', '7H × 14W', 1, 30.0671, 31.4900),

    # ─── Airport ────────────────────────────────────────────────
    _screen(70, 'Airport', 'Tahia Misr Gates', 'TahiaMisrGates.PNG',
            200000, 28000, 228000, 'LED Screen 10 sec / 2 min', '11.52 × 3.84', 6, 30.1219, 31.4056,
            quantity=3),

    # ─── Alexandria ─────────────────────────────────────────────
    _screen(71, 'Alexandria', 'Al-Mahrosa', 'Alexandria –(Al-Mahrosa).PNG',
            200000, 28000, 228000, 'LED Screen 10 sec / 2 min', '8H × 16W', 2, 31.2001, 29.9187),
    _screen(72, 'Alexandria', 'Al-Mahrosa (Mixed Sizes)', 'Alexandria –(Al-Mahrosa) alex.PNG',
            175000, 24500, 199500, 'LED Screen 10 sec / 2 min', '7 × 14 / 3 × 6', 2, 31.2001, 29.9187),
    _screen(73, 'Alexandria', 'Roshdy Corniche', 'شينروكلا يدشر-Alexandria.PNG',
            30000, 4200, 34200, 'Digital screen 10 sec', '3 × 5', 1, 31.2244, 29.9580),

    # ─── Obour City ─────────────────────────────────────────────
    _screen(74, 'Obour City', 'In Front of Carrefour Obour', 'روبعلا روفراك ماما-obour city.PNG',
            150000, 21000, 171000, 'LED Screen 7 sec / 2 min', '7 × 30', 2, 30.2125, 31.4630),
]


# ─── Mock bookings & clients ────────────────────────────────────
bookings_data = [
    {
        'id': 1,
        'client_name': 'Leap Event',
        'event_type': 'Conference',
        'screen_id': 56,
        'start_date': '2026-02-15',
        'end_date': '2026-02-17',
        'status': 'confirmed',
        'total_amount': 285000,
        'contact': '+20-100-555-0123',
    },
    {
        'id': 2,
        'client_name': 'Gea',
        'event_type': 'Marketing',
        'screen_id': 1,
        'start_date': '2026-03-01',
        'end_date': '2026-03-31',
        'status': 'pending',
        'total_amount': 684000,
        'contact': '+20-100-987-6543',
    },
    {
        'id': 3,
        'client_name': '7dogs',
        'event_type': 'Corporate',
        'screen_id': 39,
        'start_date': '2026-02-20',
        'end_date': '2026-02-25',
        'status': 'active',
        'total_amount': 399000,
        'contact': '+20-100-555-0123',
    },
    {
        'id': 4,
        'client_name': 'Keeta',
        'event_type': 'Exhibition',
        'screen_id': 24,
        'start_date': '2026-03-10',
        'end_date': '2026-03-15',
        'status': 'confirmed',
        'total_amount': 171000,
        'contact': '+20-100-444-5555',
    },
    {
        'id': 5,
        'client_name': 'Sephora',
        'event_type': 'Marketing',
        'screen_id': 42,
        'start_date': '2026-03-20',
        'end_date': '2026-04-05',
        'status': 'pending',
        'total_amount': 136800,
        'contact': '+20-100-333-4444',
    },
    {
        'id': 6,
        'client_name': 'Dio',
        'event_type': 'Entertainment',
        'screen_id': 22,
        'start_date': '2026-04-01',
        'end_date': '2026-04-10',
        'status': 'active',
        'total_amount': 171000,
        'contact': '+20-100-222-3333',
    },
]

clients_data = [
    {
        'id': 1,
        'name': 'Leap Event',
        'type': 'Corporate',
        'contact_person': 'Ahmed Hassan',
        'phone': '+20-100-555-0123',
        'email': 'contact@leapevent.eg',
        'total_bookings': 12,
        'total_spent': 5400000,
    },
    {
        'id': 2,
        'name': 'Gea',
        'type': 'Retail',
        'contact_person': 'Sarah Mohammed',
        'phone': '+20-100-987-6543',
        'email': 'info@gea.com',
        'total_bookings': 8,
        'total_spent': 7200000,
    },
    {
        'id': 3,
        'name': '7dogs',
        'type': 'Event Planning',
        'contact_person': 'Omar Hassan',
        'phone': '+20-100-555-7777',
        'email': 'contact@7dogs.eg',
        'total_bookings': 5,
        'total_spent': 1500000,
    },
    {
        'id': 4,
        'name': 'Keeta',
        'type': 'Technology',
        'contact_person': 'Fatima Ali',
        'phone': '+20-100-444-5555',
        'email': 'info@keeta.com',
        'total_bookings': 6,
        'total_spent': 2100000,
    },
    {
        'id': 5,
        'name': 'Sephora',
        'type': 'Retail',
        'contact_person': 'Layla Ahmed',
        'phone': '+20-100-333-4444',
        'email': 'marketing@sephora.eg',
        'total_bookings': 15,
        'total_spent': 8500000,
    },
    {
        'id': 6,
        'name': 'Dio',
        'type': 'Entertainment',
        'contact_person': 'Karim Mostafa',
        'phone': '+20-100-222-3333',
        'email': 'events@dio.eg',
        'total_bookings': 9,
        'total_spent': 3200000,
    },
]


# ─── Helpers ────────────────────────────────────────────────────
def _find_screen(screen_id):
    return next((s for s in screens_data if s['id'] == screen_id), None)


# ─── Routes: home / vendor ──────────────────────────────────────
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/vendor')
def dashboard():
    total_screens = len(screens_data)
    active_rentals = len([b for b in bookings_data if b['status'] == 'active'])
    monthly_revenue = sum(b['total_amount'] for b in bookings_data if b['status'] in ('confirmed', 'active'))
    active_clients = len(clients_data)

    ai_insights = {
        'peak_demand_days': ['Thursday', 'Friday', 'Saturday'],
        'trending_screen_type': 'LED Billboards',
        'avg_booking_duration': '3.5 days',
        'top_client_category': 'Corporate Events',
        'revenue_forecast': int(monthly_revenue * 1.15),
        'optimization_tips': [
            {'tip': gettext('Your LED screens have 40% higher demand during weekends'), 'impact': 'high'},
            {'tip': gettext('Consider adding 2 more screens in high-traffic areas for 25% revenue increase'), 'impact': 'medium'},
            {'tip': gettext('Corporate clients prefer 3-5 day bookings'), 'impact': 'medium'},
        ],
    }

    recent_activity = [
        {'type': 'booking', 'title': gettext('New booking confirmed'),
         'description': gettext('Innovation Corp - 2 hours ago'), 'icon': 'fas fa-check', 'color': 'green'},
        {'type': 'delivery', 'title': gettext('Delivery completed'),
         'description': gettext('LED Screen 8×16 - 4 hours ago'), 'icon': 'fas fa-truck', 'color': 'blue'},
        {'type': 'payment', 'title': gettext('Payment received'),
         'description': gettext('684,000 EGP - Ring Road Campaign'), 'icon': 'fas fa-coins', 'color': 'orange'},
        {'type': 'client', 'title': gettext('New client registered'),
         'description': gettext('Cairo Events Group'), 'icon': 'fas fa-user-plus', 'color': 'purple'},
    ]

    customer_event_requests = [
        {
            'event_name': 'Tech Summit 2026',
            'event_type': 'Conference',
            'customer_name': 'Innovation Corp',
            'date': 'Mar 15-17, 2026',
            'budget': '450,000 EGP',
            'screens_needed': 3,
            'match_score': 95,
            'location': 'New Cairo',
            'suggested_screens': ['Downtown Mall - New Cairo', 'One Mall Beside Waterway'],
        },
        {
            'event_name': 'Brand Activation',
            'event_type': 'Marketing',
            'customer_name': 'Saudi Retail Co',
            'date': 'Apr 5-12, 2026',
            'budget': '600,000 EGP',
            'screens_needed': 4,
            'match_score': 92,
            'location': 'Multiple Locations',
            'suggested_screens': ['Ring Road - Mercedes', 'Heliopolis - El Thawra'],
        },
    ]

    stats = {
        'total_screens': total_screens,
        'active_rentals': active_rentals,
        'monthly_revenue': monthly_revenue,
        'active_clients': active_clients,
    }

    return render_template('dashboard.html',
                           stats=stats,
                           screens=screens_data[:4],
                           recent_activity=recent_activity,
                           ai_insights=ai_insights,
                           customer_event_requests=customer_event_requests)

@app.route('/vendor/inventory')
def screen_inventory():
    return render_template('inventory.html', screens=screens_data)

@app.route('/vendor/bookings')
def bookings_rentals():
    return render_template('bookings.html',
                           bookings=bookings_data,
                           screens=screens_data,
                           clients=clients_data)

@app.route('/vendor/clients')
def clients_crm():
    return render_template('clients.html', clients=clients_data)

@app.route('/vendor/analytics')
def analytics_reports():
    return render_template('analytics.html')

@app.route('/vendor/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/vendor/financial')
def financial_billing():
    return render_template('financial.html')

@app.route('/vendor/map')
def map_view():
    return render_template('map.html', screens=screens_data)

@app.route('/vendor/map-view')
def map_view_big():
    return render_template('map_big.html', screens=screens_data)

@app.route('/vendor/operations')
def operations():
    return render_template('operations.html')

@app.route('/vendor/screen/<int:screen_id>')
def vendor_screen_detail(screen_id):
    screen = _find_screen(screen_id)
    if not screen:
        abort(404)
    return render_template('screen_detail.html', screen=screen, viewer='vendor')


# ─── Routes: customer ──────────────────────────────────────────
@app.route('/dashboard/customer')
def customer_dashboard():
    return render_template('customer/dashboard.html')

@app.route('/dashboard/customer/map')
def customer_map():
    return render_template('customer/map_big.html', screens=screens_data)

@app.route('/dashboard/customer/browse-displays')
def browse_displays():
    return render_template('customer/browser_displays.html', screens=screens_data)

@app.route('/dashboard/customer/bookings')
def customer_bookings():
    return render_template('customer/bookings.html', bookings=bookings_data, screens=screens_data)

@app.route('/dashboard/customer/screen/<int:screen_id>')
def customer_screen_detail(screen_id):
    screen = _find_screen(screen_id)
    if not screen:
        abort(404)
    return render_template('screen_detail.html', screen=screen, viewer='customer')

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


# ─── JSON API ──────────────────────────────────────────────────
@app.route('/api/screens')
def api_screens():
    return jsonify(screens_data)

@app.route('/api/bookings')
def api_bookings():
    return jsonify(bookings_data)

@app.route('/api/screen/<int:screen_id>')
def api_screen_detail(screen_id):
    screen = _find_screen(screen_id)
    if screen:
        return jsonify(screen)
    return jsonify({'error': 'Screen not found'}), 404

@app.route('/api/screen/<int:screen_id>/update', methods=['POST'])
def api_screen_update(screen_id):
    screen = _find_screen(screen_id)
    if not screen:
        return jsonify({'success': False, 'error': 'Screen not found'}), 404
    data = request.json or {}
    # Allow editing a few fields in-memory (resets on server restart — see CLAUDE.md)
    for field in ('district', 'address', 'size', 'gps'):
        if field in data and data[field] is not None:
            screen[field] = str(data[field])
    for int_field in ('promotion_rate', 'vat', 'sides'):
        if int_field in data and data[int_field] not in (None, ''):
            try:
                screen[int_field] = int(data[int_field])
            except (TypeError, ValueError):
                pass
    # Recompute derived fields
    screen['name'] = f"{screen['district']} — {screen['address']}" if screen['district'] else screen['address']
    screen['location'] = f"{screen['district']}, {screen['address']}" if screen['district'] else screen['address']
    screen['rental_fee'] = screen['promotion_rate']
    screen['total'] = screen['promotion_rate'] + screen['vat']
    screen['price_per_day'] = round(screen['promotion_rate'] / 30) if screen['promotion_rate'] else 0
    return jsonify({'success': True, 'screen': screen})


@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    data = request.json or {}
    new_booking = {
        'id': len(bookings_data) + 1,
        'client_name': data.get('client_name'),
        'event_type': data.get('event_type'),
        'screen_id': int(data.get('screen_id', 0)),
        'start_date': data.get('start_date'),
        'end_date': data.get('end_date'),
        'status': 'pending',
        'total_amount': int(data.get('total_amount', 0)),
        'contact': data.get('contact', ''),
        'details': data.get('details', ''),
        'num_screens': int(data.get('num_screens', 1)),
        'num_days': int(data.get('num_days', 1)),
        'people_view_screen': int(data.get('people_view_screen', 0)),
    }
    bookings_data.append(new_booking)
    return jsonify({'success': True, 'booking': new_booking})


# ─── Language ──────────────────────────────────────────────────
@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in ('ar', 'en'):
        session['lang'] = lang
    return redirect(request.referrer or url_for('customer_dashboard'))


# ─── Test routes (kept for now; remove before deploy) ─────────
@app.route('/test-i18n')
def test_i18n():
    return f"<h1>Translation Test</h1><p>Locale: {get_locale()}</p><p>{gettext('Dashboard')}</p>"

@app.route('/test-ar')
def test_ar():
    session['lang'] = 'ar'
    return f"<html dir='rtl'><body><h1>اختبار الترجمة</h1><p>{gettext('Dashboard')}</p></body></html>"

@app.route('/test-en')
def test_en():
    session['lang'] = 'en'
    return f"<h1>Translation Test</h1><p>{gettext('Dashboard')}</p>"


if __name__ == '__main__':
    app.run(debug=True, port=5900)
