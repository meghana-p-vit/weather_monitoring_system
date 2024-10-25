import smtplib
from email.mime.text import MIMEText
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS, CITIES, ALERT_THRESHOLD_TEMP, ALERT_CONSECUTIVE_READINGS

# Initialize alert count for each city to track consecutive readings
alert_count = {city: 0 for city in CITIES}

def check_alerts(weather_data):
    """Check if the weather data exceeds the defined temperature threshold."""
    temp = weather_data['temp']
    city = weather_data['city']

    # Check if the temperature exceeds the threshold
    if temp > ALERT_THRESHOLD_TEMP:
        alert_count[city] += 1
        if alert_count[city] >= ALERT_CONSECUTIVE_READINGS:
            trigger_alert(city, temp)
    else:
        alert_count[city] = 0  # Reset the alert count if temperature is below the threshold

def trigger_alert(city, temp):
    """Trigger an alert when temperature exceeds threshold for consecutive readings."""
    print(f"ALERT: {city} has exceeded the temperature threshold with {temp}°C!")
    send_email_alert(city, temp)  # Call the email alert function

def send_email_alert(city, temp):
    """Send an email alert to notify the recipient."""
    msg = MIMEText(f"ALERT: {city} has exceeded the temperature threshold with {temp}°C!")
    msg['Subject'] = f"Weather Alert for {city}"
    msg['From'] = EMAIL_USER
    msg['To'] = "meghameghana2904@gmail.com"  # Configure recipient email

    try:
        # Setup SMTP server and send email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"Email alert sent to meghameghana2904@gmail.com for {city}")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

