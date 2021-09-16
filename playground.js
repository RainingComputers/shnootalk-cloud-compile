const editors = {}
let tabHistory = []

function createEditor(tabName) {
    let editor = ace.edit(tabName)
    editor.setTheme("ace/theme/vscode")
    editor.session.setMode("ace/mode/shnootalk")
    editor.setFontSize(18)
    editor.setShowPrintMargin(false)
    editor.setHighlightActiveLine(false)

    editors[tabName] = editor
}

function makeAllTabsInactive() {
    for (let tabContent of document.getElementsByClassName("tab-content")) {
        tabContent.style.display = "none"
    }

    for (let tabButton of document.getElementsByClassName("tab-links")) {
        tabButton.className = tabButton.className.replace(/\bactive$/, "")
    }
}

function openTab(tabName) {
    tabHistory.push(tabName)

    makeAllTabsInactive()

    document.getElementById(`tab-content-${tabName}`).style.display = "block"
    document.getElementById(`tab-${tabName}`).className += " active"
}

function closeTab(tabName) {
    makeAllTabsInactive()

    document.getElementById(`tab-content-${tabName}`).remove()
    document.getElementById(`tab-${tabName}`).remove()

    tabHistory = tabHistory.filter(elem => elem != tabName)

    openTab(tabHistory.pop())
}

function closeTabEvent(evt, tabName) {
    evt.stopPropagation()

    closeTab(tabName)
}

function createTabOnEnter(evt, element) {
    if(evt.key !== 'Enter') return;
    
    document.getElementById("ask-tab-name-modal").style.display = "none"
    newTab(element.value)
}

function askNameAndCreateNewTab() {
    document.getElementById("ask-tab-name-modal").style.display = "flex"
    
    const textbox = document.getElementById("ask-tab-name-textbox")

    textbox.value = ""
    textbox.focus()
}

function newTab(tabName) {
    if (`tab-content-${tabName}` in editors) {
        openTab(tabName)
        return
    }

    makeAllTabsInactive() 
    
    const tabTemplate = document.getElementById("new-tab-button-template").content.cloneNode(true)
    
    tabTemplate.getElementById("tab-name").innerHTML = tabName
    tabTemplate.getElementById("tab-button").setAttribute("onclick", `openTab('${tabName}')`)
    tabTemplate.getElementById("tab-button").setAttribute("id", `tab-${tabName}`)
    tabTemplate.getElementById("tab-close-button").setAttribute("onclick", `closeTabEvent(event, '${tabName}')`)

    document.getElementById("tab-header").appendChild(tabTemplate)

    const contentTemplate = document.getElementById("new-editor-template").content.cloneNode(true)
    contentTemplate.getElementById("editor-div").setAttribute("id", `tab-content-${tabName}`)

    document.getElementById("content-div").appendChild(contentTemplate)

    createEditor(`tab-content-${tabName}`)

    tabHistory.push(tabName)
}

tabHistory.push("main.shtk")
createEditor("tab-content-main.shtk")