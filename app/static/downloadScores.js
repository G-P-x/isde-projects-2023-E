document.getElementById('downloadScoresButton').addEventListener('click', function() {
    // Get the classification scores
    var scores = document.getElementById('makeGraph').getAttribute('classification_scores');

    // Parse and stringify the scores to format them as JSON
    var jsonScores = JSON.stringify(JSON.parse(scores));

    // Create a Blob object from the JSON string
    var blob = new Blob([jsonScores], {type: "application/json"});

    // Create a URL for the Blob object
    var url = URL.createObjectURL(blob);

    // Create a link element
    var link = document.createElement('a');

    // Set the download attribute to the desired file name
    link.download = 'scores.json';

    // Set the href attribute to the Blob URL
    link.href = url;

    // Append the link to the body
    document.body.appendChild(link);

    // Simulate a click on the link
    link.click();

    // Remove the link from the body
    document.body.removeChild(link);
});