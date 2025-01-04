import io
import json
import uuid
import numpy as np
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.utils.fasta_processing import read_fasta
from flaskr.utils.SNPeek import SNPeek
from flaskr.utils.jukes_distance import calc_jukes_cantor_distance
from flaskr.utils.kimura_distance import calc_kimura_2p_distance
from flaskr.utils.tamura import calc_tamura_3p_distance
from flaskr.utils.heatmap import plot_heatmap
from flaskr.utils.p_distance import calc_p_distance
from flaskr.utils.plot_tree import plot_multiple_trees

bp = Blueprint('pipeline', __name__)



@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.fasta'):
            file_content = file.read()
            fasta_content = io.StringIO(file_content.decode('utf-8'))
            seq_data = read_fasta(fasta_content)

            sequences = list(seq_data.values())
            headers = list(seq_data.keys())


            db = get_db()
            db.execute(
                'INSERT INTO UploadedFile (user_id, file_name, file_data) VALUES (?, ?, ?)',
                (g.user['user_id'], file.filename, file_content)
            )
            file_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

            for header, sequence in zip(headers, sequences):
                db.execute(
                    'INSERT INTO FastaSequences (file_id, header, sequence_data) VALUES (?, ?, ?)',
                    (file_id, header, sequence)
                )

            db.commit()

            flash('File Uploaded and Process successfully')
            return redirect(url_for('pipeline.analyze'))
        else:
            flash('Invalid file format: Please upload FASTA file.')

    return render_template('pipeline/upload.html')



@bp.route('/analyze', methods=('POST', 'GET'))
@login_required
def analyze():
    plot_url = None
    db = get_db()

    # Get the latest uploaded file for the user
    uploaded_file = db.execute(
        'SELECT file_id, file_name FROM UploadedFile WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
        (g.user['user_id'],)
    ).fetchone()

    if uploaded_file is None:
        flash('No file uploaded to analyze')
        return redirect(url_for('pipeline.upload'))
    
    file_id = uploaded_file['file_id']

    # Retrieve sequences from the database
    fasta_data = db.execute(
        'SELECT header, sequence_data FROM FastaSequences WHERE file_id = ?',
        (file_id,)
    ).fetchall()

    headers = [row['header'] for row in fasta_data]
    sequences = [row['sequence_data'] for row in fasta_data]

    if request.method == 'POST':
        analysis_type = request.form.get('analysis_type')
        graph_type = request.form.get('graph_type')
        gap_deletion = request.form.get('gap_deletion') == 'on'

        if not analysis_type or not graph_type:
            flash('Please select both analysis type and graph type.')
            return redirect(url_for('pipeline.analyze'))

        # Perform the selected analysis
        if analysis_type == 'jukes_cantor':
            result = calc_jukes_cantor_distance(sequences, headers, gap_deletion=gap_deletion)
        elif analysis_type == 'kimura_2p':
            result = calc_kimura_2p_distance(sequences, headers, gap_deletion=gap_deletion)
        elif analysis_type == 'tamura_3p':
            result = calc_tamura_3p_distance(sequences, headers, gap_deletion=gap_deletion)
        elif analysis_type == 'p_distance':
            result = calc_p_distance(sequences, headers, gap_deletion=gap_deletion)
        else:
            flash('Invalid analysis type selected')
            return redirect(url_for('pipeline.analyze'))

        # Perform the selected graph
        if graph_type == 'snpeek':
            plot_url = SNPeek(sequences, headers, show_legend=True)
        elif graph_type == 'heatmap':
            plot_url = plot_heatmap(result)
        elif graph_type == 'dendrogram':
            mat1 = calc_jukes_cantor_distance(sequences, headers, gap_deletion=gap_deletion)
            mat2 = calc_kimura_2p_distance(sequences, headers, gap_deletion=gap_deletion)
            mat3 = calc_tamura_3p_distance(sequences, headers, gap_deletion=gap_deletion)
            mat4 = calc_p_distance(sequences, headers, gap_deletion=gap_deletion)
            distance_matrices = [mat1, mat2, mat3, mat4]
            titles = ["Jukes_cantor", "Kimura_2p", "Tamura_3p", "p_distance"]
            plot_url = plot_multiple_trees(distance_matrices, titles=titles)
        else:
            flash('Invalid graph type selected')
            return redirect(url_for('pipeline.analyze'))

        if result is not None and plot_url: 

            if isinstance(result, np.ndarray):
                result = result.tolist() 
            # Serialize the result object before saving to the database
            result_data = json.dumps(result)

            # Insert the new analysis result into the database
            analysis_id = str(uuid.uuid4())
            db.execute(
                'INSERT INTO AnalysisResults (analysis_id, user_id, file_id, analysis_type, result_data, plot_url) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (analysis_id, g.user['user_id'], file_id, analysis_type, result_data, plot_url)
            )
            db.commit()

            # Store only the analysis_id in the session
            session['analysis_id'] = analysis_id
            return redirect(url_for('pipeline.results'))
        else:
            flash('Analysis failed. Please try again.')

    return render_template('pipeline/analyze.html', file_name=uploaded_file['file_name'])


@bp.route('/results', methods=('GET',))
@login_required
def results():
    analysis_id = session.get('analysis_id')
    if not analysis_id:
        flash('No analysis to display.')
        return redirect(url_for('pipeline.upload'))

    db = get_db()
    analysis = db.execute(
        'SELECT result_data, plot_url FROM AnalysisResults WHERE analysis_id = ?',
        (analysis_id,)
    ).fetchone()

    if analysis is None:
        flash('Analysis results not found.')
        return redirect(url_for('pipeline.upload'))

    results = analysis['result_data']
    plot_url = analysis['plot_url']

    return render_template('pipeline/results.html', results=results, plot_url=plot_url)


@bp.route('/view/<int:upload_id>', methods=['GET'])
def view_results(upload_id):
    # Fetch the results for the given upload_id from the database
    db = get_db()
    try:
        upload = db.execute(
            'SELECT result_data, plot_url FROM AnalysisResults WHERE file_id = ? ORDER BY created_at DESC LIMIT 1',
            (upload_id,)
        ).fetchone()
    except Exception as e:
        flash("An error occurred while fetching the results.", "error")
        return redirect(url_for('dashboard'))

    if not upload:
        flash("The specified upload was not found.", "error")
        return redirect(url_for('dashboard'))

    # Extract results or placeholder
    results = upload['result_data'] if upload['result_data'] else "No results available."
    plot_url = upload['plot_url'] if upload['plot_url'] else None

    return render_template('pipeline/results.html', results=results, plot_url=plot_url)


@bp.route('/redo_analysis/<int:upload_id>', methods=['GET', 'POST'])
def redo_analysis(upload_id):
    plot_url = None
    db = get_db()

    # Retrieve the uploaded file details
    uploaded_file = db.execute(
        'SELECT file_name FROM UploadedFile WHERE file_id = ? ORDER BY created_at DESC LIMIT 1',
        (upload_id,)
    ).fetchone()

    if not uploaded_file:
        flash('The specified file could not be found.', 'danger')
        return redirect(url_for('pipeline.dashboard'))

    # Retrieve sequences from the database
    fasta_data = db.execute(
        'SELECT header, sequence_data FROM FastaSequences WHERE file_id = ?',
        (upload_id,)
    ).fetchall()

    headers = [row['header'] for row in fasta_data]
    sequences = [row['sequence_data'] for row in fasta_data]

    if request.method == 'POST':
        analysis_type = request.form.get('analysis_type')
        graph_type = request.form.get('graph_type')
        gap_deletion = request.form.get('gap_deletion') == 'on'

        if not analysis_type or not graph_type:
            flash('Please select both analysis type and graph type.')
            return redirect(url_for('pipeline.analyze'))

        # Perform the selected analysis
        if analysis_type == 'jukes_cantor':
            result = calc_jukes_cantor_distance(sequences, headers, gap_deletion=gap_deletion)
        elif analysis_type == 'kimura_2p':
            result = calc_kimura_2p_distance(sequences, headers, gap_deletion=gap_deletion)
        elif analysis_type == 'tamura_3p':
            result = calc_tamura_3p_distance(sequences, headers, gap_deletion=gap_deletion)
        elif analysis_type == 'p_distance':
            result = calc_p_distance(sequences, headers, gap_deletion=gap_deletion)
        else:
            flash('Invalid analysis type selected')
            return redirect(url_for('pipeline.analyze'))

        # Perform the selected graph
        if graph_type == 'snpeek':
            plot_url = SNPeek(sequences, headers, show_legend=True)
        elif graph_type == 'heatmap':
            plot_url = plot_heatmap(result)
        elif graph_type == 'dendrogram':
            mat1 = calc_jukes_cantor_distance(sequences, headers, gap_deletion=gap_deletion)
            mat2 = calc_kimura_2p_distance(sequences, headers, gap_deletion=gap_deletion)
            mat3 = calc_tamura_3p_distance(sequences, headers, gap_deletion=gap_deletion)
            mat4 = calc_p_distance(sequences, headers, gap_deletion=gap_deletion)
            distance_matrices = [mat1, mat2, mat3, mat4]
            titles = ["Jukes_cantor", "Kimura_2p", "Tamura_3p", "p_distance"]
            plot_url = plot_multiple_trees(distance_matrices, titles=titles)
        else:
            flash('Invalid graph type selected')
            return redirect(url_for('pipeline.analyze'))

        if result is not None and plot_url: 
            if isinstance(result, np.ndarray):
                result = result.tolist()
            # Serialize the result object before saving to the database
            result_data = json.dumps(result)

            # Insert the new analysis result into the database
            analysis_id = str(uuid.uuid4())
            db.execute(
                'INSERT INTO AnalysisResults (analysis_id, user_id, file_id, analysis_type, result_data, plot_url) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (analysis_id, g.user['user_id'], upload_id, analysis_type, result_data, plot_url)
            )
            db.commit()

            # Store only the analysis_id in the session
            session['analysis_id'] = analysis_id
            return redirect(url_for('pipeline.results'))
        else:
            flash('Analysis failed. Please try again.')

    return render_template('pipeline/analyze.html', file_name=uploaded_file['file_name'])