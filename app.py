import gradio as gr
import pandas as pd
from utils import register_face, recognize_and_mark_multiple, login

def upload_and_register(img, name):
    return register_face(img, name)

# def upload_and_recognize(img):
#     return recognize_and_mark_multiple(img)
def upload_and_recognize(img, class_id):
    return recognize_and_mark_multiple(img, class_id)


def show_attendance():
    df = pd.read_csv("attendance.csv", names=["Name", "Timestamp"])
    return df.tail(10)

# with gr.Blocks() as demo:
#     gr.Markdown("## 🧠 AI Face Recognition Attendance System")

#     with gr.Tab("📥 Register Face"):
#         with gr.Row():
#             reg_img = gr.Image()
#             reg_name = gr.Textbox(label="Enter Name")
#         reg_btn = gr.Button("Register")
#         reg_out = gr.Textbox()
#         reg_btn.click(upload_and_register, inputs=[reg_img, reg_name], outputs=reg_out)

#     # with gr.Tab("✅ Mark Attendance"):
#     #     mark_img = gr.Image()
#     #     mark_btn = gr.Button("Recognize & Mark")
#     #     mark_out = gr.Textbox()
#     #     mark_btn.click(upload_and_recognize, inputs=mark_img, outputs=mark_out)
#     with gr.Tab("✅ Mark Attendance"):
#         mark_img = gr.Image()
#         class_id = gr.Dropdown(["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6"], label="Select Class")
#         mark_btn = gr.Button("Recognize & Mark")
#         mark_out = gr.Textbox()
#         mark_btn.click(upload_and_recognize, inputs=[mark_img, class_id], outputs=mark_out)

#     with gr.Tab("📊 View Attendance Log"):
#         view_btn = gr.Button("Refresh Log")
#         attendance_df = gr.Dataframe()
#         view_btn.click(show_attendance, outputs=attendance_df)

# demo.launch(share=True)

background_css = """
<style>
    body, html {
        height: 100%;
        margin: 0;
        padding: 0;
    }
    .gradio-container {
        background-image: url('https://revaeduin.s3.ap-south-1.amazonaws.com/uploads/images/66e80256542d31726480982.webp');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;  /* keeps background fixed while scrolling */
        color: white;
    }
    .gradio-markdown, .gr-box {
        background: rgba(0, 0, 0, 0.6);  /* semi-transparent background */
        padding: 10px;
        border-radius: 10px;
    }
</style>
"""

with gr.Blocks() as demo:
    gr.HTML(background_css)
    gr.Markdown("## 🔐 Login to Face Recognition Attendance System")

    # Login section
    with gr.Column(visible=True) as login_section:
        user = gr.Textbox(label="Username")
        pwd = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_msg = gr.Textbox(visible=False)
    
    # Main app section (hidden initially)
    with gr.Column(visible=False) as app_section:
        gr.Markdown("## 🧠 AI Face Recognition Attendance System")

        with gr.Tab("📥 Register Face"):
            with gr.Row():
                reg_img = gr.Image()
                reg_name = gr.Textbox(label="Enter Name")
            reg_btn = gr.Button("Register")
            reg_out = gr.Textbox()
            reg_btn.click(upload_and_register, inputs=[reg_img, reg_name], outputs=reg_out)

        # with gr.Tab("✅ Mark Attendance"):
        #     mark_img = gr.Image()
        #     mark_btn = gr.Button("Recognize & Mark")
        #     mark_out = gr.Textbox()
        #     mark_btn.click(upload_and_recognize, inputs=mark_img, outputs=mark_out)
        with gr.Tab("✅ Mark Attendance"):
             mark_img = gr.Image(label="Upload Face Image")
             class_id = gr.Dropdown(
             ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6"],
             label="Select Class"
             )
             mark_btn = gr.Button("Recognize & Mark")
             mark_out = gr.Textbox()
             mark_btn.click(upload_and_recognize, inputs=[mark_img, class_id], outputs=mark_out)

        with gr.Tab("📊 View Attendance Log"):
            view_btn = gr.Button("Refresh Log")
            attendance_df = gr.Dataframe()
            view_btn.click(show_attendance, outputs=attendance_df)

    def login_action(username, password):
        if login(username, password):  # Calls login from utils.py
            return gr.update(visible=False), gr.update(visible=True), ""  # Hide login, show app
        else:
            return gr.update(), gr.update(), "❌ Invalid credentials"
    
    login_btn.click(login_action, inputs=[user, pwd], outputs=[login_section, app_section, login_msg])

demo.launch()




# Add custom HTML with CSS to set a background image

# background_css = """
# <style>
#     .gradio-container {
#         background-image: url('https://revaeduin.s3.ap-south-1.amazonaws.com/uploads/images/66e80256542d31726480982.webp');
#         background-size: cover;
#         background-position: center;
#         height: 100vh;
#         color: white;
#     }
#     .gradio-markdown h2, .gradio-markdown h3, .gradio-markdown p {
#         color: white !important;
#     }
# </style>
# """

# background_css = """
# <style>
#     .gradio-container {
#         background-image: url('https://revaeduin.s3.ap-south-1.amazonaws.com/uploads/images/66e80256542d31726480982.webp');
#         background-size: cover;
#         background-position: center;
#         height: 100vh;
#         color: white;  /* Optional: Change text color to be visible on dark background */
#     }
#     .gradio-markdown {
#         color: white;  /* Optional: Change text color */
#     }
#     /* Make login section background transparent */
#     .gradio-column {
#         background: rgba(255, 255, 255, 0.5);  /* Optional: Semi-transparent background */
#         padding: 30px;
#         border-radius: 10px;
#     }
#     /* Make the input boxes transparent */
#     .gradio-input {
#         background: rgba(255, 255, 255, 0.7) !important;
#         color: white !important;  /* Change text color to white */
#         border: 1px solid #fff !important; /* Optional: Add white border */
#     }
#     /* Make the button background transparent */
#     .gradio-button {
#         background: rgba(255, 255, 255, 0.7) !important;
#         color: black !important;
#         border: 1px solid #fff !important; /* Optional: Add white border */
#     }
# </style>
# """
# def login(username, password):
#     return username == "admin" and password == "admin123"

# def login_action(username, password):
#     if login(username, password):
#         return gr.update(visible=False), gr.update(visible=True), ""
#     else:
#         return gr.update(), gr.update(), "❌ Invalid credentials"

# with gr.Blocks() as demo:
#     gr.HTML(background_css)
#     gr.Markdown("## 🔐 Login to Face Recognition Attendance System")

#     with gr.Column(visible=True) as login_section:
#         user = gr.Textbox(label="Username")
#         pwd = gr.Textbox(label="Password", type="password")
#         login_btn = gr.Button("Login")
#         login_msg = gr.Textbox(visible=False)

#     with gr.Column(visible=False) as app_section:
#         gr.Markdown("## 🧠 AI Face Recognition Attendance System")

#         with gr.Tab("📥 Register Face"):
#             with gr.Row():
#                 reg_img = gr.Image()
#                 reg_name = gr.Textbox(label="Enter Name")
#             reg_btn = gr.Button("Register")
#             reg_out = gr.Textbox()

#         with gr.Tab("✅ Mark Attendance"):
#             mark_img = gr.Image()
#             mark_btn = gr.Button("Recognize & Mark")
#             mark_out = gr.Textbox()

#         with gr.Tab("📊 View Attendance Log"):
#             view_btn = gr.Button("Refresh Log")
#             attendance_df = gr.Dataframe()

#     login_btn.click(login_action, inputs=[user, pwd], outputs=[login_section, app_section, login_msg])
#     reg_btn.click(fn=None, inputs=[reg_img, reg_name], outputs=reg_out)
#     mark_btn.click(fn=None, inputs=mark_img, outputs=mark_out)
#     view_btn.click(fn=None, outputs=attendance_df)

# demo.launch()
