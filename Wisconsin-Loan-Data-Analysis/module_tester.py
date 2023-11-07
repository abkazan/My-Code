import traceback

loans = None
search = None

loans_points = 0
search_points = 0

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

def loans_test():
    global loans_points
    loans_points = 0

    # TEST: Applicant class
    
    # +1 for just getting started by creating class
    loans.Applicant
    loans_points += 1

    # check race attribute filled correctly
    codes = sorted(race_lookup.keys()) + ["999"]
    for i in range(len(codes) + 3):
        codes_subset = codes[max(0, i-3):i]
        applicant = loans.Applicant("20-30", codes_subset)
        expected = {race_lookup[code] for code in codes_subset if code in race_lookup}
        assert applicant.race == expected
    loans_points += 1

    # repr
    applicant = loans.Applicant("80-90", [])
    assert repr(applicant) == "Applicant('80-90', [])"
    applicant = loans.Applicant("90+", ["25"])
    assert repr(applicant) == "Applicant('90+', ['Korean'])"
    loans_points += 1

    # lower_age
    assert loans.Applicant("<25", []).lower_age() == 25
    assert loans.Applicant("20-30", []).lower_age() == 20
    assert loans.Applicant(">75", []).lower_age() == 75
    loans_points += 1

    # __lt__
    applicants = sorted([
        loans.Applicant(">75", ["43", "44"]),
        loans.Applicant("20-30", ["1", "3"]),
        loans.Applicant("35-44", ["22"]),
        loans.Applicant("<25", ["5"]),
    ])
    assert [a.lower_age() for a in applicants] == [20, 25, 35, 75]
    loans_points += 1

    # TEST: Loan class

    # init numeric fields
    d = {"loan_amount": "123", "property_value": "456", "interest_rate": "4.4",
         "applicant_age": "20", "applicant_race-1": "41", "applicant_race-2": "",
         "applicant_race-3": "", "applicant_race-4": "", "applicant_race-5": "",
         "co-applicant_age": "9999", "co-applicant_race-1": "", "co-applicant_race-2": "",
         "co-applicant_race-3": "", "co-applicant_race-4": "", "co-applicant_race-5": ""}
    loan = loans.Loan(d)
    assert loan.loan_amount == 123
    assert loan.property_value == 456
    assert loan.interest_rate == 4.4
    loans_points += 1

    assert str(loan) == "<Loan: 4.4% on $456.0 with 1 applicant(s)>"
    assert repr(loan) == str(loan)
    loans_points += 1

    d["loan_amount"] = "NA"
    d["property_value"] = "Exempt"
    d["interest_rate"] = "NA"
    loan = loans.Loan(d)
    assert loan.loan_amount == -1
    assert loan.property_value == -1
    assert loan.interest_rate == -1
    loans_points += 1

    # applicants/race
    assert len(loan.applicants) == 1
    assert loan.applicants[0].race == {race_lookup[d["applicant_race-1"]]}
    loans_points += 1

    d["co-applicant_age"] = "21"
    d["co-applicant_race-1"] = "3"
    d["co-applicant_race-2"] = "5"
    loan = loans.Loan(d)
    assert len(loan.applicants) == 2
    assert loan.applicants[1].race == {race_lookup[d["co-applicant_race-1"]], race_lookup[d["co-applicant_race-2"]]}
    loans_points += 1

    for i in range(1, 6):
        d[f"applicant_race-{i}"] = str(i)
    loan = loans.Loan(d)
    assert loan.applicants[0].race == {race_lookup[str(i)] for i in range(1,6)}
    loans_points += 1
    

    # yearly_amounts
    d["loan_amount"] = "1000"
    d["interest_rate"] = "100"
    loan = loans.Loan(d)
    amounts = list(loan.yearly_amounts(1050))
    expected = [1000.0, 950.0, 850.0, 650.0, 250.0]
    assert len(amounts) == len(expected)
    for v1, v2 in zip(amounts, expected):
        assert abs(v1-v2) < 0.1
    loans_points += 1

    amounts = loan.yearly_amounts(0)
    assert(next(amounts) == 1000)
    assert(next(amounts) == 2000)
    assert(next(amounts) == 4000)
    assert(next(amounts) == 8000)
    loans_points += 1

    # TEST: Bank class
    bank = loans.Bank("First Home Bank")
    assert bank.lei == "549300DMI3W6YLDVSK93"
    loans_points += 1

    assert len(bank) == 45
    assert bank[1].interest_rate == 2.5
    assert bank[1].property_value == 235000.0
    assert len(bank[1].applicants) == 2
    loans_points += 1

    assert bank[8].interest_rate == 2.75
    assert bank[8].property_value == 215000
    assert len(bank[8].applicants) == 1
    loans_points += 1
    
    assert bank[9].property_value == -1
    assert len(bank[9].applicants) == 2
    assert bank[9].interest_rate == -1
    loans_points += 1
    
    values = {'activity_year': '2020', 'lei': '549300FX7K8PTEQUU487', 'derived_msa-md': '31540', 'state_code': 'WI',
         'county_code': '55025', 'census_tract': '55025002402', 'conforming_loan_limit': 'C',
         'derived_loan_product_type': 'Conventional:First Lien',
         'derived_dwelling_category': 'Single Family (1-4 Units):Site-Built',
         'derived_ethnicity': 'Not Hispanic or Latino', 'derived_race': 'White', 'derived_sex': 'Male',
         'action_taken': '3', 'purchaser_type': '0', 'preapproval': '2', 'loan_type': '1', 'loan_purpose': '4',
         'lien_status': '1', 'reverse_mortgage': '2', 'open-end_line_of_credit': '1',
         'business_or_commercial_purpose': '2', 'loan_amount': '225000.0', 'loan_to_value_ratio': '78.671',
         'interest_rate': '3.000', 'rate_spread': 'NA', 'hoepa_status': '3', 'total_loan_costs': 'NA',
         'total_points_and_fees': 'NA', 'origination_charges': 'NA', 'discount_points': 'NA',
         'lender_credits': 'NA', 'loan_term': '360', 'prepayment_penalty_term': 'NA', 'intro_rate_period': '1',
         'negative_amortization': '2', 'interest_only_payment': '2', 'balloon_payment': '2',
         'other_nonamortizing_features': '2', 'property_value': '285000', 'construction_method': '1',
         'occupancy_type': '1', 'manufactured_home_secured_property_type': '3',
         'manufactured_home_land_property_interest': '5', 'total_units': '1', 'multifamily_affordable_units': 'NA',
         'income': '0', 'debt_to_income_ratio': '>60%', 'applicant_credit_score_type': '1',
         'co-applicant_credit_score_type': '10', 'applicant_ethnicity-1': '2', 'applicant_ethnicity-2': '',
         'applicant_ethnicity-3': '', 'applicant_ethnicity-4': '', 'applicant_ethnicity-5': '',
         'co-applicant_ethnicity-1': '5', 'co-applicant_ethnicity-2': '', 'co-applicant_ethnicity-3': '',
         'co-applicant_ethnicity-4': '', 'co-applicant_ethnicity-5': '', 'applicant_ethnicity_observed': '2',
         'co-applicant_ethnicity_observed': '4', 'applicant_race-1': '5', 'applicant_race-2': '',
         'applicant_race-3': '', 'applicant_race-4': '', 'applicant_race-5': '', 'co-applicant_race-1': '8',
         'co-applicant_race-2': '', 'co-applicant_race-3': '', 'co-applicant_race-4': '', 'co-applicant_race-5': '',
         'applicant_race_observed': '2', 'co-applicant_race_observed': '4', 'applicant_sex': '1',
         'co-applicant_sex': '5', 'applicant_sex_observed': '2', 'co-applicant_sex_observed': '4',
         'applicant_age': '55-64', 'co-applicant_age': '9999', 'applicant_age_above_62': 'Yes',
         'co-applicant_age_above_62': 'NA', 'submission_of_application': '1', 'initially_payable_to_institution': '1',
         'aus-1': '6', 'aus-2': '', 'aus-3': '', 'aus-4': '', 'aus-5': '', 'denial_reason-1': '1',
         'denial_reason-2': '', 'denial_reason-3': '', 'denial_reason-4': '', 'tract_population': '3572',
         'tract_minority_population_percent': '41.1499999999999986', 'ffiec_msa_md_median_family_income': '96600',
         'tract_to_msa_income_percentage': '64', 'tract_owner_occupied_units': '812',
         'tract_one_to_four_family_homes': '910', 'tract_median_age_of_housing_units': '45'}
    
    loan = loans.Loan(values)
    assert str(loan) == '<Loan: 3.0% on $285000.0 with 1 applicant(s)>'
    assert repr(loan) == str(loan)
    amt_ls = []
    for amt in loan.yearly_amounts(20000):
        amt_ls.append(amt)
    assert amt_ls == [225000.0, 211750.0, 198102.5, 184045.575, 169566.94225000002, 154653.95051750002, 139293.56903302504, 123472.3761040158, 107176.54738713628, 90391.84380875036, 73103.59912301287, 55296.70709670326, 36955.60830960436, 18064.27655889249]
    loans_points += 3

def search_test():
    global search_points
    search_points = 0

    # Node
    n = search.Node("test")
    assert n.key == "test"
    assert n.values == []
    assert n.left == None
    assert n.right == None
    search_points += 1

    # BST
    t = search.BST()
    search_points += 1
    
    # add
    t.add("B", 3)
    search_points += 1

    # len
    assert len(t.root) == 1
    t.add("A", 2)
    assert len(t.root) == 2
    t.add("C", 1)
    assert len(t.root) == 3
    t.add("C", 4)
    assert len(t.root) == 4
    search_points += 1

    # lookup
    assert t.root.lookup("A") == [2]
    search_points += 1
    assert t.root.lookup("C") == [1, 4]
    assert t.root.lookup("Z") == []
    search_points += 1

    # lookup with brackets
    assert t["A"] == [2]
    assert t["C"] == [1, 4]
    assert t["Z"] == []
    search_points += 1

    # check different shapes
    t = search.BST()
    t.add("B", 2)
    t.add("C", 3)
    t.add("A", 1)
    assert t.root.left.key == "A"
    assert t.root.right.key == "C"
    search_points += 1

    t = search.BST()
    t.add("A", 1)
    t.add("B", 2)
    t.add("C", 3)
    assert t.root.right.key == "B"
    assert t.root.right.right.key == "C"
    search_points += 1

    t = search.BST()
    t.add("C", 3)
    t.add("B", 2)
    t.add("A", 1)
    assert t.root.left.key == "B"
    assert t.root.left.left.key == "A"
    search_points += 1

def main():
    global search, loans

    # import modules that are here
    try:
        import loans as tmp
        loans = tmp
    except ModuleNotFoundError:
        pass

    try:
        import search as tmp
        search = tmp
    except ModuleNotFoundError:
        pass

    # we'll return this summary at the end
    result = {
        "score": None,
        "errors": [],
    }

    # run tests on both modules, as far as we can
    if loans:
        try:
            loans_test()
        except Exception as e:
            result["errors"].append(traceback.format_exc())
    else:
        result["errors"].append("could not find loans module")

    if search:
        try:
            search_test()
        except Exception as e:
            result["errors"].append(traceback.format_exc())
    else:
        result["errors"].append("could not find search module")

    # summarize results
    result["score"] = (loans_points + search_points * 2) / 40 * 100
    return result

if __name__ == "__main__":
    print(main())