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

function statusToDisplayString(status) {
    const stringMap = {
        SCHEDULED: "Scheduled",
        EXEC_TIMEDOUT: "Execution timed out",
        CLANG_LINK_TIMEDOUT: "Link timed out",
        CLANG_LINK_FAILED: "Link error",
        COMPILE_FAILED: "Compile error",
        COMPILE_TIMEDOUT: "Compile time out",
        COMPILE_STARTED: "Compile started",
    }

    return stringMap[status]
}

function setOutput(outputString) {
    byId("stdout-panel-output").innerHTML = outputString
}

function setStatus(status) {
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
    return status !== "SUCCESS"
}

function statusCallback(executionStatus) {
    const status = executionStatus.status
    setStatus(status)

    if (!isTerminalStatus(status)) {
        neither()
        showLoadingPanel()
        return
    }

    isSuccessStatus(status) ? ok() : error()

    showOutputPanel()

    if (executionStatus.output) setOutput(executionStatus.output)
    else setOutput(statusToDisplayString(executionStatus.status))
}

function run(programs) {
    dispatchProgram(statusCallback, programs)
}
