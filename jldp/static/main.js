const url_pattern = new RegExp(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi);
const target_input_id = "target"
const output_target_id = "output";
const accept_input_id = "accept";
const output_final_url = "finalurl";
const output_section = "outputsection";
const request_url = "requesturl";


function setSpinner(spinner_state){
    // true to set spinner on
    // false to turn spinner off
    const ele = document.getElementById(output_target_id);
    if (spinner_state) {
        ele.innerText = "Loading...";
    } else {
        ele.innerText = "";
    }
}


async function loadUrl(url, accept) {
    setSpinner(true);
    let api_url = new URL(document.location.href);
    api_url.searchParams.append("url", url);
    api_url.searchParams.append("accept", accept);
    document.getElementById(request_url).innerText = api_url;
    try {
        const response = await fetch(api_url);
        const data = await response.json();
        document.getElementById(output_final_url).innerText = response.headers.get("x-jldp-final-url");
        const ele = document.getElementById(output_target_id);
        setSpinner(false)
        ele.innerText = JSON.stringify(data, null, 2);
        document.getElementById(output_section).style.visibility = "visible";
    } catch (error) {
        setSpinner(false)
        const ele = document.getElementById(output_target_id);
        ele.innerText = error;
    }
}

function doLoadUrl() {
    const url = document.getElementById(target_input_id).value;
    const accept = document.getElementById(accept_input_id).value;
    loadUrl(url, accept);
}
