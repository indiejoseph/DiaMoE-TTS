import pdb
import argparse
import pandas as pd
import re

def load_pinyin_to_ipa_dict(excel_path):
    df = pd.read_excel(excel_path)
    p2i_dict = {}
    for _, row in df.iterrows():
        pinyin = str(row["pinyin"]).strip()
        initial = "" if pd.isna(row["initial"]) else str(row["initial"]).strip()
        final = "" if pd.isna(row["final"]) else str(row["final"]).strip()
        p2i_dict[pinyin] = f"{initial},{final}"
    return p2i_dict


def convert_pinyin_to_ipa(pinyin_units, p2i_dict, unmatched_set):
    result = []
    for item in pinyin_units:
        base = item.strip("#")
        if base not in p2i_dict:
            unmatched_set.add(base)
        ipa = p2i_dict.get(base, base)
        result.append(ipa)
    return result



def replace_english_punctuation(text):
    english_to_chinese_punct = {
        ",": "，",
        ".": "。",
        "?": "？",
        "!": "！",
        ":": "：",
        ";": "；",
        "\"": "\"",
        "'": "'",
        "[": "【",
        "]": "】",
        "(": "（",
        ")": "）"
    }
    for en, zh in english_to_chinese_punct.items():
        text = text.replace(en, zh)
    return text


def format_ipa_output(ipa_units):
    # Each ipa unit is "initial,final" where initial and final may have internal spaces
    # We need to:
    # 1. Replace comma with space (to combine initial and final)
    # 2. Add " | " between syllables (between ipa_units)
    
    formatted_syllables = []
    for unit in ipa_units:
        # Replace comma with space to join initial and final
        syllable = unit.replace(",", " ").strip()
        # Clean up any double spaces
        while "  " in syllable:
            syllable = syllable.replace("  ", " ")
        formatted_syllables.append(syllable)
    
    # Join syllables with " | "
    return " | ".join(formatted_syllables)


def process_file_to_ipa(input_path, output_path, excel_path):
    p2i_dict = load_pinyin_to_ipa_dict(excel_path)
    unmatched_set = set()

    log_path = output_path + ".log"

    with open(input_path, "r", encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout, \
         open(log_path, "w", encoding="utf-8") as flog:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            try:
                index, text, pinyin_line = line.split("\t")
            except ValueError:
                msg = f"[Format error] Skip line: {line}"
                print(msg)
                flog.write(msg + "\n")
                continue

            text = replace_english_punctuation(text).replace("#", "")
            pinyin_line = replace_english_punctuation(pinyin_line)

            pinyin_units = pinyin_line.strip().split()
            ipa_units = convert_pinyin_to_ipa(pinyin_units, p2i_dict, unmatched_set)
            formatted_ipa = format_ipa_output(ipa_units)
            fout.write(f"{index}\t{text}\t{formatted_ipa}\n")

        # Write log of unmatched pinyin items
        if unmatched_set:
            flog.write("\n[Summary of pinyin mapping items not found]:\n")
            for item in sorted(unmatched_set):
                flog.write(f"  - {item}\n")



# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="input data.list")
    parser.add_argument("-o", "--output", type=str, help="generate data_pinyin.list")
    parser.add_argument("-d", "--dialect", type=str, help="which dialect")
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    dialect = args.dialect
    # Example paths:
    # input_path = f"./output/{dialect}_liandutone.txt"
    # output_path = f"./output/{dialect}_ipa1.txt"


    if dialect == 'putonghua':
        excel_path = f"frontend/dialect/{dialect}/base_syllable.xlsx"              # Pinyin to IPA mapping table
    else:
        excel_path = f"frontend/dialect/{dialect}/syllable.xlsx"
    process_file_to_ipa(input_path, output_path, excel_path)
