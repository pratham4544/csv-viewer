import streamlit as st
import pandas as pd
import base64
import qrcode
from PIL import Image
import numpy as np
import streamlit as st
import base64
from io import BytesIO
from numpy import asarray


def main():
    st.title('CSV Row Information Viewer')

    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader('CSV File Information')
        # st.write(df.head())  # Displaying the first few rows of the uploaded CSV.

        current_index = st.empty()  # Placeholder to display current index
        current_index_number = st.empty()  # Placeholder to display current row number

    # Initializing index to 0 (first row)
        index = st.number_input('Enter Index:', value=0, step=1, min_value=0, max_value=len(df) - 1)

   

    # Ensure index stays within the bounds of the dataframe
        index = min(index, len(df) - 1)
        index = max(index, 0)

        # current_index.number_input('Current Index:', value=index, step=1, min_value=0, max_value=len(df) - 1)

        # current_index_number.markdown(f'Current Row: **{index + 1} / {len(df)}**')


        show_single_row(df,index)
        show_qr_code(df,index)
        
        current_index_number.markdown(f'Current Row: **{index + 1} / {len(df)}**')

        if st.button("Download CSV"):
     # Create a link to download the modified CSV file
            csv_file = df.to_csv(index=False)
            b64 = base64.b64encode(csv_file.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="modified_data.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

    

def show_single_row(df,index):
    st.subheader('Single Row Viewer')

    # Display row information in separate big-sized text areas
    st.write(f"## Row {index + 1}")
    for column_name, column_value in df.iloc[index].items():
        if pd.isnull(column_value):
            column_value = ""  # Replace NaN values with empty string for text_input
        modified_value = st.text_area(f"### {column_name}", value=str(column_value), height=60)
        df.at[index, column_name] = modified_value  # Update the dataframe with modified value


    
def show_qr_code(df,index):
    # bank_account_number = st.text_input('Enter Bank Account Numebr : ')#'6999413500377638'
    name = df.iloc[index]['Name']  # 'YESB0CMSNOC'
    upi_id = df.iloc[index]['Mention UPI ID for the reward']


    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # L -> M -> Q -> H
        box_size=4,
        border=4,
    )

    qr.add_data('upi://pay?pa='+upi_id +
                '&pn='+str(name)+'&cu=INR')

    img = qr.make_image(fill_color="black", back_color="white")

    img = img.resize((300, 300))

    st.write('UPI QR Code : ')
    st.write(name)
    st.image(img)

    return img


        
def next_index(index):
    if st.button('Next'):
        index += 1  # Increment index on button press

if __name__ == "__main__":
    main()
