function validation() {
          var z = document.forms["myForm"]["fichier"].value;

          if (z == "" || z == null) {
            alert("Choisir un fichier !");
            return false;
          }
          if (z.split('.').pop() != 'csv'){
            alert("Aie aie aie !! Ton fichier n'est pas un csv..");
            return false;
          }
        }   
