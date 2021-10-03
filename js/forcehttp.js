if (location.protocol !== 'http:') {
    location.replace(`http:${location.href.substring(location.protocol.length)}`);
}