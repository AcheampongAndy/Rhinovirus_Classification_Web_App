import io
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
from flaskr.utils.p_distance import calc_p_distance

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

    # Retrieve sequence from the database
    fasta_data = db.execute(
        'SELECT header, sequence_data FROM FastaSequences WHERE file_id = ?',
        (file_id,)
    ).fetchall()

    headers = [row['header'] for row in fasta_data]
    sequences = [row['sequence_data'] for row in fasta_data]

    print(f"sequences: {sequences}")
    print(f"headers: {headers}")

    if request.method == 'POST':
        analysis_type = request.form.get('analysis_type')
        graph_type = request.form.get('graph_type')
        gap_deletion = request.form.get('gap_deletion')

        if gap_deletion == 'on':
            gap_deletion = True
        else:
            gap_deletion = False

        print(f"analysis_type: {analysis_type}")
        print(f"graph_type: {graph_type}")

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
        else:
            flash('Invalid graph type selected')
            return redirect(url_for('pipeline.analyze'))
        '''elif graph_type == 'dendogram':
            plot_url = plot_tree()
        elif graph_type == 'heatmap':
            plot_url = plot_distances()
        elif graph_type == 'frequency':
            plot_url = plot_frequency()
        elif graph_type == 'amino_a_comp':
            plot_url = plot_amino()'''
        
        if (result is not None and result.any()) and plot_url:
            session['results'] = result.tolist()
            session['plot_url'] = plot_url
            return redirect(url_for('pipeline.results'))
        else:
            print("Debug: result or plot_url is None")
            print(f"result: {result}")
            print(f"plot_url: {plot_url}")
        

    return render_template('pipeline/analyze.html', file_name=uploaded_file['file_name'])


@bp.route('/results')
@login_required
def results():
    results = session.get('results')
    plot_url = session.get('plot_url')

    if results is not None:
        results = results.tolist()
    

    if not results or not plot_url:
        flash('No Analysis results found.')
        return redirect(url_for('pipeline.analyze'))
    
    print("Results:", results)  # Debugging output
    print("Plot URL:", plot_url)  # Debugging output
    
    return render_template('pipeline/results.html', results=results)

