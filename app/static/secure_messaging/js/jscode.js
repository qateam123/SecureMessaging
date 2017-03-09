function remainingChars(max_CHARS) {
    var text = document.getElementById("id_textFeedback").value;
    var chars = text.length;

    if(chars < max_CHARS){
      document.getElementById("chars").innerHTML = 'Characters remaining: ' + (max_CHARS - chars);
    }
    else {
      document.getElementById("chars").innerHTML = 'Character limit reached!';
      document.getElementById("chars").style.color = 'red';
    }
}
