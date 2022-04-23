var input = document.getElementById('formFile');
var preview = document.getElementById('previewFile');
input.addEventListener('change', updateImageDisplay);

function updateImageDisplay() {
  while(preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  var curFiles = input.files;
  if(curFiles.length === 0) {
    var para = document.createElement('p');
    para.textContent = 'No files currently selected for upload';
    preview.appendChild(para);
  } else {
    for(var i = 0; i < curFiles.length; i++) {
      if(validFileType(curFiles[i])) {
        var image = document.createElement('img');
        image.src = window.URL.createObjectURL(curFiles[i]);
        image.classList.add("mb-3")
        preview.appendChild(image);
      } else {
        para.textContent = 'Not a valid file type. Update your selection.';
        preview.appendChild(para);
      }
    }
  }
}

var fileTypes = [
  'image/jpeg',
  'image/jpeg',
  'image/png'
]

function validFileType(file) {
  for(var i = 0; i < fileTypes.length; i++) {
    if(file.type === fileTypes[i]) {
      return true;
    }
  }

  return false;
}