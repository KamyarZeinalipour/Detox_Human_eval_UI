import gradio as gr
import pandas as pd
import time
import os
import random

# ----- CONFIGURATION -----
CSV_PATH = input("Enter your file name: ")

# ----- LOAD OR INITIALIZE DATAFRAME -----
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

# Ensure all required columns exist
base_columns = {
    "rating_model_detox_mian": "",
    "rating_model_detox_lora": "",
    "preferred_transformation": "",
    "user_preferred": "",
    "annotator": "",
    "annotation_time": ""
}
# style-case and swap flag
if "style_case" not in df.columns:
    df["style_case"] = ""
if "swap_flag" not in df.columns:
    df["swap_flag"] = ""  # will store True/False per row

# add any missing base columns
for col, default in base_columns.items():
    if col not in df.columns:
        df[col] = default

# total examples count
TOTAL_EXAMPLES = len(df)

# Prompt for annotator name
annotator = input("Enter your annotator name: ").strip()
while annotator == "":
    annotator = input("Please enter a valid annotator name: ").strip()

# track timer
current_start_time = None


def find_resume_index():
    """
    Find the first index where ratings are incomplete.
    """
    for i, row in df.iterrows():
        if pd.isna(row['rating_model_detox_mian']) or row['rating_model_detox_mian'] == "" \
           or pd.isna(row['rating_model_detox_lora']) or row['rating_model_detox_lora'] == "":
            return i
    return len(df) - 1


def load_example(idx):
    """
    Load the example at idx, decide swap_flag if needed, and return display values.
    """
    global current_start_time, df
    # decide swap once
    if df.at[idx, 'swap_flag'] == "":
        df.at[idx, 'swap_flag'] = random.choice([True, False])
        df.to_csv(CSV_PATH, index=False)

    swapped = df.at[idx, 'swap_flag']
    row = df.loc[idx]
    # start timing
    current_start_time = time.time()

    # raw texts
    original = row['comment']
    m1 = row['model_detox_mian']
    m2 = row['model_detox_lora']

    # load saved ratings/preferences according to swap
    if swapped:
        text_model1, text_model2 = m2, m1
        r1 = row['rating_model_detox_lora'] or None
        r2 = row['rating_model_detox_mian'] or None
        # flip any saved preferences
        pref = None
        upref = None
        if row['preferred_transformation']:
            pref = 'Model 1' if row['preferred_transformation']=='Model 2' else 'Model 2'
        if row['user_preferred']:
            upref = 'Model 1' if row['user_preferred']=='Model 2' else 'Model 2'
    else:
        text_model1, text_model2 = m1, m2
        r1 = row['rating_model_detox_mian'] or None
        r2 = row['rating_model_detox_lora'] or None
        pref = row['preferred_transformation'] or None
        upref = row['user_preferred'] or None

    return (
        original,
        text_model1,
        text_model2,
        r1,
        r2,
        pref,
        upref,
        row.get('style_case', "")
    )


def format_index_text(idx):
    return f"Example {idx+1} out of {TOTAL_EXAMPLES}"


def submit_annotation(idx, rating1, rating2, preferred, user_preferred):
    """
    Save the annotation (mapping back if swapped), then load next.
    """
    global current_start_time, df, annotator
    elapsed = time.time() - (current_start_time or time.time())
    swapped = df.at[idx, 'swap_flag']

    # map ratings back to true columns
    if swapped:
        df.at[idx, 'rating_model_detox_lora'] = rating1 or ""
        df.at[idx, 'rating_model_detox_mian'] = rating2 or ""
        # flip user prefs back
        real_pref = ''
        real_user = ''
        if preferred:
            real_pref = 'Model 2' if preferred=='Model 1' else 'Model 1'
        if user_preferred:
            real_user = 'Model 2' if user_preferred=='Model 1' else 'Model 1'
        df.at[idx, 'preferred_transformation'] = real_pref
        df.at[idx, 'user_preferred'] = real_user
    else:
        df.at[idx, 'rating_model_detox_mian'] = rating1 or ""
        df.at[idx, 'rating_model_detox_lora'] = rating2 or ""
        df.at[idx, 'preferred_transformation'] = preferred or ""
        df.at[idx, 'user_preferred'] = user_preferred or ""

    df.at[idx, 'annotator'] = annotator
    df.at[idx, 'annotation_time'] = elapsed
    df.to_csv(CSV_PATH, index=False)

    # advance
    next_idx = idx+1 if idx+1 < len(df) else idx
    (orig, t1, t2, sr1, sr2, sp, sup, style) = load_example(next_idx)
    return (
        next_idx,
        format_index_text(next_idx),
        orig,
        t1,
        t2,
        sr1,
        sr2,
        sp,
        sup,
        style,
        f"Annotation took {elapsed:.2f} seconds."
    )


def go_previous(idx):
    """
    Move back one example and reload.
    """
    prev_idx = max(0, idx-1)
    (orig, t1, t2, r1, r2, p, up, style) = load_example(prev_idx)
    return (
        prev_idx,
        format_index_text(prev_idx),
        orig,
        t1,
        t2,
        r1,
        r2,
        p,
        up,
        style
    )

# ----- BUILD THE GRADIO INTERFACE -----
with gr.Blocks() as demo:
    current_index_state = gr.State(find_resume_index())
    gr.Markdown("## Annotation Tool")
    gr.Markdown(f"Annotator: {annotator}")

    with gr.Row():
        with gr.Column():
            style_text    = gr.Textbox(label="Style", interactive=False)
            original_text = gr.Textbox(label="Original Text", interactive=False, lines=5)
            model1_text   = gr.Textbox(label="Transformed Text (Model 1)", interactive=False, lines=5)
            model2_text   = gr.Textbox(label="Transformed Text (Model 2)", interactive=False, lines=5)

        with gr.Column():
            rating_options = ["A","B","C","D","E"]
            rating_model1  = gr.Radio(rating_options, label="Rating for Model 1", value=None)
            rating_model2  = gr.Radio(rating_options, label="Rating for Model 2", value=None)
            preferred_trans= gr.Radio(["Model 1","Model 2"], label="Which one keeps the semantics better?", value=None)
            user_pref      = gr.Radio(["Model 1","Model 2"], label="Which one would you prefer for personal usage?", value=None)
            gr.Markdown(
                """
                **Rating Definitions:**
                - **A**: Excellent - detoxified and preserves meaning/style.
                - **B**: Good - minor issues.
                - **C**: Fair - moderate issues.
                - **D**: Poor - major flaws.
                - **E**: Very Poor - meaning lost or toxic content remains.
                """
            )

    with gr.Row():
        prev_btn   = gr.Button("Previous")
        submit_btn = gr.Button("Submit Annotation")
    current_index_txt = gr.Textbox(label="Current Example Index", interactive=False)
    annotation_msg    = gr.Markdown("")

    # callbacks
    submit_btn.click(
        submit_annotation,
        inputs=[current_index_state, rating_model1, rating_model2, preferred_trans, user_pref],
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans, user_pref,
                 style_text, annotation_msg]
    )
    prev_btn.click(
        go_previous,
        inputs=current_index_state,
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans, user_pref,
                 style_text]
    )

    def load_initial():
        idx = find_resume_index()
        (orig, t1, t2, r1, r2, p, up, style) = load_example(idx)
        return (idx, format_index_text(idx), orig, t1, t2, r1, r2, p, up, style, "")

    demo.load(
        load_initial,
        inputs=[],
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans, user_pref,
                 style_text, annotation_msg]
    )

if __name__ == "__main__":
    demo.launch()
