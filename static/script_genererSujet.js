import jsPDF from 'jspdf';

function pdf(id){
    console.log("test");
    let texte = document.getElementById(id);
    const doc = new jsPDF();
    doc.text(texte, 10, 10);
    doc.save('fichier1.pdf');
}