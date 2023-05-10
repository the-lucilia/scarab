class RegionBlock:
    def __init__(self, regions):

        self.regions = regions
        self.first = regions[0]
        self.last = regions[-1]
        self.firstUpd = self.first.update
        self.lastUpd = self.last.update
        self.duration = self.lastUpd - self.firstUpd

        self.updateIn = False # Is update within our block?
        self.updatePast = False # Is update past our block?
