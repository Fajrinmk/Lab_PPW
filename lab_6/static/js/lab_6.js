// Calculator
var print = document.getElementById('print');
var erase = false;

var go = function(x) {
  if (x === 'ac') {
	print.value = null;
	erase = false;
  } else if (x === 'eval') {
      print.value = Math.round(evil(print.value) * 10000) / 10000;
      erase = true;
  } else if (x === 'log' || x ==='sin' || x === 'tan') {
    switch (x) {
      case 'log':
        print.value = Math.log10(print.value);
        erase = true;
        break;
      case 'sin':
        print.value = Math.sin(print.value);
        erase = true;
        break;
      case 'tan':
        print.value = Math.tan(print.value);
        erase = true;
        break;
    }
  }	else if (erase === true) {
        print.value = x;
        erase = false;
  } else {
    print.value += x;
  }
};

function evil(fn) {
  return new Function('return ' + fn)();
}

//Ganti tema

function changeTheme(x) {
	$('body').css({"backgroundColor": x['bcgColor']});
}

//simpan berbagai macam tema
if (localStorage.getItem('themes') === null){ localStorage.setItem('themes','[{"id":0,"text":"Red","bcgColor":"#F44336","fontColor":"#FAFAFA"},{"id":1,"text":"Pink","bcgColor":"#E91E63","fontColor":"#FAFAFA"},{"id":2,"text":"Purple","bcgColor":"#9C27B0","fontColor":"#FAFAFA"},{"id":3,"text":"Indigo","bcgColor":"#3F51B5","fontColor":"#FAFAFA"},{"id":4,"text":"Blue","bcgColor":"#2196F3","fontColor":"#212121"},{"id":5,"text":"Teal","bcgColor":"#009688","fontColor":"#212121"},{"id":6,"text":"Lime","bcgColor":"#CDDC39","fontColor":"#212121"},{"id":7,"text":"Yellow","bcgColor":"#FFEB3B","fontColor":"#212121"},{"id":8,"text":"Amber","bcgColor":"#FFC107","fontColor":"#212121"},{"id":9,"text":"Orange","bcgColor":"#FF5722","fontColor":"#212121"},{"id":10,"text":"Brown","bcgColor":"#795548","fontColor":"#FAFAFA"}]'); }
var themes = JSON.parse(localStorage.getItem('themes'));
//set tema default dari pertama kali user membuka webpage
if (localStorage.getItem('selectedTheme') === null) { localStorage.setItem('selectedTheme', JSON.stringify(themes[3])); }
var theme = JSON.parse(localStorage.getItem('selectedTheme'));
changeTheme(theme);



$(document).ready(function() {
    $('.my-select').select2({'data' : JSON.parse(localStorage.getItem('themes'))}).val(theme['id']).change();
    $('.apply-button').on('click', function(){
        theme = themes[$('.my-select').val()];
        changeTheme(theme);
        localStorage.setItem('selectedTheme',JSON.stringify(theme));
    })
});

//Toggle chatbox
$('.chat-head').ready(function(){
    $("img").on('click', function(){
    	$('.chat-body').toggle(500);
        var src = ($(this).attr("src") === "https://maxcdn.icons8.com/windows10/PNG/16/Arrows/angle_down-16.png")
            ? "https://maxcdn.icons8.com/windows10/PNG/16/Arrows/angle_up-16.png" 
            : "https://maxcdn.icons8.com/windows10/PNG/16/Arrows/angle_down-16.png";
  	$(this).attr("src", src);
    })
});

//enter2 di chatbox
var sender = true;

$('textarea').keypress(function(e){
    if(e.keyCode == 13 && !e.shiftKey) {
        var c = String.fromCharCode(e.which);
        var textValue = $('textarea').val();
        var fulltext = textValue + c;
        e.preventDefault();
        $('textarea').val('');

        if(sender){
            $('.msg-insert').append('<div class="msg-send">' + fulltext + '</div>');
            sender = false;
        }else{
            $('.msg-insert').append('<div class="msg-receive">' + fulltext + '</div>');
            sender = true;
        } 
    }
});


// END
