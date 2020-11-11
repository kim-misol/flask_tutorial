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

let quill = new Quill('#editorContainer', {
  modules: {
    toolbar: toolbarOptions
  },
  placeholder: 'Type Content..',
  theme: 'snow'  // or 'bubble'
});

document.querySelector('.create-post').addEventListener('click', createPostEvent);
//document.querySelector('.daft-post').addEventListener('click', draftPostEvent);

function getData(save_type){
    let form = document.querySelector('form');
    let formData = new FormData(form);
    let delta = quill.getContents();
    let text = quill.getText();
    formData.append('content_json', JSON.stringify(delta));
    formData.append('content', text);
    formData.append('save_type', save_type);

    return formData
}

function createPostEvent(event) {
    let form = document.querySelector('form');
    let formData = new FormData(form);
    let delta = quill.getContents();
    let text = quill.getText();
    formData.append('content_json', JSON.stringify(delta));
    formData.append('content', text);
    formData.append('save_type', 'save');
//    save_type = 'save';
//    formData = getData(save_type);

    fetch(window.createPostUrl, {
      method: 'POST', // or 'PUT'
      body: formData
    }).then(res => res.json().then(data => window.location = data.redirect))
    .catch(error => console.error('Error:', error));
}

function draftPostEvent(event) {
    save_type = 'draft';
    formData = getData(save_type);
    console.log(save_type)
    for (var value of formData.values()) {
       console.log(value);
    }
    fetch(window.createPostUrl, {
      method: 'POST', // or 'PUT'
      body: formData
    }).then(res => res.json())
    .then(response => console.log('Success:', JSON.stringify(response)))
    .catch(error => console.error('Error:', error));
}
