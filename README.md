# Data Annotation Tool For Detoxification Project

This repository provides a Gradio-based annotation interface for labeling and rating transformed text data. The tool allows annotators to evaluate text transformations, suggest alternative transformations, classify texts into predefined categories, rate classification reasons, and provide comments.

## Features

- Load and display text examples from a CSV file.
- Display classification reasons alongside texts.
- Annotate texts using an interactive web interface powered by Gradio.
- Rate transformed texts based on predefined criteria.
- Rate the classification reasons of the texts.
- Suggest alternative transformations for each text.
- Classify texts into one or more predefined categories.
- Save annotations, including ratings and classification reason ratings, to a CSV file for future analysis.
- Resume annotations from where you left off.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Creating a Virtual Environment](#creating-a-virtual-environment)
  - [Installing Required Packages](#installing-required-packages)
- [Usage](#usage)
  - [Preparing Your Data](#preparing-your-data)
  - [Running the Annotation Interface](#running-the-annotation-interface)
  - [Using the Interface](#using-the-interface)
    - [Interface Overview](#interface-overview)
    - [Steps for Annotation](#steps-for-annotation)
    - [Rating Definitions](#rating-definitions)
    - [Class Definitions](#class-definitions)
- [Annotations Output](#annotations-output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Prerequisites

- **Python 3.x** installed on your system.
- Ability to create and manage virtual environments in Python.
- The required Python packages are listed in the `requirements.txt` file.

## Installation

### Clone the Repository

```bash
git clone https://github.com/KamyarZeinalipour/Detox_Human_eval_UI.git
cd Detox_Human_eval_UI
```

### Creating a Virtual Environment

It is recommended to use a virtual environment to manage the dependencies for this project.

#### On macOS and Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Installing Required Packages

Install the required Python packages from the `requirements.txt` file using `pip`:

```bash
pip install -r requirements.txt
```

Ensure that the `requirements.txt` file contains the following packages:

```txt
pandas
gradio
fire
```

If you don't have a `requirements.txt` file, you can create one with the above content.

## Usage

### Preparing Your Data

Prepare a CSV file containing the text examples you want to annotate. The CSV file should have the following columns:

- `text`: The original text to be annotated.
- `Classification Reason` (optional but required for classification reason rating): The reason for the classification of the text.
- `Neutral` (optional): The text transformed into a neutral tone.
- `Formal` (optional): The text transformed into a formal tone.
- `Friendly` (optional): The text transformed into a friendly tone.
- `Class` (optional): The original class or category of the text.

**Note**: The `Classification Reason` column is used to display additional information about the classification of the text, which you will also rate during annotation.

Example of a CSV file (`examples.csv`):

```csv
text,Classification Reason,Neutral,Formal,Friendly,Class
"This is a sample text.","Reason for classification.","Neutral version of text.","Formal version of text.","Friendly version of text.","Original Class"
```

### Running the Annotation Interface

Run the annotation interface using the following command:

```bash
python script_name.py --annotator_name="Your Name" --examples_batch_folder="path/to/examples.csv"
```

Replace `script_name.py` with the actual name of the script containing the provided code.

#### Command-Line Arguments

- `--annotator_name` (**Required**): Your name or identifier as the annotator.
- `--examples_batch_folder` (**Required**): The path to the CSV file containing the examples to annotate.
- `--current_index` (Optional): The index from which to start annotating (default is `0`). Use this if you want to resume from a specific point.

### Using the Interface

After running the script, a web browser window or tab should open automatically, displaying the Gradio interface. If it doesn't open automatically, look for the local URL provided in the terminal and open it manually in your browser.

#### Interface Overview

- **Text**: Displays the original text to be annotated.
- **Class**: Shows the original class of the text if provided.
- **Classification Reason**: Displays the reason for the classification of the text.
- **Classification Reason Rating**: Radio buttons to rate the acceptability of the classification reason.
- **Suggested Class**: You can select one or more classes that you think are appropriate for the text.
- **Comments**: A field to add any comments or notes about the text or transformation.
- **Transformed Neutral/Formal/Friendly**: Shows the text transformed into Neutral, Formal, and Friendly tones.
- **Rating Neutral/Formal/Friendly**: Radio buttons to rate each transformed text based on the quality of transformation.
- **Suggested Transformation Neutral/Formal/Friendly**: Fields to suggest alternative transformations for each tone.

#### Steps for Annotation

1. **Review the Original Text**

   Read the original text provided in the **Text** field.

2. **Review the Classification Reason**

   Examine the **Classification Reason** provided for the text.

3. **Rate the Classification Reason**

   Select a rating from the **Classification Reason Rating** radio buttons:

   - **Acceptable**
   - **Partially Acceptable**
   - **Not Acceptable**
   - **Skipping**

4. **Review Transformed Texts**

   Examine the transformed versions in the **Transformed Neutral**, **Transformed Formal**, and **Transformed Friendly** fields.

5. **Assign Ratings to Transformed Texts**

   For each transformed text, select a rating based on the **Rating Definitions** provided below.

6. **Suggest Transformations**

   If you have suggestions for improving the transformation, you can provide them in the **Suggested Transformation** fields for each tone.

7. **Classify the Text**

   If applicable, select one or more classes from the **Suggested Class** options by checking the boxes.

8. **Add Comments**

   Provide any additional comments in the **Comments** field.

9. **Validate**

   Once all required fields are filled, click the **Validate** button to save the annotation and move to the next text.

   - The **Validate** button will be disabled until ratings for all transformed texts **and the classification reason** are provided.

10. **Repeat**

    Continue the process for each text until you reach the end of the dataset.

#### Rating Definitions

**For Transformed Texts:**

- **Rating-A**: *Gold Standard* - The toxic text is rewritten to be as non-toxic as possible while perfectly preserving the original meaning, and the rewritten version aligns seamlessly with the target tone.
- **Rating-B**: *Silver Standard* - The toxic text is rewritten to be mostly non-toxic while largely preserving the original meaning, and the rewritten version approaches the target tone but may have minor imperfections.
- **Rating-F**: *Insufficient* - The toxic text remains inadequately rewritten, the meaning deviates significantly, or the rewritten version fails to achieve the target tone.
- **SKIPPING**: Skip this entry if you cannot provide a rating.

**For Classification Reason Rating:**

- **Acceptable**: The classification reason is appropriate and accurately reflects the content of the text.
- **Partially Acceptable**: The classification reason is somewhat appropriate but may lack clarity or completeness.
- **Not Acceptable**: The classification reason is inappropriate, incorrect, or does not reflect the content of the text.
- **Skipping**: Skip this entry if you cannot provide a rating.

#### Class Definitions

- **Hate Speech**: Language that attacks or demeans individuals based on race, religion, gender, or other personal characteristics.
- **Threat**: Language expressing intent to cause harm or instill fear.
- **Insult**: Language that belittles or degrades an individual or group.
- **Profanity**: Obscene or offensive language not necessarily targeting anyone but considered inappropriate.
- **Misinformation**: False or misleading statements that could harm or mislead.
- **Discrimination**: Language that reinforces stereotypes or discriminates against a group.
- **Harassment**: Persistent or repeated language targeting or intimidating an individual or group.
- **Manipulation or Coercion**: Language intended to control, pressure, or exploit someone’s emotions or actions.
- **Not Toxic**: The text is not toxic.

## Annotations Output

- Annotations are saved in the `annotations` folder in the current working directory.
- The filename is `annotations_<dataset_filename>.csv`, where `<dataset_filename>` is the name of your examples CSV file.
- The annotation file includes all original data along with the new annotations:
  - `timestamp`: The time when the annotation was made.
  - `annotator`: The name of the annotator.
  - `suggested_class`: The classes suggested by the annotator.
  - `comments`: Any comments provided by the annotator.
  - `Classification Reason Rating`: The rating assigned to the classification reason.
  - `Rating_Neutral`: Rating assigned to the Neutral transformation.
  - `Suggested_Transformation_Neutral`: Any suggested transformation for Neutral tone.
  - `Rating_Formal`: Rating assigned to the Formal transformation.
  - `Suggested_Transformation_Formal`: Any suggested transformation for Formal tone.
  - `Rating_Friendly`: Rating assigned to the Friendly transformation.
  - `Suggested_Transformation_Friendly`: Any suggested transformation for Friendly tone.

## Troubleshooting

- **Interface Doesn't Launch**

  - Ensure that all required packages are installed.
  - Check for any error messages in the terminal where you ran the script.
  - Manually open the URL provided in the terminal (usually `http://127.0.0.1:7860`).

- **Errors When Running the Script**

  - Verify that the paths provided for the CSV files are correct.
  - Ensure that the CSV file is properly formatted and readable.
  - Make sure you're using the correct version of Python (Python 3.x).

- **Annotations Not Saving**

  - Ensure that you have write permissions in the directory where the script is running.
  - Check for any error messages related to file I/O in the terminal.

- **Resume Functionality Not Working**

  - Confirm that the annotations CSV file exists in the `annotations` folder.
  - Make sure you're running the script with the same `--annotator_name` and `--examples_batch_folder` arguments.

- **Dependencies Issues**

  - Ensure all required packages are installed and up to date.
  - Use the `requirements.txt` file to manage dependencies.

- **Port Conflicts**

  - If Gradio cannot launch due to a port conflict, specify a different port using the `server_port` parameter in `demo.launch()`.

    ```python
    demo.launch(server_port=7861)
    ```

- **Firewall Restrictions**

  - If accessing the interface remotely, ensure appropriate firewall settings are configured.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE.txt).

## Contact

For any questions or issues, please contact Kamyar Zeinalipour at [Kzeinalipour@umass.edu].

## Acknowledgments

- This tool utilizes [Gradio](https://gradio.app/) for the web interface.
- Command-line argument handling is powered by [Python Fire](https://github.com/google/python-fire).
