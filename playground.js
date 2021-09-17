const editors = {}
let tabHistory = []

function byId(id) {
    return document.getElementById(id)
}

function getTabContentDivId(tabName) {
    return `tab-content-${tabName}`
}

function getTabButtonId(tabName) {
    return `tab-${tabName}`
}

function pushHistory(tabName) {
    tabHistory.push(tabName)
}

function popHistory(tabName) {
    return tabHistory.pop(tabName)
}

function removeHistory(tabName) {
    tabHistory = tabHistory.filter(elem => elem != tabName)
}

function createEditor(tabName) {
    let editor = ace.edit(getTabContentDivId(tabName))
    editor.setTheme("ace/theme/vscode")
    editor.session.setMode("ace/mode/shnootalk")
    editor.setFontSize(18)
    editor.setShowPrintMargin(false)
    editor.setHighlightActiveLine(false)

    editors[tabName] = editor
}

function destroyEditor(tabName) {
    editors[tabName].destroy()
    delete editors[tabName]
}

function tabExists(tabName) {
    return tabName in editors
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
    makeAllTabsInactive()

    byId(getTabContentDivId(tabName)).style.display = "block"
    byId(getTabButtonId(tabName)).className += " active"

    pushHistory(tabName)
}

function closeTab(tabName) {
    makeAllTabsInactive()

    byId(getTabContentDivId(tabName)).remove()
    byId(getTabButtonId(tabName)).remove()

    destroyEditor(tabName)

    removeHistory(tabName);

    openTab(popHistory(tabName))
}

function closeTabEvent(evt, tabName) {
    evt.stopPropagation()

    closeTab(tabName)
}

function createTabOnEnter(evt, element) {
    if(evt.key !== 'Enter') return;
    
    byId("ask-tab-name-modal").style.display = "none"
    newTab(element.value)
}

function askNameAndCreateNewTab() {
    byId("ask-tab-name-modal").style.display = "flex"
    
    const textbox = byId("ask-tab-name-textbox")
    textbox.value = ""
    textbox.focus()
}

function newTab(tabName) {
    if (tabExists(tabName)) {
        openTab(tabName)
        return
    }

    makeAllTabsInactive() 
    
    const tabTemplate = byId("new-tab-button-template").content.cloneNode(true)
    tabTemplate.getElementById("tab-name").innerHTML = tabName
    tabTemplate.getElementById("tab-button").setAttribute("onclick", `openTab('${tabName}')`)
    tabTemplate.getElementById("tab-button").setAttribute("id", getTabButtonId(tabName))
    tabTemplate.getElementById("tab-close-button").setAttribute("onclick", `closeTabEvent(event, '${tabName}')`)

    byId("tab-header").appendChild(tabTemplate)

    const contentTemplate = byId("new-editor-template").content.cloneNode(true)
    contentTemplate.getElementById("editor-div").setAttribute("id", getTabContentDivId(tabName))

    byId("content-div").appendChild(contentTemplate)

    createEditor(tabName)
    tabHistory.push(tabName)
}

pushHistory("main.shtk")
createEditor("main.shtk")