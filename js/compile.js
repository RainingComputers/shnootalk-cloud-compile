const SERVER_URL = "http://34.96.95.247:80/shnootalk/compile/api/v1/"
const DISPATCH_ENDPOINT = SERVER_URL + "dispatch"
const POLL_FREQUENCY = 250
const MESSAGE_500 = "Something went wrong, please try again later"

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

function pollServer(statusCallback, errorCallback, programId, stopIntervalCallback) {
    request(getStatusEndPoint(programId), "GET", undefined, (response, respStatus) => {
        if (respStatus !== 200) {
            errorCallback(response.error || MESSAGE_500)
            stopIntervalCallback()
            return
        }

        statusCallback(response)

        if (response.status !== "SCHEDULED" && response.status !== "COMPILE_STARTED")
            stopIntervalCallback()
    })
}

function dispatchProgram(statusCallback, errorCallback, programs) {
    request(DISPATCH_ENDPOINT, "POST", JSON.stringify(programs), (response, respStatus) => {
        if (respStatus !== 200) {
            errorCallback(response.error || MESSAGE_500)
            return
        }

        const programId = response["_id"]

        let intervalId = setInterval(
            pollServer,
            POLL_FREQUENCY,
            statusCallback,
            errorCallback,
            programId,
            () => {
                clearInterval(intervalId)
            }
        )
    })
}
