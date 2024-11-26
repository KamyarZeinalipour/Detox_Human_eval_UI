import os
import time
import gradio as gr
import pandas as pd
import fire

def list_dir(folder, **kwargs):
    dir_only = kwargs.get("dir_only", False)
    files_only = kwargs.get("files_only", False)
    extension_filter = kwargs.get("extension_filter", "")
    assert not (dir_only and files_only and extension_filter), \
        "Arguments dir_only, files_only and extension_filter are mutually exclusive"

    apply_recursively = kwargs.get("apply_recursively", False)

    dir_text = []
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        dir_text.append(path)
        if apply_recursively and os.path.isdir(path):
            dir_text.extend(list_dir(folder=path, **kwargs))

    if dir_only:
        dir_text = [path for path in dir_text if os.path.isdir(path)]
    elif files_only:
        dir_text = [path for path in dir_text if os.path.isfile(path)]
    elif extension_filter:
        dir_text = [path for path in dir_text if path.endswith(extension_filter)]

    return dir_text

def get_start_index(anns_filepath, start_index):
    anns_df = pd.read_csv(anns_filepath)
    return max([start_index] + anns_df.index.tolist()) + 1

def main(current_index: int = 0, annotator_name: str = "", examples_batch_folder: str = ''):
    css = """
    body, input, textarea, button { 
        font-family: Arial, sans-serif; 
    }
    """

    assert annotator_name, "Annotator name MISSING. Set it when you launch the script"
    assert examples_batch_folder, "Examples' batch MISSING. Set it when you launch the script"

    _, dataset_filename = os.path.split(examples_batch_folder)
    chunk_df = pd.read_csv(examples_batch_folder)
    chunk_df['Transformed'] = chunk_df['Transformed'].fillna('[empty]')

    annotations_folder = os.path.join(os.getcwd(), "annotations")
    anns_filepath = os.path.join(annotations_folder, f"annotations_{dataset_filename}")

    if os.path.exists(anns_filepath):
        current_index = get_start_index(anns_filepath, current_index)
    else:
        os.makedirs(annotations_folder, exist_ok=True)

    print(f"Resume annotations process from {current_index}")
    df_row = chunk_df.iloc[current_index]

    def get_word_count(text):
        words = text.split()
        return len(words)

    # Added transformation_reason as an input parameter and in outputs
    def store_annotation_and_get_next(curr_idx, rating, selected_classes, suggested_transformation, transformation_reason, validate_btn):
        if rating is None or rating == '':
            return [curr_idx, gr.update(interactive=False), df_row['text'], df_row['Transformed'], df_row['Form'], df_row.get('Class', ''), gr.update(value=None), selected_classes, suggested_transformation, transformation_reason]

        # Check if no classes were selected
        if not selected_classes:
            suggested_class = "[Correct Classification]"
        else:
            # Concatenate selected classes with brackets
            suggested_class = ''.join(f"[{cls}]" for cls in selected_classes)
        
        if not suggested_transformation:
            suggested_transformation = "No Suggestion"

        if not transformation_reason:
            transformation_reason = "No Suggestion"

        if os.path.exists(anns_filepath):
            anns_df = pd.read_csv(anns_filepath)
        else:
            cols = chunk_df.columns.tolist()
            cols.extend(["timestamp", "rating", "annotator", "suggested_class", "suggested_transformation", "transformation_reason"])
            anns_df = pd.DataFrame(columns=cols)

        row = chunk_df.iloc[curr_idx].to_dict()
        row["timestamp"] = time.time()
        row["rating"] = rating
        row["annotator"] = annotator_name
        row["suggested_class"] = suggested_class
        row["suggested_transformation"] = suggested_transformation
        row["transformation_reason"] = transformation_reason  # Store transformation reason
        anns_df = pd.concat((anns_df, pd.DataFrame(row, index=[0])), ignore_index=True)
        anns_df.to_csv(anns_filepath, index=False)

        next_idx = curr_idx + 1
        if next_idx < len(chunk_df):
            next_df_row = chunk_df.iloc[next_idx]
            return [next_idx, gr.update(interactive=False), next_df_row['text'], next_df_row['Transformed'], next_df_row['Form'], next_df_row.get('Class', ''), gr.update(value=None), [], '', '']
        else:
            return [curr_idx, gr.update(interactive=False), "End of dataset", '[empty]', '[empty]', '', gr.update(value=None), [], '', '']

    # Function to enable or disable the Validate button based on the rating selection
    def enable_button(rating):
        if rating:
            return gr.update(interactive=True)
        else:
            return gr.update(interactive=False)

    with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
        index = gr.Number(value=current_index, visible=False, precision=0)

        gr.Markdown(f"#### Annotating: {dataset_filename}\n")
        with gr.Row():
            with gr.Column():
                text = gr.Textbox(label="Text", interactive=False, value=df_row['text'])
                Class = gr.Textbox(label="Class", interactive=False, value=df_row.get('Class', ''))
                suggested_class = gr.CheckboxGroup(
                    choices=[
                        "Hate Speech",
                        "Threat",
                        "Insult",
                        "Profanity",
                        "Misinformation",
                        "Discrimination",
                        "Harassment",
                        "Manipulation or Coercion",
                        "Not Toxic"
                    ], 
                    label="Suggested Class"
                )
                gr.Markdown("**[Hate Speech]**: Language that attacks or demeans individuals based on race, religion, gender, or other personal characteristics.")
                gr.Markdown("**[Threat]**: Language expressing intent to cause harm or instill fear.")
                gr.Markdown("**[Insult]**: Language that belittles or degrades an individual or group.")
                gr.Markdown("**[Profanity]**: Obscene or offensive language not necessarily targeting anyone but considered inappropriate.")
                gr.Markdown("**[Misinformation]**: False or misleading statements that could harm or mislead.")
                gr.Markdown("**[Discrimination]**: Language that reinforces stereotypes or discriminates against a group.")
                gr.Markdown("**[Harassment]**: Persistent or repeated language targeting or intimidating an individual or group.")
                gr.Markdown("**[Manipulation or Coercion]**: Language intended to control, pressure, or exploit someone’s emotions or actions.")
                gr.Markdown("**[Not Toxic]**: If the sentence is not toxic.")

            with gr.Column():
                transformed = gr.Textbox(value=df_row['Transformed'], label="Transformed", interactive=False)
                Form = gr.Textbox(label="Form", interactive=False, value=df_row['Form'])
                suggested_transformation = gr.Textbox(label="Suggested Transformation", interactive=True)
                # Added a new textbox for Transformation Reason
                transformation_reason = gr.Textbox(label="Transformation Reason", interactive=True)
                rating_radio = gr.Radio(
                    ["A", "B", "C", "D", "E", "SKIPPING"], 
                    label="Rating"
                )
                # Initialize the Validate button as non-interactive (disabled)
                eval_btn = gr.Button("Validate", interactive=False)

                gr.Markdown("**Rating-A**: The text is perfectly classified, seamlessly transformed to the target tone, and fully preserves the original meaning.")
                gr.Markdown("**Rating-B**: The text is accurately classified, effectively transformed into the target tone, and retains the original meaning with negligible changes.")
                gr.Markdown("**Rating-C**: The text is mostly classified correctly, with some effective tone transformation and minor meaning inconsistencies.")
                gr.Markdown("**Rating-D**: The text has partial classification errors, limited tone transformation, and alters some key meanings.")
                gr.Markdown("**Rating-E**: The text is incorrectly classified, fails to change tone effectively, and loses the original meaning.")

            # Trigger enable_button when the rating_radio value changes
            rating_radio.change(
                enable_button,
                inputs=rating_radio,
                outputs=eval_btn
            )

        # Modified inputs and outputs to include transformation_reason
        eval_btn.click(
            store_annotation_and_get_next,
            inputs=[index, rating_radio, suggested_class, suggested_transformation, transformation_reason, eval_btn],
            outputs=[index, eval_btn, text, transformed, Form, Class, rating_radio, suggested_class, suggested_transformation, transformation_reason]
        )

    demo.launch()

if __name__ == "__main__":
    fire.Fire(main)
