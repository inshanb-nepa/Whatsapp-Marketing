import streamlit as st
import pandas as pd
import pyautogui
import time
import pywhatkit as kit
from PIL import Image
import uuid
import os
import pyodbc
from sqlalchemy import create_engine, Table, Column, String, MetaData
from sqlalchemy.engine import URL
from sqlalchemy import inspect
import ast

st.title("Products Marketing via WhatsApp Desktop")


df_prod = pd.read_csv("Product Variant_product.product.csv")
st.write("Products DataFrame:")
st.dataframe(df_prod)
df_prod.rename(columns={"ID": "Product_ID"}, inplace=True)

# -----------Testing-----------
main_df = pd.read_excel("Demo.xlsx")
st.dataframe(main_df)
# -----------------------------

output_folder = "saved_images"
os.makedirs(output_folder, exist_ok=True)


def image():
    # Create or set the folder where images will be saved
    image_files = [
        f
        for f in os.listdir(output_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    return image_files


def image_selection():
    uploaded_image = st.file_uploader(
        "Upload an image", type=["png", "jpg", "jpeg"], key="banner_upload"
    )
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        filename = uploaded_image.name  # Use original filename
        save_path = os.path.join("saved_images", filename)
        image.save(save_path)
        st.write(f"File saved as: {filename}")

        return filename
    return None


try:
    image_files = image()
    image_options = ["-- 'Add Banner' --"] + image_files
    image_select = st.selectbox(
        "Select Image/Add Banner:", image_options, index=0, key=2
    )
    if image_select == "-- 'Add Banner' --":
        final_image = image_selection()
    else:
        final_image = image_select

    send_now = st.button("Send Message")
    if send_now:
        try:

            for _, row in main_df.iterrows():
                recom = row["Recommendation"]
                recomm = recom.split("--")[0:7]
                # product_link = f"https://www.nepawholesale.com/{row['Website_URL']}"
                recom_id = row["Recommendation_id"]
                recomm_id = recom_id.split("--")[0:7]

                phone = str(row["phoneNumber"]).strip()
                if not phone.startswith("+"):
                    phone = "+977" + phone  # Adjust country code

                # message = f"Hi!\n{message_to_send}\nRecommended Products:\n{recomm}"
                message = [
                    "Hi!\n\n"
                    "Warm Greetings!\n\n"
                    "Thank you for shopping at NepaWholesale Inc. We are glad that you visited us.\n\n"
                    "As per your recent purchases, here are recommended products for you!\n\n"
                    "Recommended Products:\n"
                ]
                df_prod["Product_ID"] = df_prod["Product_ID"].astype(int)
                recomm_id = [int(i) for i in recomm_id]

                df_link = df_prod[df_prod["Product_ID"].isin(recomm_id)]

                # print(recomm_id)
                # print(df_link)

                image_select = os.path.join("saved_images", final_image)  # ✅

                for name, pid in zip(recomm, recomm_id):
                    matched_row = df_prod[df_prod["Product_ID"] == pid]
                    if not matched_row.empty:
                        url_link = (
                            "https://www.nepawholesale.com"
                            + matched_row.iloc[0]["Website_URL"]
                        )

                        message.append(f"•{name}\n Url: {url_link}\n")

                message.append(
                    f"We are glad that you have become a part of NepaWholesale Inc.\n\nYou are welcome to shop at us, anytime.\n\nThank You Once Again &\nHave a great day."
                )

                # Combine and send message
                message = "\n".join(message)
                # encoded_msg = urllib.parse.quote(message)
                time.sleep(5)
                try:
                    kit.sendwhats_image(phone, image_select, message)
                    time.sleep(10)
                    pyautogui.hotkey("ctrl", "w")
                    st.success(f"Message Sent to {phone}.")
                    time.sleep(5)
                except Exception as e:
                    st.error(f"Failed to send to {phone}: {str(e)}")
                    pyautogui.press("esc")
                    time.sleep(3)
                    continue
            st.success("All messages sent successfully!")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
except Exception as e:
    st.error(f"Unexpected error: {str(e)}")
