const editors = {}

function createEditor(divId) {
    let editor = ace.edit(divId);
    editor.setTheme("ace/theme/vscode");
    editor.session.setMode("ace/mode/shnootalk");
    editor.setFontSize(17);
    editor.setShowPrintMargin(false)
    editor.setHighlightActiveLine(false)

    editors[divId] = editor;
}

createEditor("London");
createEditor("Paris");
createEditor("Tokyo");