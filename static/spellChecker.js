const irreguliersEnS = ["landau", "pneu", "bleu", "sarrau", "antitau", "berimbau", "burgau", "crau", "donau", "grau", "hessiau", "jautereau", "jotterau", "karbau", "kérabau", "landau", "restau", "sarrau", "saun gau", "senau", "tamarau", "tau", "uchau", "unau", "wau", "beu", "bisteu", "bleu", "émeu", "enfeu", "eu", "lieu", "neuneu", "pneu", "rebeu", "acétal", "ammonal", "aval", "bal", "barbital", "cal", "captal", "carnaval", "cérémonial", "chacal", "chloral", "chrysocal", "copal", "dial", "dispersal", "éthanal", "festival", "foiral", "furfural", "futal", "gal", "galgal", "gardénal", "graal", "joual", "kraal", "kursaal", "matorral", "mescal", "mezcal", "méthanal", "minerval", "mistral", "nopal", "pal", "pascal", "hectopascal", "kilopascal", "penthotal", "phénobarbital", "pipéronal", "raval", "récital", "régal", "rétinal", "rital", "roberval", "roseval", "salicional", "sal", "sandal", "santal", "saroual", "sial", "sisal", "sonal", "tagal", "tefal", "tergal", "thiopental", "tical", "tincal", "véronal", "zicral", "corral", "deal", "goal", "autogoal", "revival", "serial", "spiritual", "trial", "caracal", "gavial", "gayal", "narval", "quetzal", "rorqual", "serval", "metical", "rial", "riyal", "ryal", "cantal", "emmental", "emmenthal", "metical", "rial", "riyal", "ryal"];
const irreguliersOu = ["bijou", "caillou", "chou", "genou", "hibou", "joujou", "pou", "ripou"];
const irreguliersAil = ["bail", "corail", "émail", "fermail", "soupirail", "travail", "vantail", "vitrail", "gemmail"];
const autresIrreguliers = { "aïeul": "aïeux", "ail": "aulx", "ciel": "cieux", "oeil": "yeux", "vieil": "vieux", "topos": "topoï" };

function pluriel(word) {
    if (word in autresIrreguliers) {
        return autresIrreguliers[word];
    } else if (word.endsWith("s") || word.endsWith("x") || word.endsWith("z")) {
        return word;
    } else if (word.endsWith('au') || word.endsWith("eu")) {
        if (irreguliersEnS.includes(word)) {
            return word + "s";
        } else {
            return word + 'x';
        }
    } else if (word.endsWith('al')) {
        if (irreguliersEnS.includes(word)) {
            return word + 's';
        } else {
            return word.slice(0, -1) + "ux";
        }
    } else if (word.endsWith("ou")) {
        if (irreguliersOu.includes(word)) {
            return word + "x";
        } else {
            return word + "s";
        }
    } else if (word.endsWith("ail")) {
        if (irreguliersAil.includes(word)) {
            return word.slice(0, -3) + "aux";
        } else {
            return word + "s";
        }
    } else {
        return word + "s";
    }
}

// mesure de la ressemblance entre les mots en utilisant la distance de Levenshtein
function ressemblanceLev(word1, word2) {
    const m = word1.length;
    const n = word2.length;
    let matrice = [];

    for (let i = 0; i <= m; i++) {
        matrice[i] = [i];
    }

    for (let j = 0; j <= n; j++) {
        matrice[0][j] = j;
    }

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (word1[i - 1] === word2[j - 1]) {
                matrice[i][j] = matrice[i - 1][j - 1];
            } else {
                matrice[i][j] = Math.min(
                    matrice[i - 1][j - 1],
                    matrice[i][j - 1],
                    matrice[i - 1][j]
                ) + 1;
            }
        }
    }

    const distance = matrice[m][n];
    const maxLength = Math.max(word1.length, word2.length);
    const similarity = (1 - distance / maxLength) * 100;

    return similarity;
}

// nous permet de differencier des mots comme "compatible" et "incompatible"
function ressemblanceByLetter(word1, word2) {
    let similarity = 0;
    const minLength = Math.min(word1.length, word2.length);
    const maxLength = Math.max(word1.length, word2.length);
    for(let i =0; i < minLength; i++){
        if(word1[i] == word2[i]){
            similarity++;
        }
    }
    return (similarity / maxLength * 100);
}

// on fait la moyenne entre les 2 algos de ressemblance et on test aussi avec les pluriels
function seRessemble(word1, word2) {
    const similarity = (ressemblanceByLetter(word1, word2) + ressemblanceLev(word1, word2)) / 2;
    const similarityPlurl = (ressemblanceByLetter(pluriel(word1), pluriel(word2)) + ressemblanceLev(pluriel(word1), pluriel(word2))) / 2;
    console.log(word1 + " == " + word2 + " : " + similarity + " | " + similarityPlurl)
    return similarity > 50 || similarityPlurl > 50;
}

// Groupe tous les mots qui se ressemblent
function groupSimilars(answers) {
    const words = Object.keys(answers);

    for (let i = 0; i < words.length; i++) {
        const word1 = words[i];
        let mostUsedSimilar = word1;

        for (let j = i+1; j < words.length; j++) {
            const word2 = words[j];
            const similar = seRessemble(word1, word2);

            if (similar) {
                if (answers[mostUsedSimilar] >= answers[word2]) {
                    answers[mostUsedSimilar] += answers[word2];
                    delete answers[word2];
                    words.splice(j, 1);
                    j--;
                    console.log(mostUsedSimilar + " <---- " + word2)
                }
                else{
                    answers[word2] += answers[mostUsedSimilar];
                    delete answers[mostUsedSimilar];
                    words.splice(words.indexOf(mostUsedSimilar), 1);
                    i--;j--;
                    console.log(word2 + " <---- " + mostUsedSimilar)
                    mostUsedSimilar = word2;
                }
            }
        }
    }
    return answers;
}

// Ajoute un seul mot sans tout recalculer
function addWord(word, answers) {
    for(let key in answers){
        if(seRessemble(word, key)){
            answers[key]++;
            return
        }
    }
    answers[word] = 1;
}

