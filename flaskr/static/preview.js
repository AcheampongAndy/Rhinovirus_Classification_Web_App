 // Function to preview the content of the FASTA file
 document.getElementById('file').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();

        // Once the file is read, set its content to the textarea
        reader.onload = function(e) {
            const content = e.target.result;
            document.getElementById('file-content').textContent = content;
        };

        // Read the file as text
        reader.readAsText(file);
    }
});