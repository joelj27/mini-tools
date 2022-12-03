function submit_entry() {
    var data = (document.querySelectorAll("[id=exampleRadios2]"));
    for(i = 0; i < data.length; i++) {
        if(data[i].selected)
             selected_data= data[i];
    }
    
    var entry={
        data:selected_data.value
    };
    console.log(entry)
    fetch(`${window.origin}/getfile/format`, {
        method:"POST",
        credentials:"include",
        body: JSON.stringify(entry),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    }