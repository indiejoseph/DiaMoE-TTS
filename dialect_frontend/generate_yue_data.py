#!/usr/bin/env python3
"""
Generate Cantonese (Yue) syllable and tone mapping files for IPA conversion.
This script creates the necessary Excel files for the Cantonese dialect pipeline.
Based on the author's Common Voice Cantonese dataset IPA format.
"""

import pandas as pd

# Cantonese Jyutping initials to IPA mapping (matching author's dataset)
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
    'gw': 'kʷ',
    'kw': 'kʰʷ',
    'w': 'w',
    'z': 't͜s',  # Using tie bar as in author's dataset
    'c': 't͜sʰ',
    's': 's',
    'j': 'j',
    '': '∅',  # null initial
}

# Cantonese Jyutping finals to IPA mapping (matching author's dataset format)
FINALS_MAP = {
    'aa': 'a',       # long a
    'aai': 'aɪ̯',
    'aau': 'aʊ̯',
    'aam': 'am',
    'aan': 'an',
    'aang': 'aŋ',
    'aap': 'ap̚',
    'aat': 'at̚',
    'aak': 'ak̚',
    'ai': 'ɐɪ̯',
    'au': 'ɐʊ̯',
    'am': 'ɐm',
    'an': 'ɐn',
    'ang': 'ɐŋ',
    'ap': 'ɐp̚',
    'at': 'ɐt̚',
    'ak': 'ɐk̚',
    'e': 'ɛ',
    'ei': 'eɪ̯',
    'eu': 'ɛʊ̯',
    'em': 'ɛm',
    'eng': 'ɛŋ',
    'ep': 'ɛp̚',
    'ek': 'ɛk̚',
    'i': 'i',
    'iu': 'iʊ̯',
    'im': 'im',
    'in': 'in',
    'ing': 'ɪŋ',
    'ip': 'ip̚',
    'it': 'it̚',
    'ik': 'ɪk̚',
    'o': 'ɔ',
    'oi': 'ɔɪ̯',
    'ou': 'oʊ̯',
    'on': 'ɔn',
    'ong': 'ɔŋ',
    'ot': 'ɔt̚',
    'ok': 'ɔk̚',
    'u': 'u',
    'ui': 'uɪ̯',
    'un': 'un',
    'ung': 'ʊŋ',
    'ut': 'ut̚',
    'uk': 'ʊk̚',
    'oe': 'œ',
    'oeng': 'œŋ',
    'oek': 'œk̚',
    'eoi': 'ɵy̯',
    'eon': 'ɵn',
    'eot': 'ɵt̚',
    'yu': 'y',
    'yun': 'yn',
    'yut': 'yt̚',
    'm': 'm̩',
    'ng': 'ŋ̍',
}

# Cantonese tone contours (standard 6-tone system)
TONE_MAP = {
    '1': 'ᴴᴴ',  # high level 55
    '2': 'ᴹᴴ',  # high rising 35
    '3': 'ᴹᴹ',  # mid level 33
    '4': 'ᴸᴹ',  # low falling 21
    '5': 'ᴸᴴ',  # low rising 23
    '6': 'ᴸᴸ',  # low level 22
}

def get_jyutping_components(jyutping):
    """
    Parse a Jyutping syllable into initial, final, and tone.
    Returns: (initial, final, tone)
    """
    if not jyutping:
        return '', '', ''
    
    # Extract tone number (last character)
    if jyutping[-1].isdigit():
        tone = jyutping[-1]
        syllable = jyutping[:-1]
    else:
        tone = ''
        syllable = jyutping
    
    # Check for double-letter initials first
    initial = ''
    final = syllable
    
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

def generate_syllable_data():
    """Generate syllable mapping data for Cantonese."""
    rows = []
    
    # Generate all possible Jyutping combinations
    for initial_jp, initial_ipa in INITIALS_MAP.items():
        for final_jp, final_ipa in FINALS_MAP.items():
            # Skip invalid combinations
            if initial_jp == '' and final_jp in ['m', 'ng']:
                # Syllabic consonants
                jyutping_base = final_jp
            elif final_jp in ['m', 'ng'] and initial_jp != '':
                # m and ng can only be syllabic (no initial)
                continue
            else:
                jyutping_base = initial_jp + final_jp
            
            # Generate for each tone
            for tone_num, tone_mark in TONE_MAP.items():
                jyutping = jyutping_base + tone_num
                
                # Build IPA representation matching author's format
                if initial_jp == '':
                    initial_part = '∅'
                else:
                    initial_part = initial_ipa
                
                # Add stress mark and tone to final (format: ˈvowel+tone)
                final_with_tone = f'ˈ{final_ipa}{tone_mark}'
                
                rows.append({
                    'pinyin': jyutping,
                    'initial': initial_part,
                    'final': final_with_tone,
                })
    
    df = pd.DataFrame(rows)
    return df

def generate_tone_data():
    """Generate tone mark mapping (already in superscript format)."""
    # For author's format, tones are already in the final IPA form
    # So we create an identity mapping
    rows = []
    tone_marks = ['ᴴᴴ', 'ᴹᴴ', 'ᴹᴹ', 'ᴸᴹ', 'ᴸᴴ', 'ᴸᴸ']
    for mark in tone_marks:
        rows.append({
            'contour': mark,
            'mark': mark,
        })
    df = pd.DataFrame(rows)
    return df

def main():
    """Main function to generate Cantonese data files."""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'frontend/dialect/yue')
    
    print("Generating Cantonese syllable data...")
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
    print("\n--- Sample syllable mappings ---")
    print(syllable_df.head(10))
    print("\n--- Tone mappings ---")
    print(tone_df)

if __name__ == '__main__':
    main()
