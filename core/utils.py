from google.cloud import translate

def translate_text(text="Hello, world!", project_id="employiq"):

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

