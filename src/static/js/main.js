function shorten() {
    var originalUrl = document.getElementById('shortening_url').value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('shortening_url').value = this.responseText;
        }
    };
    xhttp.open("GET", "/api/get/" + encodeURIComponent(originalUrl), true);
    xhttp.send();
}