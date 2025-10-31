#!/usr/bin/env python3
"""
Generate Cantonese Jyutping from Chinese text using ToJyutping library.
This script converts Chinese text to Jyutping romanization for Cantonese dialect.
"""

import argparse
from tqdm import tqdm
from ToJyutping import get_jyutping_list

def replace_english_punctuation_with_chinese(text):
    """Replace English punctuation with Chinese equivalents."""
    en_to_zh_punct = {
        ",": "，",
        ".": "。",
        "?": "？",
        "!": "！",
        ":": "：",
        ";": "；",
        "(": "（",
        ")": "）",
        "[": "【",
        "]": "】",
    }
    
    for en, zh in en_to_zh_punct.items():
        text = text.replace(en, zh)
    return text

def text_to_jyutping(text):
    """
    Convert Chinese text to Jyutping.
    
    Args:
        text: Input Chinese text
        
    Returns:
        Jyutping string with space-separated syllables
    """
    # Get jyutping for each character
    jyutping_list = get_jyutping_list(text)
    
    result = []
    for char, jyutping in jyutping_list:
        # If it's punctuation or special character, keep it as is
        if not jyutping or jyutping == char:
            result.append(char)
        else:
            result.append(jyutping)
    
    return " ".join(result)

def get_yue_jyutping(infile, outfile):
    """
    Process input file and generate Jyutping output.
    
    Args:
        infile: Input file path with format: <id>\\t<text>
        outfile: Output file path with format: <id>\\t<text>\\t<jyutping>
    """
    print(f"Processing Cantonese text from {infile}...")
    
    with open(infile, "r", encoding="utf-8") as fr, open(outfile, "w", encoding="utf-8") as fw:
        for line in tqdm(fr.readlines()):
            line = line.strip()
            if not line:
                continue
            
            # Parse input line
            line_list = line.split("\t")
            if len(line_list) < 2:
                print(f"Warning: Skipping malformed line: {line}")
                continue
            
            idx = line_list[0]
            text = line_list[1]
            
            # Normalize punctuation
            text_normalized = replace_english_punctuation_with_chinese(text)
            
            # Convert to Jyutping
            jyutping = text_to_jyutping(text_normalized)
            jyutping = replace_english_punctuation_with_chinese(jyutping)
            
            # Write output
            fw.write(f"{idx}\t{text_normalized}\t{jyutping}\n")
    
    print(f"✓ Jyutping conversion completed! Output saved to {outfile}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Convert Chinese text to Cantonese Jyutping")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file with format: <id>\\t<text>")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file with Jyutping")
    
    args = parser.parse_args()
    get_yue_jyutping(args.input, args.output)

if __name__ == "__main__":
    main()
