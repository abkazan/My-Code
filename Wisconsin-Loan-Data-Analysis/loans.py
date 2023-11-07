import json
import zipfile
from csv import DictReader
from io import TextIOWrapper
race_lookup = {
        "1": "American Indian or Alaska Native",
        "2": "Asian",
        "21": "Asian Indian",
        "22": "Chinese",
        "23": "Filipino",
        "24": "Japanese",
        "25": "Korean",
        "26": "Vietnamese",
        "27": "Other Asian",
        "3": "Black or African American",
        "4": "Native Hawaiian or Other Pacific Islander",
        "41": "Native Hawaiian",
        "42": "Guamanian or Chamorro",
        "43": "Samoan",
        "44": "Other Pacific Islander",
        "5": "White",
}
class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r not in race_lookup.keys():
                continue
            else:
                self.race.add(race_lookup[r])
    def __repr__(self):
        race_list = [] 
        for r in self.race:
            race_list.append(r)
        return f"Applicant('{self.age}', {race_list})"
    
    def lower_age(self):
        if self.age[0] == '<' or self.age[0] == '>':
            return int(self.age[1:3])
        elif self.age[2] == '-':
            return int(self.age[0:2])
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()

class Loan:
    def __init__(self, values):
        if values["loan_amount"] != "NA" and values["loan_amount"] != "Exempt":
            self.loan_amount = float(values["loan_amount"])  
        else:
            self.loan_amount = -1
        if values["property_value"] != "NA" and values["property_value"] != "Exempt":
            self.property_value = float(values["property_value"]) 
        else:
            self.property_value = -1
        if values["interest_rate"] != "NA" and values["interest_rate"] != "Exempt":
            self.interest_rate = float(values["interest_rate"])
        else:
            self.interest_rate = -1
        self.applicants = []
        race = []
        for key in values.keys():
            if key.startswith("applicant_race") and values[key] != '':
                race.append(values[key])
        co_applicant_race = []
        if values["co-applicant_age"] != "9999":
            for key in values.keys():
                if key.startswith("co-applicant_race") and values[key] != '':
                    co_applicant_race.append(values[key])
        if co_applicant_race == []:
            self.applicants = [Applicant(values["applicant_age"], race)]
        else:
            self.applicants = [Applicant(values["applicant_age"], race), Applicant(values["co-applicant_age"], co_applicant_race)]
        
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"

    def __repr__(self):
        return str(self)
    
    def yearly_amounts(self, yearly_payment):
        # TODO: assert interest and amount are positive
        if self.interest_rate < 0 or self.loan_amount < 0:
            return "no rate or amount remaining"
        #result = []
        amt = self.loan_amount

        while amt > 0:
            yield(amt)
            # TODO: add interest rate multiplied by amt to amt
            amt += ((self.interest_rate/100) * amt)
            # TODO: subtract yearly payment from amt
            amt -= yearly_payment
        
class Bank:
    def __init__(self, name):
        self.name = ""
        self.lei = ""
        self.loans = []
        f = open('banks.json')
        data = json.load(f)
        f.close()
        for bank_dict in data:
            if bank_dict['name'] == name:
                self.name = name
                self.lei = bank_dict['lei']
                break;
        
        
        zip_path = "wi.zip"
        file_name = "wi.csv"

        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_info = zf.getinfo(file_name)
            with zf.open(file_info, 'r') as csv_file:
                text_file = TextIOWrapper(csv_file, encoding='utf-8')
                reader = DictReader(text_file)
                for row in reader:
                    if row['lei'] == self.lei:
                        loan_to_add = Loan(row)
                        self.loans.append(loan_to_add)
                    else: 
                        continue

                        
    def __getitem__(self, lookup):
        return self.loans[lookup]
    
    def __len__(self):
        return len(self.loans)
                

                # Closing file
                #f.close()
        
    
        