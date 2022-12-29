from dataclasses import dataclass
from future.backports.misc import count

class UserDonations:

    def __init__(self):
        self.donations = list()

    def addDonation(self, date, amount):
        donation = Donation(date, amount)
        self.donations.append(donation)
        # print(str(len(self.donations))+ " existing")
        
    def getTotal(self):
        total = 0
        for donation in self.donations:
            total += donation.amount
        return total
        
    def __repr__(self):
        cnt = len(self.donations)
        return f"{__name__}(cnt: {cnt})"

@dataclass
class Donation:
    date: str
    amount: float
        