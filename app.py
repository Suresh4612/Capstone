from flask import Flask, render_template, request, redirect, url_for
from getpass import getpass
import os
import replicate
import base64



app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Set up Replicate API token
REPLICATE_API_TOKEN = getpass("Enter your Replicate API token: ")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


def run_replicate_model(image_path):
    try:
        output = replicate.run(
            "microsoft/bringing-old-photos-back-to-life:c75db81db6cbd809d93cc3b7e7a088a351a3349c9fa02b6d393e35e0d51ba799",
            input={"HR": False, "image": open(image_path, "rb"), "with_scratch": True},
        )
        return output
    except Exception as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    uploaded_image = None
    restored_image = None
    loading = False
    if request.method == "POST":
        # Check if a file was submitted
        if "file" in request.files:
            file = request.files["file"]

            # Check if the file is not empty
            if file.filename != "":
                # Save the file to the server
                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                 file.save(file_path)

        with open(file_path, "rb") as image_file:
            uploaded_image = base64.b64encode(image_file.read()).decode("utf-8")

            # Run the Replicate model
            loading = False
            restored_image = run_replicate_model(f"static/uploads/{file.filename}")
            loading = True
            return render_template("result.html", uploaded_image=uploaded_image, restored_image=restored_image)

    return render_template("index.html", uploaded_image=uploaded_image, restored_image=restored_image)

if __name__ == "__main__":
    app.run(debug=True)