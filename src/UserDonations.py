from dataclasses import dataclass
from _datetime import datetime

class UserDonations:

    def __init__(self):
        self.donations = list()
        self.notes = None

    def addDonation(self, date: datetime, amount: int, note=None):
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

    def getOverview(self) -> str:
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
        avr = total / cnt if cnt > 0 else 0
        return f"Total: {total: >5.0f}, Cnt: {cnt: >2}  Min: {min: >5.0f}  Max {max: >5.0f}  Avr: {avr: >8.2f}"
    
    def getReport(self) -> str:
        result = ""
        for donation in self.donations:
            result += f"{donation.date.strftime('%d.%m.%Y')} {donation.amount}"
        result += "\n"+self.getOverview()
        return result

    def __repr__(self):
        cnt = len(self.donations)
        return f"{__name__}(cnt: {cnt})"

@dataclass
class Donation:
    date: datetime
    amount: float
