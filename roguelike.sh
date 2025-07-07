#!/bin/bash

# Game settings
ROWS=30
COLS=50
WALL_PROB=25  # percent chance of a wall
MAP=()
PLAYER_X=1
PLAYER_Y=1
PLAYER_HP=100
PLAYER_MAX_HP=100
PLAYER_ATTACK=10
PLAYER_ARMOR=10
PLAYER_LEVEL=1
PLAYER_EXP=0
EXIT_X=0
EXIT_Y=0
DUNGEON_LEVEL=1
GAME_OVER=0

# Colors
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
PURPLE='\033[35m'
CYAN='\033[36m'
WHITE='\033[37m'
RESET='\033[0m'

# Enemy types
declare -A ENEMIES=(
    ["G"]="Goblin:15:3:20:5"
    ["O"]="Orc:30:8:50:10"
    ["S"]="Skeleton:10:5:15:3"
    ["Z"]="Zombie:25:4:30:7"
    ["D"]="Demon:50:15:100:25"
)

# Items
declare -A ITEMS=(
    ["h"]="Health Potion:restore 30 HP"
    ["H"]="Greater Health Potion:restore 60 HP"
    ["w"]="Weak Weapon:increase attack by 2"
    ["W"]="Strong Weapon:increase attack by 5"
    ["a"]="Weak Armor:increase max HP by 10"
    ["A"]="Strong Armor:increase max HP by 25"
)

# Generate random map
generate_map() {
    # Initialize all walls
    for ((y=0; y<ROWS; y++)); do
        row=""
        for ((x=0; x<COLS; x++)); do
            row+="#"
        done
        MAP[y]=$row
    done

    carve_maze_recursive() {
        local x=$1
        local y=$2
        set_tile $x $y " "

        directions=(0 1 2 3)
        # Shuffle directions
        for ((i=0; i<4; i++)); do
            j=$((RANDOM % 4))
            tmp=${directions[i]}
            directions[i]=${directions[j]}
            directions[j]=$tmp
        done

        for dir in "${directions[@]}"; do
            case $dir in
                0) dx=0; dy=-1 ;; # Up
                1) dx=0; dy=1  ;; # Down
                2) dx=-1; dy=0 ;; # Left
                3) dx=1; dy=0  ;; # Right
            esac

            nx=$((x + dx * 2))
            ny=$((y + dy * 2))

            if (( nx > 0 && nx < COLS - 1 && ny > 0 && ny < ROWS - 1 )); then
                if [[ "$(get_tile $nx $ny)" == "#" ]]; then
                    set_tile $((x + dx)) $((y + dy)) " "
                    carve_maze_recursive $nx $ny
                fi
            fi
        done
    }

    # Start carving from player start
    PLAYER_X=1
    PLAYER_Y=1
    carve_maze_recursive $PLAYER_X $PLAYER_Y

    # Now find a far away tile for the exit
    local max_dist=0
    for ((y=0; y<ROWS; y++)); do
        for ((x=0; x<COLS; x++)); do
            if [[ "$(get_tile $x $y)" == " " ]]; then
                dist=$(( (x - PLAYER_X)**2 + (y - PLAYER_Y)**2 ))
                if (( dist > max_dist )); then
                    EXIT_X=$x
                    EXIT_Y=$y
                    max_dist=$dist
                fi
            fi
        done
    done
    set_tile $EXIT_X $EXIT_Y "E"

    # Sprinkle enemies/items
    for ((y=0; y<ROWS; y++)); do
        for ((x=0; x<COLS; x++)); do
            tile=$(get_tile $x $y)
            if [[ "$tile" == " " && $((RANDOM % 100)) -lt 6 ]]; then
                if (( RANDOM % 2 == 0 )); then
                    keys=("${!ENEMIES[@]}")
                    set_tile $x $y "${keys[RANDOM % ${#keys[@]}]}"
                else
                    keys=("${!ITEMS[@]}")
                    set_tile $x $y "${keys[RANDOM % ${#keys[@]}]}"
                fi
            fi
        done
    done
}


has_path_to_exit() {
    local start_x=$PLAYER_X
    local start_y=$PLAYER_Y
    local target_x=$EXIT_X
    local target_y=$EXIT_Y

    declare -A visited
    queue=()
    queue+=("$start_x,$start_y")
    visited["$start_x,$start_y"]=1

    while ((${#queue[@]} > 0)); do
        IFS=',' read -r x y <<< "${queue[0]}"
        queue=("${queue[@]:1}")

        if (( x == target_x && y == target_y )); then
            return 0  # path found
        fi

        for dx in -1 1 0 0; do
            for dy in 0 0 -1 1; do
                nx=$((x + dx))
                ny=$((y + dy))

                if (( nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS )); then
                    tile=$(get_tile $nx $ny)
                    if [[ "$tile" != "#" && -z "${visited["$nx,$ny"]}" ]]; then
                        visited["$nx,$ny"]=1
                        queue+=("$nx,$ny")
                    fi
                fi
            done
        done
    done

    return 1  # no path
}

generate_valid_map() {
    while true; do
        generate_map
        if has_path_to_exit; then
            break
        fi
    done
}


# Get tile at position
get_tile() {
    local x=$1
    local y=$2
    echo "${MAP[y]:x:1}"
}

# Set tile at position
set_tile() {
    local x=$1
    local y=$2
    local val=$3
    row="${MAP[y]}"
    MAP[y]="${row:0:x}${val}${row:x+1}"
}

# Render map
draw_map() {
    clear
    echo -e "${YELLOW}=== Dungeon Bash ===${RESET}"
    echo -e "Level: ${DUNGEON_LEVEL}  HP: ${RED}$PLAYER_HP/$PLAYER_MAX_HP${RESET}  ATK: $PLAYER_ATTACK  ARM: $PLAYER_ARMOR  LVL: $PLAYER_LEVEL  EXP: $PLAYER_EXP/$((PLAYER_LEVEL * 100))"
    
    for ((y=0; y<ROWS; y++)); do
        for ((x=0; x<COLS; x++)); do
            if [[ $x -eq $PLAYER_X && $y -eq $PLAYER_Y ]]; then
                echo -ne "${GREEN}@${RESET}"
            else
                tile="${MAP[y]:x:1}"
                case $tile in
                    "#") echo -ne "${WHITE}█${RESET}" ;;
                    "E") echo -ne "${YELLOW}E${RESET}" ;;
                    "G"|"O"|"S"|"Z"|"D") echo -ne "${RED}$tile${RESET}" ;;
                    "h"|"H"|"w"|"W"|"a"|"A") echo -ne "${BLUE}$tile${RESET}" ;;
                    *) echo -n "$tile" ;;
                esac
            fi
        done
        echo
    done
    
    echo -e "Controls: ${CYAN}WASD${RESET} to move, ${CYAN}Q${RESET} to quit"
    echo -e "Legend: ${GREEN}@${RESET} You, ${RED}G,O,S,Z,D${RESET} Enemies, ${BLUE}h,H,w,W,a,A${RESET} Items, ${YELLOW}E${RESET} Exit"
    
    if [[ -n "$MESSAGE" ]]; then
        echo -e "$MESSAGE"
        MESSAGE=""
    fi
}


fight_enemy() {
    local enemy_type=$1
    local enemy_data=${ENEMIES[$enemy_type]}
    IFS=':' read -r enemy_name enemy_hp enemy_atk enemy_exp enemy_gold <<< "$enemy_data"
    
    MESSAGE="You encounter a $enemy_name! (HP: $enemy_hp, ATK: $enemy_atk)"
    draw_map
    sleep 1
    
    while (( PLAYER_HP > 0 && enemy_hp > 0 )); do
        # Player attacks enemy
        base_damage=$(( (RANDOM % PLAYER_ATTACK) + 1 ))
        bonus_damage=$(( PLAYER_ATTACK / 10 ))  # 10% bonus of attack
        damage=$(( base_damage + bonus_damage ))
        enemy_hp=$(( enemy_hp - damage ))
        MESSAGE="You hit the $enemy_name for $damage damage! (Base: $base_damage + Bonus: $bonus_damage)"
        draw_map
        sleep 5  # pause after player attack
        
        if (( enemy_hp <= 0 )); then
            MESSAGE="You defeated the $enemy_name! Gained ${enemy_exp} EXP."
            PLAYER_EXP=$((PLAYER_EXP + enemy_exp))
            check_level_up
            return 0
        fi
        
        # Enemy attacks player (reduce damage by 10% of player's armor)
        raw_damage=$(( (RANDOM % enemy_atk) + 1 ))
        armor_reduction=$(( PLAYER_ARMOR / 10 ))  # 10% of armor
        damage=$(( raw_damage - armor_reduction ))
        if (( damage < 0 )); then
            damage=0
        fi
        
        PLAYER_HP=$(( PLAYER_HP - damage ))
        MESSAGE="$enemy_name hits you for $damage damage! (Reduced from $raw_damage by $armor_reduction due to armor)"
        draw_map
        sleep 5  # pause after enemy attack
        
        if (( PLAYER_HP <= 0 )); then
            MESSAGE="${RED}You have been slain by the $enemy_name! Game Over.${RESET}"
            GAME_OVER=1
            return 1
        fi
    done
}


# Use item
use_item() {
    local item_type=$1
    local item_data=${ITEMS[$item_type]}
    IFS=':' read -r item_name effect <<< "$item_data"
    
    case $item_type in
        "h") 
            PLAYER_HP=$((PLAYER_HP + 30))
            if (( PLAYER_HP > PLAYER_MAX_HP )); then
                PLAYER_HP=$PLAYER_MAX_HP
            fi
            MESSAGE="${GREEN}You used a $item_name and restored 30 HP!${RESET}"
            ;;
        "H")
            PLAYER_HP=$((PLAYER_HP + 60))
            if (( PLAYER_HP > PLAYER_MAX_HP )); then
                PLAYER_HP=$PLAYER_MAX_HP
            fi
            MESSAGE="${GREEN}You used a $item_name and restored 60 HP!${RESET}"
            ;;
        "w")
            PLAYER_ATTACK=$((PLAYER_ATTACK + 2))
            MESSAGE="${BLUE}You equipped a $item_name! Attack increased by 2.${RESET}"
            ;;
        "W")
            PLAYER_ATTACK=$((PLAYER_ATTACK + 5))
            MESSAGE="${BLUE}You equipped a $item_name! Attack increased by 5.${RESET}"
            ;;
        "a")
            PLAYER_MAX_HP=$((PLAYER_MAX_HP + 10))
            PLAYER_HP=$((PLAYER_HP + 10))
            PLAYER_ARMOR=$((PLAYER_ARMOR + 2))  # add armor bonus
            MESSAGE="${BLUE}You equipped a $item_name! Max HP increased by 10, Armor increased by 2.${RESET}"
            ;;
        "A")
            PLAYER_MAX_HP=$((PLAYER_MAX_HP + 25))
            PLAYER_HP=$((PLAYER_HP + 25))
            PLAYER_ARMOR=$((PLAYER_ARMOR + 5))  # add bigger armor bonus
            MESSAGE="${BLUE}You equipped a $item_name! Max HP increased by 25, Armor increased by 5.${RESET}"
            ;;
    esac
}

# Level up check
check_level_up() {
    while (( PLAYER_EXP >= PLAYER_LEVEL * 100 )); do
        PLAYER_EXP=$((PLAYER_EXP - PLAYER_LEVEL * 100))
        PLAYER_LEVEL=$((PLAYER_LEVEL + 1))
        PLAYER_MAX_HP=$((PLAYER_MAX_HP + 5))
        PLAYER_HP=$PLAYER_MAX_HP  # Heal to full on level up
        PLAYER_ATTACK=$((PLAYER_ATTACK + 3))
        MESSAGE="${PURPLE}Level Up! You are now level $PLAYER_LEVEL!${RESET}"
    done
}

# Next dungeon level
next_level() {
    DUNGEON_LEVEL=$((DUNGEON_LEVEL + 1))
    ROWS=$((ROWS + 5))
    COLS=$((COLS + 5))
    (( ROWS % 2 == 0 )) && ROWS=$((ROWS + 1))
    (( COLS % 2 == 0 )) && COLS=$((COLS + 1))
    
    PLAYER_X=1
    PLAYER_Y=1
    generate_valid_map
    MESSAGE="${YELLOW}You descend deeper into the dungeon...${RESET}"
}


# Try moving to a new tile
try_move() {
    local nx=$1
    local ny=$2

    # Bounds check
    if (( nx < 0 || ny < 0 || nx >= COLS || ny >= ROWS )); then
        MESSAGE="You can't go that way!"
        return
    fi

    tile=$(get_tile $nx $ny)

    case $tile in
        "#") 
            MESSAGE="You can't walk through walls!"
            return
            ;;
        "E")
            next_level
            ;;
        "G"|"O"|"S"|"Z"|"D")
            if fight_enemy "$tile"; then
                set_tile $nx $ny " "
                PLAYER_X=$nx
                PLAYER_Y=$ny
            fi
            ;;
        "h"|"H"|"w"|"W"|"a"|"A")
            use_item "$tile"
            set_tile $nx $ny " "
            PLAYER_X=$nx
            PLAYER_Y=$ny
            ;;
        *)
            PLAYER_X=$nx
            PLAYER_Y=$ny
            ;;
    esac
}

# Game loop
game_loop() {
    while (( GAME_OVER == 0 )); do
        draw_map
        read -sn1 input
        case $input in
            w) try_move $PLAYER_X $((PLAYER_Y - 1)) ;;
            s) try_move $PLAYER_X $((PLAYER_Y + 1)) ;;
            a) try_move $((PLAYER_X - 1)) $PLAYER_Y ;;
            d) try_move $((PLAYER_X + 1)) $PLAYER_Y ;;
            q) echo "Goodbye!"; exit 0 ;;
        esac
    done
    
    draw_map
    echo "Press any key to exit..."
    read -sn1
}

# Main
generate_valid_map
game_loop