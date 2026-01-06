import streamlit as st
import pandas as pd
import google.generativeai as genai
st.set_page_config(page_title="Smart House Tips",layout= "centered")

GEMINI_API_key = "AIzaSyBnsEE5yEWvpaCHv2H4QDHXeyQZ5B3_zlw"

try:
    genai.configure(api_key = GEMINI_API_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
except:
    model = None


if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'appliances' not in st.session_state:
    st.session_state.appliances = [] 

if 'ai_response' not in st.session_state:
    st.session_state.ai_response = None

def go_todesign():
    st.session_state.page = 'design'

def go_to_home():
    st.session_state.page = 'home'

def add_appliance():
    st.session_state.appliances.append({
        'name': '',
        'wattage': 0,
        'hours' : 0,
        'quantity' : 1
    })

def remove_appliance(index):
    st.session_state.appliances.pop(index)

def get_ai_recommendation(appliance_data, total_kwh, monthly_cost):
    if not model:
        return "Can't connect with Gemini api, please check api key"
    
    appliances_list = "/n".join([f"-{a['name']}:{a['quantity']} units, {a['wattage']} wat, Use{a['hours']} hours / day"
                                 for a in appliance_data if a['name']
                                 ])
    
    prompt = f"""
    You are an energy saving and Smart home expert in thailand.
    Home electricity usage data:
    {appliances_list}

    Summary:
    -Total electricity usage: {total_kwh:.2f} kwh/month
    -Estimated electricity cost: {monthly_cost:.2f} baht/month
    
    Please analyze and provide recommendations in the following format:

    1. Electricity usage assessment(compared to a typical thai home)
    2. 3-5 specific energy saving recommendations
    3. Appliances that should be replaced/upgraded (if any)
    4. Estimated monthly savings
    5. Environmental impace(how much co2 reduction)

    Please respond in english language only
    Please only give answer no need for excessive greeting
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
    

st.markdown("""
<style>
        .block-container{
            padding-top:2rem;
        }
        h1,h2,h3 {
            text-align: center; 
        }    
            
        div[data-testid-"column"] > div > div > div > p {
            text-align: center;
        }
                   
        div.stButton > button{
            display: block;
            margin: 0 auto;
        }
            
        .feature-card {
            padding: 2rem;
            border-radius: 15px;
            box-shadow 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            color: white;
            height: 230px;
            display: flex;
            align-item: center;
            justify-content: center;
            flex-direction: column;
            background: linear-gradient(135deg, #228b22 0%, #228b22 100%);
        }
            
        .appearance-item{
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 9px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
        }


        .result-box{
            background: linear-gradient(135deg, #FFAA33 0%, #FFAA33 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-top: 2rem; 
            margin-bottom: 2rem;
        }
            
        .result-box h2{
            margin: 0;
            font-size: 2.5rem;
        }
            
        .ai-response-box{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-top: 2rem;  
            margin-bottom: 2rem; 
        }
            
        .ai-response-box h3{
            margin-top : 0;
            color:white;    
        }
            
        button[kind="secondary"]{
            background: #0096FF !important;
            color: white !important;
            border: none !important;    
        }
            
        button[kind="primary"]{
            background: #FF0000 !important;
        }
            
        button[kind="tertiary"]{
            background: #FFBF00 !important;
        }
            
            
        
<style>
""", unsafe_allow_html=True)

if st.session_state.page == "home":

    st.header("Smart house tips")
    st.subheader("Build your smart home system to help us save the word")
    st.divider()
    st.subheader("Features")
    col1, col2, col3 = st.columns([0.3,0.3,0.3], gap = "large")

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h5> Design your power use </h5>
            <p>Specify your home's electricity usage to receive an initial estimate.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h5> Reduce your cost </h5>
            <p> Reduce or optimize energy consumption </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h5> AI Suggestion </h5>
            <p> Here is the AI Suggestion to help you</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.header("Let's design your power")

    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        st.button("Click to design", on_click=go_todesign)
elif st.session_state.page =='design':
    if st.button("<- Back to home"):
        go_to_home()
    st.header("Design your power usage")
    st.subheader("Please fill in your home's electricity usage information")

    st.divider()

    st.subheader("Household Appliances")
   
    
  

    if len(st.session_state.appliances) == 0:
        st.info("Click add electrical appliances to start!")

    common_appliances = {
        "LEDLightbulb": 10,
        "IncandescentLightbulb": 60,
        "Fan": 75,
        "TV": 100,
        "Refrigerator": 150,
        "AirConditioner": 1000
    }

    for i, appliance in enumerate(st.session_state.appliances):
        with st.container():
            st.markdown(f"""
                    <div class="appearance-item">
                        <h4> Appliances #{i+1} </h4>
                    </div>
                    """, unsafe_allow_html=True)
            col1, col2 = st.columns([3,1])

            with col1:
                use_common = st.checkbox(f"Choose order", key = f"common_{i}")
                if use_common:
                    selected = st.selectbox("Choose appliances", options=list(common_appliances.keys()), key=f"select_{i}")
                    st.session_state.appliances[i]['name'] = selected
                    st.session_state.appliances[i]['wattage'] = common_appliances[selected]
                else:
                    name = st.text_input("Name of appliance", value=st.session_state.appliances[i]['name'], placeholder = "Example TV, Air Conditioner", key=f"name_{i}")
                    st.session_state.appliances[i]['name'] = name
            
            with col2:
                st.write("")
                st.write("")
                if st.button("Delete", key=f"delete_{i}", type = 'primary'):
                    remove_appliance(i)
                    st.rerun()
    
            col1, col2, col3 = st.columns(3)
            with col1:
                if not use_common:
                    wattage = st.number_input(
                "Power(Watt)",
                min_value=0,
                value = st.session_state.appliances[i]['wattage'],
                step = 10,
                key = f"watt_{i}",
                help = "You can find this information on the appliance label"
            )
                else:
                    st.metric("Power(Watt)", f"{st.session_state.appliances[i]['wattage']} W")
            with col2:
                hours = st.number_input(
                    "Usage (hr/day)",
                    min_value=0.0,
                    max_value=24.0,
                    value = float(st.session_state.appliances[i]['hours']),
                    step=0.5,
                    key = f"hours_{i}"
            )
                st.session_state.appliances[i]['hours'] = hours
            with col3:
                quantity = st.number_input(
                    "Number (usage)",
                    min_value=1,
                    value = st.session_state.appliances[i]['quantity'],
                    step=1,
                    key = f"quantity_{i}"
            )
                st.session_state.appliances[i]['quantity'] = quantity
            st.divider()
    
    if (len(st.session_state.appliances) >0):
        if st.button("Calculate Electricity Usage", type = "tertiary"):
            total_daily_wh = 0

            for appliance in st.session_state.appliances:
                if appliance['name']:
                    daily_wh = (appliance['wattage'] * appliance['hours'] * appliance['quantity'])
                    total_daily_wh += daily_wh

            total_daily_kwh = total_daily_wh / 1000
            monthly_kwh = total_daily_kwh * 30
            monthly_cost = monthly_kwh * 4

            st.markdown(f"""
                <div class="result-box">
                        <h3>calculation results </h3>
                        <h2>{total_daily_kwh:.2f} kwh / days </h2>
                        <h2>{monthly_kwh:.2f} kwh / months </h2>
                        <h2> approximately {monthly_cost:.2f} baht / month </h2>
                </div>

                """, unsafe_allow_html = True)
            
    if st.button("Add electrical appliances", type="secondary"):
        add_appliance()
    st.divider()
    st.subheader("Details of electricity usage for each appliance")

    breakdown_data = []
    for appliance in st.session_state.appliances:
        if appliance ['name']:
            daily_wh = (appliance['wattage'] * appliance['hours'] * appliance['quantity'])
            daily_kwh = daily_wh / 1000
            monthly_kwh = daily_kwh * 30
            cost = monthly_kwh * 4

            breakdown_data.append({
                'appliance': appliance['name'],
                'quantity' : appliance['quantity'],
                'power(W)' : appliance['wattage'],
                'usage (hr/day)': appliance['hours'],
                'power/day (kwh)' : f"{daily_kwh:.2f}",
                'power/month' : f"{monthly_kwh:.2f}",
                'cost / month (baht)' : f"{cost:.2f}"
            })

    if breakdown_data:
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, width ="stretch")

    st.divider()
    st.subheader("Basic Instructions")

    suggestions = []
    high_power_item = [a for a in st.session_state.appliances if a ['wattage'] * a ['hours'] * a ['quantity'] > 5000]

    if high_power_item:
        for item in high_power_item:
            if "Air" in item ['name']:
                suggestions.append(f"{item['name']}: Set the temperature to 25-26 degrees celcius and clean the filter regularly")
            else:
                suggestions.append(f"{item['name']}: High energy consumption, consider adjusting usage time")

   
    if suggestions:
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.success("You have used energy efficiently!")

    st.divider()
    st.subheader("Do You need some suggestions from AI?")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Asking for advice from AI.", width ="stretch"):
            with st.spinner("AI Analysing"):
                ai_response = get_ai_recommendation(st.session_state.appliances, monthly_kwh, cost)
                st.session_state.ai_response = ai_response

    if st.session_state.ai_response:
        st.markdown("""
        <div class="ai-response-box">
            <h3>Advice from Gemini Ai</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.ai_response)