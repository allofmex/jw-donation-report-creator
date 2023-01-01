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

    def getList(self):
        return self.donations

    def getTotal(self):
        total = 0
        for donation in self.donations:
            total += donation.amount
        return total

    def getNotes(self):
        return self.notes

    def getOverview(self):
        min = -1
        max = 0
        cnt = 0
        total = 0
        for donation in self.donations:
            if min == -1 or min > donation.amount:
                min = donation.amount
            if max < donation.amount:
                max = donation.amount
            total += donation.amount
            cnt += 1
        avr = total / cnt
        return f"Total: {total: >5.0f}, Cnt: {cnt: >2}  Min: {min: >5.0f}  Max {max: >5.0f}  Avr: {avr: >8.2f}"

    def __repr__(self):
        cnt = len(self.donations)
        return f"{__name__}(cnt: {cnt})"

@dataclass
class Donation:
    date: str
    amount: float
