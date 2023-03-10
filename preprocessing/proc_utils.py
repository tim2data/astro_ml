import pandas as pd

PLANETS_LIST = ['neptune', 'pluto']
HOUSES_LIST = ['AC', '2', '3', 'IC', '5', '6', 'DC', '8', '9', 'MC', '11', '12']
SIGNS_LIST = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def convert_to_int(df, series_id):
    if df[series_id].dtype == int:
        print("The series is already of integer type.")
    else:
        df[series_id] = df[series_id].astype(int)
        
# define the preprocessing pipeline
def preprocess_data(df):
    # drop rows with NaN in birth_time column
    df.dropna(subset=['sun_sign'], inplace=True)
    df.dropna(subset=['birth_time'], inplace=True)
    df.dropna(subset=['neptune_house'], inplace=True)
    
    convert_to_int(df, 'birth_year')
    
    cols_to_replace = ['uranus_retrograde', 'jupiter_retrograde', 'pluto_retrograde', 'mercury_retrograde', 'saturn_retrograde', 'venus_retrograde', 'mars_retrograde']
    df[cols_to_replace] = df[cols_to_replace].fillna(False)

    
    for planet in PLANETS_LIST:
        convert_to_int(df, f"{planet}_house")
        convert_to_int(df, f"{planet}_pos_degrees")
        convert_to_int(df, f"{planet}_pos_minutes")
        
    for house in HOUSES_LIST:
        convert_to_int(df, f"house_{house}_pos_degrees")
        convert_to_int(df, f"house_{house}_pos_minutes")

    return df

def get_sign_pos(series):
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return series.apply(lambda x: zodiac_signs.index(x)) 
    

def add_absolute_positions(df):
    for planet in PLANETS_LIST:
        df[f"{planet}_absolute_pos"] = get_sign_pos(df[f"{planet}_sign"])*30 + df[f"{planet}_pos_degrees"] + round(df[f"{planet}_pos_minutes"]/60, 2)
    
    return df

def add_aspects(df):
    aspects = [0, 60, 90, 120, 180]
    # take each planet and then list the other planets and look for degrees?
    # 120.43	248.67
    # we want to know if the absolute difference between them divided
    for planet in PLANETS_LIST:
        for other_planet in PLANETS_LIST:
            if (planet !== other_planet):
                angle = abs(df[f"{planet}_absolute_pos"] - df[f"{other_planet}_absolute_pos"])
                
                df[f"{planet}_{other_planet}"] = 'no'
                
                for aspect in aspects:
                    if abs(angle - aspect) <= 5:
                        df[f"{planet}_{other_planet}"] = 'yes'
                        
    return df
            
    