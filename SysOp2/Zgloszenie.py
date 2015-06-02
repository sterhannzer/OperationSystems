class Zgloszenie():

    def __init__(self, numer, priorytet):
        self.nr = numer
        self.priorytet = priorytet
        self.obsluzony = False

    def get_nr(self):
        return self.nr

    def obsluzony(self):
        self.obsluzony = True

    def __str__(self):
        return str(self.nr)

    def __unicode__(self):
        return self.nr
