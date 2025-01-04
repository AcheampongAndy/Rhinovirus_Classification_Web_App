# Rhinovirus Classification Web App

## Overview
This web application provides an interface for analyzing and visualizing FASTA sequence data related to Rhinovirus classification. It supports various phylogenetic analysis methods and visualizations, allowing users to upload sequences, perform analyses, and view results.

## Features
- User authentication system.
- File upload functionality for FASTA files.
- Phylogenetic distance calculations:
  - Jukes-Cantor
  - Kimura 2-parameter
  - Tamura 3-parameter
  - p-distance
- Sequence visualization using the SNPeek graph.
- Results storage and retrieval.

## Technologies Used
- **Frontend**: HTML, CSS, Jinja2 templates
- **Backend**: Python (Flask framework)
- **Database**: SQLite
- **Visualization**: Matplotlib, Biopython

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd Rhinovirus_Classification_Web_App
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   flask init-db
   ```

4. Run the application:
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Usage Instructions
1. **Sign Up/Login**:
   - Create a new account or log in with existing credentials.

2. **Upload FASTA File**:
   - Navigate to the upload page and select a FASTA file.

3. **Analyze Sequences**:
   - Choose an analysis type and graph type.
   - Perform the analysis and view results.

4. **View Results**:
   - Access analysis results and visualizations from the results page.

## Database Schema
- **User**: Stores user information.
- **UploadedFile**: Tracks uploaded files.
- **FastaSequences**: Stores parsed sequences from uploaded FASTA files.
- **AnalysisResults**: Saves analysis results and associated metadata.

## Citation
This project draws inspiration from the `rhinotypeR` package and acknowledges the contributions of:
- Martha M. Luka
- Ruth Nanjala
- Wafaa M. Rashed
- Winfred Gatua
- Olaitan I. Awe

If you use this application in your research, please consider citing their work appropriately.

## ALX Full Stack Software Engineering Program
This web application was developed as the final project for the completion of the ALX Full Stack Software Engineering program.


## Contributions
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or fixes.

## Contact
For questions or support, please contact:
- **Name**: Acheampong Andrews
- **Email**: acheampongandrews1999@gmail.com
- **GitHub**: [GitHub Repository](https://github.com/AcheampongAndy/Rhinovirus_Classification_Web_App)
- **Website**: [Your Website](https://acheampongandy.github.io/My_Portfolio/)
