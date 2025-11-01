#!/usr/bin/env python3
"""
Map Cantonese Jyutping to IPA format matching the Common Voice dataset.
This script creates syllable mappings that split components as in the dataset.
"""

import pandas as pd

# Jyutping initials to IPA (following dataset format)
INITIALS_MAP = {
    'b': 'p',
    'p': 'pʰ',
    'm': 'm',
    'f': 'f',
    'd': 't',
    't': 'tʰ',
    'n': 'n',
    'l': 'l',
    'g': 'k',
    'k': 'kʰ',
    'ng': 'ŋ',
    'h': 'h',
    'gw': 'k w',  # Split labialized consonants
    'kw': 'kʰ w',  # Split labialized consonants
    'w': 'w',
    'z': 't͜s',
    'c': 't͜sʰ',
    's': 's',
    'j': 'j',
    '': '∅',
}

# Jyutping finals to IPA components (nucleus + coda, split format)
# Format: final -> (nucleus_ipa, coda_ipa or None)
FINALS_MAP = {
    # Long vowels
    'aa': ('a', None),
    'aai': ('a', 'ɪ̯'),
    'aau': ('a', 'ʊ̯'),
    'aam': ('a', 'm'),
    'aan': ('a', 'n'),
    'aang': ('a', 'ŋ'),
    'aap': ('a', 'p̚'),
    'aat': ('a', 't̚'),
    'aak': ('ă', 'k'),  # Uses a-breve for aak finals
    
    # Mid vowels with /ɐ/
    'ai': ('ɐ', 'ɪ̯'),
    'au': ('ɐ', 'ʊ̯'),
    'am': ('ɐ', 'm'),
    'an': ('ɐ', 'n'),
    'ang': ('ɐ', 'ŋ'),
    'ap': ('ɐ̆', 'p'),  # Uses ɐ-breve, no unreleased marker in output
    'at': ('ɐ̆', 't'),
    'ak': ('ɐ̆', 'k'),
    
    # Front vowels /e, ɛ/
    'e': ('ɛ', None),
    'ei': ('e', 'ɪ̯'),
    'eu': ('ɛ', 'ʊ̯'),
    'em': ('ɛ', 'm'),
    'eng': ('ɛ', 'ŋ'),
    'ep': ('ɛ̆', 'p'),
    'ek': ('e', 'k'),
    
    # High front vowels /i/
    'i': ('i', None),
    'iu': ('i', 'ʊ̯'),
    'im': ('i', 'm'),
    'in': ('i', 'n'),
    'ing': ('ɪ', 'ŋ'),
    'ip': ('ɪ̆', 'p'),
    'it': ('ɪ̆', 't'),
    'ik': ('ɪ̆', 'k'),
    
    # Back vowels /o, ɔ/
    'o': ('ɔ', None),
    'oi': ('ɔ', 'ɪ̯'),
    'ou': ('o', 'ʊ̯'),
    'on': ('ɔ', 'n'),
    'ong': ('ɔ', 'ŋ'),
    'ot': ('ɔ̆', 't'),
    'ok': ('ɔ̆', 'k'),
    
    # High back vowels /u/
    'u': ('u', None),
    'ui': ('u', 'ɪ̯'),
    'un': ('u', 'n'),
    'ung': ('ʊ', 'ŋ'),
    'ut': ('u', 't'),
    'uk': ('ʊ̆', 'k'),
    
    # Rounded front vowels /œ, ɵ/
    'oe': ('œ', None),
    'oeng': ('œ', 'ŋ'),
    'oek': ('œ̆', 'k'),
    'eoi': ('ɞ', 'ʏ̯'),
    'eon': ('ɞ', 'n'),
    'eot': ('ɞ̆', 't'),
    
    # Rounded high front vowels /y/
    'yu': ('y', None),
    'yun': ('y', 'n'),
    'yut': ('y̆', 't'),
    
    # Syllabic consonants
    'm': ('m̩', None),
    'ng': ('ŋ̍', None),
}

# Cantonese tone numbers to IPA tone marks
TONE_MAP = {
    '1': 'ᴴᴴ',  # high level 55
    '2': 'ᴹᴴ',  # high rising 35
    '3': 'ᴹᴹ',  # mid level 33
    '4': 'ᴸᴹ',  # low falling 21
    '5': 'ᴸᴴ',  # low rising 23
    '6': 'ᴸᴸ',  # low level 22
}

def parse_jyutping(jyutping):
    """Parse Jyutping syllable into initial, final, tone."""
    if not jyutping:
        return '', '', ''
    
    # Extract tone
    if jyutping[-1].isdigit():
        tone = jyutping[-1]
        syllable = jyutping[:-1]
    else:
        tone = ''
        syllable = jyutping
    
    # Extract initial
    initial = ''
    final = syllable
    
    # Check double-letter initials first
    if syllable.startswith('ng'):
        initial = 'ng'
        final = syllable[2:]
    elif syllable.startswith('gw'):
        initial = 'gw'
        final = syllable[2:]
    elif syllable.startswith('kw'):
        initial = 'kw'
        final = syllable[2:]
    elif syllable and syllable[0] in 'bpmfdtnlgkhwzcsj':
        initial = syllable[0]
        final = syllable[1:]
    
    # Handle syllabic consonants
    if not final and initial in ['m', 'ng']:
        final = initial
        initial = ''
    
    return initial, final, tone

def jyutping_to_ipa_split(jyutping):
    """
    Convert Jyutping to split IPA format matching dataset.
    Returns list of IPA components.
    """
    initial_jp, final_jp, tone_num = parse_jyutping(jyutping)
    
    # Get IPA components
    initial_ipa = INITIALS_MAP.get(initial_jp, '∅')
    
    if final_jp not in FINALS_MAP:
        # Unknown final, return as-is
        return [initial_ipa if initial_ipa != '∅' else '', f"[UNKNOWN:{jyutping}]"]
    
    nucleus, coda = FINALS_MAP[final_jp]
    tone_mark = TONE_MAP.get(tone_num, '')
    
    # Build IPA components list
    components = []
    
    # Add initial (may be split like "k w")
    if initial_ipa and initial_ipa != '∅':
        components.extend(initial_ipa.split())
    
    # Add nucleus with stress and tone
    if nucleus:
        nucleus_with_tone = f"ˈ{nucleus}{tone_mark}"
        components.append(nucleus_with_tone)
    
    # Add coda if present
    if coda:
        components.append(coda)
    
    return components

def generate_syllable_data():
    """Generate syllable mapping data matching dataset format."""
    rows = []
    
    # Generate mappings for all Jyutping combinations
    for initial_jp, initial_ipa in INITIALS_MAP.items():
        for final_jp, (nucleus, coda) in FINALS_MAP.items():
            # Skip invalid combinations
            if initial_jp == '' and final_jp in ['m', 'ng']:
                jyutping_base = final_jp
            elif final_jp in ['m', 'ng'] and initial_jp != '':
                continue
            else:
                jyutping_base = initial_jp + final_jp
            
            # Generate for each tone
            for tone_num, tone_mark in TONE_MAP.items():
                jyutping = jyutping_base + tone_num
                
                # Get split components
                components = jyutping_to_ipa_split(jyutping)
                
                # Separate into initial and final for pinyin2ipa.py compatibility
                # Format: initial,final (comma-separated)
                if len(components) == 0:
                    initial_part = ""
                    final_part = ""
                elif len(components) == 1:
                    # Just a vowel with tone or syllabic consonant
                    initial_part = ""
                    final_part = components[0]
                else:
                    # Has initial consonant(s) and final
                    # Components can be: [initial(s), vowel+tone, coda?]
                    # or for labialized: [k, w, vowel+tone, coda?]
                    
                    # Find where the stressed vowel starts (marked with ˈ)
                    stress_idx = -1
                    for i, comp in enumerate(components):
                        if 'ˈ' in comp:
                            stress_idx = i
                            break
                    
                    if stress_idx > 0:
                        # Everything before stress mark is initial
                        initial_part = " ".join(components[:stress_idx])
                        # Everything from stress mark onward is final
                        final_part = " ".join(components[stress_idx:])
                    else:
                        # No stress mark found (shouldn't happen), treat first as initial
                        initial_part = components[0] if len(components) > 1 else ""
                        final_part = " ".join(components[1:]) if len(components) > 1 else components[0]
                
                rows.append({
                    'pinyin': jyutping,
                    'initial': initial_part,
                    'final': final_part,
                })
    
    df = pd.DataFrame(rows)
    return df

def generate_tone_data():
    """Generate tone mark mapping."""
    rows = []
    for contour, mark in TONE_MAP.items():
        rows.append({
            'contour': contour,
            'mark': mark,
        })
    df = pd.DataFrame(rows)
    return df

def main():
    """Main function to generate Cantonese data files."""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Output to cantonese directory (not yue)
    output_dir = os.path.join(script_dir, 'frontend/dialect/cantonese')
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating Cantonese syllable data (dataset format)...")
    syllable_df = generate_syllable_data()
    syllable_path = f'{output_dir}/syllable.xlsx'
    syllable_df.to_excel(syllable_path, index=False)
    print(f"✓ Created {syllable_path} with {len(syllable_df)} syllables")
    
    print("\nGenerating Cantonese tone data...")
    tone_df = generate_tone_data()
    tone_path = f'{output_dir}/tone.xlsx'
    tone_df.to_excel(tone_path, index=False)
    print(f"✓ Created {tone_path} with {len(tone_df)} tone mappings")
    
    # Show samples
    print("\n--- Sample syllable mappings (pinyin2ipa format) ---")
    print(syllable_df.head(15))
    
    # Test with actual examples
    print("\n--- Testing with dataset examples ---")
    test_cases = [
        ('gwai2', 'k w', 'ˈɐᴹᴴ ɪ̯'),
        ('nei5', 'n', 'ˈeᴸᴴ ɪ̯'),
        ('hou2', 'h', 'ˈoʊ̯ᴹᴴ'),
        ('mat1', 'm', 'ˈɐ̆ᴴᴴ t'),
    ]
    
    for jyutping, exp_init, exp_final in test_cases:
        row = syllable_df[syllable_df['pinyin'] == jyutping]
        if len(row) > 0:
            actual_init = row.iloc[0]['initial']
            actual_final = row.iloc[0]['final']
            init_match = "✓" if actual_init == exp_init else "✗"
            final_match = "✓" if actual_final == exp_final else "✗"
            print(f"{init_match}{final_match} {jyutping}: [{actual_init}] , [{actual_final}]")
            if actual_init != exp_init or actual_final != exp_final:
                print(f"    Expected: [{exp_init}] , [{exp_final}]")
        else:
            print(f"✗ {jyutping}: NOT FOUND")

if __name__ == '__main__':
    main()
