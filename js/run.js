function byId(id) {
    return document.getElementById(id)
}

function showLoadingPanel() {
    byId("loading-panel").style.display = "flex"
    byId("stdout-panel").style.display = "none"
}

function showOutputPanel() {
    byId("loading-panel").style.display = "none"
    byId("stdout-panel").style.display = "flex"
}

function disableRunButton() {
    byId("run-button").disabled = true
}

function enableRunButton() {
    byId("run-button").disabled = false
}

function statusToDisplayString(status) {
    const stringMap = {
        SENDING_REQUEST: "Sending request",
        SCHEDULED: "Scheduled",
        EXEC_TIMEDOUT: "Execution timed out",
        CLANG_LINK_TIMEDOUT: "Link timed out",
        CLANG_LINK_FAILED: "Link error",
        COMPILE_FAILED: "Compile error",
        COMPILE_TIMEDOUT: "Compile time out",
        COMPILE_STARTED: "Compile started"
    }

    return stringMap[status]
}

function setOutput(outputString) {
    byId("stdout-panel-output").innerHTML = outputString
}

function setLoadingPanelStatus(status) {
    byId("loading-panel-status").innerHTML = statusToDisplayString(status)
}

function error() {
    byId("exec-error").style.display = "block"
    byId("exec-ok").style.display = "none"
}

function ok() {
    byId("exec-error").style.display = "none"
    byId("exec-ok").style.display = "block"
}

function neither() {
    byId("exec-error").style.display = "none"
    byId("exec-ok").style.display = "none"
}

function isTerminalStatus(status) {
    return status !== "SCHEDULED" && status !== "COMPILE_STARTED"
}

function isSuccessStatus(status) {
    return status === "SUCCESS"
}

function statusCallback(executionStatus) {
    const compileStatus = executionStatus.status
    setLoadingPanelStatus(compileStatus)

    if (!isTerminalStatus(compileStatus)) {
        neither()
        showLoadingPanel()
        return
    }

    isSuccessStatus(compileStatus) ? ok() : error()

    showOutputPanel()

    if (executionStatus.output) setOutput(executionStatus.output)
    else setOutput(statusToDisplayString(executionStatus.status))

    enableRunButton()
}

function errorCallback(errorString) {
    showOutputPanel()
    setOutput(errorString)
    enableRunButton()
    error()
}

function run(programs) {
    disableRunButton()
    neither()
    setLoadingPanelStatus("SENDING_REQUEST")
    showLoadingPanel()
    dispatchProgram(statusCallback, errorCallback, programs)
}
