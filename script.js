var found=[],lost=[],USER="admin";
var $=function(id){return document.getElementById(id)};
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML}
function toast(m){var t=$('toast');t.textContent=m;t.className='toast on';clearTimeout(toast.t);toast.t=setTimeout(function(){t.className='toast'},2200)}

var TOKEN=null;
function showApp(){$('login').classList.add('hidden');$('app').classList.remove('hidden');$('hello').textContent='Signed in as '+USER}
function bad(msg){var p=$('loginPanel');$('err').textContent=msg;p.classList.remove('shake');void p.offsetWidth;p.classList.add('shake')}
function login(){
  fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({username:$('u').value.trim(),password:$('p').value})})
  .then(function(r){return r.json().then(function(j){return [r.ok,j]})})
  .then(function(x){
    if(!x[0]){bad(x[1].error||'Login failed.');return}
    TOKEN=x[1].token;USER=$('u').value.trim();showApp();
  }).catch(function(){bad('Cannot reach the server. Run: python server.py')});
}
$('loginBtn').onclick=login;
['u','p'].forEach(function(id){$(id).addEventListener('keydown',function(e){if(e.key==='Enter')login()})});
$('logout').onclick=function(){
  $('app').classList.add('hidden');$('login').classList.remove('hidden');$('p').value='';$('err').textContent='';
  TOKEN=null;
};

function read(form){
  var d=new FormData(form);
  return {item:d.get('item').trim().toLowerCase(),color:d.get('color').trim().toLowerCase(),
    location:d.get('location').trim().toLowerCase(),who:d.get('who').trim(),phone:d.get('phone').trim()};
}
function chips(){
  $('fl').innerHTML=found.map(function(x){return '<span class="chip">'+esc(x.color+' '+x.item)+'</span>'}).join('');
  $('ll').innerHTML=lost.map(function(x){return '<span class="chip">'+esc(x.color+' '+x.item)+'</span>'}).join('');
  $('cF').textContent=found.length;$('cL').textContent=lost.length;
}
function render(out){
  $('cM').textContent=out.length;
  if(!out.length){
    $('res').innerHTML='<div class="empty">'+(found.length&&lost.length?'No matching item found.':'Add a found item and a lost report. A match needs the same item and color.')+'</div>';
    return;
  }
  $('res').innerHTML=out.map(function(m,i){
    return '<div class="pair"><div class="half f" style="animation-delay:'+(i*.15)+'s"><h3>Found: '+esc(m.Color+' '+m.Item)+'</h3>'
    +'<p><b>Finder:</b> '+esc(m.Finder)+'</p><p><b>Phone:</b> '+esc(m['Finder Phone'])+'</p><p><b>Found at:</b> '+esc(m['Found Location'])+'</p></div>'
    +'<div class="half l" style="animation-delay:'+(i*.15)+'s"><h3>Lost by: '+esc(m.Owner)+'</h3>'
    +'<p><b>Phone:</b> '+esc(m['Owner Phone'])+'</p><p><b>Lost at:</b> '+esc(m['Lost Location'])+'</p></div>'
    +'<div class="stamp" style="animation-delay:'+(.75+i*.15)+'s">MATCH</div></div>';}).join('');
}
function match(){
  return fetch('/api/match',{method:'POST',headers:{'Content-Type':'application/json','X-Token':TOKEN||''},
    body:JSON.stringify({found:found,lost:lost})})
  .then(function(r){if(r.status===401){$('logout').click();throw 0}return r.json()})
  .then(function(j){render(j.matches);return j.matches.length})
  .catch(function(){toast('Server not reachable. Run: python server.py');return 0});
}
function add(form,arr,msg){
  form.addEventListener('submit',function(e){
    e.preventDefault();arr.push(read(form));form.reset();chips();
    match().then(function(n){
      toast(n?msg+' Match found!':msg);
      if(n)$('res').scrollIntoView({behavior:'smooth',block:'center'});
    });
  });
}
add($('ff'),found,'Found item added.');
add($('lf'),lost,'Lost item added.');
