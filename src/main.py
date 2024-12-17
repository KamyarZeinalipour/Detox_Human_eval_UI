import os
import time
import gradio as gr
import pandas as pd
import fire

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
    
    # Ensure 'Neutral', 'Formal', 'Friendly' columns exist and fill NaN with '[empty]'
    for col in ['Neutral', 'Formal', 'Friendly']:
        if col not in chunk_df.columns:
            chunk_df[col] = '[empty]'
        else:
            chunk_df[col] = chunk_df[col].fillna('[empty]')

    annotations_folder = os.path.join(os.getcwd(), "annotations")
    anns_filepath = os.path.join(annotations_folder, f"annotations_{dataset_filename}")

    if os.path.exists(anns_filepath):
        current_index = get_start_index(anns_filepath, current_index)
    else:
        os.makedirs(annotations_folder, exist_ok=True)

    print(f"Resume annotations process from {current_index}")
    df_row = chunk_df.iloc[current_index]

    # Function to store annotations and get the next data entry
    def store_annotation_and_get_next(curr_idx, selected_classes, comments, 
                                      rating_neutral, suggested_transformation_neutral,
                                      rating_formal, suggested_transformation_formal,
                                      rating_friendly, suggested_transformation_friendly):
        # Check if any rating is missing
        if any(rating is None or rating == '' for rating in [rating_neutral, rating_formal, rating_friendly]):
            # Optionally, display a warning message
            # gr.warning("Please select ratings for all transformed texts.")
            return [curr_idx, gr.update(interactive=False), df_row['text'], 
                    df_row['Neutral'], df_row['Formal'], df_row['Friendly'], df_row.get('Class', ''), 
                    selected_classes, comments, 
                    rating_neutral, suggested_transformation_neutral,
                    rating_formal, suggested_transformation_formal,
                    rating_friendly, suggested_transformation_friendly]

        # Process suggested classes
        if not selected_classes:
            suggested_class = "[Correct Classification]"
        else:
            suggested_class = ''.join(f"[{cls}]" for cls in selected_classes)

        if not comments:
            comments = "No Comments"    
        
        # Handle suggested transformations
        if not suggested_transformation_neutral:
            suggested_transformation_neutral = "No Suggestion"
        if not suggested_transformation_formal:
            suggested_transformation_formal = "No Suggestion"
        if not suggested_transformation_friendly:
            suggested_transformation_friendly = "No Suggestion"

        if os.path.exists(anns_filepath):
            anns_df = pd.read_csv(anns_filepath)
        else:
            cols = chunk_df.columns.tolist()
            additional_cols = ["timestamp", "annotator", "suggested_class",  "comments",
                               "Rating_Neutral", "Suggested_Transformation_Neutral",
                               "Rating_Formal", "Suggested_Transformation_Formal",
                               "Rating_Friendly", "Suggested_Transformation_Friendly"]
            cols.extend(additional_cols)
            anns_df = pd.DataFrame(columns=cols)

        row = chunk_df.iloc[curr_idx].to_dict()
        row["timestamp"] = time.time()
        row["annotator"] = annotator_name
        row["suggested_class"] = suggested_class
        row["comments"] = comments 
        row["Rating_Neutral"] = rating_neutral
        row["Suggested_Transformation_Neutral"] = suggested_transformation_neutral
        row["Rating_Formal"] = rating_formal
        row["Suggested_Transformation_Formal"] = suggested_transformation_formal
        row["Rating_Friendly"] = rating_friendly
        row["Suggested_Transformation_Friendly"] = suggested_transformation_friendly

        anns_df = pd.concat((anns_df, pd.DataFrame(row, index=[0])), ignore_index=True)
        anns_df.to_csv(anns_filepath, index=False)

        next_idx = curr_idx + 1
        if next_idx < len(chunk_df):
            next_df_row = chunk_df.iloc[next_idx]
            return [next_idx, gr.update(interactive=False), next_df_row['text'], 
                    next_df_row['Neutral'], next_df_row['Formal'], next_df_row['Friendly'], next_df_row.get('Class', ''), 
                    [], '',
                    None, '', None, '', None, '']
        else:
            return [curr_idx, gr.update(interactive=False), "End of dataset", 
                    "End of dataset", "End of dataset", "End of dataset", "End of dataset", 
                    [], "End of dataset",
                    None, "End of dataset", None, "End of dataset", None, "End of dataset"]

    # Function to enable or disable the Validate button based on ratings
    def enable_button(rating_neutral_value, rating_formal_value, rating_friendly_value):
        if all([rating_neutral_value, rating_formal_value, rating_friendly_value]):
            return gr.update(interactive=True)
        else:
            return gr.update(interactive=False)

    with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
        index = gr.Number(value=current_index, visible=False, precision=0)

        gr.Markdown(f"#### Annotating: {dataset_filename}\n")
        with gr.Row():
            with gr.Column():
                # Display the original text and class
                text = gr.Textbox(label="Text", interactive=False, value=df_row['text'])
                Class = gr.Textbox(label="Class", interactive=False, value=df_row.get('Class', ''))

                # Suggested class and comments
                suggested_class = gr.CheckboxGroup(
                    choices=[
                        "Insult",
                        "Threat",
                        "Obscene",
                        "Identity_attack",
                        "Sexual_explicit",
                        "Not Toxic"
                    ], 
                    label="Suggested Class"
                )
                comments = gr.Textbox(label="Comments")

                # Validate button (will be enabled based on ratings)
                eval_btn = gr.Button("Validate", interactive=False)
                markdown_content = """
### **Class Definitions and Descriptions**

#### **1. Obscene**
- **Definition**: Language or content that is offensive, vulgar, or indecent.
- **Description**: Obscene material includes swearing, crude or sexually explicit language, or graphic imagery intended to shock or offend. It typically violates community standards of decency.

---

#### **2. Threat**
- **Definition**: Statements or actions indicating an intent to cause harm to someone or something.
- **Description**: Threats involve direct or implied messages of violence, harm, or coercion. They can be targeted at individuals, groups, or entities, creating fear or intimidation.

---

#### **3. Insult**
- **Definition**: Language intended to demean, mock, or offend a person or group.
- **Description**: Insults can include derogatory remarks, name-calling, or ridicule aimed at belittling others. They often involve personal attacks and are meant to provoke or hurt emotionally.

---

#### **4. Identity Attack**
- **Definition**: Language that targets or demeans individuals based on inherent aspects of their identity.
- **Description**: Identity attacks include hateful or discriminatory statements about race, ethnicity, religion, gender, sexual orientation, disability, or other identity traits. Such language perpetuates prejudice and marginalization.

---

#### **5. Sexual Explicit**
- **Definition**: Content that is overtly sexual in nature or depicts sexual acts in an explicit manner.
- **Description**: Sexual explicit material includes graphic or suggestive descriptions of sexual acts, imagery, or innuendo. This class covers anything from crude sexual remarks to explicit depictions that are inappropriate in many contexts.
"""         

                gr.Markdown(markdown_content)


            with gr.Column():
                # Transformed texts and their ratings
                transformed_neutral = gr.Textbox(value=df_row['Neutral'], label="Transformed Neutral", interactive=False)
                rating_neutral = gr.Radio(
                    ["A", "B", "F", "SKIPPING"], 
                    label="Rating Neutral"
                )
                suggested_transformation_neutral = gr.Textbox(label="Suggested Transformation Neutral", interactive=True)

                transformed_formal = gr.Textbox(value=df_row['Formal'], label="Transformed Formal", interactive=False)
                rating_formal = gr.Radio(
                    ["A", "B", "F", "SKIPPING"], 
                    label="Rating Formal"
                )
                suggested_transformation_formal = gr.Textbox(label="Suggested Transformation Formal", interactive=True)

                transformed_friendly = gr.Textbox(value=df_row['Friendly'], label="Transformed Friendly", interactive=False)
                rating_friendly = gr.Radio(
                    ["A", "B", "F", "SKIPPING"], 
                    label="Rating Friendly"
                )
                suggested_transformation_friendly = gr.Textbox(label="Suggested Transformation Friendly", interactive=True)
                markdown_content_v2 = """
### **Ratings Definitions**

#### **Rating-A**: *Gold Standard*  
- The toxic text is rewritten to be as non-toxic as possible while perfectly preserving the original meaning, and the rewritten version aligns seamlessly with the target tone.

---

#### **Rating-B**: *Silver Standard*  
- The toxic text is rewritten to be mostly non-toxic while largely preserving the original meaning, and the rewritten version approaches the target tone but may have minor imperfections.

---

#### **Rating-F**: *Insufficient*  
- The toxic text remains inadequately rewritten, the meaning deviates significantly, or the rewritten version fails to achieve the target tone.

---

#### **SKIPPING**  
- Skip this entry if you cannot provide a rating.
"""             
               
                gr.Markdown(markdown_content_v2)

                # Function to update the Validate button based on ratings
                def update_validate_button(rating_neutral_value, rating_formal_value, rating_friendly_value):
                    return enable_button(rating_neutral_value, rating_formal_value, rating_friendly_value)

                # Attach change events to ratings
                rating_neutral.change(
                    update_validate_button,
                    inputs=[rating_neutral, rating_formal, rating_friendly],
                    outputs=eval_btn
                )
                rating_formal.change(
                    update_validate_button,
                    inputs=[rating_neutral, rating_formal, rating_friendly],
                    outputs=eval_btn
                )
                rating_friendly.change(
                    update_validate_button,
                    inputs=[rating_neutral, rating_formal, rating_friendly],
                    outputs=eval_btn
                )

            # Click event for the Validate button
            eval_btn.click(
                store_annotation_and_get_next,
                inputs=[
                    index, suggested_class, comments,
                    rating_neutral, suggested_transformation_neutral,
                    rating_formal, suggested_transformation_formal,
                    rating_friendly, suggested_transformation_friendly
                ],
                outputs=[
                    index, eval_btn, text,
                    transformed_neutral, transformed_formal, transformed_friendly, 
                    Class, suggested_class, comments,
                    rating_neutral, suggested_transformation_neutral,
                    rating_formal, suggested_transformation_formal,
                    rating_friendly, suggested_transformation_friendly
                ]
            )

        demo.launch()

if __name__ == "__main__":
    fire.Fire(main)
