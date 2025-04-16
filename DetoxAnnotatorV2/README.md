# Detoxification Annotation Tool V2

This tool is built with Gradio and Python to help you evaluate and compare the quality of detoxification outputs. The evaluation focuses on two important aspects:
- **Toxicity Reduction:** How effectively the toxic content has been reduced.
- **Meaning Preservation:** How well the original meaning is retained after detoxification.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Running the Tool](#running-the-tool)
- [How to Annotate Examples](#how-to-annotate-examples)
- [Rating Definitions](#rating-definitions)
- [Navigation and Saving](#navigation-and-saving)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.7+** is required.
- Install the following Python libraries:
  - `gradio`
  - `pandas`
  - (optional) Any other dependencies you might need

You can install the required packages using pip:

```bash
pip install gradio pandas
```

## Setup and Installation

1. **Download or Clone the Code:**
   - Save the provided Python code into a file, for example `annotation_tool.py`.

2. **Prepare Your CSV File:**
   - Create a CSV file containing the examples you want to annotate.  
   - Your CSV must have at least the following columns:
     - **comment:** The original text to be annotated.
     - **model_detox_mian:** The detoxified text from Model 1.
     - **model_detox_lora:** The detoxified text from Model 2.
   - Additional columns will be automatically created if they are missing, such as:
     - `rating_model_detox_mian`
     - `rating_model_detox_lora`
     - `preferred_transformation`
     - `user_preferred`
     - `annotator`
     - `annotation_time`

## Running the Tool

1. **Start the Script:**
   - Open a terminal or command prompt.
   - Run the script with Python:
     ```bash
     python annotation_tool.py
     ```

2. **Provide Input:**
   - When prompted, enter the full file name (or path) of your CSV file.
   - Next, you will be prompted to enter your annotator name.

3. **Gradio Interface Launch:**
   - The Gradio web interface will launch automatically in your browser.
   - You will see the annotation interface, including the example text and annotations options.

## How to Annotate Examples

Once the Gradio interface loads:

1. **Review the Example:**
   - **Example Index:** The current example number and total count are shown.
   - **Original Text:** This is the comment text that needs evaluation.
   - **Transformed Text (Model 1 and Model 2):** Two detoxified versions of the original text. One is generated from Model 1 and the other from Model 2.

2. **Rate Each Detoxification:**
   - **Ratings (A to E):** Select a rating for each model based on both toxicity reduction and meaning preservation.
   - A Markdown section within the interface explains the rating definitions.

3. **Determine Your Preferences:**
   - **Semantic Judgment:** Choose which transformation better retains the original meaning by selecting either "Model 1" or "Model 2".
   - **Personal Usage Preference:** Indicate which one you would personally prefer to use for your own purposes (again, choosing between "Model 1" and "Model 2").

4. **Submit Your Annotation:**
   - Click **"Submit Annotation"** to save the ratings.
   - The tool will record how long you spent on the annotation and save your responses to the CSV.
   - After submission, the tool will automatically load the next example.

5. **Navigation:**
   - If needed, click the **"Previous"** button to go back to an earlier example and revise annotations.

## Rating Definitions

Each rating (A to E) is determined based on:
- **Toxicity Reduction:** How effective is the detoxification?
- **Meaning Preservation:** How well does the detoxified text retain the original meaning?

The definitions are as follows:

- **A: Outstanding**  
  Detoxification drastically reduces toxicity while completely preserving the original meaning.

- **B: Very Good**  
  Significant toxicity reduction with nearly all of the original meaning intact.

- **C: Good**  
  Moderate toxicity reduction but with noticeable loss of some meaning.

- **D: Fair**  
  Limited toxicity reduction accompanied by a considerable compromise of the original meaning.

- **E: Poor**  
  Detoxification fails to reduce toxicity effectively and largely loses the original meaning.

## Navigation and Saving

- **Automatic Navigation:**  
  After each submission, the script automatically loads the next unannotated example.

- **Saving Your Work:**  
  All annotations are saved back to the same CSV file that you provided, including details such as:
  - Annotator's name
  - Time spent on each annotation
  - Ratings from both models
  - Your preference selections

## Troubleshooting

- **CSV File Not Found:**  
  Ensure that you provide the correct path to your CSV file when prompted.

- **Incomplete Annotations:**  
  Make sure that each rating and preference is filled before clicking **Submit Annotation**.

- **Interface Not Loading:**  
  Check your Python and Gradio installation if the browser does not open automatically.
