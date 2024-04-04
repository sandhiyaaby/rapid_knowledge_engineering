import json

def json_to_bullet_points(data, indent=0):
    bullet_points = ""
    for key, value in data.items():
        bullet_points += "\t" * indent + "- " + key + "\n"
        if isinstance(value, dict):
            bullet_points += json_to_bullet_points(value, indent + 1)
        elif isinstance(value, list):
            bullet_points += "\t" * (indent + 1) + " Egs: " + ", ".join(value) + "\n"
    return bullet_points

# Example JSON data
json_data = {'Bedroom_Interior_Design': {'Bed_Frames': {'By_Material': ['Wood', 'Metal', 'Upholstered'], 'By_Style': ['Traditional', 'Modern', 'Industrial'], 'By_Function': ['Standard', 'Storage-Enhancing', 'Multi-Functional']}, 'Mattresses_and_Bases': {'By_Material': ['Foam', 'Innerspring', 'Hybrid'], 'By_Support_Level': ['Soft', 'Medium', 'Firm'], 'By_Size': ['Single', 'Double', 'Queen', 'King']}, 'Storage_Solutions': {'Built-in_Storage_Beds': {}, 'Headboards_with_Shelves': {}, 'Modular_Storage_Systems': {}}, 'Textiles': {'Bed_Linen': ['Cotton', 'Linen', 'Silk'], 'Cushions': ['Decorative', 'Functional'], 'Window_Treatments': ['Blackout_Curtains', 'Blinds', 'Sheers'], 'Rugs': ['Area_Rugs', 'Bedside_Rugs']}, 'Lighting': {'Ceiling_Lamps': ['Chandeliers', 'Pendants', 'Flush_Mounts'], 'Reading_Lamps': ['Wall-Mounted', 'Tabletop', 'Floor-Standing'], 'Mood_Lights': ['LED_Strips', 'Bedside_Lamps', 'Projectors']}, 'Color_Schemes': {'By_Psychological_Effect': ['Calming', 'Energizing', 'Grounding']}, 'Sound_Management': {'Sound_Absorbing_Panels': ['Wall-Mounted', 'Ceiling-Mounted']}, 'Plants_and_Nature-Inspired_Decor': {'Live_Plants': ['Low_Light', 'High_Light'], 'Decor': ['Wall_Art', 'Sculptures', 'Bedding_with_Nature_Prints']}, 'Double-Function_Furniture': {'By_Type': ['Sofa_Beds', 'Murphy_Beds', 'Ottoman_Storage']}, 'Comfort_Guides': {'Mattress_Guides': ['By_Sleep_Position', 'Weight', 'Preferred_Comfort'], 'Duvet_and_Pillow_Guides': ['By_Warmth_Rating', 'Material', 'Allergenic_Properties']}}}


# Convert JSON data to bullet points
bullet_points = json_to_bullet_points(json_data)
print(bullet_points)



def extract_json_from_text(text):
    start_index = text.find('{')
    end_index = text.rfind('}') + 1
    if start_index != -1 and end_index != -1:
        json_str = text[start_index:end_index]
        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            return None
    else:
        return None


# Example text containing JSON
text_with_json = '''
bla bla bla dhfhfkh njfkvhkvhkfdv dkjfdhf lorem ipsum whatever 

{ 
"Textiles": {
        "Bedlinens": {
            "Material": ["Cotton", "Linen", "Synthetic"]
        },
        "Curtain": {
            "Material": ["Cotton", "Linen", "Synthetic"],
            "Function": ["Blackout", "Decorative"]
        }
    }
}

djkckdsfckjs jksdnfvjkbfjfk jkdjfcdkvksf
'''

# Extract JSON data from the text
# json_data = extract_json_from_text(text_with_json)
# print(json_data)

