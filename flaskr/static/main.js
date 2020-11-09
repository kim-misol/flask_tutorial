var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  ['blockquote', 'code-block'],

  [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'direction': 'rtl' }],                         // text direction

  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  [{ 'font': [] }],
  [{ 'align': [] }],

  ['clean']                                         // remove formatting button
];

let quill = new Quill('#editor-container', {
  modules: {
    toolbar: toolbarOptions
  },
  placeholder: 'Type Content...',
  theme: 'snow'  // or 'bubble'
});

//document.querySelector('.create-post').addEventListener('click', createPostEvent);

function createPostEvent(event) {
    let form = document.querySelector('form');
    let formData = new FormData(form);
    let delta = quill.getContents();
    let text = quill.getText();
    formData.append('content_json', JSON.stringify(delta));
    formData.append('content', text);
    console.log(JSON.stringify(delta))
    console.log(formData.content_json)
    console.log(typeof(formData))

    for (var value of formData.values()) {
      console.log(value);
    }

//    fetch(window.createPostUrl, {
//      headers: {
//        "Content-Type": "multipart/form-data"
//      },
//      method: 'POST', // or 'PUT'
//      body: formData // data can be `string` or {object}!
//    }).then(res => res.json())
//    .then(response => console.log('Success:', JSON.stringify(response)))
//    .catch(error => console.error('Error:', error));

    fetch(window.createPostUrl, {
      mode: 'cors',
      method: 'POST', // or 'PUT'
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: JSON.stringify(formData)
    }).then(res => res.json())
    .then(response => console.log('Success:', JSON.stringify(response)))
    .catch(error => console.error('Error:', error));
}

$(document).ready(function() {
    $('.create-post').click(function() {
        console.log('clicked submit button');
        let form = document.querySelector('form');
        let formData = new FormData(form);
        let delta = quill.getContents();
        let text = quill.getText();
        formData.append('content_json', JSON.stringify(delta));
        formData.append('content', text);
        for (var value of formData.values()) {
          console.log(value);
        }
        $.ajax({
            url: window.createPostUrl,
            type: 'POST',
            contentType: 'application/json; charset=utf-8',
            dataType:'JSON',
            data: JSON.stringify(formData),
            processData: false,
            success: function(d) {
                if (d.success) {
                    alert('Success');
                } else {
                    alert("Fail - " + d.message);
                }
            },
            failure: function(err) {
                console.log(err);
            }
        });
    });
});