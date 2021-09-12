const editors = {}

function openTab(evt, contentId) {
    for (let tabContent of document.getElementsByClassName("tab-content")) {
        tabContent.style.display = "none";
    }

    for (let tabButton of document.getElementsByClassName("toolbar-tab")) {
        tabButton.className = tabButton.className.replace(" active", "");
    }

    document.getElementById(contentId).style.display = "block";
    evt.currentTarget.className += " active";
}

function createEditor(tabId) {
    let editor = ace.edit(tabId);
    editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/shnootalk");
    editor.setFontSize(18);
    editor.setShowPrintMargin(false)
    editor.setHighlightActiveLine(false)

    const lineNumberGutter = editor.container.getElementsByClassName('ace_gutter')[0];

    new ResizeObserver(function() {
        document.getElementById("tab-header").style.paddingLeft = lineNumberGutter.style.width;
    }).observe(lineNumberGutter);

    editors[tabId] = editor;
}

createEditor("main.shtk");
createEditor("Paris");
createEditor("Tokyo");