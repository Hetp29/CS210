import csv 
from collections import defaultdict

def load_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data 

def calculate(data):
    fire_count = 0
    fire_level_40_plus = 0 
    
    for pokemon in data:
        if pokemon['type'] == 'fire':
            fire_count += 1
            if pokemon['level'] and float(pokemon['level']) >= 40:
                fire_level_40_plus += 1
                
    if fire_count == 0:
        return 0
    
    percent = (fire_level_40_plus / fire_count) * 100
    return round(percent)

def fill_missing_types(data):
    weakness_to_types = defaultdict(list)
    for pokemon in data:
        if pokemon['weakness'] and pokemon['type'] != 'NaN':
            weakness_to_types[pokemon['weakness']].append(pokemon['type'])
            
    weakness_common_type = {}
    for weakness, types in weakness_to_types.items():
        type_counts = defaultdict(int)
        for type in types:
            type_counts[type] += 1
        
        max_count = max(type_counts.values(), default = 0)
        common_types = [t for t, count in type_counts.items() if count == max_count]
        
        common_types.sort()
        weakness_common_type[weakness] = common_types[0]
        
    for pokemon in data:
        if pokemon['type'] == 'NaN' and pokemon['weakness'] in weakness_common_type:
            pokemon['type'] = weakness_common_type[pokemon['weakness']]
        
    return data 

def fill_missing_stats(data):
    above_threshold_stats = {'atk': [], 'def': [], 'hp': []}
    below_threshold_stats = {'atk': [], 'def': [], 'hp': []}
    
    for pokemon in data:
        if pokemon['level'] and pokemon['level'] != 'NaN':
            level = float(pokemon['level'])
            
            stats_dict = above_threshold_stats if level > 40 else below_threshold_stats
            
            for stat in ['atk', 'def', 'hp']:
                if pokemon[stat] and pokemon[stat] != 'NaN':
                    stats_dict[stat].append(float(pokemon[stat]))
                    
    above_threshold_avgs = {
        stat: round(sum(values)/len(values), 1) if values else 0 
        for stat, values in above_threshold_stats.items()
    }
    
    below_threshold_avgs = {
        stat: round(sum(values)/len(values), 1) if values else 0 
        for stat, values in below_threshold_stats.items()
    }
    
    for pokemon in data:
        if pokemon['level'] and pokemon['level'] != 'NaN':
            level = float(pokemon['level'])
            avgs = above_threshold_avgs if level > 40 else below_threshold_avgs
            
            for stat in ['atk', 'def', 'hp']:
                if pokemon[stat] == 'NaN':
                    pokemon[stat] = str(avgs[stat])
        
    return data            

def create_type_to_personality_map(data):
    type_to_personality = defaultdict(set)
    
    for pokemon in data:
        if pokemon['type'] and pokemon['type'] != 'NaN' and pokemon['personality'] and pokemon['personality'] != 'NaN':
            type_to_personality[pokemon['type']].add(pokemon['personality'])
    
    result = {
        pokemon_type: sorted(personalities)
        for pokemon_type, personalities in type_to_personality.items()
    }
    
    return result

def calculate_average_hp_for_stage3(data):
    stage3_hp_values = []
    
    for pokemon in data:
        if pokemon['stage'] and pokemon['stage'] != 'NaN' and float(pokemon['stage']) == 3.0:
            if pokemon['hp'] and pokemon['hp'] != 'NaN':
                stage3_hp_values.append(float(pokemon['hp']))
    
    if not stage3_hp_values:
        return 0
    
    average = sum(stage3_hp_values) / len(stage3_hp_values)
    return round(average)

def write_data_to_csv(data, filename):
    if data:
        fieldnames = data[0].keys()
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            

def main():
    data = load_data('pokemonTrain.csv')
    
    percent = calculate(data)
    with open('pokemon1.txt', 'w') as file:
        file.write(f"Percentage of fire type Pokemons at or above level 40 = {percent}")
    
    data = fill_missing_types(data)
    data = fill_missing_stats(data)
    
    write_data_to_csv(data, 'pokemonResult.csv')
    processed_data = load_data('pokemonResult.csv')
    
    type_to_personality = create_type_to_personality_map(processed_data)
    with open('pokemon4.txt', 'w') as file:
        file.write("Pokemon type to personality mapping:\n\n")
        for pokemon_type, personalities in sorted(type_to_personality.items()):
            file.write(f"   {pokemon_type}: {', '.join(personalities)}\n")
            
    avg_hp = calculate_average_hp_for_stage3(processed_data)
    with open('pokemon5.txt', 'w') as file:
        file.write(f"Average hit point for Pokemons of stage 3.0 = {avg_hp}")
        
if __name__ == "__main__":
    main()