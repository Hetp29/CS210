import csv 
import re 
from collections import defaultdict

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def replace_age_ranges(data):
    for row in data:
        if row['age'] and row['age'] != 'NaN':
            if '-' in row['age']:
                age_range = re.findall(r'\d+', row['age'])
                if len(age_range) == 2:
                    avg_age = round((int(age_range[0]) + int(age_range[1])) / 2)
                    row['age'] = str(avg_age)
    
    return data 

def format_dates(data):
    for row in data:
        for date_field in ['date_onset_symptoms', 'date_admission_hospital', 'date_confirmation']:
            if row[date_field] and row[date_field] != 'NaN':
                match = re.match(r'(\d{2})\.(\d{2})\.(\d{4})', row[date_field])
                if match:
                    day, month, year = match.groups()
                    row[date_field] = f'{month}.{day}.{year}'
        
    return data 

def fill_missing_geo_coordinates(data):
    province_to_coords = defaultdict(lambda: {'lat': [], 'lon': []})
    
    for row in data:
        province = row['province']
        if province and province != 'NaN':
            if row['latitude'] and row['latitude'] != 'NaN':
                province_to_coords[province]['lat'].append(float(row['latitude']))
            if row['longitude'] and row['longitude'] != 'NaN':
                province_to_coords[province]['lon'].append(float(row['longitude']))
        
    province_avg_coords = {}
    for province, coords in province_to_coords.items():
        lat_avg = round(sum(coords['lat']) / len(coords['lat']), 2) if coords['lat'] else None
        lon_avg = round(sum(coords['lon']) / len(coords['lon']), 2) if coords['lon'] else None
        province_avg_coords[province] = {'lat': lat_avg, 'lon': lon_avg}
        
    for row in data:
        province = row['province']
        if province and province != 'NaN' and province in province_avg_coords:
            if row['latitude'] == 'NaN' and province_avg_coords[province]['lat']:
                row['latitude'] = str(province_avg_coords[province]['lat'])
            if row['longitude'] == 'NaN' and province_avg_coords[province]['lon']:
                row['longitude'] = str(province_avg_coords[province]['lon'])
        
    return data 

def fill_missing_cities(data):
    province_to_cities = defaultdict(lambda: defaultdict(int))
    
    for row in data:
        province = row['province']
        city = row['city']
        if province and province != 'NaN' and city and city != 'NaN':
            province_to_cities[province][city] += 1
    
    province_to_most_common_city = {}
    for province, cities in province_to_cities.items():
        if cities:
            max_count = max(cities.values())
            most_common_cities = [city for city, count in cities.items() if count == max_count]
            most_common_cities.sort()
            province_to_most_common_city[province] = most_common_cities[0]
    
    for row in data:
        province = row['province']
        if row['city'] == 'NaN' and province in province_to_most_common_city:
            row['city'] = province_to_most_common_city[province]
    
    return data

def fill_missing_symptoms(data):
    province_to_symptoms = defaultdict(lambda: defaultdict(int))
    
    for row in data:
        province = row['province']
        symptoms_str = row['symptoms']
        
        if province and province != 'NaN' and symptoms_str and symptoms_str != 'NaN':
            symptoms = re.split(r';\s*', symptoms_str)
            for symptom in symptoms:
                symptom = symptom.strip()
                if symptom:  # Skip empty strings
                    province_to_symptoms[province][symptom] += 1
    
    province_to_most_common_symptom = {}
    for province, symptoms in province_to_symptoms.items():
        if symptoms:
            max_count = max(symptoms.values())
            most_common_symptoms = [symptom for symptom, count in symptoms.items() if count == max_count]
            most_common_symptoms.sort()
            province_to_most_common_symptom[province] = most_common_symptoms[0]

    for row in data:
        province = row['province']
        if row['symptoms'] == 'NaN' and province in province_to_most_common_symptom:
            row['symptoms'] = province_to_most_common_symptom[province]
    
    return data

def write_data_to_csv(data, filename):
    if data:
        fieldnames = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

def main():
    data = load_data('covidTrain.csv')

    data = replace_age_ranges(data)
    
    data = format_dates(data)
    
    data = fill_missing_geo_coordinates(data)
    data = fill_missing_cities(data)
    data = fill_missing_symptoms(data)
    write_data_to_csv(data, 'covidResult.csv')

if __name__ == "__main__":
    main()