#!/bin/bash
set -e

# Usage example: bash single_frontend.sh 1-6 shijiazhuang example.txt


if [ $# -lt 3 ]; then
  echo "Usage: $0 <step_list, e.g. 1-6 or all or 2 4 6> <dialect_name> <inputTXT>"
  exit 1
fi

# Valid dialect list
allowed_dialects=("xian" "shijiazhuang" "putonghua" "chengdu" "zhengzhou" "gaoxiong" "qingdao" "jingjujingbai" "jingjuyunbai" "nanjing" "wuhan" "shanghai" "yue")

# Extract parameters
dialect="${@: -2:1}"
input_path="${@: -1}"
step_args=("${@:1:$#-2}")
path_no_ext="${input_path%.txt}"
# Check if dialect is valid
if [[ ! " ${allowed_dialects[@]} " =~ " ${dialect} " ]]; then
  echo "Error: Unsupported dialect '${dialect}'. Currently supported: ${allowed_dialects[*]}"
  exit 1
fi

# Parse step list
if [ "${step_args[0]}" == "all" ]; then
  if [ "$dialect" == "yue" ]; then
    steps=(0 5 6)  # Cantonese uses simplified pipeline
  else
    steps=(1 2 3 4 5 6)
  fi
elif [[ "${step_args[0]}" =~ ^[0-9]+-[0-9]+$ ]]; then
  IFS='-' read start end <<< "${step_args[0]}"
  steps=($(seq $start $end))
else
  steps=("${step_args[@]}")
fi

echo "Preparing to process frontend for ${dialect} dialect."

# Execute steps sequentially
for step in "${steps[@]}"; do

  if [ "$step" -eq 0 ]; then
    # Step 0: Generate Jyutping for Cantonese (yue only)
    echo "===== Convert Chinese to Cantonese Jyutping ====="
    if [ "$dialect" != "yue" ]; then
      echo "Skip this step: Step 0 is only for Cantonese (yue)"
      continue
    fi
    python gen_yue_jyutping.py --input ${input_path} \
                               --output ${path_no_ext}_jyutping.txt

  elif [ "$step" -eq 1 ]; then
    # Step 1 script and parameters
    echo "===== Fix erhua in Mandarin frontend ====="
    if [ "$dialect" == "putonghua" ] || [ "$dialect" == "yue" ]; then
      echo "Skip this step: ${dialect} does not need this step"
      continue
    fi
    python fix_erhua.py --input ${input_path} \
                        --output ${path_no_ext}_fix_pinyin.txt

  elif [ "$step" -eq 2 ]; then
    # Step 2 script and parameters
    echo "===== Map Chinese characters to dialect pinyin ====="
    if [ "$dialect" == "putonghua" ] || [ "$dialect" == "yue" ]; then
      echo "Skip this step: ${dialect} does not need this step"
      continue
    fi
    python hanzi2dialect_pinyin.py --input ${path_no_ext}_fix_pinyin.txt \
                                   --output ${path_no_ext}_hanzi.txt \
                                   --dialect ${dialect}

  elif [ "$step" -eq 3 ]; then
    # Step 3 script and parameters
    echo "===== Supplement word mapping to dialect pinyin ====="
    if [ "$dialect" == "yue" ]; then
      echo "Skip this step: ${dialect} does not need this step"
      continue
    fi
    python word2dialect_pinyin.py --input ${path_no_ext}_hanzi.txt \
                                  --output ${path_no_ext}_word.txt \
                                  --dialect ${dialect}

  elif [ "$step" -eq 4 ]; then
    # Step 4 script and parameters
    echo "===== Tone sandhi ====="
    if [ "$dialect" == "yue" ]; then
      echo "Skip this step: ${dialect} does not need this step"
      continue
    fi
    python liandu_tone.py --input ${path_no_ext}_word.txt \
                          --output ${path_no_ext}_liandutone.txt \
                          --dialect ${dialect}

  elif [ "$step" -eq 5 ]; then
    # Step 5 script and parameters
    echo "===== Pinyin to IPA ====="
    if [ "$dialect" == "yue" ]; then
      # For Cantonese, use jyutping output from step 0
      python pinyin2ipa.py --input ${path_no_ext}_jyutping.txt \
                           --output ${path_no_ext}_ipa1.txt \
                           --dialect ${dialect}
    else
      python pinyin2ipa.py --input ${path_no_ext}_liandutone.txt \
                           --output ${path_no_ext}_ipa1.txt \
                           --dialect ${dialect}
    fi

  elif [ "$step" -eq 6 ]; then
    # Step 6 script and parameters
    echo "===== IPA tone symbol mapping ====="
    python ipa_tone.py --input ${path_no_ext}_ipa1.txt \
                       --output ${path_no_ext}_ipa_format.txt \
                       --dialect ${dialect}

  else
    echo "Unknown step number: $step"
    exit 1
  fi

done

echo "===== Frontend task completed! ====="