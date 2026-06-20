from typing import Dict

STAT_NAME_TO_KEY: Dict[str, str] = {
    'Bullet resistance': 'bullet_resistance',
    'Vitality': 'vitality',
    'Healing efficiency': 'healing_efficiency',
    'Health regeneration': 'health_regeneration',
    'Movement speed': 'movement_speed',
    'Carry weight': 'carry_weight',
    'Stamina recovery': 'stamina_recovery',
    'Bleeding protection': 'bleeding_protection',
    'Rupture protection': 'rupture_protection',
    'Explosion protection': 'explosion_protection',
    'Fire protection': 'fire_protection',
    'Electro protection': 'electro_protection',
    'Chemical protection': 'chemical_protection',
    'Radiation protection': 'radiation_protection',
    'Temperature protection': 'temperature_protection',
    'Bio protection': 'bio_protection',
    'Psi protection': 'psi_protection',
    'Healing per second': 'healing_per_second',
    'Stamina': 'stamina',
    'Burn reaction': 'burn_reaction',
    'Rupture reaction': 'rupture_reaction',
    'Radiation': 'radiation',
    'Temperature': 'temperature',
    'Biological infection': 'biological_infection',
    'Psy-emissions': 'psi',
    'Frost': 'cold',
    'Bleeding': 'bleeding',
    'Burning': 'burning',
}


def stat_key(display_name: str) -> str:
    return STAT_NAME_TO_KEY.get(display_name, display_name.lower().replace(' ', '_'))
