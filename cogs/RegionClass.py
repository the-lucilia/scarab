# Custom class to create Region Objects for the bot
# We need the name (<NAME>), update time(<LASTUPDATE>), delegate (<DELEGATE>),
# endos (<DELEGATEVOTES>), and founder (<FOUNDER>)

class Region:
    def __init__(self, name, update, delegate, endos, founder):
        self.name = name
        self.update = update
        self.delegate = delegate
        self.endos = endos
        self.founder = founder
