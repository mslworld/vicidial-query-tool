import streamlit as st
import re

st.title("📞 Vici Dialer Query Generator")

# State + Area Code Mapping
state_area_codes = {
    "AK": ['907'], "AL": ['205','251','256','334','659','938'],
    "AR": ['479','501','870'], "AZ": ['480','520','602','623','928'],
    "CA": ['209','213','279','310','323','341','408','415','424','442','510','530','559','562','619','626','628','650','657','661','669','707','714','747','760','805','818','820','831','858','909','916','925','949','951'],
    "CO": ['303','719','720','970'], "CT": ['203','475','860','959'],
    "DE": ['302'], "FL": ['239','305','321','352','386','407','561','689','727','754','772','786','813','850','863','904','941','954'],
    "GA": ['229','404','470','478','678','706','762','770','912'],
    "HI": ['808'], "IA": ['319','515','563','641','712'],
    "ID": ['208','986'],
    "IL": ['217','224','309','312','331','618','630','708','773','779','815','847','872'],
    "IN": ['219','260','317','463','574','765','812','930'],
    "KS": ['316','620','785','913'], "KY": ['270','364','502','606','859'],
    "LA": ['225','318','337','504','985'],
    "MA": ['339','351','413','508','617','774','781','857','978'],
    "MD": ['227','240','301','410','443','667'],
    "ME": ['207'],
    "MI": ['231','248','269','313','517','586','616','734','810','906','947','989'],
    "MN": ['218','320','507','612','651','763','952'],
    "MO": ['314','417','573','636','660','816'],
    "MS": ['228','601','662','769'],
    "MT": ['406'],
    "NC": ['252','336','704','743','828','910','919','980','984'],
    "ND": ['701'], "NE": ['308','402','531'],
    "NH": ['603'],
    "NJ": ['201','551','609','640','732','848','856','862','908','973'],
    "NM": ['505','575'],
    "NV": ['702','725','775'],
    "NY": ['212','315','332','347','516','518','585','607','631','646','680','716','718','838','845','914','917','929','934'],
    "OH": ['216','220','234','283','326','330','380','419','440','513','567','614','740','937'],
    "OK": ['405','539','572','580','918'],
    "OR": ['458','503','541','971'],
    "PA": ['215','223','267','272','412','445','484','570','610','717','724','814','878'],
    "RI": ['401'],
    "SC": ['803','839','843','854','864'],
    "SD": ['605'],
    "TN": ['423','615','629','731','865','901','931'],
    "TX": ['210','214','254','281','325','346','361','409','430','432','469','512','682','713','726','737','806','817','830','832','903','915','936','940','956','972','979'],
    "UT": ['385','435','801'],
    "VA": ['276','434','540','571','703','757','804'],
    "VT": ['802'],
    "WA": ['206','253','360','425','509','564'],
    "WI": ['262','414','534','608','715','920'],
    "WV": ['304','681'],
    "WY": ['307'],
    "DC": ['202','301','703']
}

# State name mapping (full names to abbreviations)
state_names = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    "hawaii": "HI", "iowa": "IA", "idaho": "ID", "illinois": "IL", "indiana": "IN",
    "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "massachusetts": "MA", "maryland": "MD",
    "maine": "ME", "michigan": "MI", "minnesota": "MN", "missouri": "MO", "mississippi": "MS",
    "montana": "MT", "north carolina": "NC", "north dakota": "ND", "nebraska": "NE", "new hampshire": "NH",
    "new jersey": "NJ", "new mexico": "NM", "nevada": "NV", "new york": "NY", "ohio": "OH",
    "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "virginia": "VA",
    "vermont": "VT", "washington": "WA", "wisconsin": "WI", "west virginia": "WV", "wyoming": "WY",
    "district of columbia": "DC", "dc": "DC"
}

def normalize_state(input_state):
    """
    Normalize state input to standard 2-letter abbreviation.
    Handles: uppercase, lowercase, mixed case, special characters, full names
    """
    # Remove special characters and convert to lowercase
    cleaned = re.sub(r'[^a-zA-Z]', '', input_state).lower()
    
    # Check if it's already a 2-letter abbreviation
    if len(cleaned) == 2:
        return cleaned.upper()
    
    # Check if it's a full state name
    if cleaned in state_names:
        return state_names[cleaned]
    
    # Handle 2-letter inputs with mixed case
    if len(input_state.strip()) == 2:
        return input_state.strip().upper()
    
    return None

# MULTI-LINE INPUT 🔥
user_input = st.text_area("Enter States (row, column, comma, space — sab chalega)")

if st.button("Generate Query"):

    # Split by comma, space, newline (ALL formats supported)
    states = re.split(r"[,\s\n]+", user_input)

    # Clean and normalize states
    normalized_states = []
    invalid_states = []

    for state in states:
        state = state.strip()
        if state:
            normalized = normalize_state(state)
            if normalized:
                normalized_states.append(normalized)
            else:
                invalid_states.append(state)

    area_codes = []

    for state in normalized_states:
        if state in state_area_codes:
            area_codes.extend(state_area_codes[state])

    if area_codes:
        formatted_codes = ",".join([f"'{code}'" for code in sorted(set(area_codes))])
        query = f"left(phone_number,3) IN ({formatted_codes})"

        st.success("✅ Query Generated")
        st.code(query, language='sql')

    if invalid_states:
        st.warning(f"⚠️ Invalid States Ignored: {', '.join(set(invalid_states))}")
