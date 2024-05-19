$(document).ready(function () {
    //$("#image_id").on("load", function () {
        var scripts = document.getElementById('makeHistogram');
        var histogram = scripts.getAttribute('histogram');
        // The image has been loaded, now you can run the makeHistogram function
        makeHistogram(histogram);
    //});
    //makeHistogram();
});

function makeHistogram(counts) {
    console.log(counts);
    counts = JSON.parse(counts);
    // Create a data object for the Histogram
    var data = {
    labels: Array.from({ length: counts.length }, (_, i) => i),  // Etichette per i bin
    datasets: [{
        label: 'Histogram',
        data: counts,  // Histogram data
        backgroundColor: 'rgba(255, b, 0, 0.2)',
        borderColor: 'rgba(255, b, 0, 0.2)',
        borderWidth: 1
    }]
    };

    // // Create an options object for the chart (you can further customize the options)
    var options = {
    scales: {
        y: {
            beginAtZero: true
        }
    }
    };

    // Get the reference to the canvas element where the chart will be displayed
    var ctx = document.getElementById("histogramOutput").getContext('2d');

    // Create the histogram chart using Chart.js
    var Histogram = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: options
    });
}