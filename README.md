# Data Annotation Tool For Detoxification Project

This is a data annotation tool built with [Gradio](https://gradio.app/) that allows annotators to label and rate text data for tasks such as toxicity classification and transformation suggestions. The tool provides an interactive web interface where annotators can read data points, provide ratings, suggest classes, and suggest transformations. Annotations are saved to a CSV file for further processing.

## Features

- **Interactive Web Interface**: Annotate data through a user-friendly Gradio web application.
- **Resume Annotation**: Start from where you left off; the tool automatically resumes from the last annotated index.
- **Flexible Annotation Options**:
  - Provide ratings for each data point.
  - Suggest classes from a predefined list.
  - Suggest transformations for text data.
- **Data Management**: Annotations are saved to a CSV file in the `annotations` directory.
- **Customizable**: Easily modify or extend the tool to fit different annotation tasks.

## Requirements

- Python 3.x
- The following Python packages:
  - [gradio](https://gradio.app/)
  - [pandas](https://pandas.pydata.org/)
  - [fire](https://github.com/google/python-fire)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a Virtual Environment (Recommended)**

   Create a virtual environment to manage dependencies without affecting your global Python installation.

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Or you can install the packages individually:

   ```bash
   pip install gradio pandas fire
   ```

## Usage

The script is designed to be run from the command line and will launch a Gradio web interface for annotation.

### Command-Line Arguments

The script requires the following arguments:

- `annotator_name` (required): The name of the annotator. This will be stored in the annotations.
- `examples_batch_folder` (required): The path to the CSV file containing the batch of examples to annotate.
- `current_index` (optional): The index from which to resume annotation. Defaults to `0`.

### Running the Script

Navigate to the directory containing the script and run:

```bash
python your_script_name.py --annotator_name "Your Name" --examples_batch_folder /path/to/your/dataset.csv
```

Replace `your_script_name.py` with the actual name of the script file.

To resume from a specific index:

```bash
python your_script_name.py --annotator_name "Your Name" --examples_batch_folder /path/to/your/dataset.csv --current_index 10
```

### Data File Format

The CSV file provided in `examples_batch_folder` should have at least the following columns:

- `text`: The original text data.
- `Transformed`: The transformed version of the text. If not available, it will be filled with `[empty]`.
- `Form`: The form or category of the text.
- `Class`: Existing class labels.

**Example CSV Format:**

| text                | Transformed        | Form    | Class    |
|---------------------|--------------------|---------|----------|
| Original text here. | Transformed text.  | Form A  | Class 1  |

### Launching the Web Interface

After running the script, a Gradio web interface will launch automatically, and a local URL (e.g., `http://127.0.0.1:7860/`) will be displayed in the terminal. Open this URL in your web browser to start annotating.

### Using the Web Interface

1. **Text Fields**:

   - **Text**: Displays the original text data. (Non-editable)
   - **Transformed**: Displays the transformed text. (Non-editable)
   - **Form**: Displays the form or category of the text. (Non-editable)
   - **Class**: Displays any existing class labels. (Non-editable)

2. **Suggested Class**:

   - A checkbox group to select suggested classes.
   - **Options**:

     - **Hate Speech**: Language that attacks or demeans individuals based on race, religion, gender, or other personal characteristics.
     - **Threat**: Language expressing intent to cause harm or instill fear.
     - **Insult**: Language that belittles or degrades an individual or group.
     - **Profanity**: Obscene or offensive language not necessarily targeting anyone but considered inappropriate.
     - **Misinformation**: False or misleading statements that could harm or mislead.
     - **Discrimination**: Language that reinforces stereotypes or discriminates against a group.
     - **Harassment**: Persistent or repeated language targeting or intimidating an individual or group.
     - **Manipulation or Coercion**: Language intended to control, pressure, or exploit someone’s emotions or actions.
     - **Not Toxic**: If the sentence is not toxic.

3. **Suggested Transformation**:

   - A textbox to input any suggested transformations for the text data.

4. **Rating**:

   - A set of radio buttons to select the rating for the data point.
   - **Options**:

     - **Rating-A**: The text is perfectly classified, seamlessly transformed to the target tone, and fully preserves the original meaning.
     - **Rating-B**: The text is accurately classified, effectively transformed into the target tone, and retains the original meaning with negligible changes.
     - **Rating-C**: The text is mostly classified correctly, with some effective tone transformation and minor meaning inconsistencies.
     - **Rating-D**: The text has partial classification errors, limited tone transformation, and alters some key meanings.
     - **Rating-E**: The text is incorrectly classified, fails to change tone effectively, and loses the original meaning.
     - **SKIPPING**: Skip this data point without annotating.

   - **Note**: The "Validate" button will be enabled only after selecting a rating.

5. **Validate Button**:

   - Click to save the annotation and move to the next data point.
   - If you haven't selected a rating, the button will remain disabled.

### Saving Annotations

- Annotations are automatically saved to a CSV file in the `annotations` directory.
- The filename is prefixed with `annotations_` followed by the dataset filename.
- If the annotations file already exists, the script will append new annotations to it.

**Annotations CSV Format:**

The annotations CSV will include the following columns:

- Original columns from the dataset (`text`, `Transformed`, `Form`, `Class`, etc.)
- `timestamp`: The time when the annotation was made.
- `rating`: The selected rating.
- `annotator`: The name of the annotator.
- `suggested_class`: The classes suggested by the annotator.
- `suggested_transformation`: The transformation suggested by the annotator.

### Exiting and Resuming

- **Exit**: You can exit the script at any time by closing the terminal or stopping the script execution.
- **Resume**: To resume annotation, run the script again with the same `annotator_name` and `examples_batch_folder`. The script will detect the existing annotations file and resume from the next unannotated index.

## Customization

You can customize the tool according to your annotation needs:

- **Modify Classes**: Change the options in the `suggested_class` checkbox group.
- **Update Rating Criteria**: Edit the descriptions of the rating options to fit your criteria.
- **Extend Functionality**: Add more fields or modify the existing ones in the Gradio interface.

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

For any questions or issues, please contact [Kamyar Zeinalipour] at [Kzeinalipour@umass.edu].
