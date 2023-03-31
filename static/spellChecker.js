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
function ressemblance(word1, word2) {
    const m = word1.length;
    const n = word2.length;
    const matrix = [];

    for (let i = 0; i <= m; i++) {
        matrix[i] = [i];
    }

    for (let j = 0; j <= n; j++) {
        matrix[0][j] = j;
    }

    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (word1[i - 1] === word2[j - 1]) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1],
                    matrix[i][j - 1],
                    matrix[i - 1][j]
                ) + 1;
            }
        }
    }

    const distance = matrix[m][n];
    const maxLength = Math.max(word1.length, word2.length);
    const similarity = (1 - distance / maxLength) * 100;

    return similarity.toFixed(2);
}

function groupSimilars(answers) {
    const words = Object.keys(answers);

    for (let i = 0; i < words.length; i++) {
        console.log(words);
        const word1 = words[i];
        let mostUsedSimilar = word1;
        for (let j = i+1; j < words.length; j++) {
            const word2 = words[j];
            const similarity = ressemblance(word1, word2);
            console.log(word1 + " == " + word2 + " : " + similarity)

            if (similarity > 80) {
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

function addWord(word, answers) {
    for(let key in answers){
        if(ressemblance(word, key) > 80){
            answers[key]++;
            return
        }
    }
    answers[word] = 1;
}

mySet = {"pithon" : 5, "javascript" : 10, "java script" : 9, "python" : 25, "java" : 15, "c++" : 12, "pyhton" : 1}

