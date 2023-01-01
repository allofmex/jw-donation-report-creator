from dataclasses import dataclass
from future.backports.misc import count

class UserDonations:

    def __init__(self):
        self.donations = list()
        self.notes = None

    def addDonation(self, date, amount, note):
        donation = Donation(date, amount)
        self.donations.append(donation)
        if note is not None:
            if self.notes is None:
                self.notes = list()
            self.notes.append(note)
        # print(str(len(self.donations))+ " existing")

    def getList(self):
        return self.donations

    def getTotal(self):
        total = 0
        for donation in self.donations:
            total += donation.amount
        return total

    def getNotes(self):
        return self.notes

    def __repr__(self):
        cnt = len(self.donations)
        return f"{__name__}(cnt: {cnt})"

@dataclass
class Donation:
    date: str
    amount: float
        