import re

# Full Name → Abbreviation Mapping
state_name_to_abbr = {
    "ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ", "ARKANSAS": "AR",
    "CALIFORNIA": "CA", "COLORADO": "CO", "CONNECTICUT": "CT",
    "DELAWARE": "DE", "FLORIDA": "FL", "GEORGIA": "GA",
    "HAWAII": "HI", "IDAHO": "ID", "ILLINOIS": "IL",
    "INDIANA": "IN", "IOWA": "IA", "KANSAS": "KS",
    "KENTUCKY": "KY", "LOUISIANA": "LA", "MAINE": "ME",
    "MARYLAND": "MD", "MASSACHUSETTS": "MA", "MICHIGAN": "MI",
    "MINNESOTA": "MN", "MISSISSIPPI": "MS", "MISSOURI": "MO",
    "MONTANA": "MT", "NEBRASKA": "NE", "NEVADA": "NV",
    "NEW HAMPSHIRE": "NH", "NEW JERSEY": "NJ", "NEW MEXICO": "NM",
    "NEW YORK": "NY", "NORTH CAROLINA": "NC", "NORTH DAKOTA": "ND",
    "OHIO": "OH", "OKLAHOMA": "OK", "OREGON": "OR",
    "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI",
    "SOUTH CAROLINA": "SC", "SOUTH DAKOTA": "SD",
    "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT",
    "VERMONT": "VT", "VIRGINIA": "VA", "WASHINGTON": "WA",
    "WEST VIRGINIA": "WV", "WISCONSIN": "WI", "WYOMING": "WY",
    "DISTRICT OF COLUMBIA": "DC"
}

# INPUT
user_input = st.text_area("Enter States")

if st.button("Generate Query"):

    # ✅ Only split by comma OR newline (space NOT included)
    raw_states = re.split(r"[,\n]+", user_input)

    area_codes = []
    invalid_states = []

    for state in raw_states:
        state = state.strip().upper()

        if not state:
            continue

        # ✅ Convert full name → abbreviation
        if state in state_name_to_abbr:
            state = state_name_to_abbr[state]

        # ✅ Match with area codes
        if state in state_area_codes:
            area_codes.extend(state_area_codes[state])
        else:
            invalid_states.append(state)

    if area_codes:
        # remove duplicates + sort
        formatted_codes = ",".join([f"'{code}'" for code in sorted(set(area_codes))])
        query = f"left(phone_number,3) IN ({formatted_codes})"

        st.success("✅ Query Generated")
        st.code(query, language='sql')

    if invalid_states:
        st.warning(f"⚠️ Invalid States Ignored: {', '.join(set(invalid_states))}")
