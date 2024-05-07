def game_logic(user_choice, opp_choice):
    logic = {
        'paper': 'rock',
        'scissors': 'paper',
        'rock': 'scissors',
        
    }

    if user_choice == opp_choice:
        return 'tie'
    
    elif logic[user_choice] == opp_choice:
        return 'win'
    
    else:
        return 'lose'