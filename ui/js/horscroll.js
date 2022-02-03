function wheelHandler(element, event) {
    const toLeft = event.deltaY < 0 && element.scrollLeft > 0
    const toRight =
        event.deltaY > 0 && element.scrollLeft < element.scrollWidth - element.clientWidth

    if (toLeft || toRight) {
        event.preventDefault()
        event.stopPropagation()

        element.scrollBy({ left: event.deltaY })
    }
}

for (let element of document.getElementsByClassName("hor-scroll")) {
    element.addEventListener("wheel", (event) => wheelHandler(element, event))
}
