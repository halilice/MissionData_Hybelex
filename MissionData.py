# Importing the package
import streamlit as st

# Importing the module
from visualisations import home, basic_indic, geog_dist, range_veh, tesla_map, nissan_map, chevrolet_map, ford_map

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://clipart-library.com/new_gallery/120-1209434_nutritional-content-green-transparent-background-png.png");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
     
     
     menu = ["Home", "Basic Indicators",  "Geographic Distribution", 
             "Vehicule Ranges"]

     choice = st.sidebar.selectbox("Menu", menu)

     if choice == "Home":
          st.title("Mission Data Project")
          st.text("""
             This is project that I implemented in a workshop called Mission Data in formation
             program of Wild Code School. I analysed the electric vehicle dataset of Washington
             in three days under rules of workshop and I deployed it on Streamlit. In addition 
             that, I made a presentation on Canvas website.
             The client is managing the fleet of electric and hybrid cars in different states 
             of the country and they demanded from me to analyse the dataset deeply for seeing 
             which areas need improvement.
                  """)
          home()

     elif choice == "Basic Indicators":
         basic_indic()


     elif choice == "Geographic Distribution":
         submenu = ["General Info", "Tesla", "Nissan", "Chevrolet", "Ford"]
         choice_sub = st.sidebar.selectbox("Drop down to choose", submenu)
         if choice_sub == "General Info":
             geog_dist()
         elif choice_sub == "Tesla":
             tesla_map()
         elif choice_sub == "Nissan":
             nissan_map()
         elif choice_sub == "Chevrolet":
             chevrolet_map()
         else:
             ford_map()

     else:
          range_veh()
       
main()