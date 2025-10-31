# Cantonese (Yue) Dialect Frontend

This directory contains the Cantonese (Yue) dialect frontend for the DiaMoE-TTS system. The Cantonese frontend uses the [ToJyutping](https://github.com/ToJyutping/ToJyutping) library to convert Chinese text to Jyutping romanization, which is then converted to IPA.

## Features

- **Direct Jyutping Conversion**: Uses ToJyutping library for accurate Cantonese pronunciation
- **Standard 6-Tone System**: Supports Cantonese's 6-tone system (55, 35, 33, 21, 23, 22)
- **IPA Format**: Output matches the Common Voice Cantonese dataset IPA format
- **Simplified Pipeline**: Only requires 3 steps (Chinese → Jyutping → IPA → IPA formatting)

## Installation

The ToJyutping library is automatically installed with the requirements:

```bash
pip install ToJyutping
```

## Usage

### Quick Start

Process a Cantonese text file:

```bash
cd dialect_frontend
bash single_frontend.sh all yue input.txt
```

### Step-by-Step Processing

For Cantonese, the pipeline consists of 3 steps:

```bash
# Step 0: Convert Chinese to Jyutping
bash single_frontend.sh 0 yue input.txt

# Step 5: Convert Jyutping to IPA
bash single_frontend.sh 5 yue input.txt

# Step 6: Format IPA with tone marks
bash single_frontend.sh 6 yue input.txt
```

### Input Format

Input files should be tab-separated with the following format:
```
<utterance_id>	<chinese_text>
```

Example (`example_yue.txt`):
```
utt001	今天天氣很好
utt002	我鍾意學廣東話
utt003	你好嗎
```

### Output Format

After processing, the output will contain IPA representations:

```
utt001	今天天氣很好	k ˈɐmᴴᴴ | tʰ ˈinᴴᴴ | tʰ ˈinᴴᴴ | h ˈeɪ̯ᴹᴹ | h ˈɐnᴹᴴ | h ˈoʊ̯ᴹᴴ
utt002	我鍾意學廣東話	ŋ ˈɔᴸᴴ | t͜s ˈʊŋᴴᴴ | j ˈiᴹᴹ | h ˈɔk̚ᴸᴸ | kʷ ˈɔŋᴹᴴ | t ˈʊŋᴴᴴ | w ˈaᴹᴴ
utt003	你好嗎	n ˈeɪ̯ᴸᴴ | h ˈoʊ̯ᴹᴴ | m ˈaᴴᴴ
```

## IPA Format Details

The Cantonese IPA format follows the Common Voice Cantonese dataset conventions:

### Initials
- Plosives: `p`, `pʰ`, `t`, `tʰ`, `k`, `kʰ`
- Nasals: `m`, `n`, `ŋ`
- Fricatives: `f`, `s`, `h`
- Affricates: `t͜s`, `t͜sʰ` (with tie bar)
- Approximants: `w`, `j`, `l`
- Labialized: `kʷ`, `kʰʷ`
- Null initial: `∅`

### Finals
- Monophthongs: `a`, `ɐ`, `ɛ`, `e`, `i`, `ɪ`, `o`, `ɔ`, `u`, `ʊ`, `œ`, `ɵ`, `y`
- Diphthongs: `aɪ̯`, `ɐɪ̯`, `eɪ̯`, `oʊ̯`, `iʊ̯`, `ɐʊ̯`, etc.
- Nasals: `m`, `n`, `ŋ`
- Unreleased stops: `p̚`, `t̚`, `k̚`
- Syllabic consonants: `m̩`, `ŋ̍`

### Tones
- Tone 1 (55): `ᴴᴴ` - high level
- Tone 2 (35): `ᴹᴴ` - high rising
- Tone 3 (33): `ᴹᴹ` - mid level
- Tone 4 (21): `ᴸᴹ` - low falling
- Tone 5 (23): `ᴸᴴ` - low rising
- Tone 6 (22): `ᴸᴸ` - low level

## Files

- `syllable.xlsx`: Jyutping to IPA syllable mappings (6492 syllables)
- `tone.xlsx`: Tone mark mappings

## Technical Details

### Jyutping to IPA Mapping

The system uses comprehensive mapping tables to convert Jyutping syllables to IPA. The mapping includes:

1. **Initial consonants**: 19 Cantonese initial consonants
2. **Finals**: 53 Cantonese finals (vowels, diphthongs, nasals, stops)
3. **Tones**: 6 tone levels with IPA tone marks

### Processing Pipeline

1. **Text → Jyutping** (`gen_yue_jyutping.py`):
   - Uses ToJyutping library
   - Handles polyphonic characters
   - Preserves punctuation

2. **Jyutping → IPA** (`pinyin2ipa.py`):
   - Maps Jyutping syllables to IPA using `syllable.xlsx`
   - Separates initials and finals
   - Adds tone marks

3. **IPA Formatting** (`ipa_tone.py`):
   - Applies final tone mark formatting
   - Uses `tone.xlsx` for tone mark mapping

## Example

Run the example:
```bash
cd dialect_frontend
bash single_frontend.sh all yue example_yue.txt
cat example_yue_ipa_format.txt
```

## References

- [ToJyutping Library](https://github.com/ToJyutping/ToJyutping)
- [Common Voice Cantonese Dataset](https://commonvoice.mozilla.org/)
- [Jyutping Romanization](https://en.wikipedia.org/wiki/Jyutping)

## Notes

- The Cantonese frontend does not require Steps 1-4 (erhua fixing, character mapping, word mapping, tone sandhi) as it generates Jyutping directly from Chinese text
- The output IPA format is compatible with the Common Voice Cantonese dataset format used by the author
- For best results, ensure input text uses traditional Chinese characters commonly used in Hong Kong Cantonese
