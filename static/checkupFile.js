var parsed_file;
var index_invalide;

function validation() {
  var z = document.getElementById("myFile").files[0];
  var name_file = document.getElementById("myFile").value;

  if (name_file == "" || z == null) {
    alert("Choisir un fichier !");
    return false;
  }
  if (name_file.split('.').pop() != 'csv') {
    alert("Aie aie aie !! Ton fichier n'est pas un csv..");
    return false;
  }


  const reader = new FileReader();
  reader.addEventListener('load', (event) => {
    fileContent = event.target.result.replaceAll(";", ",");
    //console.log(fileContent);
    parsed_file = $.csv.toArrays(fileContent);
    console.log(parsed_file[2])
    // parsed_file.splice(0, 1) // splice car on veut skip la première ligne (elle ne contient aucune donnée utile normalement)
    //enfait non sinon ca oublie un etudiant si ya pas d'entete 
    Verif_content(); // fonction qui va verifier que le fichier est en parfaite forme
  });
  reader.readAsText(z);

  $('#comfirmButtons').removeClass("hidden")

  // trouvé sur https://stackoverflow.com/questions/12571650/catching-all-javascript-unhandled-exceptions afin de retournr l'exception
  window.onerror = function myErrorHandler(errorMsg, url, lineNumber) {
    efface(true); // afin de pouvoir re-essayer sans avoir a F5
    alert("Il y a eu une erreur sur votre fichier csv..\nATTENTION au format (numEtu , prenom , nom)\n\n" + errorMsg);
    return false;
  }

}

function efface(isError=false) {
  $('#comfirmButtons').addClass("hidden")

  $('#myFile').val("")

  $('#TabToSend').val("")

  $('#etudiant_ajt').empty()
}

function Verif_content() {
  index_invalide = []
  tableau_des_bons_etudiants = []
  // Verification de la donnée qui est notre fichier parsé
  for (i in parsed_file) {
    line = parsed_file[i];
    if (line.length != 3 || line[0].length != 8 || ! /^\d+$/.test(line[0]) || line[1].length == 0 || line[2].length == 0) { // verif des elements de chaque lignes
      index_invalide.push(i);
      console.log(line);
    }
    else {
      tableau_des_bons_etudiants.push(line);
    }
  }
  affiche_etudiant_a_ajouter();


  StudentTab = $('#TabToSend');
  StudentTab.val(JSON.stringify(tableau_des_bons_etudiants)); // pour mettre dans mon html mon tableau à l'emplacmeent hidden
}

function affiche_etudiant_a_ajouter() {
  // on declare notre tableau et on le vide au cas ou
  tableau = $('#etudiant_ajt');
  tableau.empty();

  html = `
  <tr>
    <th>
    Numéro Etudiant
    </th>

    <th>
    Prénom
    </th>

    <th>
    Nom
    </th>
  </tr>
  `
  tableau.append(html);
  for (i in parsed_file) {
    if (index_invalide.includes(i))
      style = "background-color : red;"
    else {
      style = ""
    }
    html = `
  <tr style="${style}"> 
  <td>
    ${parsed_file[i][0]}
  </td>
  <td>
    ${parsed_file[i][1]}
  </td>
  <td>
    ${parsed_file[i][2]}
  </td>  
  </tr>
  `
    tableau.append(html);
  }

}
