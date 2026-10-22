'''
                                           TELECOMMUNICATION BILLING SYSTEM
'''
VALID_PLANS = ['Prepaid', 'Bronze', 'Silver', 'Gold']

LOOKUP_VALID_PLANS = set(VALID_PLANS)

BASE_FEE = [
    ('Prepaid', 0),
    ('Bronze', 20000),
    ('Silver', 50000),
    ('Gold', 100000)
]
LINE_WIDTH = 79
SEPARATOR = '=' * LINE_WIDTH

CALL_OVERAGE_TIERS = [
    (0,50,500,300),
    (50,200,400,250),
    (200,float('inf'),300,200)
]

SMS_OVERAGE_TIERS = [
    (0,100,200),
    (100,500,150),
    (500,float('inf'),100)

]

PLAN_ALLOWANCES = {
    "Prepaid": {"minutes": 0, "sms": 0, "data": 0},
    "Bronze": {"minutes": 50, "sms": 100, "data": 1},
    "Silver": {"minutes": 200, "sms": 500, "data": 5},
    "Gold": {"minutes": float('inf'), "sms": float('inf'), "data": 20}
}

DATA_OVERAGE_TIERS = [
    (0,5,5000),
    (5,20,4000),
    (20,float('inf'),3000)
]

def collect_customer_details():
    d = {}
    d['name'] = get_text_input('Enter Customer Name: ')
    d['plan'] = validate_plan('Enter Plan (Prepaid/Bronze/Silver/Gold): ')
    d['peak'] = get_nonnegative_integer('Enter Peak Hour Minutes: ')
    d['off_peak'] = get_nonnegative_integer('Enter Off-Peak Minutes: ')
    d['sms'] = get_nonnegative_integer('Enter SMS Sent: ')
    d['data'] = get_nonnegative_integer('Enter Data Used (GB): ')
    
    return d

def display_plan_allowances(d):
    plan = PLAN_ALLOWANCES[d['plan']]
    print_header(f"PLAN ALLOWANCES ({d['plan']})")
    if d['plan'] != 'Gold':
        print(f"  {'Calls (Peak only)':<22}: {plan['minutes']} minutes")
        print(f"  {'SMS':<22}: {plan['sms']} messages")
        print(f"  {'Data':<22}: {plan['data']} GB")
    else:
        print(f"  {'Calls':<22}: UNLIMITED")
        print(f"  {'SMS':<22}: UNLIMITED")
        print(f"  {'Data':<22}: {plan['data']} GB")

def validate_plan(prompt):
    while True:
        plan = get_text_input(prompt)
        if plan in LOOKUP_VALID_PLANS:
            return plan
        print(f'Subscription plan not found, please choose: {'/'.join(VALID_PLANS)}')
        
def get_nonnegative_integer(prompt):
    while True:
        try:
            value = int(get_input(prompt))
            if value < 0:
                print('Invalid input, please enter a non-negative integer...')
            else:
                return value
        except ValueError:
            print('Invalid input, please enter an integer...')

def get_input(prompt):
    while True:
        entry = input(prompt)
        if entry.strip():
            return entry.strip()
        print('Field Cannot be empty, Please enter something...')

def get_text_input(prompt):
    return get_input(prompt).title()

def get_base_fee(plan_name):
    return next(fee for plan, fee in BASE_FEE if plan == plan_name)
    
def print_header(heading):
    print(SEPARATOR)
    print(f"   {heading}")
    print(SEPARATOR)

def display_customer_bill(d, base_fee, overage, total):
    print_header('CUSTOMER BILL')
    print(f"  {'Customer':<22}: {d['name']}")
    plan_name = f"{d['plan']} (Pay-as-you-go)" if d['plan'] == 'Prepaid' else d['plan']
    print(f"  {'Plan':<22}: {plan_name}")
    print(f"  {'Base Fee':<22}: {base_fee:,.0f} UGX")
    if d['plan'] != 'Prepaid':
        print(f"  {'Overage':<22}: {overage:,.0f} UGX")
    print(f"  {'TOTAL BILL':<22}= {total:,.0f} UGX")

def display_usage_summary(d):
    print_header('USAGE SUMMARY')
    plan = PLAN_ALLOWANCES[d['plan']]
    if d['plan'] == 'Gold':
        print(f"  {'Peak Minutes':<22}: {d['peak']} (FREE - Unlimited)")
        print(f"  {'Off-Peak Minutes':<22}: {d['off_peak']} (FREE - Unlimited)")
        print(f"  {'SMS':<22}: {d['sms']} (FREE - Unlimited)")
    else:
        peak_note = allowance_note(d['peak'], plan['minutes'], 'min')
        sms_note = allowance_note(d['sms'], plan['sms'], 'SMS')
        print(f"  {'Peak Minutes':<22}: {d['peak']}{peak_note}")
        print(f"  {'Off-Peak Minutes':<22}: {d['off_peak']} (not covered by allowance - billed from min 1)")
        print(f"  {'SMS':<22}: {d['sms']}{sms_note}")

    data_note = allowance_note(d['data'], plan['data'], 'GB')
    print(f"  {'Data':<22}: {d['data']} GB{data_note}")

def allowance_note(used, allowance, unit):
    if used < allowance:
        difference = allowance - used
        if unit == 'min':
            return f" ({difference} below the {allowance}-min allowance)"
        if unit == 'GB':
            return f" ({difference} GB below allowance)"
        return f" ({difference} below allowance)"
    if used > allowance:
        difference = used - allowance
        if unit == 'min':
            return f" ({difference} over the {allowance}-min allowance)"
        if unit == 'GB':
            return f" ({difference} GB over allowance)"
        return f" ({difference} over allowance)"
    return " (at allowance)"

def get_tier_breakdown(total_usage, allowance, tiers, rate_index):
    breakdown = []
    for tier in tiers:
        start, end = tier[0], tier[1]
        rate = tier[rate_index]
        units = max(0, min(end, total_usage) - max(start, allowance))
        if units:
            breakdown.append((units, rate, units * rate))
    return breakdown

def print_tier_charges(label, breakdown, unit, rate_unit):
    if not breakdown:
        print(f"  {label:<22}: No overage charges")
        return

    for index, (units, rate, charge) in enumerate(breakdown):
        prefix = f"  {label:<22}: " if index == 0 else "                          "
        unit_text = f" {unit}" if unit else ""
        rate_width = 9 if rate_unit == 'UGX' else 10
        print(f"{prefix}{units}{unit_text} @ {rate:,.0f} {rate_unit:<{rate_width}}= {charge:>10,.0f} UGX")

def display_overage_charges(d):
    plan = PLAN_ALLOWANCES[d['plan']]
    is_prepaid = d['plan'] == 'Prepaid'
    is_gold = d['plan'] == 'Gold'
    title = 'USAGE CHARGES (Prepaid - pay-as-you-go, no base fee, no allowance)' if is_prepaid else 'OVERAGE CHARGES'
    print_header(title)

    if is_gold:
        print(f"  {'Calls Overage':<22}: {'Unlimited plan':<23}= {0:>10,.0f} UGX")
        print(f"  {'SMS Overage':<22}: {'Unlimited plan':<23}= {0:>10,.0f} UGX")
        data_charges = get_tier_breakdown(d['data'], plan['data'], DATA_OVERAGE_TIERS, 2)
        print_tier_charges('Data Overage', data_charges, 'GB', 'UGX/GB')
        total_overage = sum(charge for _, _, charge in data_charges)
    else:
        peak_charges = get_tier_breakdown(d['peak'], plan['minutes'], CALL_OVERAGE_TIERS, 2)
        off_peak_charges = get_tier_breakdown(d['off_peak'], 0, CALL_OVERAGE_TIERS, 3)
        sms_charges = get_tier_breakdown(d['sms'], plan['sms'], SMS_OVERAGE_TIERS, 2)
        data_charges = get_tier_breakdown(d['data'], plan['data'], DATA_OVERAGE_TIERS, 2)

        if is_prepaid:
            print_tier_charges('Peak Calls', peak_charges, 'min', 'UGX/min')
            print_tier_charges('Off-Peak Calls', off_peak_charges, 'min', 'UGX/min')
            print_tier_charges('SMS', sms_charges, '', 'UGX')
            print_tier_charges('Data', data_charges, 'GB', 'UGX/GB')
        else:
            print_tier_charges('Peak Call Overage', peak_charges, 'min', 'UGX/min')
            print_tier_charges('Off-Peak Call Charge', off_peak_charges, 'min', 'UGX/min')
            print_tier_charges('SMS Overage', sms_charges, 'SMS', 'UGX')
            print_tier_charges('Data Overage', data_charges, 'GB', 'UGX/GB')

        total_overage = sum(
            charge
            for breakdown in (peak_charges, off_peak_charges, sms_charges, data_charges)
            for _, _, charge in breakdown
        )

    print("                          " + "-" * 39)
    total_label = 'TOTAL CHARGES' if is_prepaid else 'TOTAL OVERAGE'
    print(f"  {total_label:<22}= {total_overage:>10,.0f} UGX")
    return total_overage

def main():
    print_header("TELECOMMUNICATION BILLING SYSTEM v1.0")
    customer_count = 0
    total_revenue = 0
    plan_counts = {plan: 0 for plan in VALID_PLANS}

    while True:
        d = collect_customer_details()
        if d['plan'] != 'Prepaid':
            display_plan_allowances(d)
            display_usage_summary(d)
        overage = display_overage_charges(d)
        base_fee = get_base_fee(d['plan'])
        total_bill = base_fee + overage
        display_customer_bill(d, base_fee, overage, total_bill)

        customer_count += 1
        total_revenue += total_bill
        plan_counts[d['plan']] += 1

        if not ask_another_customer():
            break

    display_daily_report(customer_count, total_revenue, plan_counts)

def ask_another_customer():
    while True:
        answer = get_text_input('Add another customer? (yes/no): ')
        if answer in {'Yes', 'No'}:
            return answer == 'Yes'
        print('Please answer yes or no.')

def display_daily_report(customer_count, total_revenue, plan_counts):
    print_header('DAILY BILLING REPORT')
    average_bill = total_revenue / customer_count if customer_count else 0
    popular_count = max(plan_counts.values())
    popular_plans = [plan for plan, count in plan_counts.items() if count == popular_count]
    popular_text = ' / '.join(popular_plans)
    if len(popular_plans) > 1:
        popular_text += ' (tie)'
    print(f"  {'Total Customers':<22}: {customer_count}")
    print(f"  {'Total Revenue':<22}: {total_revenue:,.0f} UGX")
    print(f"  {'Average Bill':<22}: {average_bill:,.2f} UGX")
    breakdown = ' | '.join(f'{plan}: {plan_counts[plan]}' for plan in VALID_PLANS)
    print(f"  {'Plan Breakdown':<22}: {breakdown}")
    print(f"  {'Most Popular Plan':<22}: {popular_text}")


if __name__ == '__main__':
    try:
        main()
    except (EOFError,KeyboardInterrupt):
        print('Program Interrupted by User, closing...')
