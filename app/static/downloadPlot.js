document.getElementById('downloadButton').addEventListener('click', function() {
    // Get the canvas element
    var canvas = document.getElementById('classificationOutput');

    // Create a link element
    var link = document.createElement('a');

    // Set the download attribute to the desired file name
    link.download = 'graph.png';

    // Get the data URL of the canvas
    link.href = canvas.toDataURL();

    // Append the link to the body
    document.body.appendChild(link);

    // Simulate a click on the link
    link.click();

    // Remove the link from the body
    document.body.removeChild(link);
});
