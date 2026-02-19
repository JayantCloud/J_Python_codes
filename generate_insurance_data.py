import mysql.connector
import random
import datetime

# -----------------------------
# 1. Connect to MySQL Database
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",      # running locally
    user="root",           # MySQL username
    password="ABCabc88@",       # MySQL password
    database="practice_db" # database you created in Workbench
)
cursor = conn.cursor()

# -----------------------------
# 2. Helper Functions
# -----------------------------
def random_name():
    first_names = ["Amit", "Priya", "John", "Sara", "Michael", "Anita", "Raj", "Meera", "David", "Sophia"]
    last_names = ["Sharma", "Khan", "Patel", "Singh", "Gupta", "Brown", "Taylor", "Miller", "Wilson", "Clark"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_date(start_year=1970, end_year=2025):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 1, 1)
    delta = end - start
    return start + datetime.timedelta(days=random.randint(0, delta.days))

def random_address():
    streets = ["MG Road", "Ring Road", "Park Street", "Main Street", "Highway 21", "Lake View"]
    return f"{random.randint(1,999)} {random.choice(streets)}"

# -----------------------------
# 3. Residences
# -----------------------------
residences = []
cities = [
    ("Delhi","Delhi","India","Urban"),
    ("Lucknow","UP","India","Urban"),
    ("Patna","Bihar","India","Urban"),
    ("Varanasi","UP","India","Urban"),
    ("Ghazipur","UP","India","Rural"),
    ("Toronto","Ontario","Canada","Urban"),
    ("Munich","Bavaria","Germany","Urban"),
    ("Sydney","NSW","Australia","Urban"),
    ("New York","NY","USA","Urban"),
    ("London","England","UK","Urban")
]
for city,state,country,ur in cities:
    avg_value = round(random.uniform(30000,300000),2)
    residences.append((city,state,country,ur,avg_value))

cursor.executemany("""
INSERT INTO residences (city,state,country,urban_rural,avg_property_value)
VALUES (%s,%s,%s,%s,%s)
""", residences)

# -----------------------------
# 4. Policyholders (fetch valid residence IDs)
# -----------------------------
cursor.execute("SELECT residence_id FROM residences")
residence_ids = [row[0] for row in cursor.fetchall()]

policyholders = []
occupations = ["Engineer","Doctor","Teacher","Analyst","Driver","Farmer","Lawyer","Accountant","Nurse","Software Developer"]
for i in range(500):
    name = random_name()
    dob = random_date(1950,2000)
    gender = random.choice(["Male","Female"])
    occupation = random.choice(occupations)
    income = round(random.uniform(25000,250000),2)
    residence_id = random.choice(residence_ids)  # always valid
    policyholders.append((name,dob,gender,random_address(),occupation,income,residence_id))

cursor.executemany("""
INSERT INTO policyholders (name,dob,gender,address,occupation,income,residence_id)
VALUES (%s,%s,%s,%s,%s,%s,%s)
""", policyholders)

# -----------------------------
# 5. Earnings (fetch valid policyholder IDs)
# -----------------------------
cursor.execute("SELECT policyholder_id FROM policyholders")
policyholder_ids = [row[0] for row in cursor.fetchall()]

earnings = []
for ph_id in policyholder_ids:
    for year in range(2015,2025):
        annual_income = round(random.uniform(25000,250000),2)
        bonus = round(random.uniform(2000,25000),2)
        tax_paid = round(annual_income*0.12,2)
        earnings.append((ph_id,year,annual_income,bonus,tax_paid))

cursor.executemany("""
INSERT INTO earnings (policyholder_id,year,annual_income,bonus,tax_paid)
VALUES (%s,%s,%s,%s,%s)
""", earnings)

# -----------------------------
# 6. Policies (fetch valid policyholder IDs)
# -----------------------------
policies = []
for i in range(1000):
    ph_id = random.choice(policyholder_ids)
    policy_type = random.choice(["Life","Health","Auto","Pension"])
    start_date = random_date(2010,2025)
    end_date = start_date + datetime.timedelta(days=random.randint(365,3650))
    premium = round(random.uniform(1000,10000),2)
    coverage = round(random.uniform(100000,1000000),2)
    policies.append((ph_id,policy_type,start_date,end_date,premium,coverage))

cursor.executemany("""
INSERT INTO policies (policyholder_id,policy_type,start_date,end_date,premium_amount,coverage_amount)
VALUES (%s,%s,%s,%s,%s,%s)
""", policies)

# -----------------------------
# 7. Claims (fetch valid policy IDs)
# -----------------------------
cursor.execute("SELECT policy_id FROM policies")
policy_ids = [row[0] for row in cursor.fetchall()]

claims = []
for i in range(2000):
    policy_id = random.choice(policy_ids)
    claim_date = random_date(2015,2025)
    claim_type = random.choice(["Accident","Hospitalization","Death","Theft","Critical Illness"])
    claim_amount = round(random.uniform(5000,200000),2)
    status = random.choice(["Pending","Approved","Rejected","Settled"])
    claims.append((policy_id,claim_date,claim_type,claim_amount,status))

cursor.executemany("""
INSERT INTO claims (policy_id,claim_date,claim_type,claim_amount,status)
VALUES (%s,%s,%s,%s,%s)
""", claims)

# -----------------------------
# 8. Payments (fetch valid claim IDs)
# -----------------------------
cursor.execute("SELECT claim_id FROM claims")
claim_ids = [row[0] for row in cursor.fetchall()]

payments = []
for i in range(1500):
    claim_id = random.choice(claim_ids)
    payment_date = random_date(2015,2025)
    paid_amount = round(random.uniform(1000,150000),2)
    method = random.choice(["Bank Transfer","Cheque","Online","UPI"])
    payments.append((claim_id,payment_date,paid_amount,method))

cursor.executemany("""
INSERT INTO payments (claim_id,payment_date,paid_amount,payment_method)
VALUES (%s,%s,%s,%s)
""", payments)

# -----------------------------
# 9. Commit and Close
# -----------------------------
conn.commit()
cursor.close()
conn.close()

print("Realistic insurance dataset populated successfully.")
