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
  placeholder: 'Type Content..',
  theme: 'snow'  // or 'bubble'
});

document.querySelector('.create-post').addEventListener('click', createPostEvent);

function createPostEvent(event) {
    let form = document.querySelector('form');
    let formData = new FormData(form);
    let delta = quill.getContents();
    let text = quill.getText();
    formData.append('content_json', JSON.stringify(delta));
    formData.append('content', text);

    fetch(window.createPostUrl, {
      method: 'POST', // or 'PUT'
      body: formData
    }).then(res => res.json())
    .then(response => console.log('Success:', JSON.stringify(response)))
    .catch(error => console.error('Error:', error));
}
