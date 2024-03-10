def prompt(position, round, motion):
    if round == 0:
        if position == "Proposition":
            return f"Welcome to the first round, Proposition! Your motion is: '{motion}'. In this initial phase, your goal is to provide a comprehensive and convincing opening statement. Emphasize the key points supporting your position within the 3-minute timeframe. do not use any markdown text or headers it should be just plein text to be read"
        elif position == "Opposition":
            return f"Welcome to the first round, Opposition! Your motion is: '{motion}'. Your task is to deliver a compelling opening statement that challenges the motion. Articulate your position effectively within the given 3-minute timeframe. do not use any markdown text or headers it should be just plein text to be read"
    else:
        return f"Round {round} prompt for {position} on the motion '{motion}': You now have 3 minutes to present a well-structured debate. Begin with a concise recap of your team's stance. Additionally, you can now engage in rebuttals against arguments presented by the opposing team. However, ensure that you introduce new perspectives and avoid repetition of your initial arguments. do not use any markdown text or headers it should be just plein text to be read"

def clean_text_prompt(text):
    return f"Ensure your arguments are presented in a clear and organized manner, using bullet points:\n{text}"
