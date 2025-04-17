import gradio as gr
import pandas as pd
import time
import os

# ----- CONFIGURATION -----
CSV_PATH = input("Enter your file name: ")

# ----- GLOBALS -----
# Load the CSV file.
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

# Ensure the annotation columns exist.
new_columns = {
    "rating_model_detox_mian": "",
    "rating_model_detox_lora": "",
    "preferred_transformation": "",
    "user_preferred": "",  # New column for personal usage preference
    "annotator": "",
    "annotation_time": ""
}
# Optionally, add default for style_case if not already present.
if "style_case" not in df.columns:
    df["style_case"] = ""
    
for col, default in new_columns.items():
    if col not in df.columns:
        df[col] = default

# Get total examples count.
TOTAL_EXAMPLES = len(df)

# Prompt user for annotator name on the terminal.
annotator = input("Enter your annotator name: ").strip()
while annotator == "":
    annotator = input("Please enter a valid annotator name: ").strip()

# A variable to hold the start time for each annotation.
current_start_time = None

def find_resume_index():
    """
    Return the first row that has not been annotated (i.e. an empty rating).
    If all rows have annotations, return the last row.
    """
    for i, row in df.iterrows():
        if (pd.isna(row['rating_model_detox_mian']) or row['rating_model_detox_mian'] == "") \
           or (pd.isna(row['rating_model_detox_lora']) or row['rating_model_detox_lora'] == ""):
            return i
    return len(df) - 1

def load_example(idx):
    """
    Given the index, load the texts and any stored annotation values.
    Also, start/reset the timer.
    Returns:
      comment_text, text_model1, text_model2, rating1, rating2, preferred, user_pref, style
    """
    global current_start_time
    if idx < 0 or idx >= len(df):
        # Defensive: if index out of range, return an error message.
        return "Index out of range", "", "", None, None, None, None, ""
    row = df.loc[idx]
    current_start_time = time.time()  # start timer
    
    comment_text = row["comment"]
    text_model1 = row["model_detox_mian"]
    text_model2 = row["model_detox_lora"]
    rating1 = row["rating_model_detox_mian"] if row["rating_model_detox_mian"] != "" else None
    rating2 = row["rating_model_detox_lora"] if row["rating_model_detox_lora"] != "" else None
    preferred = row["preferred_transformation"] if row["preferred_transformation"] != "" else None
    user_pref = row["user_preferred"] if row["user_preferred"] != "" else None
    style = row["style_case"] if row["style_case"] != "" else ""
    return comment_text, text_model1, text_model2, rating1, rating2, preferred, user_pref, style

def format_index_text(idx):
    """ Format the index display as 'Example X out of N'. """
    return f"Example {idx+1} out of {TOTAL_EXAMPLES}"

def submit_annotation(idx, rating1, rating2, preferred, user_preferred):
    """
    On clicking submit, record the elapsed time and update the CSV.
    Then load the next annotation example.
    """
    global current_start_time, df, annotator
    if current_start_time is None:
        annotation_duration = 0
    else:
        annotation_duration = time.time() - current_start_time

    # Update the dataframe with the new annotations.
    df.at[idx, "rating_model_detox_mian"] = rating1 if rating1 is not None else ""
    df.at[idx, "rating_model_detox_lora"] = rating2 if rating2 is not None else ""
    df.at[idx, "preferred_transformation"] = preferred if preferred is not None else ""
    df.at[idx, "user_preferred"] = user_preferred if user_preferred is not None else ""
    df.at[idx, "annotator"] = annotator
    df.at[idx, "annotation_time"] = annotation_duration

    df.to_csv(CSV_PATH, index=False)
    
    # Advance to the next example (if exists)
    next_idx = idx + 1 if idx + 1 < len(df) else idx

    # Load the new example.
    (comment_text, text_model1, text_model2, saved_rating1,
     saved_rating2, saved_preferred, saved_user_pref, saved_style) = load_example(next_idx)
    return (next_idx, format_index_text(next_idx),
            comment_text, text_model1, text_model2,
            saved_rating1, saved_rating2, saved_preferred, saved_user_pref, saved_style,
            f"Annotation took {annotation_duration:.2f} seconds.")

def go_previous(current_idx):
    """
    Step back one example index. If already at start (0), then stay there.
    """
    new_idx = current_idx - 1 if current_idx > 0 else 0
    (comment_text, text_model1, text_model2, saved_rating1,
     saved_rating2, saved_preferred, saved_user_pref, saved_style) = load_example(new_idx)
    return (new_idx, format_index_text(new_idx),
            comment_text, text_model1, text_model2,
            saved_rating1, saved_rating2, saved_preferred, saved_user_pref, saved_style)

# ----- BUILD THE GRADIO INTERFACE -----
with gr.Blocks() as demo:
    
    # State variable to save the current row index.
    current_index_state = gr.State(find_resume_index())
    
    gr.Markdown("## Annotation Tool")
    gr.Markdown(f"Annotator: {annotator}")
    with gr.Row():
        with gr.Column():
            
            # Display the current example count.
            
            # Read-only textboxes.
            style_text = gr.Textbox(label="Style", interactive=False)
            original_text = gr.Textbox(label="Original Text", interactive=False, lines=5)
            model1_text = gr.Textbox(label="Transformed Text (Model 1)", interactive=False, lines=5)
            model2_text = gr.Textbox(label="Transformed Text (Model 2)", interactive=False, lines=5)
            
            
            # Display rating definitions addressing both toxicity reduction and meaning preservation.

        with gr.Column():
            # Radio buttons for ratings.
            rating_options = ["A", "B", "C", "D", "E"]
            rating_model1 = gr.Radio(choices=rating_options, label="Rating for Model 1", value=None)
            rating_model2 = gr.Radio(choices=rating_options, label="Rating for Model 2", value=None)
            
            # Radio button for semantic preservation judgment.
            preferred_trans = gr.Radio(choices=["Model 1", "Model 2"], label="Which one keeps the semantics better?", value=None)
            
            # Additional radio button for personal usage preference.
            user_pref = gr.Radio(choices=["Model 1", "Model 2"], label="Which one would you prefer for personal usage?", value=None)
            rating_definition = gr.Markdown(
                                """
                                **Rating Definitions (considering both toxicity reduction and meaning preservation):**
                                - **A**:  Excellent -  Detoxified, meaning and original style preserved, and matches the target style perfectly.
                                - **B**: Good -  Mostly successful, with minor issues in one area (e.g., slight style shift or wording change).
                                - **C**: Fair - Adequate attempt, but moderate issues in meaning, style, detoxification, or target tone. 
                                - **D**: Poor - Major flaws in meaning or tone, or detoxification is incomplete or overdone. 
                                - **E**: Very Poor - Meaning is lost, toxic content remains, or the output ignores the target style entirely.
                                """
                            )
            

        # Buttons for submission and going back.
    with gr.Row():
        prev_btn = gr.Button("Previous")
        submit_btn = gr.Button("Submit Annotation")
    current_index_txt = gr.Textbox(label="Current Example Index", interactive=False)
    annotation_message = gr.Markdown("")

    # Callback for submit.
    submit_btn.click(
        submit_annotation,
        inputs=[current_index_state, rating_model1, rating_model2, preferred_trans, user_pref],
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans, user_pref, style_text,
                 annotation_message]
    )
    
    # Callback for previous.
    prev_btn.click(
        go_previous,
        inputs=current_index_state,
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans, user_pref, style_text]
    )
    
    # Load the initial example on startup.
    def load_initial():
        idx = find_resume_index()
        (comment_text, text_model1, text_model2, saved_rating1,
         saved_rating2, saved_preferred, saved_user_pref, saved_style) = load_example(idx)
        return (idx, format_index_text(idx),
                comment_text, text_model1, text_model2,
                saved_rating1, saved_rating2, saved_preferred, saved_user_pref, saved_style, "")
    
    demo.load(load_initial, inputs=[], outputs=[current_index_state, current_index_txt,
                                                  original_text, model1_text, model2_text,
                                                  rating_model1, rating_model2, preferred_trans, user_pref, style_text, annotation_message])
    
demo.launch()
