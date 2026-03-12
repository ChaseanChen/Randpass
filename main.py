# Generate random password
randpass() {
    local c_info="\033[1;34m"    # Info - blue
    local c_succ="\033[1;32m"    # Success - green
    local c_err="\033[1;31m"     # Error - red
    local c_warn="\033[1;33m"    # Warning - yellow
    local c_reset="\033[0m"      # Reset color

    echo "${c_info}[INFO] Generating random passwords...${c_reset}"
    
    local pass
    if ! pass=$(python3 -c "import string, secrets, random; charset=''.join(c for c in string.ascii_letters+string.digits if c not in 'l10oO'); chars=[secrets.choice(charset) for _ in range(12)]+[secrets.choice(string.ascii_lowercase),secrets.choice(string.ascii_uppercase),secrets.choice(string.digits),secrets.choice('23456789')]; random.SystemRandom().shuffle(chars); print(''.join(chars))" 2>/dev/null); then
        echo "${c_err}[ERROR] Password generation failed! Please check if Python is installed on your system.${c_reset}" >&2
        return 1
    fi
    
    if [[ -z "$pass" ]]; then
        echo "${c_err}[ERROR] Password generation error, empty result!${c_reset}" >&2
        return 1
    fi
    
    echo "${c_succ}[SUCCESS] Password generated.${c_reset}"
    printf "Password is : ${c_succ}%s${c_reset}\n\n" "$pass"

    if [[ -n "$1" ]]; then
        local file_name="$1"
        local save_path="${2:-$HOME/Documents}"
        
        save_path="${save_path%/}"
        local full_file_path="$save_path/${file_name}.txt"
        
        echo "${c_info}[INFO] Received file save command.${c_reset}"
        echo "${c_info}[INFO] Target file name : ${file_name}.txt${c_reset}"
        echo "${c_info}[INFO] Target directory : ${save_path}${c_reset}"
        
        if [[ ! -d "$save_path" ]]; then
            echo "${c_info}[INFO] The directory does not exist; attempting to create it...${c_reset}"
            if ! { mkdir -p "$save_path"; } 2>/dev/null; then
                echo "${c_err}[ERROR] Directory creation failed! Please check if the path is valid or if you have sufficient permissions (${save_path}).${c_reset}" >&2
                return 1
            fi
            echo "${c_succ}[SUCCESS] The directory was created successfully.${c_reset}"
        fi
        
        echo "${c_info}[INFO] Appending password to file...${c_reset}"
        
        if [[ ! -f "$full_file_path" ]]; then
            touch "$full_file_path" 2>/dev/null
            chmod 600 "$full_file_path" 2>/dev/null
        fi
        
        local current_time=$(date "+%Y-%m-%d %H:%M:%S")
        if ! { printf "[%s] %s\n" "$current_time" "$pass" >> "$full_file_path"; } 2>/dev/null; then
            echo "${c_err}[ERROR] Failed to write to file! Please check file read/write permissions or disk space (${full_file_path}).${c_reset}" >&2
            return 1
        fi
        
        chmod 600 "$full_file_path" 2>/dev/null
        
        echo "${c_succ}[SUCCESS] The password has been securely saved to : ${full_file_path}${c_reset}"
    else
        echo "${c_warn}[WARN] No filename specified. The generated password will not be saved to any file.${c_reset}"
    fi
}