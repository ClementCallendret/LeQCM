window.jsPDF = window.jspdf.jsPDF;

function pdf(id){
    let texte = document.getElementById(id);

    console.log(id);
    console.log(texte);


    // Créer un objet jsPDF
    const pdf = new jsPDF();
    
    const html = texte.innerHTML;

    // Ajouter le contenu HTML au PDF
    pdf.html(html, 
        {
        callback: function () {
            // Télécharger le fichier PDF
            pdf.save('sujet1.pdf');
        }
    });
}