const SERVER_URL = "http://34.96.95.247:80/shnootalk/compile/api/v1/"
const DISPATCH_ENDPOINT = SERVER_URL + "dispatch"
const POLL_FREQUENCY = 250

function getStatusEndPoint(programId) {
    return SERVER_URL + "status/" + programId
}

function request(url, method, data, callback) {
    var xmlhttp = new XMLHttpRequest()

    xmlhttp.onreadystatechange = () => {
        if (xmlhttp.readyState == XMLHttpRequest.DONE && callback) {
            callback(JSON.parse(xmlhttp.responseText), xmlhttp.status)
        }
    }

    xmlhttp.open(method, url)
    xmlhttp.setRequestHeader("Content-type", "application/json")
    xmlhttp.send(data)
}

function pollServer(statusCallback, programId, stopIntervalCallback) {
    request(getStatusEndPoint(programId), "GET", undefined, (response) => {
        statusCallback(response)

        if (response.status !== "SCHEDULED" && response.status !== "COMPILE_STARTED")
            stopIntervalCallback()
    })
}

function dispatchProgram(statusCallback, programs) {
    request(DISPATCH_ENDPOINT, "POST", JSON.stringify(programs), (response) => {
        const programId = response["_id"]

        let intervalId = setInterval(pollServer, POLL_FREQUENCY, statusCallback, programId, () => {
            clearInterval(intervalId)
        })
    })
}
