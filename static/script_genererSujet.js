window.jsPDF = window.jspdf.jsPDF;

// Define the jspdf instance

function pdf(id) {
    var doc = new jsPDF();
    console.log(id)
    // Get the HTML content of the element specified by the `id` parameter
    const texte = document.getElementById(id).innerHTML;
    console.log(texte)



    // Set font size and style
    doc.setFont('helvetica', 'bold');

    doc.setFontSize(2);

    // Set font family
    
    // Convert HTML content to PDF document using html2pdf
    doc.html(texte, {
        callback: function (doc) {
            doc.save();
        }
     });
    
}
function generatePDF(id) {
    var element = document.getElementById(id);
    var opt = {
      margin:       0.5,
      filename:     'myfile.pdf',
      image:        { type: 'jpeg', quality: 0.99 },
      html2canvas:  { scale: 2 },
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    
    // New Promise-based usage:
    html2pdf().set(opt).from(element).save();
    }