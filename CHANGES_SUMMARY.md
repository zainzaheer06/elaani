# Pure Signage Changes Summary

## Changes Made on April 27, 2026

### 1. User Account Name Changed
**File:** `Pure Signage/app.py`
- Changed user account name from "Omar Al-Rashid" to "Nour El-Masry" (Egyptian female name)
- Updated email from "omar@example.com" to "nour@example.com"
- Location: `inject_current_user()` function

### 2. Booking Details Page Enhancements
**File:** `Pure Signage/templates/bookings.html`

#### Added to Booking Details Modal:
- **Number of Screens**: Displays how many screens are included in the booking
- **Number of Days**: Shows the duration of the booking in days
- **People View Screen**: Displays estimated number of people who will view the screen

These fields are now visible when viewing booking details via the "View Details" button.

### 3. Create New Booking Page Enhancements
**File:** `Pure Signage/templates/bookings.html`

#### Added Input Fields:
- **Number of Screens**: Input field to specify how many screens are needed (default: 1)
- **Number of Days**: Auto-calculated read-only field based on start and end dates
- **No. of People View Screen**: Input field for estimated viewer count

#### Updated JavaScript:
- Modified `calculateTotal()` function to automatically update the "Number of Days" field when dates are selected

### 4. Backend API Updates
**File:** `Pure Signage/app.py`

Updated the `/api/booking/create` endpoint to accept and store new fields:
- `details`: Event details/description
- `num_screens`: Number of screens booked
- `num_days`: Duration in days
- `people_view_screen`: Estimated viewer count

### 5. Analytics Page - Seasonal Trends Enhancement
**File:** `Pure Signage/templates/analytics.html`

#### Added New Seasonal Trend Categories:
1. **Exhibition** - Trade Shows & Expos (+35%)
2. **Entertainment** - Concerts & Shows (+28%)
3. **Occasional Event** - Special Occasions & Celebrations (+22%)
4. **FnB** - Food & Beverage Events (+18%)

These new categories are displayed alongside existing trends (Wedding Season, School Events, Corporate Events, Ramadan Events) in the Seasonal Trends section of the Analytics page.

## Testing
- Flask app imports successfully without errors
- All changes maintain existing functionality
- No breaking changes to the database structure (in-memory data)

## URLs Affected
- `http://127.0.0.1:5900/vendor/bookings` - Booking management page
- `http://127.0.0.1:5900/vendor/analytics` - Analytics page with seasonal trends

## Notes
- All changes are backward compatible
- The booking data structure has been extended but existing bookings will still work
- New fields will default to sensible values if not provided
