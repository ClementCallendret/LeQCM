import Markdoc from '@markdoc/markdoc';


function preview(){
    text = '##Markdown'
    const ast = Markdoc.parse(text)
    const content = Markdoc.transform(ast)

    const html = Markdoc.renderers.html(content);
    document.getElementById("enoncePreview").append(html)
}