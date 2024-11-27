# Data Annotation Tool For Detoxification Project

This repository provides a Gradio-based annotation interface for labeling and rating transformed text data. The tool allows annotators to evaluate text transformations, suggest alternative transformations, classify texts into predefined categories, and provide comments.

## Features

- Load and display text examples from a CSV file.
- Annotate texts using an interactive web interface powered by Gradio.
- Rate transformed texts based on predefined criteria.
- Suggest alternative transformations for each text.
- Classify texts into one or more predefined categories.
- Save annotations to a CSV file for future analysis.
- Resume annotations from where you left off.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Preparing Your Data](#preparing-your-data)
  - [Running the Annotation Interface](#running-the-annotation-interface)
  - [Using the Interface](#using-the-interface)
    - [Interface Overview](#interface-overview)
    - [Rating Definitions](#rating-definitions)
    - [Class Definitions](#class-definitions)
- [Annotations Output](#annotations-output)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Prerequisites

- Python 3.x installed on your system.
- The following Python packages:
  - `pandas`
  - `gradio`
  - `fire`

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Install Required Packages**

   Install the required Python packages using `pip`:

   ```bash
   pip install pandas gradio fire
   ```

## Usage

### Preparing Your Data

Prepare a CSV file containing the text examples you want to annotate. The CSV file should have the following columns:

- `text`: The original text to be annotated.
- `Neutral` (optional): The text transformed into a neutral tone.
- `Formal` (optional): The text transformed into a formal tone.
- `Friendly` (optional): The text transformed into a friendly tone.
- `Class` (optional): The original class or category of the text.

Example of a CSV file (`examples.csv`):

```csv
text,Neutral,Formal,Friendly,Class
"This is a sample text.","Neutral version of text.","Formal version of text.","Friendly version of text.","Original Class"
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
- **Suggested Class**: You can select one or more classes that you think are appropriate for the text.
- **Comments**: A field to add any comments or notes about the text or transformation.
- **Transformed Neutral/Formal/Friendly**: Shows the text transformed into Neutral, Formal, and Friendly tones.
- **Rating Neutral/Formal/Friendly**: Radio buttons to rate each transformed text based on the quality of transformation.
- **Suggested Transformation Neutral/Formal/Friendly**: Fields to suggest alternative transformations for each tone.

#### Steps for Annotation

1. **Review the Original Text**

   Read the original text provided in the **Text** field.

2. **Review Transformed Texts**

   Examine the transformed versions in the **Transformed Neutral**, **Transformed Formal**, and **Transformed Friendly** fields.

3. **Assign Ratings**

   For each transformed text, select a rating based on the **Rating Definitions** provided below.

4. **Suggest Transformations**

   If you have suggestions for improving the transformation, you can provide them in the **Suggested Transformation** fields for each tone.

5. **Classify the Text**

   If applicable, select one or more classes from the **Suggested Class** options by checking the boxes.

6. **Add Comments**

   Provide any additional comments in the **Comments** field.

7. **Validate**

   Once all required fields are filled, click the **Validate** button to save the annotation and move to the next text.

   - The **Validate** button will be disabled until ratings for all transformed texts are provided.

8. **Repeat**

   Continue the process for each text until you reach the end of the dataset.

#### Rating Definitions

- **A**: The text is perfectly transformed to the target tone and fully preserves the original meaning.
- **B**: The text is effectively transformed into the target tone with negligible changes in meaning.
- **C**: The text has some effective tone transformation with minor meaning inconsistencies.
- **D**: The text has limited tone transformation and alters some key meanings.
- **E**: The text fails to change tone effectively and loses the original meaning.
- **SKIPPING**: Skip this entry if you cannot provide a rating.

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
  - `Rating_Neutral/Formal/Friendly`: Ratings assigned to each transformed text.
  - `Suggested_Transformation_Neutral/Formal/Friendly`: Suggested transformations for each tone.

## Troubleshooting

- **Interface Doesn't Launch**

  - Ensure that all required packages are installed (`pandas`, `gradio`, `fire`).
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

## Troubleshooting

- **Dependencies Issues**: Ensure all required packages are installed and up to date.
- **Port Conflicts**: If Gradio cannot launch due to a port conflict, specify a different port using the `server_port` parameter in `demo.launch()`.

  ```python
  demo.launch(server_port=7861)
  ```

- **Firewall Restrictions**: If accessing the interface remotely, ensure appropriate firewall settings are configured.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE.txt).

## Contact

For any questions or issues, please contact Kamyar Zeinalipour at [Kzeinalipour@umass.edu].


## Acknowledgments

- This tool utilizes [Gradio](https://gradio.app/) for the web interface.
- Command-line argument handling is powered by [Python Fire](https://github.com/google/python-fire).
