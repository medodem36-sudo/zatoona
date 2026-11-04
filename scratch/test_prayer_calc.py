import math
from datetime import datetime, date

def calculate_offline_prayer_times(city_name, target_date, dst_active=False):
    # Egyptian cities coordinates
    cities = {
        'Cairo': {'lat': 30.0444, 'lng': 31.2357},
        'Alexandria': {'lat': 31.2001, 'lng': 29.9187},
        'Minya': {'lat': 28.1099, 'lng': 30.7503}
    }
    coords = cities.get(city_name, cities['Cairo'])
    lat = coords['lat']
    lng = coords['lng']
    
    # Timezone: Egypt standard is UTC+2, or UTC+3 during DST
    tz_offset = 3 if dst_active else 2

    # Day of year
    day_of_year = target_date.timetuple().tm_yday
    
    # Solar declination and equation of time (Spencer 1971 / standard NOAA formula)
    # B in radians
    b = 2 * math.pi * (day_of_year - 81) / 365.0
    # Equation of time in minutes
    eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
    # Declination in degrees
    decl = 23.45 * math.sin(b)
    decl_rad = math.radians(decl)
    lat_rad = math.radians(lat)
    
    # Solar noon (transit) in hours
    transit = 12.0 + tz_offset - (lng / 15.0) - (eot / 60.0)
    
    def hour_angle(altitude_deg):
        alt_rad = math.radians(altitude_deg)
        cos_ha = (math.sin(alt_rad) - math.sin(lat_rad) * math.sin(decl_rad)) / (math.cos(lat_rad) * math.cos(decl_rad))
        if cos_ha > 1: return 0.0 # Never rises
        if cos_ha < -1: return 180.0 # Never sets
        return math.degrees(math.acos(cos_ha))
    
    # Angles for Egyptian General Authority of Survey (Method 5)
    # Fajr: -19.5 deg
    # Sunrise/Sunset: -0.833 deg
    # Isha: -17.5 deg
    ha_fajr = hour_angle(-19.5)
    ha_sunrise = hour_angle(-0.833)
    
    # Asr (Shafi'i: shadow factor = 1)
    # altitude = arccot(1 + tan|lat - decl|)
    diff_lat_decl = abs(lat_rad - decl_rad)
    asr_alt = math.degrees(math.atan(1.0 / (1.0 + math.tan(diff_lat_decl))))
    ha_asr = hour_angle(asr_alt)
    
    ha_maghrib = ha_sunrise
    ha_isha = hour_angle(-17.5)
    
    fajr_hours = transit - (ha_fajr / 15.0)
    sunrise_hours = transit - (ha_sunrise / 15.0)
    dhuhr_hours = transit
    asr_hours = transit + (ha_asr / 15.0)
    maghrib_hours = transit + (ha_maghrib / 15.0)
    isha_hours = transit + (ha_isha / 15.0)
    
    def to_hhmm(hrs):
        hrs = hrs % 24
        total_mins = int(round(hrs * 60))
        h = (total_mins // 60) % 24
        m = total_mins % 60
        return f"{h:02d}:{m:02d}"
    
    return {
        'fajr': to_hhmm(fajr_hours),
        'sunrise': to_hhmm(sunrise_hours),
        'dhuhr': to_hhmm(dhuhr_hours),
        'asr': to_hhmm(asr_hours),
        'maghrib': to_hhmm(maghrib_hours),
        'isha': to_hhmm(isha_hours)
    }

print("Cairo today:", calculate_offline_prayer_times('Cairo', date.today(), dst_active=False))
print("Minya today:", calculate_offline_prayer_times('Minya', date.today(), dst_active=False))
print("Alexandria today:", calculate_offline_prayer_times('Alexandria', date.today(), dst_active=False))
